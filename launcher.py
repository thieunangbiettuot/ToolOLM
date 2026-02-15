#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║              OLM MASTER PRO V4.0 - LAUNCHER                  ║
║                  Ultimate Edition                            ║
╚══════════════════════════════════════════════════════════════╝
"""

import os
import sys
import time
import json
import requests
import hashlib
import uuid
import socket
import base64
import subprocess
import tempfile
import re
import pickle
import threading
from datetime import datetime, timedelta
from pathlib import Path

# ==================== CONFIGURATION ====================
API_TOKEN = "698b226d9150d31d216157a5"
URL_MAIN = "https://raw.githubusercontent.com/thieunangbiettuot/ToolOLM/refs/heads/main/main.py"
URL_VIP = "https://raw.githubusercontent.com/thieunangbiettuot/ToolOLM/refs/heads/main/vip_users.txt"

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'x-requested-with': 'XMLHttpRequest',
}

# ==================== COLORS & EFFECTS ====================
class Color:
    # Basic Colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright Colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Styles
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    HIDDEN = '\033[8m'
    
    # Background
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    
    # Reset
    RESET = '\033[0m'
    END = '\033[0m'

# ==================== FILE PATHS ====================
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

KEY = b'OLM_ULTRA_SECRET_2026'

# ==================== ENCRYPTION ====================
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

# ==================== UI UTILITIES ====================
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_terminal_width():
    try:
        return os.get_terminal_size().columns
    except:
        return 80

def center_text(text, width=None):
    if width is None:
        width = get_terminal_width()
    # Remove ANSI codes for length calculation
    clean_text = re.sub(r'\033\[[0-9;]+m', '', text)
    padding = (width - len(clean_text)) // 2
    return ' ' * padding + text

def print_center(text, color=''):
    print(center_text(f"{color}{text}{Color.RESET}"))

def print_gradient_line(char='═', width=None):
    if width is None:
        width = get_terminal_width()
    colors = [Color.CYAN, Color.BRIGHT_CYAN, Color.BLUE, Color.BRIGHT_BLUE]
    segment_width = width // len(colors)
    line = ''
    for i, color in enumerate(colors):
        segment = char * segment_width
        line += f"{color}{segment}"
    line += Color.RESET
    print(line)

def loading_animation(text, duration=1.5):
    """Animated loading with dots"""
    frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        print(f"\r{Color.YELLOW}{frames[i % len(frames)]} {text}...{Color.RESET}", end='', flush=True)
        time.sleep(0.1)
        i += 1
    print(f"\r{' ' * (len(text) + 10)}\r", end='', flush=True)

def progress_bar(progress, total, width=40, text=''):
    """Animated progress bar"""
    percent = int((progress / total) * 100)
    filled = int((progress / total) * width)
    bar = '█' * filled + '░' * (width - filled)
    
    # Gradient color based on progress
    if percent < 33:
        color = Color.RED
    elif percent < 66:
        color = Color.YELLOW
    else:
        color = Color.GREEN
    
    print(f"\r{color}{bar}{Color.RESET} {Color.BOLD}{percent}%{Color.RESET} {text}", end='', flush=True)

def typewriter_effect(text, delay=0.03, color=''):
    """Typewriter effect for text"""
    for char in text:
        print(f"{color}{char}{Color.RESET}", end='', flush=True)
        time.sleep(delay)
    print()

def box_print(text, color=Color.CYAN, width=None):
    """Print text in a beautiful box"""
    if width is None:
        width = min(get_terminal_width() - 4, 70)
    
    lines = text.split('\n')
    max_len = max(len(line) for line in lines)
    box_width = min(max_len + 4, width)
    
    print(f"{color}╔{'═' * (box_width - 2)}╗{Color.RESET}")
    for line in lines:
        padding = box_width - len(line) - 4
        left_pad = padding // 2
        right_pad = padding - left_pad
        print(f"{color}║{Color.RESET} {' ' * left_pad}{Color.BOLD}{line}{Color.RESET}{' ' * right_pad} {color}║{Color.RESET}")
    print(f"{color}╚{'═' * (box_width - 2)}╝{Color.RESET}")

def banner():
    """Ultra modern banner with gradient"""
    clear()
    width = get_terminal_width()
    
    # Top gradient line
    print_gradient_line('═', width)
    print()
    
    # Title with gradient effect
    title = "OLM MASTER PRO"
    version = "V 4.0 ULTIMATE"
    
    print_center(f"{Color.BRIGHT_CYAN}{Color.BOLD}{title}{Color.RESET}")
    print_center(f"{Color.BRIGHT_MAGENTA}{version}{Color.RESET}")
    
    print()
    
    # Decorative elements
    print_center(f"{Color.DIM}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Color.RESET}")
    print_center(f"{Color.BRIGHT_YELLOW}Created by: Tuấn Anh{Color.RESET}")
    print_center(f"{Color.DIM}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Color.RESET}")
    
    print()
    # Bottom gradient line
    print_gradient_line('═', width)
    print()

def success_box(message):
    """Success message box"""
    print()
    box_print(f"✓ {message}", Color.GREEN)
    print()

def error_box(message):
    """Error message box"""
    print()
    box_print(f"✗ {message}", Color.RED)
    print()

def info_box(message):
    """Info message box"""
    print()
    box_print(f"ℹ {message}", Color.CYAN)
    print()

def warning_box(message):
    """Warning message box"""
    print()
    box_print(f"⚠ {message}", Color.YELLOW)
    print()

# ==================== IP & SIGNATURE ====================
def ip():
    try:
        return requests.get('https://api.ipify.org', timeout=5).text.strip()
    except:
        return "0.0.0.0"

def sig(d):
    return hashlib.sha256(f"{d['mode']}{d['expire']}{d['ip']}".encode()).hexdigest()[:16]

# ==================== LICENSE MANAGEMENT ====================
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
        'mode': mode, 
        'remain': n,
        'expire': (datetime.now() + timedelta(days=expire_days)).strftime("%d/%m/%Y"),
        'ip': ip()
    }
    d['sig'] = sig(d)
    with open(LIC, 'w') as f:
        f.write(enc(d))

# ==================== ACCOUNT LOCK ====================
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

# ==================== ACCOUNT MANAGEMENT ====================
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
    """Beautiful account selection menu"""
    accounts = load_accounts()
    if not accounts:
        return None, None
    
    print()
    print(f"{Color.CYAN}╔{'═' * 60}╗{Color.RESET}")
    print(f"{Color.CYAN}║{Color.BRIGHT_YELLOW}{Color.BOLD}{'TÀI KHOẢN ĐÃ LƯU'.center(60)}{Color.RESET}{Color.CYAN}║{Color.RESET}")
    print(f"{Color.CYAN}╠{'═' * 60}╣{Color.RESET}")
    
    items = list(accounts.items())
    for i, (name, data) in enumerate(items, 1):
        saved_time = data.get('saved_at', '')
        
        # Alternate colors for better readability
        num_color = Color.BRIGHT_YELLOW if i % 2 == 0 else Color.YELLOW
        name_color = Color.BRIGHT_WHITE if i % 2 == 0 else Color.WHITE
        time_color = Color.BRIGHT_CYAN if i % 2 == 0 else Color.CYAN
        
        line = f"  {num_color}[{i}]{Color.RESET} {name_color}{name}{Color.RESET} {time_color}({saved_time}){Color.RESET}"
        print(f"{Color.CYAN}║{Color.RESET} {line:<54} {Color.CYAN}║{Color.RESET}")
    
    print(f"{Color.CYAN}╠{'═' * 60}╣{Color.RESET}")
    print(f"{Color.CYAN}║{Color.RESET}   {Color.YELLOW}[0]{Color.RESET} {Color.BRIGHT_GREEN}Đăng nhập mới{Color.RESET}{' ' * 38} {Color.CYAN}║{Color.RESET}")
    print(f"{Color.CYAN}╚{'═' * 60}╝{Color.RESET}")
    print()
    
    try:
        choice = input(f"{Color.BRIGHT_YELLOW}➤ Chọn: {Color.RESET}").strip()
        if choice == '0':
            return None, None
        idx = int(choice) - 1
        if 0 <= idx < len(items):
            name, data = items[idx]
            return data.get('username'), data.get('password')
    except:
        pass
    return None, None

# ==================== VIP CHECK ====================
def check_vip_user(username):
    """Check VIP status with loading animation"""
    try:
        loading_animation("Checking VIP status", 0.5)
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

# ==================== KEY GENERATION ====================
def gen_key():
    """Generate unique key"""
    import random
    now = datetime.now()
    dev = hashlib.md5(f"{socket.gethostname()}{uuid.getnode()}".encode()).hexdigest()[:16]
    unique = f"{dev}{now.timestamp()}{random.randint(1000, 9999)}"
    h = hashlib.sha256(unique.encode()).hexdigest()
    return f"OLM-{now:%d%m}-{h[:4].upper()}-{h[4:8].upper()}"

def create_short_link(url):
    """Create short link with link4m"""
    try:
        # URL encode properly
        encoded_url = requests.utils.quote(url, safe='')
        api = f"https://link4m.co/api-shorten/v2?api={API_TOKEN}&url={encoded_url}"
        
        loading_animation("Creating short link", 1.0)
        
        r = requests.get(api, timeout=10)
        
        if r.status_code == 200:
            data = r.json()
            if data.get('status') == 'success' and 'shortenedUrl' in data:
                return data['shortenedUrl']
    except Exception as e:
        pass
    return None

# ==================== GET KEY FLOW ====================
def get_key():
    """Beautiful key input flow"""
    print()
    print(f"{Color.CYAN}╔{'═' * 60}╗{Color.RESET}")
    print(f"{Color.CYAN}║{Color.BRIGHT_YELLOW}{Color.BOLD}{'KÍCH HOẠT KEY FREE'.center(60)}{Color.RESET}{Color.CYAN}║{Color.RESET}")
    print(f"{Color.CYAN}╚{'═' * 60}╝{Color.RESET}")
    print()
    
    for attempt in range(3):
        # Generate key
        k = gen_key()
        
        # Create destination URL (pastebin or your blog)
        dest_url = f"https://pastebin.com/raw/olmkey?k={k}"
        
        # Create short link
        short_link = create_short_link(dest_url)
        
        if not short_link:
            error_box("Không thể tạo link, thử lại...")
            time.sleep(1)
            continue
        
        # Display link in beautiful box
        print()
        print(f"{Color.GREEN}╔{'═' * 60}╗{Color.RESET}")
        print(f"{Color.GREEN}║{Color.RESET} {Color.BRIGHT_CYAN}🔗 Link rút gọn:{Color.RESET}{' ' * 40} {Color.GREEN}║{Color.RESET}")
        print(f"{Color.GREEN}║{Color.RESET}    {Color.BRIGHT_YELLOW}{Color.BOLD}{short_link}{Color.RESET}{' ' * (57 - len(short_link))} {Color.GREEN}║{Color.RESET}")
        print(f"{Color.GREEN}╠{'═' * 60}╣{Color.RESET}")
        print(f"{Color.GREEN}║{Color.RESET} {Color.WHITE}1. Vượt link trên để lấy mã{Color.RESET}{' ' * 31} {Color.GREEN}║{Color.RESET}")
        print(f"{Color.GREEN}║{Color.RESET} {Color.WHITE}2. Nhập mã vào ô bên dưới{Color.RESET}{' ' * 32} {Color.GREEN}║{Color.RESET}")
        print(f"{Color.GREEN}║{Color.RESET} {Color.YELLOW}   Hoặc nhập 'r' để đổi link mới{Color.RESET}{' ' * 27} {Color.GREEN}║{Color.RESET}")
        print(f"{Color.GREEN}╚{'═' * 60}╝{Color.RESET}")
        print()
        
        # Input with retry
        for retry in range(3):
            inp = input(f"{Color.BRIGHT_YELLOW}🔑 Nhập mã: {Color.RESET}").strip()
            
            # Check for new link request
            if inp.lower() == 'r':
                print()
                loading_animation("Tạo link mới", 1.0)
                break
            
            # Validate key
            if inp.upper() == k:
                # Success animation
                print()
                loading_animation("Validating key", 1.0)
                save_lic("FREE", 4)
                success_box("KEY HỢP LỆ - ĐÃ KÍCH HOẠT 4 LƯỢT")
                time.sleep(1)
                return True
            
            # Admin bypass
            if inp.upper() == "ADMIN_VIP_2026":
                save_lic("VIP", 999999)
                success_box("ADMIN KEY - VIP UNLIMITED")
                time.sleep(1)
                return True
            
            # Wrong key
            if retry < 2:
                remaining = 2 - retry
                warning_box(f"Mã sai! Còn {remaining} lần thử")
                time.sleep(1)
            else:
                error_box("Hết lượt thử cho link này")
                time.sleep(1)
        
        # Check if user wants new link
        if inp.lower() == 'r':
            continue
        
        # If failed all retries, ask for new link
        if retry == 2:
            continue
    
    error_box("Không thể kích hoạt key")
    return False

# ==================== OLM LOGIN ====================
def login_olm():
    """Beautiful login flow"""
    banner()
    
    lock = load_lock()
    saved_user, saved_pass = select_account()
    
    if saved_user and saved_pass:
        username = saved_user
        password = saved_pass
        success_box("Sử dụng tài khoản đã lưu")
        time.sleep(0.5)
    else:
        print()
        print(f"{Color.CYAN}╔{'═' * 60}╗{Color.RESET}")
        print(f"{Color.CYAN}║{Color.BRIGHT_YELLOW}{Color.BOLD}{'ĐĂNG NHẬP OLM'.center(60)}{Color.RESET}{Color.CYAN}║{Color.RESET}")
        print(f"{Color.CYAN}╚{'═' * 60}╝{Color.RESET}")
        print()
        username = input(f"{Color.BRIGHT_CYAN}👤 Username: {Color.RESET}").strip()
        password = input(f"{Color.BRIGHT_CYAN}🔑 Password: {Color.RESET}").strip()
    
    if not username or not password:
        error_box("Username/Password không được để trống")
        time.sleep(2)
        return None, None, None, False
    
    # Check account lock
    if lock and lock.get('user') != username:
        error_box("Key đã liên kết với tài khoản khác")
        info_box("Chọn [3] Đổi tài khoản trong menu để thay đổi")
        time.sleep(3)
        return None, None, None, False
    
    # Login with animation
    print()
    loading_animation("Đang đăng nhập OLM", 2.0)
    
    try:
        session = requests.Session()
        session.headers.update(HEADERS)
        
        session.get("https://olm.vn/dangnhap", headers=HEADERS, timeout=10)
        csrf = session.cookies.get('XSRF-TOKEN')
        
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
        
        check_res = session.get("https://olm.vn/thong-tin-tai-khoan/info", headers=HEADERS, timeout=10)
        match = re.search(r'name="name".*?value="(.*?)"', check_res.text)
        
        if match and match.group(1).strip():
            user_name = match.group(1).strip()
            
            # Extract user_id
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
            
            # Success display
            print()
            success_box(f"ĐĂNG NHẬP THÀNH CÔNG")
            print()
            print(f"{Color.CYAN}╔{'═' * 60}╗{Color.RESET}")
            print(f"{Color.CYAN}║{Color.RESET} {Color.BRIGHT_WHITE}👤 Tên:{Color.RESET} {Color.BRIGHT_CYAN}{user_name}{Color.RESET}{' ' * (50 - len(user_name))} {Color.CYAN}║{Color.RESET}")
            
            if is_vip:
                print(f"{Color.CYAN}║{Color.RESET} {Color.BRIGHT_YELLOW}👑 VIP:{Color.RESET} {Color.BRIGHT_GREEN}{Color.BOLD}UNLIMITED{Color.RESET}{' ' * 42} {Color.CYAN}║{Color.RESET}")
            else:
                print(f"{Color.CYAN}║{Color.RESET} {Color.BRIGHT_YELLOW}📦 FREE:{Color.RESET} {Color.YELLOW}4 lượt/ngày{Color.RESET}{' ' * 39} {Color.CYAN}║{Color.RESET}")
            
            print(f"{Color.CYAN}╚{'═' * 60}╝{Color.RESET}")
            print()
            
            # Save account lock
            if not lock:
                save_lock(username)
            
            # Ask to save account
            if not saved_user:
                save_choice = input(f"{Color.YELLOW}💾 Lưu tài khoản? (y/n): {Color.RESET}").strip().lower()
                if save_choice == 'y':
                    if save_account(user_name, username, password):
                        success_box("Đã lưu tài khoản")
                    time.sleep(0.5)
            
            time.sleep(1)
            return session, user_id, user_name, is_vip
        else:
            error_box("Sai username hoặc password")
            time.sleep(2)
            return None, None, None, False
            
    except Exception as e:
        error_box(f"Lỗi kết nối: {str(e)}")
        time.sleep(2)
        return None, None, None, False

# ==================== RUN MAIN TOOL ====================
def run_tool(session, user_id, user_name):
    """Download and run main.py"""
    banner()
    
    print()
    loading_animation("Đang tải tool từ GitHub", 2.0)
    
    try:
        # Download main.py
        r = requests.get(URL_MAIN, timeout=15)
        r.raise_for_status()
        
        # Save session
        with open(SESS, 'wb') as f:
            pickle.dump({
                'cookies': session.cookies.get_dict(), 
                'user_id': user_id, 
                'user_name': user_name
            }, f)
        
        # Create temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode='w', encoding='utf-8') as f:
            f.write(r.text)
            temp = f.name
        
        # Set environment
        env = os.environ.copy()
        env['OLM_LICENSE_FILE'] = LIC
        env['OLM_SESSION_FILE'] = SESS
        env['OLM_LOCK_FILE'] = LOCK
        
        # Progress bar simulation
        print()
        for i in range(101):
            progress_bar(i, 100, 40, 'Loading tool')
            time.sleep(0.01)
        print()
        
        success_box("Tool đã sẵn sàng!")
        time.sleep(1)
        
        # Run tool
        subprocess.run([sys.executable, temp], env=env)
        
        # Cleanup
        try:
            os.remove(temp)
            os.remove(SESS)
        except:
            pass
            
    except Exception as e:
        error_box(f"Không thể tải tool: {str(e)}")
        input(f"\n{Color.YELLOW}Nhấn Enter để thoát...{Color.RESET}")

# ==================== MAIN ====================
if __name__ == "__main__":
    try:
        # Check existing license
        existing_lic = load_lic()
        
        if existing_lic and existing_lic.get('remain', 0) > 0:
            banner()
            mode = existing_lic['mode']
            remain = existing_lic['remain']
            
            if mode == 'VIP':
                info_box(f"License: VIP | UNLIMITED")
            else:
                info_box(f"License: FREE | {remain} lượt còn lại")
            
            time.sleep(1)
            
            # Login
            session, user_id, user_name, is_vip = login_olm()
            if session:
                run_tool(session, user_id, user_name)
            sys.exit(0)
        
        # Fresh start
        session, user_id, user_name, is_vip = login_olm()
        if not session:
            sys.exit(1)
        
        # VIP or FREE
        if is_vip:
            save_lic("VIP", 999999)
            run_tool(session, user_id, user_name)
        else:
            # Get FREE key
            if get_key():
                run_tool(session, user_id, user_name)
        
        sys.exit(0)
        
    except KeyboardInterrupt:
        print(f"\n\n{Color.YELLOW}👋 Tạm biệt!{Color.RESET}\n")
        sys.exit(0)
    except Exception as e:
        error_box(f"Lỗi không mong đợi: {str(e)}")
        sys.exit(1)
