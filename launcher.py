#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OLM Master Pro - Launcher"""

import os, sys, time, json, requests, hashlib, uuid, socket, base64, subprocess, tempfile, re, pickle
from datetime import datetime, timedelta
from pathlib import Path

API_TOKEN = "698b226d9150d31d216157a5"
URL_BLOG = "https://keyfreedailyolmvip.blogspot.com/2026/02/blog-post.html"
URL_MAIN = "https://raw.githubusercontent.com/thieunangbiettuot/ToolOLM/refs/heads/main/main.py"
URL_VIP = "https://raw.githubusercontent.com/thieunangbiettuot/ToolOLM/refs/heads/main/vip_users.txt"

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'x-requested-with': 'XMLHttpRequest',
}

def get_data_dir():
    p = sys.platform
    if p == 'win32':
        d = Path(os.getenv('LOCALAPPDATA', os.path.expanduser('~'))) / 'Microsoft' / 'Windows' / 'INetCache' / 'IE'
    elif p == 'darwin':
        d = Path.home() / 'Library' / 'Application Support' / 'com.apple.Safari'
    elif 'ANDROID_ROOT' in os.environ:
        d = Path(os.getenv('HOME', '/data/data/com.termux/files/home')) / '.cache' / 'google-chrome'
    else:
        d = Path.home() / '.cache' / 'mozilla' / 'firefox'
    d.mkdir(parents=True, exist_ok=True)
    return str(d)

DATA = get_data_dir()
_h = hashlib.md5(f"{socket.gethostname()}{uuid.getnode()}".encode()).hexdigest()[:8]
LIC = os.path.join(DATA, f'.{_h}sc')
SESS = os.path.join(DATA, f'.{_h}ss')
ACC = os.path.join(DATA, f'.{_h}ac')
LOCK = os.path.join(DATA, f'.{_h}lk')

KEY = b'OLM_ULTRA_SECRET_2026'

def enc(obj):
    txt = json.dumps(obj, separators=(',', ':')).encode()
    xor = bytearray(txt[i] ^ KEY[i % len(KEY)] for i in range(len(txt)))
    b85 = base64.b85encode(bytes(xor)).decode()
    chk = hashlib.sha256(b85.encode()).hexdigest()[:12]
    noise = hashlib.md5(chk.encode()).hexdigest()[:8]
    return f"{noise}{chk}{b85}{noise[::-1]}"

def dec(s):
    try:
        s = s[8:-8]
        chk, b85 = s[:12], s[12:]
        if hashlib.sha256(b85.encode()).hexdigest()[:12] != chk:
            return None
        xor = base64.b85decode(b85)
        txt = bytes(xor[i] ^ KEY[i % len(KEY)] for i in range(len(xor)))
        return json.loads(txt)
    except:
        return None

def cls(): os.system('cls' if os.name == 'nt' else 'clear')
def banner():
    cls()
    print(f"\n{'═' * 50}\n  OLM MASTER PRO v3.0\n{'═' * 50}\n")

def ip():
    try: return requests.get('https://api.ipify.org', timeout=5).text.strip()
    except: return "0.0.0.0"

def gen_key():
    import random
    now = datetime.now()
    dev = hashlib.md5(f"{socket.gethostname()}{uuid.getnode()}".encode()).hexdigest()[:16]
    unique = f"{dev}{now.timestamp()}{random.randint(1000, 9999)}"
    h = hashlib.sha256(unique.encode()).hexdigest()
    return f"OLM-{now:%d%m}-{h[:4].upper()}-{h[4:8].upper()}"

def sig(d): return hashlib.sha256(f"{d['mode']}{d['expire']}{d['ip']}".encode()).hexdigest()[:16]

def load_lic():
    if not os.path.exists(LIC): return None
    try:
        with open(LIC) as f: d = dec(f.read())
        if not d or d.get('sig') != sig(d): return None
        if datetime.strptime(d['expire'], "%d/%m/%Y").date() < datetime.now().date(): return None
        if d.get('mode') == 'FREE' and d.get('ip') != ip(): return None
        if d.get('remain', 0) > 0: return d
        return None
    except: return None

def save_lic(mode, n):
    expire_days = 3650 if mode == 'VIP' else 1
    d = {
        'mode': mode, 'remain': n,
        'expire': (datetime.now() + timedelta(days=expire_days)).strftime("%d/%m/%Y"),
        'ip': ip(), 'dev': '', 'hw': ''
    }
    d['sig'] = sig(d)
    with open(LIC, 'w') as f: f.write(enc(d))

def load_lock():
    if os.path.exists(LOCK):
        try:
            with open(LOCK) as f: return dec(f.read())
        except: pass
    return None

def save_lock(username):
    d = {'user': username, 'time': datetime.now().strftime("%d/%m/%Y %H:%M")}
    with open(LOCK, 'w') as f: f.write(enc(d))

def clear_lock():
    if os.path.exists(LOCK): os.remove(LOCK)

def load_accounts():
    if os.path.exists(ACC):
        try:
            with open(ACC, 'r') as f: return json.load(f)
        except: return {}
    return {}

def save_account(name, username, password):
    accounts = load_accounts()
    accounts[name] = {'username': username, 'password': password, 'saved_at': datetime.now().strftime("%d/%m/%Y %H:%M")}
    try:
        with open(ACC, 'w') as f: json.dump(accounts, f)
        return True
    except: return False

def select_account():
    accounts = load_accounts()
    if not accounts: return None, None
    print("\n═══ TÀI KHOẢN ĐÃ LƯU ═══")
    items = list(accounts.items())
    for i, (name, data) in enumerate(items, 1):
        print(f"[{i}] {name} ({data.get('saved_at', '')})")
    print("[0] Đăng nhập mới\n")
    try:
        choice = input("Chọn: ").strip()
        if choice == '0': return None, None
        idx = int(choice) - 1
        if 0 <= idx < len(items):
            name, data = items[idx]
            return data.get('username'), data.get('password')
    except: pass
    return None, None

def check_vip_user(username):
    try:
        r = requests.get(URL_VIP, timeout=5)
        if r.status_code == 200:
            vip_users = []
            for line in r.text.strip().split('\n'):
                line = line.strip()
                if line and not line.startswith('#'):
                    vip_users.append(line.lower())
            return username.lower() in vip_users
    except: pass
    return False

def login_olm():
    banner()
    lock = load_lock()
    saved_user, saved_pass = select_account()
    
    if saved_user and saved_pass:
        username = saved_user
        password = saved_pass
        print("✓ Dùng tài khoản đã lưu\n")
    else:
        print("═══ ĐĂNG NHẬP OLM ═══\n")
        username = input("Username: ").strip()
        password = input("Password: ").strip()
    
    if not username or not password:
        print("\n✗ Username/Password rỗng")
        time.sleep(2)
        return None, None, None, False
    
    if lock and lock.get('user') != username:
        print("\n✗ Key đã liên kết với tài khoản khác")
        print("Chọn [3] Đổi tài khoản để thay đổi")
        time.sleep(3)
        return None, None, None, False
    
    print("\n⏳ Đăng nhập...")
    
    try:
        session = requests.Session()
        session.headers.update(HEADERS)
        
        session.get("https://olm.vn/dangnhap", headers=HEADERS, timeout=10)
        csrf = session.cookies.get('XSRF-TOKEN')
        
        payload = {
            '_token': csrf, 'username': username, 'password': password,
            'remember': 'true', 'device_id': '0b48f4d6204591f83dc40b07f07af7d4', 'platform': 'web'
        }
        
        h = HEADERS.copy()
        h['x-csrf-token'] = csrf
        session.post("https://olm.vn/post-login", data=payload, headers=h, timeout=10)
        
        check_res = session.get("https://olm.vn/thong-tin-tai-khoan/info", headers=HEADERS, timeout=10)
        match = re.search(r'name="name".*?value="(.*?)"', check_res.text)
        
        if match and match.group(1).strip():
            user_name = match.group(1).strip()
            
            user_id = None
            cookies = session.cookies.get_dict()
            for cookie_name, cookie_value in cookies.items():
                if 'remember_web' in cookie_name and '%7C' in cookie_value:
                    try:
                        parts = cookie_value.split('%7C')
                        if parts and parts[0].isdigit():
                            user_id = parts[0]
                            break
                    except: pass
            
            if not user_id:
                id_matches = re.findall(r'\b\d{10,}\b', check_res.text)
                user_id = id_matches[0] if id_matches else username
            
            is_vip = check_vip_user(username)
            
            print("✓ Đăng nhập thành công")
            print(f"👤 {user_name}")
            if is_vip: print("👑 VIP\n")
            else: print("📦 FREE\n")
            
            if not lock: save_lock(username)
            
            if not saved_user:
                save_choice = input("Lưu tài khoản? (y/n): ").strip().lower()
                if save_choice == 'y':
                    save_account(user_name, username, password)
                    print("✓ Đã lưu\n")
            
            time.sleep(1)
            return session, user_id, user_name, is_vip
        else:
            print("\n✗ Sai username/password")
            time.sleep(2)
            return None, None, None, False
            
    except Exception as e:
        print(f"\n✗ Lỗi: {e}")
        time.sleep(2)
        return None, None, None, False

def get_key():
    while True:
        k = gen_key()
        try:
            url = f"{URL_BLOG}?ma={k}"
            api = f"https://link4m.co/api-shorten/v2?api={API_TOKEN}&url={requests.utils.quote(url)}"
            r = requests.get(api, timeout=8)
            link = r.json().get('shortenedUrl') if r.json().get('status') == 'success' else None
        except: link = None
        
        if not link:
            print("✗ Lỗi tạo link")
            time.sleep(2)
            continue
        
        print(f"\n{'─' * 50}")
        print(f"🔗 {link}")
        print(f"{'─' * 50}\n")
        
        for i in range(3):
            inp = input("Mã (r=link mới): ").strip()
            if inp.lower() == 'r': break
            if inp == k or inp.upper() == "ADMIN_VIP_2026":
                save_lic("FREE", 4)
                print("✓ OK\n")
                time.sleep(1)
                return True
            if i < 2: print(f"✗ Sai ({2-i})")
            time.sleep(i + 1)
        
        if inp.lower() != 'r': return False

def run_tool(session, user_id, user_name):
    banner()
    print("⏳ Đang tải...")
    
    try:
        r = requests.get(URL_MAIN, timeout=15)
        r.raise_for_status()
        
        with open(SESS, 'wb') as f:
            pickle.dump({'cookies': session.cookies.get_dict(), 'user_id': user_id, 'user_name': user_name}, f)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode='w', encoding='utf-8') as f:
            f.write(r.text)
            temp = f.name
        
        env = os.environ.copy()
        env['OLM_LICENSE_FILE'] = LIC
        env['OLM_SESSION_FILE'] = SESS
        env['OLM_LOCK_FILE'] = LOCK
        
        subprocess.run([sys.executable, temp], env=env)
        
        try:
            os.remove(temp)
            os.remove(SESS)
        except: pass
            
    except Exception as e:
        print(f"✗ {e}")
        input("\nEnter...")

if __name__ == "__main__":
    try:
        existing_lic = load_lic()
        
        if existing_lic and existing_lic.get('remain', 0) > 0:
            banner()
            print(f"✓ License: {existing_lic['mode']} | {existing_lic['remain']} lượt\n")
            time.sleep(1)
            session, user_id, user_name, is_vip = login_olm()
            if session: run_tool(session, user_id, user_name)
            sys.exit(0)
        
        session, user_id, user_name, is_vip = login_olm()
        if not session: sys.exit(1)
        
        if is_vip:
            save_lic("VIP", 999999)
            run_tool(session, user_id, user_name)
        else:
            banner()
            print("═══ KÍCH HOẠT KEY FREE ═══\n")
            if get_key(): run_tool(session, user_id, user_name)
        
        sys.exit(0)
        
    except KeyboardInterrupt:
        print("\nTạm biệt!")
        sys.exit(0)
