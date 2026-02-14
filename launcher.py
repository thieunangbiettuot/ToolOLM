#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║              OLM MASTER PRO V1.0 - LAUNCHER                  ║
║                    Created by: Tuấn Anh                      ║
╚══════════════════════════════════════════════════════════════╝
"""

import os
import sys
import time
import json
import random
import hashlib
import uuid
import base64
import pickle
import subprocess
import tempfile
import platform
from datetime import datetime, timedelta

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Đang cài đặt thư viện cần thiết...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "beautifulsoup4", "--quiet"])
    import requests
    from bs4 import BeautifulSoup

import re

# ==================== CẤU HÌNH ====================
GITHUB_MAIN_URL = "https://github.com/thieunangbiettuot/ToolOLM/raw/refs/heads/main/main.py"
GITHUB_VIP_URL = "https://raw.githubusercontent.com/thieunangbiettuot/ToolOLM/refs/heads/main/vip_users.txt"

# Link4m API configs (với fallback)
LINK_SERVICES = [
    {"name": "link4m_1", "api": "https://link4m.co/api-shorten/v2", "token": "67e4dc9b4d2e04d44dc3be8f02f2c72b9e67a4b9"},
    {"name": "link4m_2", "api": "https://link4m.co/api-shorten/v2", "token": "backup_token_here_if_needed"},
]

# Encryption secret
SECRET_KEY = b"OLM_MASTER_PRO_V1_SECURE_2026"

# ==================== MÀU SẮC & ICONS ====================
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
    'success': '✅', 'error': '❌', 'warning': '⚠️', 'info': 'ℹ️',
    'user': '👤', 'key': '🔑', 'lock': '🔐', 'star': '⭐',
    'fire': '🔥', 'rocket': '🚀', 'check': '✔️', 'exit': '🚪',
    'link': '🔗', 'clock': '⏰', 'refresh': '🔄', 'magic': '✨'
}

# ==================== CROSS-PLATFORM FILE PATHS ====================
def get_device_hash():
    """Tạo hash duy nhất cho thiết bị"""
    hostname = platform.node()
    mac = uuid.getnode()
    unique_str = f"{hostname}{mac}".encode()
    return hashlib.md5(unique_str).hexdigest()[:8]

def get_app_data_dir():
    """Lấy thư mục AppData phù hợp với từng hệ điều hành"""
    system = platform.system()
    device_hash = get_device_hash()
    
    if system == "Windows":
        base = os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Microsoft', 'Windows', 'INetCache', 'IE')
    elif system == "Darwin":  # macOS/iOS
        base = os.path.expanduser('~/Library/Application Support/com.apple.Safari')
    elif 'ANDROID_ROOT' in os.environ or 'TERMUX_VERSION' in os.environ:  # Android/Termux
        base = os.path.expanduser('~/.cache/google-chrome')
    else:  # Linux
        base = os.path.expanduser('~/.cache/mozilla/firefox')
    
    os.makedirs(base, exist_ok=True)
    
    return {
        'license': os.path.join(base, f'.{device_hash}sc'),
        'session': os.path.join(base, f'.{device_hash}ss'),
        'accounts': os.path.join(base, f'.{device_hash}ac'),
        'lock': os.path.join(base, f'.{device_hash}lk')
    }

PATHS = get_app_data_dir()

# ==================== ENCRYPTION/DECRYPTION ====================
def xor_encrypt(data, key):
    """XOR encryption"""
    key_len = len(key)
    return bytes([data[i] ^ key[i % key_len] for i in range(len(data))])

def encrypt_data(data_dict):
    """Mã hóa dữ liệu: JSON → XOR → Base85 → Checksum → Noise"""
    try:
        # JSON
        json_str = json.dumps(data_dict, separators=(',', ':'))
        json_bytes = json_str.encode('utf-8')
        
        # XOR
        encrypted = xor_encrypt(json_bytes, SECRET_KEY)
        
        # Base85
        b85_data = base64.b85encode(encrypted).decode('ascii')
        
        # Checksum (SHA256, lấy 12 ký tự)
        checksum = hashlib.sha256(b85_data.encode()).hexdigest()[:12]
        
        # Noise (MD5)
        noise = hashlib.md5(str(time.time()).encode()).hexdigest()
        noise_prefix = noise[:8]
        noise_suffix = noise[-8:][::-1]  # Reverse
        
        # Kết hợp
        result = f"{noise_prefix}{checksum}{b85_data}{noise_suffix}"
        return result
    except Exception as e:
        return None

def decrypt_data(encrypted_str):
    """Giải mã dữ liệu"""
    try:
        if not encrypted_str or len(encrypted_str) < 28:
            return None
        
        # Tách noise và checksum
        data_part = encrypted_str[8:-8]  # Bỏ noise
        checksum_received = data_part[:12]
        b85_data = data_part[12:]
        
        # Verify checksum
        checksum_calculated = hashlib.sha256(b85_data.encode()).hexdigest()[:12]
        if checksum_received != checksum_calculated:
            return None  # Bị sửa
        
        # Base85 decode
        encrypted = base64.b85decode(b85_data.encode('ascii'))
        
        # XOR decrypt
        decrypted = xor_encrypt(encrypted, SECRET_KEY)
        
        # JSON parse
        json_str = decrypted.decode('utf-8')
        data_dict = json.loads(json_str)
        
        return data_dict
    except Exception as e:
        return None

# ==================== FILE I/O ====================
def save_file(filepath, data_dict):
    """Lưu file đã mã hóa"""
    encrypted = encrypt_data(data_dict)
    if encrypted:
        with open(filepath, 'w') as f:
            f.write(encrypted)
        return True
    return False

def load_file(filepath):
    """Đọc file đã mã hóa"""
    if not os.path.exists(filepath):
        return None
    try:
        with open(filepath, 'r') as f:
            encrypted = f.read()
        return decrypt_data(encrypted)
    except:
        return None

# ==================== UI HELPERS ====================
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print('\033[2J\033[H', end='')  # Fallback cho Termux

def print_header(title=""):
    clear_screen()
    print(f"{Colors.BLUE}{'═' * 60}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{ICONS['rocket']} OLM MASTER PRO V1.0 {ICONS['fire']}".center(68))
    if title:
        print(f"{Colors.CYAN}{title}".center(68))
    print(f"{Colors.BLUE}{'═' * 60}{Colors.END}\n")

def print_status(msg, icon='info', color=Colors.WHITE):
    print(f"{ICONS.get(icon, '')} {color}{msg}{Colors.END}")

def wait_enter(prompt="Nhấn Enter để tiếp tục..."):
    input(f"\n{Colors.YELLOW}{prompt}{Colors.END}")

# ==================== CHECK VIP ====================
def check_vip_status(username):
    """Check VIP từ GitHub (realtime, ngầm)"""
    try:
        response = requests.get(GITHUB_VIP_URL, timeout=10)
        if response.status_code == 200:
            vip_list = response.text.lower().split('\n')
            # Lọc comment và dòng trống
            vip_users = [line.strip() for line in vip_list 
                        if line.strip() and not line.strip().startswith('#')]
            
            return username.lower() in vip_users
    except:
        pass
    return False

# ==================== ACCOUNT MANAGEMENT ====================
def load_accounts():
    """Tải danh sách tài khoản"""
    data = load_file(PATHS['accounts'])
    return data if data else {}

def save_accounts(accounts_dict):
    """Lưu danh sách tài khoản"""
    return save_file(PATHS['accounts'], accounts_dict)

def select_account():
    """Chọn tài khoản từ danh sách hoặc đăng nhập mới"""
    accounts = load_accounts()
    
    if accounts:
        print(f"\n{Colors.CYAN}{ICONS['user']} TÀI KHOẢN ĐÃ LƯU:{Colors.END}")
        print(f"{Colors.CYAN}{'─' * 50}{Colors.END}")
        
        acc_list = list(accounts.items())
        for idx, (name, data) in enumerate(acc_list, 1):
            saved_at = data.get('saved_at', '')
            print(f"  {Colors.YELLOW}[{idx}]{Colors.END} {name} {Colors.CYAN}({saved_at}){Colors.END}")
        
        print(f"  {Colors.YELLOW}[0]{Colors.END} Đăng nhập mới")
        print(f"{Colors.CYAN}{'─' * 50}{Colors.END}")
        
        choice = input(f"{Colors.YELLOW}Chọn (0-{len(acc_list)}): {Colors.END}").strip()
        
        if choice.isdigit():
            idx = int(choice)
            if idx == 0:
                return None, None
            elif 1 <= idx <= len(acc_list):
                name, data = acc_list[idx - 1]
                return data.get('username'), data.get('password')
    
    return None, None

def save_account(name, username, password):
    """Lưu tài khoản mới"""
    accounts = load_accounts()
    accounts[name] = {
        'username': username,
        'password': password,
        'saved_at': datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    if save_accounts(accounts):
        print_status(f"Đã lưu tài khoản: {name}", 'success', Colors.GREEN)
        return True
    return False

# ==================== ACCOUNT LOCK ====================
def get_locked_account():
    """Lấy account đang lock"""
    data = load_file(PATHS['lock'])
    return data.get('username') if data else None

def set_locked_account(username):
    """Lock account"""
    return save_file(PATHS['lock'], {'username': username})

def clear_locked_account():
    """Xóa account lock"""
    if os.path.exists(PATHS['lock']):
        os.remove(PATHS['lock'])

# ==================== LICENSE MANAGEMENT ====================
def get_current_ip():
    """Lấy IP hiện tại"""
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        return response.json()['ip']
    except:
        return "unknown"

def compute_signature(license_data):
    """Tính signature cho license"""
    sig_str = f"{license_data.get('mode', '')}{license_data.get('expire', '')}{license_data.get('ip', '')}"
    return hashlib.sha256(sig_str.encode()).hexdigest()[:16]

def load_license():
    """Tải license"""
    data = load_file(PATHS['license'])
    if not data:
        return None
    
    # Verify signature
    if data.get('sig') != compute_signature(data):
        os.remove(PATHS['license'])
        return None
    
    # Check expire
    try:
        expire_date = datetime.strptime(data['expire'], "%d/%m/%Y").date()
        if expire_date < datetime.now().date():
            os.remove(PATHS['license'])
            return None
    except:
        return None
    
    # Check IP (FREE only)
    if data.get('mode') == 'FREE':
        if data.get('ip') != get_current_ip():
            print_status("IP đã thay đổi, cần vượt link mới", 'warning', Colors.YELLOW)
            os.remove(PATHS['license'])
            return None
    
    # Check remain
    if data.get('remain', 0) <= 0:
        os.remove(PATHS['license'])
        clear_locked_account()
        return None
    
    return data

def save_license(mode, key, expire_days, attempts):
    """Lưu license"""
    expire_date = (datetime.now() + timedelta(days=expire_days)).strftime("%d/%m/%Y")
    current_ip = get_current_ip()
    
    license_data = {
        'mode': mode,
        'key': key,
        'expire': expire_date,
        'remain': attempts,
        'ip': current_ip,
        'created_at': datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }
    
    license_data['sig'] = compute_signature(license_data)
    
    return save_file(PATHS['license'], license_data)

# ==================== KEY GENERATION ====================
def generate_unique_key():
    """Tạo key FREE unique"""
    now = datetime.now()
    device_id = get_device_hash()
    unique_string = f"{device_id}{now.timestamp()}{random.randint(1000, 9999)}"
    hash_value = hashlib.sha256(unique_string.encode()).hexdigest()
    
    key = f"OLM-{now:%d%m}-{hash_value[:4].upper()}-{hash_value[4:8].upper()}"
    return key

def shorten_link_with_fallback(long_url):
    """Rút gọn link với fallback"""
    for service in LINK_SERVICES:
        try:
            print_status(f"Đang tạo link rút gọn...", 'link', Colors.YELLOW)
            
            response = requests.post(
                service['api'],
                json={'url': long_url},
                headers={
                    'api-token': service['token'],
                    'Content-Type': 'application/json'
                },
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('status') == 'success':
                    short_url = result.get('shortenedUrl')
                    if short_url:
                        return short_url
        except Exception as e:
            continue
    
    return None

def get_free_key_via_link():
    """Lấy key FREE qua link4m (có thể tạo lại link)"""
    max_regenerate = 3
    
    for attempt in range(max_regenerate):
        # Tạo key mới
        key = generate_unique_key()
        
        # Tạo link với key
        base_url = "https://olm.vn"  # Link gốc
        long_url = f"{base_url}?key={key}"
        
        # Rút gọn
        short_url = shorten_link_with_fallback(long_url)
        
        if not short_url:
            print_status("Không thể tạo link rút gọn", 'error', Colors.RED)
            time.sleep(2)
            continue
        
        # Hiển thị link
        print(f"\n{Colors.GREEN}{'═' * 50}{Colors.END}")
        print(f"{Colors.YELLOW}Bước 1:{Colors.END} Vượt link sau để lấy mã:")
        print(f"{Colors.CYAN}{ICONS['link']} {short_url}{Colors.END}")
        print(f"{Colors.GREEN}{'═' * 50}{Colors.END}\n")
        
        # Rate limiting
        fail_count = 0
        for i in range(3):
            user_input = input(f"{Colors.YELLOW}Bước 2 - Nhập mã (hoặc 'r' để tạo link mới): {Colors.END}").strip()
            
            if user_input.lower() == 'r':
                if attempt < max_regenerate - 1:
                    print_status("Đang tạo link mới...", 'refresh', Colors.YELLOW)
                    time.sleep(1)
                    break
                else:
                    print_status("Đã hết lượt tạo link mới", 'error', Colors.RED)
                    return None
            
            if user_input == key:
                print_status("Xác thực thành công!", 'success', Colors.GREEN)
                return key
            
            fail_count += 1
            time.sleep(fail_count)
            
            if i < 2:
                print_status(f"Sai mã ({2-i} lần còn lại)", 'error', Colors.RED)
        
        if user_input != key and user_input.lower() != 'r':
            print_status("Đã hết lượt thử", 'error', Colors.RED)
            return None
    
    print_status("Đã hết lượt tạo link", 'error', Colors.RED)
    return None

# ==================== LOGIN OLM ====================
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'vi-VN,vi;q=0.9',
    'x-requested-with': 'XMLHttpRequest',
    'origin': 'https://olm.vn',
    'referer': 'https://olm.vn/'
}

def login_olm(username, password):
    """Đăng nhập OLM"""
    session = requests.Session()
    session.headers.update(HEADERS)
    
    try:
        print_status("Đang đăng nhập...", 'clock', Colors.YELLOW)
        
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
        
        if match and match.group(1).strip():
            user_name = match.group(1).strip()
            
            # Lấy user_id
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
            
            return session, user_id, user_name
        
        return None, None, None
        
    except Exception as e:
        return None, None, None

# ==================== SAVE SESSION ====================
def save_session(session, user_id, user_name):
    """Lưu session"""
    session_data = {
        'cookies': dict(session.cookies),
        'user_id': user_id,
        'user_name': user_name
    }
    
    try:
        with open(PATHS['session'], 'wb') as f:
            pickle.dump(session_data, f)
        return True
    except:
        return False

# ==================== MAIN LAUNCHER ====================
def main():
    print_header("LAUNCHER")
    
    # 1. CHỌN TÀI KHOẢN
    saved_username, saved_password = select_account()
    
    if saved_username and saved_password:
        username, password = saved_username, saved_password
        print_status(f"Sử dụng tài khoản: {saved_username}", 'user', Colors.GREEN)
    else:
        print(f"\n{Colors.CYAN}ĐĂNG NHẬP MỚI{Colors.END}")
        username = input(f"{ICONS['user']} {Colors.YELLOW}Tên đăng nhập: {Colors.END}").strip()
        password = input(f"{ICONS['key']} {Colors.YELLOW}Mật khẩu: {Colors.END}").strip()
    
    if not username or not password:
        print_status("Thông tin không hợp lệ!", 'error', Colors.RED)
        wait_enter()
        sys.exit(1)
    
    # 2. ĐĂNG NHẬP OLM
    session, user_id, user_name = login_olm(username, password)
    
    if not session:
        print_status("Đăng nhập thất bại!", 'error', Colors.RED)
        wait_enter()
        sys.exit(1)
    
    print_status(f"Đăng nhập thành công: {user_name}", 'success', Colors.GREEN)
    
    # Hỏi lưu tài khoản (nếu mới)
    if not saved_username or saved_username != username:
        save_choice = input(f"\n{Colors.YELLOW}Lưu tài khoản? (y/n): {Colors.END}").strip().lower()
        if save_choice == 'y':
            save_account(user_name, username, password)
    
    # 3. CHECK VIP (ngầm)
    print_status("Đang kiểm tra quyền...", 'clock', Colors.YELLOW)
    is_vip = check_vip_status(username)
    
    # 4. XỬ LÝ LICENSE
    existing_license = load_license()
    
    if is_vip:
        # VIP
        print_status(f"Chào mừng VIP: {user_name}", 'star', Colors.PURPLE + Colors.BOLD)
        print_status("Bạn có quyền UNLIMITED", 'fire', Colors.PURPLE)
        
        save_license('VIP', 'VIP_' + username, 3650, 999999)  # 10 năm
        
    elif existing_license and existing_license.get('remain', 0) > 0:
        # CÒN LƯỢT
        print_status(f"Còn {existing_license['remain']} lượt", 'star', Colors.GREEN)
        
        # Check account lock
        locked_acc = get_locked_account()
        if locked_acc and locked_acc != username:
            print_status(f"Key đang được sử dụng bởi: {locked_acc}", 'warning', Colors.YELLOW)
            print_status("Tiếp tục sẽ chuyển sang tài khoản mới", 'info', Colors.CYAN)
        
        set_locked_account(username)
        
    else:
        # FREE - CẦN VƯỢT LINK
        print_status("Tài khoản FREE (4 lượt/ngày)", 'info', Colors.CYAN)
        print_status("Vượt link để lấy key...", 'link', Colors.YELLOW)
        
        time.sleep(1)
        
        key = get_free_key_via_link()
        
        if not key:
            print_status("Không thể lấy key!", 'error', Colors.RED)
            wait_enter()
            sys.exit(1)
        
        # Lưu license FREE
        save_license('FREE', key, 1, 4)  # 1 ngày, 4 lượt
        set_locked_account(username)
        
        print_status("Đã kích hoạt 4 lượt!", 'success', Colors.GREEN)
    
    # 5. LƯU SESSION
    if not save_session(session, user_id, user_name):
        print_status("Lỗi lưu session!", 'error', Colors.RED)
        wait_enter()
        sys.exit(1)
    
    # 6. DOWNLOAD MAIN.PY
    print_status("Đang tải main.py...", 'clock', Colors.YELLOW)
    
    try:
        response = requests.get(GITHUB_MAIN_URL, timeout=15)
        if response.status_code == 200:
            # Lưu vào temp
            temp_dir = tempfile.gettempdir()
            main_path = os.path.join(temp_dir, f'olm_main_{get_device_hash()}.py')
            
            with open(main_path, 'wb') as f:
                f.write(response.content)
            
            print_status("Khởi động tool...", 'rocket', Colors.GREEN)
            time.sleep(1)
            
            # 7. CHẠY MAIN.PY
            subprocess.run([sys.executable, main_path])
            
            # Cleanup
            try:
                os.remove(main_path)
            except:
                pass
            
        else:
            print_status("Không thể tải main.py!", 'error', Colors.RED)
            wait_enter()
            sys.exit(1)
            
    except Exception as e:
        print_status(f"Lỗi: {str(e)}", 'error', Colors.RED)
        wait_enter()
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{ICONS['exit']} {Colors.YELLOW}Đã dừng{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{ICONS['error']} {Colors.RED}Lỗi: {str(e)}{Colors.END}")
        wait_enter()
        sys.exit(1)
