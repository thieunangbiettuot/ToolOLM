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
    "698b226d9150d31d216157a5",
    "backup_token_here_if_needed"
]
URL_VIP = "https://raw.githubusercontent.com/thieunangbiettuot/ToolOLM/refs/heads/main/vip_users.txt"
URL_MAIN = "https://raw.githubusercontent.com/thieunangbiettuot/ToolOLM/refs/heads/main/main.py"

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'x-requested-with': 'XMLHttpRequest',
}

# Màu sắc
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

ICONS = {
    'success': '✅', 'error': '❌', 'warning': '⚠️', 'info': 'ℹ️',
    'lock': '🔐', 'user': '👤', 'key': '🔑', 'crown': '👑',
    'star': '⭐', 'rocket': '🚀', 'check': '✔️', 'exit': '🚪',
    'refresh': '🔄', 'download': '📥', 'upload': '📤', 'link': '🔗',
    'list': '📋', 'magic': '✨', 'brain': '🧠', 'heart': '❤️',
    'video': '🎥', 'book': '📖', 'fire': '🔥', 'clock': '⏰'
}

# ========== TIỆN ÍCH ==========
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    clear_screen()
    print(f"{Colors.BLUE}{Colors.BOLD}╔══════════════════════════════════════════════════════════════╗{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}║               OLM MASTER PRO - LAUNCHER V1.0                 ║{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}║                  Created by: Tuấn Anh                        ║{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}╚══════════════════════════════════════════════════════════════╝{Colors.END}")
    print()

def print_status(message, icon='info', color=Colors.WHITE):
    print(f"{ICONS.get(icon, '•')} {color}{message}{Colors.END}")

def input_prompt(prompt, color=Colors.YELLOW):
    return input(f"{color}{prompt}{Colors.END}").strip()

def wait_enter():
    input_prompt("Nhấn Enter để tiếp tục...", Colors.YELLOW)

# ========== DETECT PLATFORM ==========
def is_android():
    return 'ANDROID_ROOT' in os.environ or 'TERMUX_VERSION' in os.environ

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

# ========== BẢO MẬT ĐƠN GIẢN ==========
def encode_data(data):
    """Mã hóa đơn giản"""
    json_str = json.dumps(data)
    return base64.b64encode(json_str.encode()).decode()

def decode_data(encoded):
    """Giải mã đơn giản"""
    try:
        json_str = base64.b64decode(encoded).decode()
        return json.loads(json_str)
    except:
        return None

def save_license(data):
    """Lưu license"""
    try:
        encoded = encode_data(data)
        with open(LICENSE_FILE, 'w') as f:
            f.write(encoded)
        return True
    except:
        return False

def load_license():
    """Tải license"""
    try:
        if os.path.exists(LICENSE_FILE):
            with open(LICENSE_FILE, 'r') as f:
                encoded = f.read()
            return decode_data(encoded)
    except:
        pass
    return None

# ========== QUẢN LÝ TÀI KHOẢN ==========
def load_accounts():
    """Tải danh sách tài khoản"""
    try:
        if os.path.exists(ACCOUNTS_FILE):
            with open(ACCOUNTS_FILE, 'r') as f:
                encoded = f.read()
            return decode_data(encoded) or {}
    except:
        pass
    return {}

def save_accounts(accounts):
    """Lưu danh sách tài khoản"""
    try:
        encoded = encode_data(accounts)
        with open(ACCOUNTS_FILE, 'w') as f:
            f.write(encoded)
        return True
    except:
        return False

def select_saved_account():
    """Chọn tài khoản đã lưu"""
    accounts = load_accounts()
    if not accounts:
        return None, None
    
    print(f"\n{Colors.CYAN}👤 TÀI KHOẢN ĐÃ LƯU:{Colors.END}")
    print(f"{Colors.CYAN}{'─' * 40}{Colors.END}")
    
    account_list = list(accounts.items())
    for idx, (name, data) in enumerate(account_list, 1):
        saved_time = data.get('saved_at', '')
        print(f"  {Colors.YELLOW}{idx}.{Colors.END} {name} ({saved_time})")
    
    print(f"  {Colors.YELLOW}0.{Colors.END} Đăng nhập mới")
    print(f"{Colors.CYAN}{'─' * 40}{Colors.END}")
    
    choice = input_prompt("Chọn: ")
    
    if choice == '0':
        return None, None
    
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(account_list):
            name, data = account_list[idx]
            return data.get('username'), data.get('password')
    
    return None, None

def save_current_account(name, username, password):
    """Lưu tài khoản hiện tại"""
    accounts = load_accounts()
    accounts[name] = {
        'username': username,
        'password': password,
        'saved_at': datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    return save_accounts(accounts)

# ========== CHECK VIP ==========
def check_vip(username):
    """Kiểm tra tài khoản VIP"""
    try:
        print_status("Đang kiểm tra VIP...", 'clock', Colors.YELLOW)
        response = requests.get(URL_VIP, timeout=TIMEOUT)
        if response.status_code == 200:
            vip_list = [line.strip().lower() for line in response.text.splitlines() 
                       if line.strip() and not line.startswith('#')]
            return username.lower() in vip_list
    except:
        pass
    return False

# ========== TẠO KEY ==========
def generate_key():
    """Tạo key FREE"""
    now = datetime.now()
    device_id = DEVICE_HASH[:8]
    unique_str = f"{device_id}{now.timestamp()}{random.randint(1000, 9999)}"
    hash_value = hashlib.sha256(unique_str.encode()).hexdigest().upper()
    ddmm = now.strftime("%d%m")
    xxxx = hash_value[:4]
    yyyy = hash_value[4:8]
    return f"OLMFREE-{ddmm}-{xxxx}-{yyyy}"

# ========== TẠO LINK NGẮN ==========
def create_short_link(url):
    """Tạo link ngắn"""
    for token in API_TOKENS:
        try:
            encoded = requests.utils.quote(url)
            api_url = f"https://link4m.co/api-shorten/v2?api={token}&url={encoded}"
            response = requests.get(api_url, timeout=5)
            data = response.json()
            if data.get("status") == "success":
                return data.get("shortenedUrl")
        except:
            pass
    return url

# ========== XỬ LÝ FREE ==========
def handle_free_license():
    """Xử lý license FREE - vượt link"""
    blog_base = "https://keyfreedailyolmvip.blogspot.com/2026/02/blog-post.html"
    max_attempts = 3
    
    print_header_free()
    
    for attempt in range(max_attempts):
        key = generate_key()
        blog_url = f"{blog_base}?ma={key}"
        short_link = create_short_link(blog_url)
        
        print(f"\n{Colors.CYAN}🔗 LINK VƯỢT: {Colors.GREEN}{short_link}{Colors.END}")
        print(f"{Colors.YELLOW}Mã key của bạn: {Colors.GREEN}{Colors.BOLD}{key}{Colors.END}")
        print()
        
        key_input = input_prompt("Nhập mã key (r = tạo lại): ")
        
        if key_input.lower() == 'r':
            continue
        
        if key_input == key:
            # Tạo license FREE
            license_data = {
                'mode': 'FREE',
                'remain': 4,
                'expire': (datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y"),
                'created': datetime.now().strftime("%d/%m/%Y %H:%M")
            }
            save_license(license_data)
            print_status("Kích hoạt FREE thành công! Bạn có 4 lượt.", 'success', Colors.GREEN)
            return True
        else:
            remaining = max_attempts - attempt - 1
            if remaining > 0:
                print_status(f"Sai key! Còn {remaining} lần thử", 'error', Colors.RED)
                time.sleep(attempt + 1)
            else:
                print_status("Hết lượt thử!", 'error', Colors.RED)
    
    return False

def print_header_free():
    """In header cho FREE"""
    clear_screen()
    print(f"{Colors.YELLOW}{Colors.BOLD}╔══════════════════════════════════════════════════════════════╗{Colors.END}")
    print(f"{Colors.YELLOW}{Colors.BOLD}║                  KÍCH HOẠT BẢN FREE                           ║{Colors.END}")
    print(f"{Colors.YELLOW}{Colors.BOLD}╚══════════════════════════════════════════════════════════════╝{Colors.END}")
    print(f"\n{Colors.CYAN}Bạn cần vượt link để lấy key kích hoạt{Colors.END}")
    print(f"{Colors.CYAN}Mỗi key có 4 lượt làm bài, hiệu lực 1 ngày{Colors.END}")

# ========== ĐĂNG NHẬP ==========
def login_olm():
    """Đăng nhập OLM"""
    print_banner()
    
    saved_username, saved_password = select_saved_account()
    
    use_saved = False
    if saved_username and saved_password:
        use_saved = input_prompt("Sử dụng tài khoản đã lưu? (y/n): ").lower() == 'y'
    
    if use_saved:
        username = saved_username
        password = saved_password
        print_status("Đang đăng nhập với tài khoản đã lưu...", 'user', Colors.GREEN)
    else:
        username = input_prompt(f"{ICONS['user']} Tên đăng nhập: ")
        password = input_prompt(f"{ICONS['key']} Mật khẩu: ")
    
    if not username or not password:
        print_status("Thông tin không được để trống!", 'error', Colors.RED)
        wait_enter()
        return None, None, None
    
    session = requests.Session()
    session.headers.update(HEADERS)
    
    print_status("Đang đăng nhập...", 'clock', Colors.YELLOW)
    
    try:
        # Lấy trang đăng nhập
        session.get("https://olm.vn/dangnhap", headers=HEADERS)
        csrf = session.cookies.get('XSRF-TOKEN')
        
        # Đăng nhập
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
        
        # Kiểm tra đăng nhập
        check_res = session.get("https://olm.vn/thong-tin-tai-khoan/info", headers=HEADERS)
        match = re.search(r'name="name".*?value="(.*?)"', check_res.text)
        
        if match and match.group(1).strip():
            user_name = match.group(1).strip()
            
            # Lấy user_id
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
            
            # Kiểm tra VIP
            is_vip_user = check_vip(username)
            
            print_status(f"Đăng nhập thành công: {user_name}", 'success', Colors.GREEN)
            
            if is_vip_user:
                print_status("Tài khoản VIP", 'crown', Colors.MAGENTA)
            else:
                print_status("Tài khoản FREE", 'info', Colors.YELLOW)
            
            # Lưu tài khoản nếu người dùng muốn
            if not use_saved and input_prompt("Lưu tài khoản? (y/n): ").lower() == 'y':
                if save_current_account(user_name, username, password):
                    print_status("Đã lưu tài khoản", 'success', Colors.GREEN)
            
            return session, user_id, user_name, is_vip_user
            
        else:
            print_status("Đăng nhập thất bại!", 'error', Colors.RED)
            wait_enter()
            return None, None, None, False
            
    except Exception as e:
        print_status(f"Lỗi đăng nhập: {str(e)}", 'error', Colors.RED)
        wait_enter()
        return None, None, None, False

# ========== XỬ LÝ LICENSE ==========
def ensure_license(is_vip_user):
    """Đảm bảo có license hợp lệ"""
    license_data = load_license()
    
    # Nếu là VIP
    if is_vip_user:
        vip_license = {
            'mode': 'VIP',
            'remain': -1,  # -1 = unlimited
            'expire': (datetime.now() + timedelta(days=365)).strftime("%d/%m/%Y"),
            'created': datetime.now().strftime("%d/%m/%Y %H:%M")
        }
        save_license(vip_license)
        print_status("Đã kích hoạt chế độ VIP", 'crown', Colors.MAGENTA)
        return True
    
    # Nếu là FREE, kiểm tra license
    if license_data:
        # Kiểm tra hạn
        expire = datetime.strptime(license_data['expire'], "%d/%m/%Y")
        if expire >= datetime.now() and license_data.get('remain', 0) > 0:
            print_status(f"License còn {license_data['remain']} lượt", 'info', Colors.CYAN)
            return True
        else:
            print_status("License hết hạn hoặc hết lượt", 'warning', Colors.YELLOW)
    
    # Chưa có license hoặc hết hạn -> tạo mới
    print_status("Bạn cần kích hoạt bản FREE", 'info', Colors.YELLOW)
    return handle_free_license()

# ========== CHẠY MAIN.PY ==========
def run_main(session, user_id, user_name):
    """Chạy main.py"""
    temp_dir = tempfile.mkdtemp()
    main_path = os.path.join(temp_dir, 'main.py')
    
    try:
        print_status("Đang tải main.py...", 'download', Colors.BLUE)
        response = requests.get(URL_MAIN, timeout=TIMEOUT)
        
        if response.status_code == 200:
            with open(main_path, 'w', encoding='utf-8') as f:
                f.write(response.text)
        else:
            print_status("Không tải được main.py", 'error', Colors.RED)
            return
    except Exception as e:
        print_status(f"Lỗi tải main.py: {str(e)}", 'error', Colors.RED)
        return
    
    # Lưu session
    session_data = {
        'cookies': session.cookies.get_dict(),
        'user_id': user_id,
        'user_name': user_name
    }
    
    with open(SESSION_FILE, 'wb') as f:
        pickle.dump(session_data, f)
    
    # Set environment variables
    os.environ['OLM_SESSION_FILE'] = SESSION_FILE
    os.environ['OLM_LICENSE_FILE'] = LICENSE_FILE
    
    try:
        print_status("Khởi động OLM MASTER PRO...", 'rocket', Colors.GREEN)
        time.sleep(1)
        subprocess.call([sys.executable, main_path])
    except Exception as e:
        print_status(f"Lỗi chạy main: {str(e)}", 'error', Colors.RED)
        wait_enter()
    finally:
        # Dọn dẹp
        try:
            os.remove(main_path)
            os.rmdir(temp_dir)
        except:
            pass

# ========== MAIN ==========
def main():
    """Chương trình chính"""
    while True:
        # Đăng nhập
        session, user_id, user_name, is_vip_user = login_olm()
        
        if not session:
            if input_prompt("Thử lại? (y/n): ").lower() != 'y':
                break
            continue
        
        # Xử lý license
        if not ensure_license(is_vip_user):
            print_status("Không thể kích hoạt license!", 'error', Colors.RED)
            if input_prompt("Thử lại? (y/n): ").lower() != 'y':
                break
            continue
        
        # Chạy main
        run_main(session, user_id, user_name)
        
        # Sau khi main kết thúc, hỏi có đổi tài khoản không
        print(f"\n{Colors.CYAN}{'─' * 50}{Colors.END}")
        if input_prompt("Đăng nhập tài khoản khác? (y/n): ").lower() != 'y':
            break
    
    print_status("Tạm biệt!", 'exit', Colors.GREEN)
    time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Đã dừng chương trình{Colors.END}")
        sys.exit(0)
