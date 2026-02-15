#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║               OLM MASTER PRO - LAUNCHER V1.0                 ║
║                    Created by: Tuấn Anh                      ║
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
import random
import uuid
from datetime import datetime, timedelta
from pathlib import Path

# ========== CẤU HÌNH ==========
API_TOKENS = [
    "698b226d9150d31d216157a5",  # Token 1
    "backup_token_here_if_needed"  # Token 2, thay bằng token thực nếu có
]
URL_VIP = "https://raw.githubusercontent.com/thieunangbiettuot/ToolOLM/refs/heads/main/vip_users.txt"
URL_MAIN = "https://raw.githubusercontent.com/thieunangbiettuot/ToolOLM/refs/heads/main/main.py"

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'x-requested-with': 'XMLHttpRequest',
}

# Màu sắc và hiệu ứng
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

# Icon Unicode cho UI rực rỡ
ICONS = {
    'success': '✅',
    'error': '❌',
    'warning': '⚠️',
    'info': 'ℹ️',
    'lock': '🔐',
    'user': '👤',
    'key': '🔑',
    'star': '⭐',
    'rocket': '🚀',
    'diamond': '💎',
    'crown': '👑',
    'check': '✔️',
    'exit': '🚪',
    'refresh': '🔄',
    'download': '📥',
    'upload': '📤',
    'link': '🔗',
    'list': '📋',
    'magic': '✨',
    'brain': '🧠',
    'heart': '❤️',
    'video': '🎥',
    'book': '📖',
    'fire': '🔥',
    'clock': '⏰'
}

# ========== TIỆN ÍCH HIỂN THỊ ==========
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def animate_text(text, color=Colors.WHITE, delay=0.05):
    """Hiệu ứng chữ chạy rực rỡ"""
    for char in text:
        sys.stdout.write(f"{color}{char}{Colors.END}")
        sys.stdout.flush()
        time.sleep(delay)
    print()

def spinner_animation(message, duration=2, color=Colors.CYAN):
    """Hiệu ứng spinner động"""
    spinner = ['|', '/', '-', '\\']
    end_time = time.time() + duration
    i = 0
    print(f"{color}{message}{Colors.END}", end='')
    while time.time() < end_time:
        sys.stdout.write(f"\r{color}{message} {spinner[i % 4]}{Colors.END}")
        sys.stdout.flush()
        i += 1
        time.sleep(0.2)
    print("\r" + " " * (len(message) + 2) + "\r", end='')

def print_banner():
    clear_screen()
    animate_text("╔══════════════════════════════════════════════════════════════╗", delay=0.01, color=Colors.BLUE + Colors.BOLD)
    animate_text("║               OLM MASTER PRO V1.0                            ║", delay=0.01, color=Colors.BLUE + Colors.BOLD)
    animate_text("║                  Created by: Tuấn Anh                        ║", delay=0.01, color=Colors.BLUE + Colors.BOLD)
    animate_text("╚══════════════════════════════════════════════════════════════╝", delay=0.01, color=Colors.BLUE + Colors.BOLD)
    print()

def print_status(message, icon='info', color=Colors.WHITE):
    print(f"{ICONS.get(icon, '•')} {color}{message}{Colors.END}")

def print_menu(title, options, color=Colors.CYAN):
    print(f"\n{color}{Colors.BOLD}{ICONS['list']} {title.upper()}{Colors.END}")
    print(f"{color}{'─' * 40}{Colors.END}")
    for key, value in options.items():
        print(f" {Colors.YELLOW}{key}.{Colors.END} {value}")
    print(f"{color}{'─' * 40}{Colors.END}")

def input_prompt(prompt, color=Colors.YELLOW):
    return input(f"{color}{prompt}{Colors.END}").strip()

def wait_enter():
    input_prompt(f"{ICONS['info']} Nhấn Enter để tiếp tục...", Colors.YELLOW)

# ========== DETECT PLATFORM ==========
def is_android():
    return 'ANDROID_ROOT' in os.environ or 'TERMUX_VERSION' in os.environ

def get_terminal_width():
    try:
        cols = os.get_terminal_size().columns
        return min(cols - 2, 45 if is_android() else 68)
    except:
        return 45 if is_android() else 60

TIMEOUT = 5 if is_android() else 8

# ========== THƯ MỤC DỮ LIỆU ==========
def get_data_dir():
    sys_plat = platform.system().lower()
    if 'windows' in sys_plat:
        base_dir = os.getenv('LOCALAPPDATA')
        dir_path = Path(base_dir) / 'Microsoft' / 'Windows' / 'INetCache' / 'IE'
    elif 'darwin' in sys_plat:
        base_dir = os.path.expanduser('~/Library/Application Support')
        dir_path = Path(base_dir) / 'com.apple.Safari'
    elif 'linux' in sys_plat:
        base_dir = os.path.expanduser('~/.cache')
        dir_path = Path(base_dir) / 'mozilla' / 'firefox'
    elif is_android():
        base_dir = os.path.expanduser('~/.cache')
        dir_path = Path(base_dir) / 'google-chrome'
    else:
        base_dir = os.path.expanduser('~/.cache')
        dir_path = Path(base_dir) / 'olm_master'
    dir_path.mkdir(parents=True, exist_ok=True)
    return str(dir_path)

DATA_DIR = get_data_dir()
DEVICE_HASH = hashlib.md5(f"{socket.gethostname()}{uuid.getnode()}".encode()).hexdigest()[:16]
LICENSE_FILE = os.path.join(DATA_DIR, f'.{DEVICE_HASH}sc')
SESSION_FILE = os.path.join(DATA_DIR, f'.{DEVICE_HASH}ss')
ACCOUNTS_FILE = os.path.join(DATA_DIR, f'.{DEVICE_HASH}ac')
LOCK_FILE = os.path.join(DATA_DIR, f'.{DEVICE_HASH}lk')

# ========== BẢO MẬT ==========
SECRET_KEY = b'OLM_MASTER_PRO_2026_SECRET_KEY_42'

def encrypt_data(data):
    json_str = json.dumps(data)
    bytes_data = json_str.encode()
    xor_data = bytearray(b ^ SECRET_KEY[i % len(SECRET_KEY)] for i, b in enumerate(bytes_data))
    b85_data = base64.b85encode(xor_data).decode()
    checksum = hashlib.sha256(b85_data.encode()).hexdigest()[:12]
    noise_prefix = hashlib.md5(os.urandom(16)).hexdigest()[:8]
    noise_suffix = noise_prefix[::-1]
    return f"{noise_prefix}{checksum}{b85_data}{noise_suffix}"

def decrypt_data(encrypted_str):
    try:
        noise_len = 8
        prefix = encrypted_str[:noise_len]
        suffix = encrypted_str[-noise_len:]
        if suffix != prefix[::-1]:
            return None
        content = encrypted_str[noise_len:-noise_len]
        checksum = content[:12]
        b85_data = content[12:]
        if hashlib.sha256(b85_data.encode()).hexdigest()[:12] != checksum:
            return None
        xor_data = base64.b85decode(b85_data)
        bytes_data = bytes(b ^ SECRET_KEY[i % len(SECRET_KEY)] for i, b in enumerate(xor_data))
        json_str = bytes_data.decode()
        return json.loads(json_str)
    except:
        return None

def save_file(filename, data):
    encrypted = encrypt_data(data)
    with open(filename, 'w') as f:
        f.write(encrypted)

def load_file(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            encrypted = f.read()
        data = decrypt_data(encrypted)
        if data:
            return data
    return None

def verify_integrity(data):
    if not data:
        return False
    sig_expected = hashlib.sha256(f"{data.get('mode', '')}{data.get('expire', '')}{data.get('ip', '')}".encode()).hexdigest()
    return data.get('sig') == sig_expected

# ========== ANTI-DEBUG ==========
def check_env():
    import sys
    if hasattr(sys, 'gettrace') and sys.gettrace():
        sys.exit(0)
    if 'PYTEST' in os.environ or 'JUPYTER' in os.environ:
        time.sleep(3)

check_env()

# ========== QUẢN LÝ TÀI KHOẢN ==========
def load_accounts():
    return load_file(ACCOUNTS_FILE) or {}

def save_accounts(accounts):
    save_file(ACCOUNTS_FILE, accounts)

def select_saved_account():
    accounts = load_accounts()
    if not accounts:
        return None, None
    width = get_terminal_width()
    print(f"{Colors.CYAN}╔{'═' * (width - 2)}╗{Colors.END}")
    print(f"{Colors.CYAN}║{Colors.BOLD}{' TÀI KHOẢN ĐÃ LƯU '.center(width - 2)}{Colors.END}{Colors.CYAN}║{Colors.END}")
    print(f"{Colors.CYAN}╚{'═' * (width - 2)}╝{Colors.END}")
    account_list = list(accounts.items())
    for idx, (name, data) in enumerate(account_list, 1):
        saved_time = data.get('saved_at', '')
        print(f"{Colors.YELLOW}[{idx}]{Colors.END} {name} ({saved_time})")
    print(f"{Colors.YELLOW}[0]{Colors.END} Đăng nhập mới")
    choice = input_prompt("Chọn: ")
    if choice == '0':
        return None, None
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(account_list):
            name, data = account_list[idx]
            return data['username'], data['password']
    except:
        pass
    return None, None

def save_current_account(name, username, password):
    accounts = load_accounts()
    accounts[name] = {
        'username': username,
        'password': password,
        'saved_at': datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    save_accounts(accounts)

# ========== ACCOUNT LOCK ==========
def load_lock():
    return load_file(LOCK_FILE)

def save_lock(username):
    save_file(LOCK_FILE, {'user': username})

def delete_lock():
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)

# ========== LICENSE ==========
def get_current_ip():
    try:
        return requests.get('https://api.ipify.org', timeout=5).text
    except:
        return 'unknown'

def load_license():
    data = load_file(LICENSE_FILE)
    if not data or not verify_integrity(data):
        if os.path.exists(LICENSE_FILE):
            os.remove(LICENSE_FILE)
        return None
    expire_date = datetime.strptime(data['expire'], "%d/%m/%Y").date()
    if expire_date < datetime.now().date():
        return None
    if data.get('mode') == 'FREE' and data.get('ip') != get_current_ip():
        return None
    if data.get('remain', 0) <= 0:
        return None
    return data

def save_license(mode, remain, expire, ip, sig):
    data = {
        'mode': mode,
        'remain': remain,
        'expire': expire,
        'ip': ip,
        'sig': sig
    }
    save_file(LICENSE_FILE, data)

def compute_sig(data):
    return hashlib.sha256(f"{data['mode']}{data['expire']}{data['ip']}".encode()).hexdigest()

# ========== CHECK VIP ==========
def check_vip(username):
    try:
        spinner_animation("Đang kiểm tra VIP...", 1, Colors.MAGENTA)
        response = requests.get(URL_VIP, timeout=TIMEOUT)
        if response.status_code == 200:
            vip_list = [line.strip().lower() for line in response.text.splitlines() if line.strip() and not line.startswith('#')]
            return username.lower() in vip_list
    except:
        pass
    return False

# ========== TẠO LINK NGẮN ==========
def create_short_link(url, max_tries=3):
    for _ in range(max_tries):
        for token in API_TOKENS:
            try:
                encoded = requests.utils.quote(url)
                api_url = f"https://link4m.co/api-shorten/v2?api={token}&url={encoded}"
                response = requests.get(api_url, timeout=TIMEOUT)
                data = response.json()
                if data.get("status") == "success":
                    return data.get("shortenedUrl")
            except:
                pass
        time.sleep(1)
    return url

# ========== TẠO KEY ==========
def generate_key():
    now = datetime.now()
    device_id = DEVICE_HASH
    unique_str = f"{device_id}{now.timestamp()}{random.randint(1000, 9999)}"
    hash_value = hashlib.sha256(unique_str.encode()).hexdigest()
    ddmm = now.strftime("%d%m")
    xxxx = hash_value[:4].upper()
    yyyy = hash_value[4:8].upper()
    return f"OLMFREE-{ddmm}-{xxxx}-{yyyy}"

# ========== VƯỢT LINK ==========
def handle_free_license():
    blog_base = "https://keyfreedailyolmvip.blogspot.com/2026/02/blog-post.html"
    max_attempts = 3
    for attempt in range(max_attempts):
        key = generate_key()
        blog_url = f"{blog_base}?ma={key.replace('OLMFREE-', 'OLM-')}"
        short_link = create_short_link(blog_url)
        print_status(f"Link vượt: {short_link}", 'link', Colors.CYAN)
        key_input = input_prompt(f"Mã key (r=link mới): ")
        if key_input.lower() == 'r':
            continue
        if key_input == key:
            expire = (datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y")
            ip = get_current_ip()
            sig = compute_sig({'mode': 'FREE', 'expire': expire, 'ip': ip})
            save_license('FREE', 4, expire, ip, sig)
            print_status("License FREE kích hoạt thành công!", 'success', Colors.GREEN)
            return
        print_status(f"Sai mã ({max_attempts - attempt - 1} lần còn lại)", 'error', Colors.RED)
        time.sleep(attempt + 1)
    print_status("Hết lượt thử, thoát.", 'error', Colors.RED)
    sys.exit(0)

# ========== ĐĂNG NHẬP ==========
def login_olm():
    print_banner()
    saved_username, saved_password = select_saved_account()
    use_saved = False
    if saved_username and saved_password:
        use_saved = input_prompt("Sử dụng tài khoản đã lưu? (y/n): ").lower() == 'y'
    if use_saved:
        username = saved_username
        password = saved_password
    else:
        username = input_prompt(f"{ICONS['user']} Tên đăng nhập: ")
        password = input_prompt(f"{ICONS['key']} Mật khẩu: ")
    if not username or not password:
        print_status("Thông tin không được để trống!", 'error', Colors.RED)
        wait_enter()
        return None, None, None
    session = requests.Session()
    session.headers.update(HEADERS)
    spinner_animation("Đang đăng nhập...", 2, Colors.GREEN)
    try:
        session.get("https://olm.vn/dangnhap", headers=HEADERS)
        csrf = session.cookies.get('XSRF-TOKEN')
        payload = {
            '_token': csrf,
            'username': username,
            'password': password,
            'remember': 'true',
            'device_id': '0b48f4d6204591f83dc40b07f07af7d4',
            'platform': 'web'
        }
        h_login = HEADERS.copy()
        h_login['x-csrf-token'] = csrf
        session.post("https://olm.vn/post-login", data=payload, headers=h_login)
        check_res = session.get("https://olm.vn/thong-tin-tai-khoan/info", headers=HEADERS)
        match = re.search(r'name="name".*?value="(.*?)"', check_res.text)
        if match and match.group(1).strip() != "":
            user_name = match.group(1).strip()
            user_id = None
            cookies = session.cookies.get_dict()
            for cookie_name, cookie_value in cookies.items():
                if 'remember_web' in cookie_name and '%7C' in cookie_value:
                    parts = cookie_value.split('%7C')
                    if parts and parts[0].isdigit():
                        user_id = parts[0]
                        break
            if not user_id:
                id_matches = re.findall(r'\b\d{10,}\b', check_res.text)
                user_id = id_matches[0] if id_matches else username
            is_vip = check_vip(username)
            print_status(f"Đăng nhập thành công: {user_name}", 'success', Colors.GREEN)
            if is_vip:
                print_status("Tài khoản VIP - Unlimited", 'crown', Colors.MAGENTA)
            else:
                print_status("Tài khoản FREE", 'info', Colors.YELLOW)
            lock_data = load_lock()
            if lock_data and lock_data.get('user') != username:
                print_status("Tài khoản không khớp với lock, vui lòng đổi tài khoản.", 'error', Colors.RED)
                return None, None, None
            if not lock_data:
                save_lock(username)
            if not use_saved:
                save_choice = input_prompt("Lưu tài khoản? (y/n): ").lower()
                if save_choice == 'y':
                    save_current_account(user_name, username, password)
            return session, user_id, user_name
    except Exception as e:
        print_status(f"Lỗi đăng nhập: {str(e)}", 'error', Colors.RED)
    return None, None, None

# ========== CHẠY MAIN.PY ==========
def run_main(session, user_id, user_name):
    temp_dir = tempfile.mkdtemp()
    main_path = os.path.join(temp_dir, 'main.py')
    try:
        spinner_animation("Tải main.py...", 1, Colors.BLUE)
        response = requests.get(URL_MAIN, timeout=TIMEOUT)
        if response.status_code == 200:
            with open(main_path, 'w', encoding='utf-8') as f:
                f.write(response.text)
        else:
            print_status("Không tải được main.py", 'error', Colors.RED)
            return
    except:
        print_status("Lỗi tải main.py", 'error', Colors.RED)
        return
    session_data = {'cookies': session.cookies.get_dict(), 'user_id': user_id, 'user_name': user_name}
    session_temp = os.path.join(temp_dir, 'session.pkl')
    with open(session_temp, 'wb') as f:
        pickle.dump(session_data, f)
    os.environ['OLM_SESSION_FILE'] = session_temp
    os.environ['OLM_LICENSE_FILE'] = LICENSE_FILE
    try:
        subprocess.call([sys.executable, main_path])
    except Exception as e:
        print_status(f"Lỗi chạy main: {str(e)}", 'error', Colors.RED)
    finally:
        try:
            os.remove(main_path)
            os.remove(session_temp)
            os.rmdir(temp_dir)
        except:
            pass

# ========== MAIN LAUNCHER ==========
def main():
    check_env()
    print_banner()
    license_data = load_license()
    session, user_id, user_name = login_olm()
    if not session:
        sys.exit(0)
    if check_vip(user_name):
        expire = (datetime.now() + timedelta(days=365)).strftime("%d/%m/%Y")  # VIP 1 năm
        ip = ''  # No IP lock for VIP
        sig = compute_sig({'mode': 'VIP', 'expire': expire, 'ip': ip})
        save_license('VIP', -1, expire, ip, sig)  # -1 for unlimited
    elif not license_data:
        handle_free_license()
    run_main(session, user_id, user_name)
    sys.exit(0)

if __name__ == "__main__":
    main()
