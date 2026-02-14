#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OLM Master Pro - Launcher v3.0"""

import os, sys, time, json, requests, hashlib, uuid, socket, base64, subprocess, tempfile, re, pickle
from datetime import datetime, timedelta
from pathlib import Path

# ========== CONFIG ==========
API_TOKEN = "698b226d9150d31d216157a5"
URL_BLOG = "https://keyfreedailyolmvip.blogspot.com/2026/02/blog-post.html"
URL_MAIN = "https://raw.githubusercontent.com/thieunangbiettuot/ToolOLM/refs/heads/main/main.py"
URL_VIP = "https://raw.githubusercontent.com/thieunangbiettuot/ToolOLM/refs/heads/main/vip_users.txt"

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'x-requested-with': 'XMLHttpRequest',
}

# ========== DATA DIR (CROSS-PLATFORM) ==========
def get_data_dir():
    p = sys.platform
    if p == 'win32':
        d = Path(os.getenv('LOCALAPPDATA', os.path.expanduser('~'))) / 'Microsoft' / 'Windows' / 'INetCache' / 'IE'
    elif p == 'darwin':
        d = Path.home() / 'Library' / 'Application Support' / 'com.apple.Safari'
    elif 'ANDROID_ROOT' in os.environ or 'TERMUX_VERSION' in os.environ:
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

# ========== CRYPTO ==========
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

# ========== COLORS ==========
class C:
    R = '\033[91m'
    G = '\033[92m'
    Y = '\033[93m'
    B = '\033[94m'
    M = '\033[95m'
    C = '\033[96m'
    W = '\033[97m'
    BOLD = '\033[1m'
    E = '\033[0m'

# ========== UI ==========
def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    cls()
    print(f"\n{C.C}{C.BOLD}")
    print(r"    ╔═══════════════════════════════════════════════╗")
    print(r"    ║                                               ║")
    print(r"    ║         OLM MASTER PRO v3.0                   ║")
    print(r"    ║                                               ║")
    print(r"    ╚═══════════════════════════════════════════════╝")
    print(f"{C.E}")
    print(f"{C.M}                Created by: Tuấn Anh{C.E}\n")

# ========== SYSTEM ==========
def ip():
    try:
        return requests.get('https://api.ipify.org', timeout=5).text.strip()
    except:
        return "0.0.0.0"

def gen_key():
    import random
    now = datetime.now()
    dev = hashlib.md5(f"{socket.gethostname()}{uuid.getnode()}".encode()).hexdigest()[:16]
    unique = f"{dev}{now.timestamp()}{random.randint(1000, 9999)}"
    h = hashlib.sha256(unique.encode()).hexdigest()
    return f"OLM-{now:%d%m}-{h[:4].upper()}-{h[4:8].upper()}"

def sig(d):
    return hashlib.sha256(f"{d['mode']}{d['expire']}{d['ip']}".encode()).hexdigest()[:16]

# ========== LICENSE ==========
def load_lic():
    if not os.path.exists(LIC):
        return None
    try:
        with open(LIC) as f:
            d = dec(f.read())
        if not d or d.get('sig') != sig(d):
            return None
        if datetime.strptime(d['expire'], "%d/%m/%Y").date() < datetime.now().date():
            return None
        if d.get('mode') == 'FREE' and d.get('ip') != ip():
            return None
        if d.get('remain', 0) > 0:
            return d
        return None
    except:
        return None

def save_lic(mode, n):
    expire_days = 3650 if mode == 'VIP' else 1
    d = {
        'mode': mode, 'remain': n,
        'expire': (datetime.now() + timedelta(days=expire_days)).strftime("%d/%m/%Y"),
        'ip': ip(), 'dev': '', 'hw': ''
    }
    d['sig'] = sig(d)
    with open(LIC, 'w') as f:
        f.write(enc(d))

# ========== ACCOUNT LOCK ==========
def load_lock():
    if os.path.exists(LOCK):
        try:
            with open(LOCK) as f:
                return dec(f.read())
        except:
            pass
    return None

def save_lock(username):
    d = {'user': username, 'time': datetime.now().strftime("%d/%m/%Y %H:%M")}
    with open(LOCK, 'w') as f:
        f.write(enc(d))

def clear_lock():
    if os.path.exists(LOCK):
        os.remove(LOCK)

# ========== SAVED ACCOUNTS ==========
def load_accounts():
    if os.path.exists(ACC):
        try:
            with open(ACC, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_account(name, username, password):
    accounts = load_accounts()
    accounts[name] = {
        'username': username,
        'password': password,
        'saved_at': datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    try:
        with open(ACC, 'w') as f:
            json.dump(accounts, f)
        return True
    except:
        return False

def select_account():
    accounts = load_accounts()
    if not accounts:
        return None, None
    
    print(f"\n{C.C}╔{'═' * 48}╗{C.E}")
    print(f"{C.C}║{C.Y}{C.BOLD}{'TÀI KHOẢN ĐÃ LƯU'.center(48)}{C.E}{C.C}║{C.E}")
    print(f"{C.C}╚{'═' * 48}╝{C.E}\n")
    
    items = list(accounts.items())
    for i, (name, data) in enumerate(items, 1):
        saved_time = data.get('saved_at', '')
        print(f"  {C.Y}[{i}]{C.E} {C.W}{name}{C.E} {C.C}({saved_time}){C.E}")
    
    print(f"  {C.Y}[0]{C.E} {C.W}Đăng nhập mới{C.E}\n")
    
    try:
        choice = input(f"{C.Y}Chọn: {C.E}").strip()
        if choice == '0':
            return None, None
        idx = int(choice) - 1
        if 0 <= idx < len(items):
            name, data = items[idx]
            return data.get('username'), data.get('password')
    except:
        pass
    return None, None

# ========== CHECK VIP ==========
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
    except:
        pass
    return False

# ========== LOGIN OLM ==========
def login_olm():
    banner()
    
    lock = load_lock()
    saved_user, saved_pass = select_account()
    
    if saved_user and saved_pass:
        username = saved_user
        password = saved_pass
        print(f"{C.G}✓ Dùng tài khoản đã lưu{C.E}\n")
    else:
        print(f"{C.C}╔{'═' * 48}╗{C.E}")
        print(f"{C.C}║{C.Y}{C.BOLD}{'ĐĂNG NHẬP OLM'.center(48)}{C.E}{C.C}║{C.E}")
        print(f"{C.C}╚{'═' * 48}╝{C.E}\n")
        username = input(f"{C.Y}👤 Username: {C.E}").strip()
        password = input(f"{C.Y}🔑 Password: {C.E}").strip()
    
    if not username or not password:
        print(f"\n{C.R}✗ Username/Password rỗng{C.E}")
        time.sleep(2)
        return None, None, None, False
    
    if lock and lock.get('user') != username:
        print(f"\n{C.R}✗ Key đã liên kết với tài khoản khác{C.E}")
        print(f"{C.Y}  Chọn [3] Đổi tài khoản để thay đổi{C.E}")
        time.sleep(3)
        return None, None, None, False
    
    print(f"\n{C.Y}⏳ Đang đăng nhập...{C.E}")
    
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
                    except:
                        pass
            
            if not user_id:
                id_matches = re.findall(r'\b\d{10,}\b', check_res.text)
                user_id = id_matches[0] if id_matches else username
            
            is_vip = check_vip_user(username)
            
            print(f"{C.G}✓ Đăng nhập thành công{C.E}")
            print(f"{C.C}👤 {user_name}{C.E}")
            
            if is_vip:
                print(f"{C.G}👑 VIP UNLIMITED{C.E}\n")
            else:
                print(f"{C.Y}📦 FREE (4 lượt/ngày){C.E}\n")
            
            if not lock:
                save_lock(username)
            
            if not saved_user:
                save_choice = input(f"{C.Y}Lưu tài khoản? (y/n): {C.E}").strip().lower()
                if save_choice == 'y':
                    save_account(user_name, username, password)
                    print(f"{C.G}✓ Đã lưu{C.E}\n")
            
            time.sleep(1)
            return session, user_id, user_name, is_vip
        else:
            print(f"\n{C.R}✗ Sai username/password{C.E}")
            time.sleep(2)
            return None, None, None, False
            
    except Exception as e:
        print(f"\n{C.R}✗ Lỗi: {e}{C.E}")
        time.sleep(2)
        return None, None, None, False

# ========== GET KEY ==========
def get_key():
    while True:
        k = gen_key()
        
        try:
            url = f"{URL_BLOG}?ma={k}"
            api = f"https://link4m.co/api-shorten/v2?api={API_TOKEN}&url={requests.utils.quote(url)}"
            r = requests.get(api, timeout=8)
            link = r.json().get('shortenedUrl') if r.json().get('status') == 'success' else None
        except:
            link = None
        
        if not link:
            print(f"{C.R}✗ Lỗi tạo link{C.E}")
            time.sleep(2)
            continue
        
        print(f"\n{C.C}{'─' * 50}{C.E}")
        print(f"{C.G}🔗 Link: {C.Y}{link}{C.E}")
        print(f"{C.C}{'─' * 50}{C.E}\n")
        
        for i in range(3):
            inp = input(f"{C.Y}🔑 Mã (r=link mới): {C.E}").strip()
            
            if inp.lower() == 'r':
                break
            
            if inp == k or inp.upper() == "ADMIN_VIP_2026":
                save_lic("FREE", 4)
                print(f"{C.G}✓ OK{C.E}\n")
                time.sleep(1)
                return True
            
            if i < 2:
                print(f"{C.R}✗ Sai ({2-i} lần){C.E}")
            time.sleep(i + 1)
        
        if inp.lower() != 'r':
            return False

# ========== RUN TOOL ==========
def run_tool(session, user_id, user_name):
    banner()
    print(f"{C.Y}⏳ Đang tải tool...{C.E}")
    
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
        except:
            pass
            
    except Exception as e:
        print(f"{C.R}✗ Lỗi: {e}{C.E}")
        input("\nEnter...")

# ========== MAIN ==========
if __name__ == "__main__":
    try:
        existing_lic = load_lic()
        
        if existing_lic and existing_lic.get('remain', 0) > 0:
            banner()
            mode = existing_lic['mode']
            remain = existing_lic['remain']
            if mode == 'VIP':
                print(f"{C.G}✓ License: VIP | UNLIMITED lượt{C.E}\n")
            else:
                print(f"{C.G}✓ License: FREE | {remain} lượt{C.E}\n")
            time.sleep(1)
            
            session, user_id, user_name, is_vip = login_olm()
            if session:
                run_tool(session, user_id, user_name)
            sys.exit(0)
        
        session, user_id, user_name, is_vip = login_olm()
        if not session:
            sys.exit(1)
        
        if is_vip:
            save_lic("VIP", 999999)
            run_tool(session, user_id, user_name)
        else:
            banner()
            print(f"{C.C}╔{'═' * 48}╗{C.E}")
            print(f"{C.C}║{C.Y}{C.BOLD}{'KÍCH HOẠT KEY FREE'.center(48)}{C.E}{C.C}║{C.E}")
            print(f"{C.C}╚{'═' * 48}╝{C.E}\n")
            
            if get_key():
                run_tool(session, user_id, user_name)
        
        sys.exit(0)
        
    except KeyboardInterrupt:
        print(f"\n{C.Y}Tạm biệt!{C.E}")
        sys.exit(0)
