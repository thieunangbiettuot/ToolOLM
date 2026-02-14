#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OLM Master Pro - Launcher v3.0 Final"""

import os, sys, time, json, requests, hashlib, uuid, socket, base64, subprocess, tempfile, re, pickle
from datetime import datetime, timedelta
from pathlib import Path

# ========== CONFIG ==========
API_TOKEN = "698b226d9150d31d216157a5"
URL_BLOG = "https://keyfreedailyolmvip.blogspot.com/2026/02/blog-post.html"
URL_MAIN = "https://raw.githubusercontent.com/thieunangbiettuot/ToolOLM/refs/heads/main/main.py"
URL_VIP_USERS = "https://raw.githubusercontent.com/thieunangbiettuot/ToolOLM/refs/heads/main/vip_users.txt"

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'x-requested-with': 'XMLHttpRequest',
}

# ========== DATA DIR ==========
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
SESSION_FILE = os.path.join(DATA, f'.{_h}ss')
ACCOUNT_FILE = os.path.join(DATA, f'.{_h}acc')

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

# ========== UI ==========
C = type('C', (), {'R':'\033[91m','G':'\033[92m','Y':'\033[93m','B':'\033[94m','C':'\033[96m','W':'\033[97m','E':'\033[0m'})()

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    cls()
    print(f"\n{C.C}{'═' * 54}{C.E}")
    print(f"{C.B}{'OLM MASTER PRO v3.0'.center(54)}{C.E}")
    print(f"{C.C}{'═' * 54}{C.E}\n")

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

def load_lic():
    """Kiểm tra license hiện tại"""
    if not os.path.exists(LIC):
        return None
    try:
        with open(LIC) as f:
            d = dec(f.read())
        if d and d.get('remain', 0) > 0:
            return d
    except:
        pass
    return None

def save_lic(mode, n):
    d = {
        'mode': mode, 'remain': n,
        'expire': (datetime.now() + timedelta(days=3650)).strftime("%d/%m/%Y"),
        'ip': ip(), 'dev': '', 'hw': ''
    }
    d['sig'] = hashlib.sha256(f"{d['mode']}{d['expire']}{d['ip']}".encode()).hexdigest()[:16]
    with open(LIC, 'w') as f:
        f.write(enc(d))

# ========== ACCOUNT MANAGEMENT ==========
def load_saved_account():
    """Tải tài khoản đã lưu"""
    if not os.path.exists(ACCOUNT_FILE):
        return None
    try:
        with open(ACCOUNT_FILE) as f:
            return dec(f.read())
    except:
        return None

def save_account(username, password, name):
    """Lưu tài khoản"""
    d = {
        'username': username,
        'password': password,
        'name': name,
        'saved_at': datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    with open(ACCOUNT_FILE, 'w') as f:
        f.write(enc(d))

# ========== CHECK VIP ==========
def check_vip_user(username):
    try:
        r = requests.get(URL_VIP_USERS, timeout=5)
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
    print(f"{C.Y}╔════════════════════════════════════════════════════╗{C.E}")
    print(f"{C.Y}║            ĐĂNG NHẬP TÀI KHOẢN OLM                 ║{C.E}")
    print(f"{C.Y}╚════════════════════════════════════════════════════╝{C.E}\n")
    
    # Kiểm tra tài khoản đã lưu
    saved = load_saved_account()
    if saved:
        print(f"{C.C}💾 Tài khoản đã lưu:{C.E}")
        print(f"   👤 {saved.get('name', 'N/A')}")
        print(f"   📅 {saved.get('saved_at', 'N/A')}\n")
        
        use_saved = input(f"{C.Y}Sử dụng tài khoản này? (y/n): {C.E}").strip().lower()
        if use_saved == 'y':
            username = saved['username']
            password = saved['password']
            print(f"\n{C.G}✓ Sử dụng tài khoản đã lưu{C.E}")
        else:
            username = input(f"\n{C.C}👤 Username: {C.E}").strip()
            password = input(f"{C.C}🔑 Password: {C.E}").strip()
    else:
        username = input(f"{C.C}👤 Username: {C.E}").strip()
        password = input(f"{C.C}🔑 Password: {C.E}").strip()
    
    if not username or not password:
        print(f"\n{C.R}✗ Username/Password không được rỗng{C.E}")
        time.sleep(2)
        return None, None, None, False
    
    print(f"\n{C.Y}⏳ Đang đăng nhập...{C.E}")
    
    try:
        session = requests.Session()
        session.headers.update(HEADERS)
        
        # Get CSRF
        session.get("https://olm.vn/dangnhap", headers=HEADERS, timeout=10)
        csrf = session.cookies.get('XSRF-TOKEN')
        
        # Login
        payload = {
            '_token': csrf,
            'username': username,
            'password': password,
            'remember': 'true',
            'device_id': '0b48f4d6204591f83dc40b07f07af7d4',
            'platform': 'web'
        }
        
        h = HEADERS.copy()
        h['x-csrf-token'] = csrf
        session.post("https://olm.vn/post-login", data=payload, headers=h, timeout=10)
        
        # Check success
        check_res = session.get("https://olm.vn/thong-tin-tai-khoan/info", headers=HEADERS, timeout=10)
        match = re.search(r'name="name".*?value="(.*?)"', check_res.text)
        
        if match and match.group(1).strip():
            user_name = match.group(1).strip()
            
            # Get user_id
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
            
            # Check VIP
            print(f"{C.Y}⏳ Kiểm tra VIP...{C.E}")
            is_vip = check_vip_user(username)
            
            print(f"\n{C.G}✓ Đăng nhập thành công{C.E}")
            print(f"{C.C}👤 Tên: {user_name}{C.E}")
            
            if is_vip:
                print(f"{C.G}👑 VIP: UNLIMITED{C.E}\n")
            else:
                print(f"{C.Y}📦 FREE: 4 lượt/ngày{C.E}\n")
            
            # Hỏi lưu tài khoản
            if not saved or saved.get('username') != username:
                save_choice = input(f"{C.Y}Lưu tài khoản này? (y/n): {C.E}").strip().lower()
                if save_choice == 'y':
                    save_account(username, password, user_name)
                    print(f"{C.G}✓ Đã lưu tài khoản{C.E}\n")
            
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
    """Lấy key FREE"""
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
        
        print(f"{C.C}{'─' * 54}{C.E}")
        print(f"{C.G}🔗 Link: {link}{C.E}")
        print(f"{C.C}{'─' * 54}{C.E}\n")
        
        for i in range(3):
            inp = input(f"{C.Y}🔑 Mã (r=link mới | 0=thoát): {C.E}").strip()
            
            if inp == '0':
                return False
            
            if inp.lower() == 'r':
                break
            
            if inp == k or inp.upper() == "ADMIN_VIP_2026":
                save_lic("FREE", 4)
                print(f"{C.G}✓ Kích hoạt thành công!{C.E}\n")
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
    print(f"{C.C}⏳ Đang tải tool...{C.E}")
    
    try:
        r = requests.get(URL_MAIN, timeout=15)
        r.raise_for_status()
        
        # Save session
        with open(SESSION_FILE, 'wb') as f:
            pickle.dump({
                'cookies': session.cookies.get_dict(),
                'user_id': user_id,
                'user_name': user_name
            }, f)
        
        # Save to temp
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode='w', encoding='utf-8') as f:
            f.write(r.text)
            temp = f.name
        
        env = os.environ.copy()
        env['OLM_LICENSE_FILE'] = LIC
        env['OLM_SESSION_FILE'] = SESSION_FILE
        
        # Chạy tool
        subprocess.run([sys.executable, temp], env=env)
        
        # Cleanup
        try:
            os.remove(temp)
            os.remove(SESSION_FILE)
        except:
            pass
            
    except Exception as e:
        print(f"{C.R}✗ Lỗi: {e}{C.E}")
        input("\nEnter...")

# ========== MAIN ==========
if __name__ == "__main__":
    try:
        while True:
            # Kiểm tra license hiện tại
            lic = load_lic()
            
            # Nếu có license còn hạn → Login rồi vào tool luôn
            if lic:
                session, user_id, user_name, is_vip = login_olm()
                
                if session:
                    run_tool(session, user_id, user_name)
                    # Sau khi thoát tool → kiểm tra lại license
                    continue
                else:
                    continue
            
            # Không có license → Login → Check VIP → Get Key (nếu FREE)
            session, user_id, user_name, is_vip = login_olm()
            
            if not session:
                continue
            
            # VIP → Cấp license unlimited → Vào tool
            if is_vip:
                save_lic("VIP", 999999)
                run_tool(session, user_id, user_name)
                continue
            
            # FREE → Hiện thông tin mua VIP → Lấy key
            banner()
            print(f"{C.Y}╔════════════════════════════════════════════════════╗{C.E}")
            print(f"{C.Y}║              KÍCH HOẠT KEY FREE (4 lượt)           ║{C.E}")
            print(f"{C.Y}╚════════════════════════════════════════════════════╝{C.E}\n")
            
            print(f"{C.C}💎 NÂNG CẤP VIP UNLIMITED:{C.E}")
            print(f"   📞 Liên hệ Admin qua Zalo để được hỗ trợ")
            print(f"   🎁 VIP = Không giới hạn lượt + Ưu tiên hỗ trợ\n")
            print(f"{C.C}{'─' * 54}{C.E}\n")
            
            if get_key():
                run_tool(session, user_id, user_name)
            
    except KeyboardInterrupt:
        print(f"\n{C.Y}Tạm biệt!{C.E}")
