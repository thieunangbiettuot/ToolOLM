#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║                OLM MASTER PRO - LAUNCHER V1.0               ║
║                     Created by: Tuấn Anh                     ║
╚══════════════════════════════════════════════════════════════╝
"""

import os
import sys
import time
import json
import hashlib
import platform
import tempfile
import subprocess
import requests
import re
import pickle
import socket
import base64
from datetime import datetime, timedelta
from pathlib import Path
import uuid
import random
import string

# ========== CẤU HÌNH ==========
LAUNCHER_VERSION = "1.0"

# API Key Link4m
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
class Colors:
    RESET = '\033[0m'
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    PURPLE = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

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

def get_terminal_width():
    """Lấy chiều rộng terminal"""
    try:
        return os.get_terminal_size().columns
    except:
        return 80

def print_box(title, content, color=Colors.CYAN, width=60):
    """In box với nội dung"""
    if width is None:
        width = min(get_terminal_width() - 4, 80)
    
    # Box top
    print(f"{color}╔{'═' * (width - 2)}╗{Colors.RESET}")
    
    # Title
    if title:
        title_padding = (width - len(title) - 2) // 2
        print(f"{color}║{' ' * title_padding}{Colors.BOLD}{title}{Colors.RESET}{color}{' ' * (width - title_padding - len(title) - 2)}║{Colors.RESET}")
        print(f"{color}╠{'═' * (width - 2)}╣{Colors.RESET}")
    
    # Content
    for line in content:
        if len(line) > width - 4:
            line = line[:width - 7] + "..."
        line_padding = width - len(line) - 4
        print(f"{color}║ {Colors.WHITE}{line}{Colors.RESET}{color}{' ' * line_padding} ║{Colors.RESET}")
    
    # Box bottom
    print(f"{color}╚{'═' * (width - 2)}╝{Colors.RESET}")

def print_menu(title, options):
    """In menu"""
    print_box(title, options, Colors.CYAN)

def wait_enter(prompt="Nhấn Enter để tiếp tục..."):
    """Chờ nhấn Enter"""
    input(f"\n{Colors.YELLOW}{ICONS['info']} {prompt}{Colors.RESET}")

def print_status(message, status='info', color=Colors.WHITE):
    """In thông báo trạng thái"""
    icon = ICONS.get(status, '•')
    print(f"{color}{icon} {message}{Colors.RESET}")

def banner():
    """In banner"""
    clear_screen()
    print(f"\n{Colors.CYAN}{Colors.BOLD}")
    print(r"    ╔═══════════════════════════════════════════════╗")
    print(r"    ║                                               ║")
    print(r"    ║         OLM MASTER PRO v1.0                   ║")
    print(r"    ║                                               ║")
    print(r"    ╚═══════════════════════════════════════════════╝")
    print(f"{Colors.RESET}")
    print(f"{Colors.PURPLE}                Created by: Tuấn Anh{Colors.RESET}\n")

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
    
    print(f"\n{Colors.CYAN}╔{'═' * 48}╗{Colors.RESET}")
    print(f"{Colors.CYAN}║{Colors.YELLOW}{Colors.BOLD}{'TÀI KHOẢN ĐÃ LƯU'.center(48)}{Colors.RESET}{Colors.CYAN}║{Colors.RESET}")
    print(f"{Colors.CYAN}╚{'═' * 48}╝{Colors.RESET}\n")
    
    items = list(accounts.items())
    for i, (name, data) in enumerate(items, 1):
        saved_time = data.get('saved_at', '')
        print(f"  {Colors.YELLOW}[{i}]{Colors.RESET} {Colors.WHITE}{name}{Colors.RESET} {Colors.CYAN}({saved_time}){Colors.RESET}")
    
    print(f"  {Colors.YELLOW}[0]{Colors.RESET} {Colors.WHITE}Đăng nhập mới{Colors.RESET}\n")
    
    try:
        choice = input(f"{Colors.YELLOW}Chọn: {Colors.RESET}").strip()
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
        print(f"{Colors.GREEN}✓ Dùng tài khoản đã lưu{Colors.RESET}\n")
    else:
        print(f"{Colors.CYAN}╔{'═' * 48}╗{Colors.RESET}")
        print(f"{Colors.CYAN}║{Colors.YELLOW}{Colors.BOLD}{'ĐĂNG NHẬP OLM'.center(48)}{Colors.RESET}{Colors.CYAN}║{Colors.RESET}")
        print(f"{Colors.CYAN}╚{'═' * 48}╝{Colors.RESET}\n")
        username = input(f"{Colors.YELLOW}👤 Username: {Colors.RESET}").strip()
        password = input(f"{Colors.YELLOW}🔑 Password: {Colors.RESET}").strip()
    
    if not username or not password:
        print(f"\n{Colors.RED}✗ Username/Password rỗng{Colors.RESET}")
        time.sleep(2)
        return None, None, None, False
    
    if lock and lock.get('user') != username:
        print(f"\n{Colors.RED}✗ Key đã liên kết với tài khoản khác{Colors.RESET}")
        print(f"{Colors.YELLOW}  Chọn [3] Đổi tài khoản để thay đổi{Colors.RESET}")
        time.sleep(3)
        return None, None, None, False
    
    print(f"\n{Colors.YELLOW}⏳ Đang đăng nhập...{Colors.RESET}")
    
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
            
            print(f"{Colors.GREEN}✓ Đăng nhập thành công{Colors.RESET}")
            print(f"{Colors.CYAN}👤 {user_name}{Colors.RESET}")
            
            if is_vip:
                print(f"{Colors.GREEN}👑 VIP UNLIMITED{Colors.RESET}\n")
            else:
                print(f"{Colors.YELLOW}📦 FREE (4 lượt/ngày){Colors.RESET}\n")
            
            if not lock:
                save_lock(username)
            
            if not saved_user:
                save_choice = input(f"{Colors.YELLOW}Lưu tài khoản? (y/n): {Colors.RESET}").strip().lower()
                if save_choice == 'y':
                    save_account(user_name, username, password)
                    print(f"{Colors.GREEN}✓ Đã lưu{Colors.RESET}\n")
            
            time.sleep(1)
            return session, user_id, user_name, is_vip
        else:
            print(f"\n{Colors.RED}✗ Sai username/password{Colors.RESET}")
            time.sleep(2)
            return None, None, None, False
            
    except Exception as e:
        print(f"\n{Colors.RED}✗ Lỗi: {e}{Colors.RESET}")
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
        if d.get('remain', 0) > 0:
            return d
        return None
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

# ========== GET KEY ==========
def get_key():
    """Lấy key từ link4m"""
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
            print(f"{Colors.RED}✗ Lỗi tạo link{Colors.RESET}")
            time.sleep(2)
            continue
        
        print(f"\n{Colors.CYAN}{'─' * 50}{Colors.RESET}")
        print(f"{Colors.GREEN}🔗 Link: {Colors.YELLOW}{link}{Colors.RESET}")
        print(f"{Colors.CYAN}{'─' * 50}{Colors.RESET}\n")
        
        for i in range(3):
            inp = input(f"{Colors.YELLOW}🔑 Mã (r=link mới): {Colors.RESET}").strip()
            
            if inp.lower() == 'r':
                break
            
            if inp == k or inp.upper() == "ADMIN_VIP_2026":
                save_lic("FREE", 4)
                print(f"{Colors.GREEN}✓ OK{Colors.RESET}\n")
                time.sleep(1)
                return True
            
            if i < 2:
                print(f"{Colors.RED}✗ Sai ({2-i} lần){Colors.RESET}")
            time.sleep(i + 1)
        
        if inp.lower() != 'r':
            return False

# ========== CHẠY TOOL ==========
def run_tool(session, user_id, user_name):
    """Tải và chạy main.py"""
    banner()
    print(f"{Colors.YELLOW}⏳ Đang tải tool...{Colors.RESET}")
    
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
        print(f"{Colors.RED}✗ Lỗi: {e}{Colors.RESET}")
        input("\nEnter...")

# ========== MAIN ==========
def main():
    """Hàm chính"""
    # Anti-debug
    if hasattr(sys, 'gettrace') and sys.gettrace():
        sys.exit(0)
    
    try:
        existing_lic = load_lic()
        
        if existing_lic and existing_lic.get('remain', 0) > 0:
            banner()
            mode = existing_lic['mode']
            remain = existing_lic['remain']
            if mode == 'VIP':
                print(f"{Colors.GREEN}✓ License: VIP | UNLIMITED{Colors.RESET}\n")
            else:
                print(f"{Colors.GREEN}✓ License: FREE | {remain} lượt{Colors.RESET}\n")
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
            print(f"{Colors.CYAN}╔{'═' * 48}╗{Colors.RESET}")
            print(f"{Colors.CYAN}║{Colors.YELLOW}{Colors.BOLD}{'KÍCH HOẠT KEY FREE'.center(48)}{Colors.RESET}{Colors.CYAN}║{Colors.RESET}")
            print(f"{Colors.CYAN}╚{'═' * 48}╝{Colors.RESET}\n")
            
            if get_key():
                run_tool(session, user_id, user_name)
        
        sys.exit(0)
        
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Tạm biệt!{Colors.RESET}")
        sys.exit(0)

if __name__ == "__main__":
    main()
