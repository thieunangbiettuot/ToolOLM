#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║                    OLM MASTER PRO - LAUNCHER                 ║
║                    Created by: Tuấn Anh                      ║
╚══════════════════════════════════════════════════════════════╝
"""

import os
import sys
import time
import json
import hashlib
import requests
import platform
import base64
import string
import random
import uuid
from datetime import datetime
import tempfile
import pickle

# ========== COLORS & ICONS ==========
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

ICONS = {
    'success': '✅',
    'error': '❌',
    'warning': '⚠️',
    'info': 'ℹ️',
    'key': '🔑',
    'user': '👤',
    'rocket': '🚀',
    'lock': '🔐',
    'download': '📥'
}

# ========== CROSS-PLATFORM PATHS ==========
def get_appdata_path():
    system = platform.system()
    if system == "Windows":
        return os.path.join(os.getenv('LOCALAPPDATA', ''), 'Microsoft', 'Windows', 'INetCache', 'IE')
    elif system == "Darwin":  # macOS
        return os.path.expanduser('~/Library/Application Support/com.apple.Safari')
    else:  # Linux/Android
        if 'ANDROID_ROOT' in os.environ or 'TERMUX_VERSION' in os.environ:
            return os.path.expanduser('~/.cache/google-chrome')
        else:
            return os.path.expanduser('~/.cache/mozilla/firefox')

def get_device_hash():
    mac = uuid.getnode()
    hostname = platform.node()
    return hashlib.md5(f"{mac}{hostname}".encode()).hexdigest()[:16]

def get_file_paths():
    appdata = get_appdata_path()
    device_hash = get_device_hash()
    return {
        'license': os.path.join(appdata, f'.{device_hash}sc'),
        'account_lock': os.path.join(appdata, f'.{device_hash}lk'),
        'accounts': os.path.join(appdata, f'.{device_hash}ac'),
        'session': os.path.join(appdata, f'.{device_hash}ss')
    }

# ========== ENCRYPTION UTILS ==========
SECRET_KEY = "OLM_MASTER_PRO_SECRET_KEY_2024"

def encrypt_data(data):
    json_data = json.dumps(data).encode()
    xor_data = bytes(a ^ ord(SECRET_KEY[i % len(SECRET_KEY)]) for i, a in enumerate(json_data))
    encoded = base64.b85encode(xor_data).decode()
    checksum = hashlib.sha256(encoded.encode()).hexdigest()[:12]
    noise_prefix = ''.join(random.choices(string.ascii_letters, k=8))
    noise_suffix = ''.join(reversed(noise_prefix))
    return f"{noise_prefix}{checksum}{encoded}{noise_suffix}"

def decrypt_data(encrypted_str):
    try:
        if len(encrypted_str) < 36:  # 8 + 12 + 8 + data
            return None
        encoded = encrypted_str[20:-8]  # Remove noise and checksum
        decoded_bytes = base64.b85decode(encoded)
        decrypted = bytes(a ^ ord(SECRET_KEY[i % len(SECRET_KEY)]) for i, a in enumerate(decoded_bytes))
        return json.loads(decrypted.decode())
    except:
        return None

# ========== UI FUNCTIONS ==========
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title=""):
    clear_screen()
    print(f"{Colors.BLUE}{'═' * 60}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}     OLM MASTER PRO - AUTO SOLVER{Colors.END}")
    print(f"{Colors.PURPLE}     Created by: Tuấn Anh{Colors.END}")
    if title:
        print(f"{Colors.CYAN}{'─' * 60}{Colors.END}")
        print(f"{Colors.CYAN}     {title}{Colors.END}")
    print(f"{Colors.BLUE}{'═' * 60}{Colors.END}\n")

def print_status(message, icon='info', color=Colors.WHITE):
    print(f"{ICONS.get(icon, '')} {color}{message}{Colors.END}")

# ========== ACCOUNT MANAGEMENT ==========
def load_saved_accounts():
    paths = get_file_paths()
    if os.path.exists(paths['accounts']):
        try:
            with open(paths['accounts'], 'r', encoding='utf-8') as f:
                encrypted = f.read()
                return decrypt_data(encrypted) or {}
        except:
            return {}
    return {}

def save_accounts(accounts):
    paths = get_file_paths()
    try:
        encrypted = encrypt_data(accounts)
        with open(paths['accounts'], 'w', encoding='utf-8') as f:
            f.write(encrypted)
        return True
    except:
        return False

def display_saved_accounts():
    accounts = load_saved_accounts()
    if not accounts:
        return None, None
    
    print(f"{Colors.CYAN}{ICONS['user']} TÀI KHOẢN ĐÃ LƯU:{Colors.END}")
    print(f"{Colors.CYAN}{'─' * 40}{Colors.END}")
    
    account_list = list(accounts.items())
    for idx, (name, data) in enumerate(account_list, 1):
        saved_time = data.get('saved_at', '')
        print(f"  {Colors.YELLOW}{idx}.{Colors.END} {name} {Colors.CYAN}({saved_time}){Colors.END}")
    
    print(f"  {Colors.YELLOW}0.{Colors.END} Đăng nhập mới")
    print(f"{Colors.CYAN}{'─' * 40}{Colors.END}")
    
    choice = input(f"{Colors.YELLOW}Chọn tài khoản (0-{len(account_list)}): {Colors.END}").strip()
    
    if choice == '0':
        return None, None
    
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(account_list):
            name, data = account_list[idx]
            return data.get('username'), data.get('password')
    
    return None, None

def save_current_account(name, username, password):
    accounts = load_saved_accounts()
    accounts[name] = {
        'username': username,
        'password': password,
        'saved_at': datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    return save_accounts(accounts)

# ========== LICENSE MANAGEMENT ==========
def load_license():
    paths = get_file_paths()
    if not os.path.exists(paths['license']):
        return None
    
    try:
        with open(paths['license'], 'r', encoding='utf-8') as f:
            encrypted = f.read()
            data = decrypt_data(encrypted)
            if not data:
                return None
            
            # Check expire date
            expire_date = datetime.strptime(data['expire'], "%d/%m/%Y").date()
            if expire_date < datetime.now().date():
                return None
            
            # Check IP for FREE license
            if data.get('mode') == 'FREE' and data.get('ip') != get_public_ip():
                return None
            
            return data
    except:
        return None

def save_license(mode, expire, ip=None, remain=0):
    paths = get_file_paths()
    data = {
        'mode': mode,
        'expire': expire,
        'ip': ip,
        'remain': remain
    }
    try:
        encrypted = encrypt_data(data)
        with open(paths['license'], 'w', encoding='utf-8') as f:
            f.write(encrypted)
        return True
    except:
        return False

def get_public_ip():
    try:
        response = requests.get('https://httpbin.org/ip', timeout=5)
        return response.json()['origin'].split(',')[0].strip()
    except:
        return '127.0.0.1'

# ========== VIP CHECK ==========
def check_vip(username):
    try:
        url = "https://raw.githubusercontent.com/thieunangbiettuot/ToolOLM/refs/heads/main/vip_users.txt"
        response = requests.get(url, timeout=10)
        if username.lower() in response.text.lower():
            return True
    except:
        pass
    return False

# ========== KEY GENERATION ==========
def generate_free_key():
    now = datetime.now()
    device_id = hashlib.md5(f"{uuid.getnode()}".encode()).hexdigest()[:16]
    unique_str = f"{device_id}{now.microsecond}{random.randint(1000, 9999)}"
    hash_val = hashlib.sha256(unique_str.encode()).hexdigest()
    key = f"OLMFREE-{now.strftime('%d%m')}-{hash_val[:4].upper()}-{hash_val[4:8].upper()}"
    return key

# ========== LOGIN FUNCTIONS ==========
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'vi-VN,vi;q=0.9,en-US;q=0.8',
    'x-requested-with': 'XMLHttpRequest',
    'origin': 'https://olm.vn',
    'referer': 'https://olm.vn/'
}

def login_olm(saved_username=None, saved_password=None):
    print_header("ĐĂNG NHẬP OLM")
    
    if saved_username and saved_password:
        use_saved = input(f"{Colors.YELLOW}Sử dụng tài khoản đã lưu? (y/n): {Colors.END}").strip().lower()
        if use_saved == 'y':
            username = saved_username
            password = saved_password
            print_status("Đang đăng nhập với tài khoản đã lưu...", 'user', Colors.GREEN)
        else:
            username = input(f"{ICONS['user']} {Colors.YELLOW}Tên đăng nhập: {Colors.END}").strip()
            password = input(f"{ICONS['key']} {Colors.YELLOW}Mật khẩu: {Colors.END}").strip()
    else:
        username = input(f"{ICONS['user']} {Colors.YELLOW}Tên đăng nhập: {Colors.END}").strip()
        password = input(f"{ICONS['key']} {Colors.YELLOW}Mật khẩu: {Colors.END}").strip()
    
    if not username or not password:
        print_status("Tên đăng nhập và mật khẩu không được để trống!", 'error', Colors.RED)
        return None, None, None
    
    session = requests.Session()
    session.headers.update(HEADERS)
    
    try:
        print_status("Đang đăng nhập...", 'info', Colors.YELLOW)
        
        # Get login page
        session.get("https://olm.vn/dangnhap", headers=HEADERS)
        csrf = session.cookies.get('XSRF-TOKEN')
        
        # Create login payload
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
        
        # Login
        session.post("https://olm.vn/post-login", data=payload, headers=h_login)
        
        # Check login success
        check_res = session.get("https://olm.vn/thong-tin-tai-khoan/info", headers=HEADERS)
        match = re.search(r'name="name".*?value="(.*?)"', check_res.text)
        
        if match and match.group(1).strip() != "":
            user_name = match.group(1).strip()
            print_status(f"ĐĂNG NHẬP THÀNH CÔNG!", 'success', Colors.GREEN + Colors.BOLD)
            print_status(f"Tên người dùng: {user_name}", 'user', Colors.CYAN)
            
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
                import re
                id_matches = re.findall(r'\b\d{10,}\b', check_res.text)
                user_id = id_matches[0] if id_matches else username
            
            # Ask to save account
            if not saved_username or saved_username != username:
                save_choice = input(f"\n{Colors.YELLOW}Lưu tài khoản này? (y/n): {Colors.END}").strip().lower()
                if save_choice == 'y':
                    save_current_account(user_name, username, password)
            
            return session, user_id, user_name
        else:
            print_status("ĐĂNG NHẬP THẤT BẠI!", 'error', Colors.RED)
            print_status("Sai tên đăng nhập hoặc mật khẩu", 'error', Colors.RED)
            return None, None, None
            
    except Exception as e:
        print_status(f"Lỗi đăng nhập: {str(e)}", 'error', Colors.RED)
        return None, None, None

# ========== MAIN FUNCTION ==========
def main():
    print_header("OLM MASTER PRO LAUNCHER")
    
    # Check existing license
    license_data = load_license()
    if license_data:
        print_status("Đang kiểm tra license...", 'info', Colors.YELLOW)
        time.sleep(1)
        
        # Check if still valid
        remain = license_data.get('remain', 0)
        expire = license_data.get('expire')
        mode = license_data.get('mode')
        
        if remain > 0 and datetime.strptime(expire, "%d/%m/%Y").date() >= datetime.now().date():
            if mode == 'FREE':
                current_ip = get_public_ip()
                if license_data.get('ip') != current_ip:
                    print_status("Đổi IP detected - cần lấy key mới", 'warning', Colors.YELLOW)
                    license_data = None
            # Valid license found
            print_status(f"Tìm thấy license {mode} còn {remain} lượt", 'success', Colors.GREEN)
        else:
            print_status("License đã hết hạn hoặc hết lượt", 'warning', Colors.YELLOW)
            license_data = None
    
    # If no valid license, need to login and get new one
    if not license_data:
        # Select saved account or login new
        saved_username, saved_password = display_saved_accounts()
        
        # Login
        session, user_id, user_name = login_olm(saved_username, saved_password)
        if not session:
            print_status("Không thể đăng nhập!", 'error', Colors.RED)
            return
        
        # Check VIP status
        print_status("Đang kiểm tra VIP status...", 'info', Colors.YELLOW)
        is_vip = check_vip(user_name)
        
        if is_vip:
            print_status("Tài khoản VIP - Unlimited lượt", 'success', Colors.GREEN + Colors.BOLD)
            save_license('VIP', '31/12/2099', remain=-1)  # Unlimited
            license_data = {'mode': 'VIP', 'remain': -1}
        else:
            print_status("Tài khoản FREE - Cần lấy key", 'warning', Colors.YELLOW)
            # Generate and show key
            free_key = generate_free_key()
            print(f"\n{Colors.CYAN}KEY CỦA BẠN:{Colors.END}")
            print(f"{Colors.YELLOW}{free_key}{Colors.END}")
            print(f"{Colors.RED}Lưu ý: Key có hiệu lực 1 ngày và 4 lượt{Colors.END}")
            
            # User enters key
            user_input = input(f"\n{Colors.YELLOW}Nhập key để tiếp tục: {Colors.END}").strip()
            if user_input == free_key:
                save_license('FREE', datetime.now().strftime("%d/%m/%Y"), get_public_ip(), 4)
                license_data = {'mode': 'FREE', 'remain': 4}
                print_status("Key hợp lệ - Bắt đầu sử dụng!", 'success', Colors.GREEN)
            else:
                print_status("Key không hợp lệ!", 'error', Colors.RED)
                return
    
    # Save session to temp file
    temp_dir = tempfile.gettempdir()
    session_file = os.path.join(temp_dir, f'olm_session_{get_device_hash()}.tmp')
    
    try:
        with open(session_file, 'wb') as f:
            pickle.dump({
                'session': session,
                'user_id': user_id,
                'user_name': user_name,
                'license': license_data
            }, f)
        
        print_status("Đang tải main.py từ GitHub...", 'download', Colors.CYAN)
        
        # Download main.py from GitHub
        main_url = "https://github.com/thieunangbiettuot/ToolOLM/raw/refs/heads/main/main.py"
        main_file = os.path.join(temp_dir, 'main.py')
        
        try:
            response = requests.get(main_url, timeout=15)
            if response.status_code == 200:
                with open(main_file, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                
                print_status("Đang khởi chạy main.py...", 'rocket', Colors.GREEN)
                time.sleep(2)
                
                # Run main.py with session file as argument
                os.system(f'{sys.executable} "{main_file}" "{session_file}"')
                
            else:
                print_status("Không thể tải main.py!", 'error', Colors.RED)
        except Exception as e:
            print_status(f"Lỗi tải main.py: {str(e)}", 'error', Colors.RED)
            
    except Exception as e:
        print_status(f"Lỗi lưu session: {str(e)}", 'error', Colors.RED)

if __name__ == "__main__":
    try:
        import re
        main()
    except KeyboardInterrupt:
        print(f"\n\n{ICONS['error']} {Colors.YELLOW}Đã dừng chương trình{Colors.END}")
    except Exception as e:
        print(f"\n{ICONS['error']} {Colors.RED}Lỗi không mong muốn: {str(e)}{Colors.END}")
