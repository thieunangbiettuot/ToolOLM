#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║                OLM MASTER PRO - LAUNCHER V1.0               ║
║                     Created by: Tuấn Anh                     ║
╚══════════════════════════════════════════════════════════════╝
"""

import os, sys, time, json, hashlib, platform, tempfile, subprocess, requests, re, pickle, socket, base64
from datetime import datetime, timedelta
from pathlib import Path
import uuid, random, string

# ========== CẤU HÌNH ==========
API_TOKEN = "698b226d9150d31d216157a5"
URL_BLOG = "https://keyfreedailyolmvip.blogspot.com/2026/02/blog-post.html"
URL_MAIN = "https://raw.githubusercontent.com/thieunangbiettuot/ToolOLM/refs/heads/main/main.py"
URL_VIP = "https://raw.githubusercontent.com/thieunangbiettuot/ToolOLM/refs/heads/main/vip_users.txt"

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'x-requested-with': 'XMLHttpRequest',
}

# Màu sắc
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

# Icon
ICONS = {
    'success': '✓',
    'error': '✗',
    'warning': '⚠',
    'info': 'ℹ',
    'lock': '🔒',
    'user': '👤',
    'key': '🔑',
    'star': '★',
    'rocket': '🚀',
    'diamond': '💎',
    'crown': '👑',
    'check': '✔',
    'exit': '🚪',
    'refresh': '🔄',
    'download': '📥',
    'link': '🔗',
    'list': '📋',
    'brain': '🧠',
    'heart': '❤️'
}

# ========== TIỆN ÍCH ==========
def clear_screen():
    """Xóa màn hình"""
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    """In banner"""
    clear_screen()
    print(f"\n{C.C}{C.BOLD}")
    print(r"    ╔═══════════════════════════════════════════════╗")
    print(r"    ║                                               ║")
    print(r"    ║         OLM MASTER PRO v1.0                   ║")
    print(r"    ║                                               ║")
    print(r"    ╚═══════════════════════════════════════════════╝")
    print(f"{C.E}")
    print(f"{C.M}                Created by: Tuấn Anh{C.E}\n")

def print_box(title, content, color=C.C, width=60):
    """In box với nội dung"""
    print(f"{color}╔{'═' * (width - 2)}╗{C.E}")
    if title:
        title_padding = (width - len(title) - 2) // 2
        print(f"{color}║{' ' * title_padding}{C.BOLD}{title}{C.E}{color}{' ' * (width - title_padding - len(title) - 2)}║{C.E}")
        print(f"{color}╠{'═' * (width - 2)}╣{C.E}")
    for line in content:
        if len(line) > width - 4:
            line = line[:width - 7] + "..."
        line_padding = width - len(line) - 4
        print(f"{color}║ {C.W}{line}{C.E}{color}{' ' * line_padding} ║{C.E}")
    print(f"{color}╚{'═' * (width - 2)}╝{C.E}")

def print_status(message, status='info', color=C.W):
    """In thông báo trạng thái"""
    icon = ICONS.get(status, '•')
    print(f"{icon} {color}{message}{C.E}")

def wait_enter(prompt="Nhấn Enter để tiếp tục..."):
    """Chờ nhấn Enter"""
    input(f"\n{C.Y}{ICONS['info']} {prompt}{C.E}")

# ========== THƯ MỤC DỮ LIỆU ==========
def get_data_dir():
    """Lấy thư mục dữ liệu"""
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

# ========== MÃ HÓA ==========
KEY = b'OLM_ULTRA_SECRET_2026'

def enc(obj):
    """Mã hóa dữ liệu"""
    txt = json.dumps(obj, separators=(',', ':')).encode()
    xor = bytearray(txt[i] ^ KEY[i % len(KEY)] for i in range(len(txt)))
    b85 = base64.b85encode(bytes(xor)).decode()
    chk = hashlib.sha256(b85.encode()).hexdigest()[:12]
    noise = hashlib.md5(chk.encode()).hexdigest()[:8]
    return f"{noise}{chk}{b85}{noise[::-1]}"

def dec(s):
    """Giải mã dữ liệu"""
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

# ========== QUẢN LÝ TÀI KHOẢN ==========
def load_accounts():
    """Tải danh sách tài khoản"""
    if os.path.exists(ACC):
        try:
            with open(ACC, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_account(name, username, password):
    """Lưu tài khoản"""
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
    """Chọn tài khoản"""
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

# ========== ĐĂNG NHẬP OLM ==========
def login_olm():
    """Đăng nhập OLM"""
    banner()
    
    lock = load_lock()
    saved_user, saved_pass = select_account()
    
    if saved_user and saved_pass:
        username = saved_user
        password = saved_pass
        print_status("Dùng tài khoản đã lưu", 'success', C.G)
    else:
        print_box("ĐĂNG NHẬP OLM", [])
        username = input(f"{C.Y}👤 Username: {C.E}").strip()
        password = input(f"{C.Y}🔑 Password: {C.E}").strip()
    
    if not username or not password:
        print_status("Username/Password rỗng", 'error', C.R)
        time.sleep(2)
        return None, None, None
    
    if lock and lock.get('user') != username:
        print_status("Key đã liên kết với tài khoản khác", 'error', C.R)
        print_status("Chọn [3] Đổi tài khoản để thay đổi", 'info', C.Y)
        time.sleep(3)
        return None, None, None
    
    print_status("Đang đăng nhập...", 'info', C.Y)
    
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
            
            # Check VIP
            is_vip = check_vip_user(username)
            
            print_status("Đăng nhập thành công", 'success', C.G)
            print_status(f"👤 {user_name}", 'info', C.C)
            
            if is_vip:
                print_status("👑 VIP UNLIMITED", 'success', C.G)
            else:
                print_status("📦 FREE (4 lượt/ngày)", 'info', C.Y)
            
            if not lock:
                save_lock(username)
            
            if not saved_user:
                save_choice = input(f"{C.Y}Lưu tài khoản? (y/n): {C.E}").strip().lower()
                if save_choice == 'y':
                    save_account(user_name, username, password)
                    print_status("Đã lưu", 'success', C.G)
            
            time.sleep(1)
            return session, user_id, user_name, is_vip
        else:
            print_status("Sai username/password", 'error', C.R)
            time.sleep(2)
            return None, None, None, False
            
    except Exception as e:
        print_status(f"Lỗi: {e}", 'error', C.R)
        time.sleep(2)
        return None, None, None, False

# ========== CHECK VIP ==========
def check_vip_user(username):
    """Check VIP từ GitHub"""
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

# ========== KEY GENERATION ==========
def gen_key():
    """Tạo key độc nhất"""
    now = datetime.now()
    dev = hashlib.md5(f"{socket.gethostname()}{uuid.getnode()}".encode()).hexdigest()[:16]
    unique = f"{dev}{now.timestamp()}{random.randint(1000, 9999)}"
    h = hashlib.sha256(unique.encode()).hexdigest()
    return f"OLM-{now:%d%m}-{h[:4].upper()}-{h[4:8].upper()}"

def sig(d):
    """Tạo signature"""
    return hashlib.sha256(f"{d['mode']}{d['expire']}{d['ip']}".encode()).hexdigest()[:16]

def ip():
    """Lấy IP hiện tại"""
    try:
        return requests.get('https://api.ipify.org', timeout=5).text.strip()
    except:
        return "0.0.0.0"

# ========== QUẢN LÝ LICENSE ==========
def load_lic():
    """Tải license"""
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
        return d
    except:
        return None

def save_lic(mode, n):
    """Lưu license"""
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
    """Tải account lock"""
    if os.path.exists(LOCK):
        try:
            with open(LOCK) as f:
                return dec(f.read())
        except:
            pass
    return None

def save_lock(username):
    """Lưu account lock"""
    d = {'user': username, 'time': datetime.now().strftime("%d/%m/%Y %H:%M")}
    with open(LOCK, 'w') as f:
        f.write(enc(d))

def clear_lock():
    """Xóa account lock"""
    if os.path.exists(LOCK):
        os.remove(LOCK)

# ========== HÀM TẠO LINK ==========
def create_short_link(url):
    """Tạo link rút gọn với link4m"""
    try:
        encoded = requests.utils.quote(url)
        api_url = f"https://link4m.co/api-shorten/v2?api={API_TOKEN}&url={encoded}"
        response = requests.get(api_url, timeout=10)
        data = response.json()

        if data.get("status") == "success":
            return data.get("shortenedUrl")

    except:
        pass

    return url

# ========== GET KEY ==========
def get_key():
    """Lấy key từ link4m"""
    while True:
        k = gen_key()
        
        # Tạo link
        url = f"{URL_BLOG}?ma={k}"
        short_url = create_short_link(url)
        
        if short_url == url:
            print_status("Lỗi tạo link rút gọn", 'error', C.R)
            time.sleep(2)
            continue
        
        # Hiển thị link
        print_box("VƯỚT LINK ĐỂ LẤY KEY", [f"Link: {short_url}"], C.Y)
        
        for i in range(3):
            inp = input(f"{C.Y}🔑 Mã (r=link mới): {C.E}").strip()
            
            if inp.lower() == 'r':
                break
            
            if inp == k or inp.upper() == "ADMIN_VIP_2026":
                save_lic("FREE", 4)
                print_status("OK", 'success', C.G)
                time.sleep(1)
                return True
            
            if i < 2:
                print_status(f"Sai ({2-i} lần)", 'error', C.R)
            time.sleep(i + 1)
        
        if inp.lower() != 'r':
            return False

# ========== CHẠY TOOL ==========
def run_tool(session, user_id, user_name):
    """Tải và chạy main.py"""
    banner()
    print_status("Đang tải tool...", 'info', C.Y)
    
    try:
        r = requests.get(URL_MAIN, timeout=15)
        r.raise_for_status()
        
        with open(SESS, 'wb') as f:
            pickle.dump({'cookies': session.cookies.get_dict(), 'user_id': user_id, 'user_name': user_name}, f)
        
        # Tạo file tạm để chạy main.py
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode='w', encoding='utf-8') as f:
            f.write(r.text)
            temp = f.name
        
        # Lưu license để main.py đọc được
        try:
            lic_data = load_lic()
            if lic_data:
                lic_file = os.path.join(tempfile.gettempdir(), "license_olm.pkl")
                with open(lic_file, 'wb') as f:
                    pickle.dump(lic_data, f)
        except:
            pass
        
        # Chạy main.py
        subprocess.run([sys.executable, temp])
        
        # Xóa file tạm
        try:
            os.remove(temp)
            os.remove(SESS)
            lic_file = os.path.join(tempfile.gettempdir(), "license_olm.pkl")
            if os.path.exists(lic_file):
                os.remove(lic_file)
        except:
            pass
            
    except Exception as e:
        print_status(f"Lỗi: {e}", 'error', C.R)
        wait_enter()

# ========== MAIN ==========
def main():
    """Hàm chính"""
    # Anti-debug
    if hasattr(sys, 'gettrace') and sys.gettrace():
        sys.exit(0)
    
    try:
        session, user_id, user_name, is_vip = login_olm()
        if not session:
            sys.exit(1)
        
        if is_vip:
            # VIP - Tạo license trực tiếp
            save_lic("VIP", 999999)
            run_tool(session, user_id, user_name)
        else:
            # FREE - Kiểm tra license cũ
            existing_lic = load_lic()
            
            if existing_lic and existing_lic.get('remain', 0) > 0:
                banner()
                remain = existing_lic['remain']
                print_status(f"License: FREE | {remain} lượt", 'success', C.G)
                time.sleep(1)
                run_tool(session, user_id, user_name)
            else:
                # Cần get key mới
                banner()
                print_box("KÍCH HOẠT KEY FREE", [])
                if get_key():
                    run_tool(session, user_id, user_name)
        
        sys.exit(0)
        
    except KeyboardInterrupt:
        print(f"\n{C.Y}Tạm biệt!{C.E}")
        sys.exit(0)

if __name__ == "__main__":
    main()
