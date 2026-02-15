#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║              OLM MASTER PRO V1.0 - LAUNCHER                  ║
║                  Created by: Tuấn Anh                        ║
╚══════════════════════════════════════════════════════════════╝
"""

import os
import sys
import time
import json
import hashlib
import uuid
import base64
import random
import requests
import re
import pickle
import tempfile
import subprocess
import platform
from datetime import datetime, timedelta

# ========== CẤU HÌNH ==========
GITHUB_MAIN = "https://raw.githubusercontent.com/thieunangbiettuot/ToolOLM/refs/heads/main/main.py"
GITHUB_VIP = "https://raw.githubusercontent.com/thieunangbiettuot/ToolOLM/refs/heads/main/vip_users.txt"

LINK_SERVICES = [
    {"name": "link4m_1", "api": "https://link4m.co/api-shorten/v2", "token": "67972e91b83ea2ab66c0c86d"},
    {"name": "link4m_2", "api": "https://link4m.co/api-shorten/v2", "token": "BACKUP_TOKEN_IF_NEEDED"},
]

# ========== MÀU SẮC ==========
class C:
    R = '\033[91m'  # Red
    G = '\033[92m'  # Green
    Y = '\033[93m'  # Yellow
    B = '\033[94m'  # Blue
    M = '\033[95m'  # Magenta
    C = '\033[96m'  # Cyan
    W = '\033[97m'  # White
    BD = '\033[1m'  # Bold
    E = '\033[0m'   # End

# ========== PHÁT HIỆN HỆ ĐIỀU HÀNH ==========
def get_os_type():
    """Phát hiện hệ điều hành"""
    system = platform.system().lower()
    if 'android' in platform.platform().lower() or 'ANDROID_ROOT' in os.environ or 'TERMUX_VERSION' in os.environ:
        return 'android'
    return system

def is_android():
    """Kiểm tra có phải Android/Termux không"""
    return get_os_type() == 'android'

def get_terminal_width():
    """Lấy độ rộng terminal"""
    try:
        cols = os.get_terminal_size().columns
        if is_android():
            return min(cols - 2, 45)
        return min(cols - 2, 68)
    except:
        return 45 if is_android() else 60

# ========== ĐƯỜNG DẪN FILE ==========
def get_base_path():
    """Lấy đường dẫn cơ sở để lưu file"""
    os_type = get_os_type()
    
    if os_type == 'windows':
        base = os.path.join(os.environ.get('LOCALAPPDATA', os.path.expanduser('~')), 
                           'Microsoft', 'Windows', 'INetCache', 'IE')
    elif os_type == 'darwin':  # macOS
        base = os.path.join(os.path.expanduser('~'), 'Library', 'Application Support', 
                           'com.apple.Safari')
    elif os_type == 'android':
        base = os.path.join(os.path.expanduser('~'), '.cache', 'google-chrome')
    else:  # Linux
        base = os.path.join(os.path.expanduser('~'), '.cache', 'mozilla', 'firefox')
    
    os.makedirs(base, exist_ok=True)
    return base

def get_device_hash():
    """Tạo hash thiết bị duy nhất"""
    hostname = platform.node()
    mac = uuid.getnode()
    device_str = f"{hostname}{mac}{platform.system()}"
    return hashlib.md5(device_str.encode()).hexdigest()[:12]

DEVICE_HASH = get_device_hash()
BASE_PATH = get_base_path()

# File paths
LICENSE_FILE = os.path.join(BASE_PATH, f'.{DEVICE_HASH}sc')
SESSION_FILE = os.path.join(BASE_PATH, f'.{DEVICE_HASH}ss')
ACCOUNTS_FILE = os.path.join(BASE_PATH, f'.{DEVICE_HASH}ac')
LOCK_FILE = os.path.join(BASE_PATH, f'.{DEVICE_HASH}lk')

# ========== MÃ HÓA/GIẢI MÃ ==========
SECRET_KEY = f"{DEVICE_HASH}:olmv1:secret".encode()

def xor_cipher(data, key):
    """XOR encryption/decryption"""
    key_len = len(key)
    return bytes([data[i] ^ key[i % key_len] for i in range(len(data))])

def encode_data(data):
    """Mã hóa dữ liệu"""
    try:
        # Convert to JSON
        json_str = json.dumps(data)
        json_bytes = json_str.encode('utf-8')
        
        # XOR encrypt
        encrypted = xor_cipher(json_bytes, SECRET_KEY)
        
        # Base85 encode
        b85 = base64.b85encode(encrypted).decode('ascii')
        
        # Add checksum
        checksum = hashlib.sha256(b85.encode()).hexdigest()[:12]
        
        # Add noise
        noise_prefix = hashlib.md5(f"{time.time()}{random.random()}".encode()).hexdigest()[:8]
        noise_suffix = noise_prefix[::-1]
        
        # Combine
        result = f"{noise_prefix}{checksum}{b85}{noise_suffix}"
        return result
    except Exception as e:
        return None

def decode_data(encoded):
    """Giải mã dữ liệu"""
    try:
        # Remove noise
        data = encoded[8:-8]
        
        # Extract checksum and b85
        checksum = data[:12]
        b85 = data[12:]
        
        # Verify checksum
        expected_checksum = hashlib.sha256(b85.encode()).hexdigest()[:12]
        if checksum != expected_checksum:
            return None
        
        # Decode
        encrypted = base64.b85decode(b85)
        decrypted = xor_cipher(encrypted, SECRET_KEY)
        json_str = decrypted.decode('utf-8')
        
        return json.loads(json_str)
    except Exception as e:
        return None

# ========== FILE I/O ==========
def save_file(filepath, data):
    """Lưu file"""
    try:
        encoded = encode_data(data)
        if encoded:
            with open(filepath, 'w') as f:
                f.write(encoded)
            return True
    except:
        pass
    return False

def load_file(filepath):
    """Đọc file"""
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                encoded = f.read()
            return decode_data(encoded)
    except:
        pass
    return None

# ========== ANTI-DEBUG ==========
def check_env():
    """Kiểm tra môi trường"""
    if hasattr(sys, 'gettrace') and sys.gettrace():
        sys.exit(0)
    
    dangerous_env = ['PYTEST', 'JUPYTER', 'IPYTHON']
    for env in dangerous_env:
        if env in os.environ:
            time.sleep(3)
            break

# ========== UI ==========
def clear():
    """Xóa màn hình"""
    os.system('cls' if os.name == 'nt' else 'clear')
    if is_android():
        print('\033[2J\033[H', end='')

def print_line(char='═', width=None):
    """In đường kẻ"""
    if width is None:
        width = get_terminal_width()
    print(f"{C.C}{char * width}{C.E}")

def print_header(title="OLM MASTER PRO V1.0"):
    """In header"""
    clear()
    width = get_terminal_width()
    print_line('═', width)
    padding = (width - len(title)) // 2
    print(f"{C.B}{C.BD}{' ' * padding}{title}{C.E}")
    print_line('═', width)
    print()

def print_msg(msg, icon='•', color=C.W):
    """In thông báo"""
    print(f"{icon} {color}{msg}{C.E}")

# ========== VIP CHECK ==========
def check_vip_status(username):
    """Kiểm tra VIP từ GitHub (ngầm)"""
    try:
        response = requests.get(GITHUB_VIP, timeout=10)
        if response.status_code == 200:
            vip_list = response.text.strip().split('\n')
            # Lọc comment và khoảng trắng
            vip_users = [line.strip().lower() for line in vip_list 
                        if line.strip() and not line.strip().startswith('#')]
            return username.lower() in vip_users
    except:
        pass
    return False

# ========== KEY GENERATION ==========
def generate_key():
    """Tạo key FREE duy nhất"""
    now = datetime.now()
    device_id = DEVICE_HASH
    timestamp = str(time.time()).encode()
    random_num = str(random.randint(1000, 9999)).encode()
    unique_string = device_id.encode() + timestamp + random_num
    
    hash_value = hashlib.sha256(unique_string).hexdigest()
    
    key = f"OLMFREE-{now:%d%m}-{hash_value[:4].upper()}-{hash_value[4:8].upper()}"
    return key

def create_short_link(key, service_idx=0):
    """Tạo link rút gọn"""
    if service_idx >= len(LINK_SERVICES):
        return None
    
    service = LINK_SERVICES[service_idx]
    
    try:
        # Tạo URL chứa key (giả định - có thể thay đổi)
        full_url = f"https://olmmaster.vercel.app/?key={key}"
        
        payload = {
            'url': full_url,
            'api_token': service['token']
        }
        
        response = requests.post(service['api'], json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if 'shortenedUrl' in data:
                return data['shortenedUrl']
            elif 'url' in data:
                return data['url']
    except:
        pass
    
    return None

# ========== BYPASS LINK ==========
def bypass_link_flow():
    """Flow vượt link để lấy key"""
    print_header("LẤY KEY MIỄN PHÍ")
    
    # Tạo key
    key = generate_key()
    
    # Thử tạo link
    print_msg("Đang tạo link...", '⏳', C.Y)
    
    short_link = None
    for i in range(len(LINK_SERVICES)):
        short_link = create_short_link(key, i)
        if short_link:
            break
    
    if not short_link:
        print_msg("Không thể tạo link!", '❌', C.R)
        input(f"\n{C.Y}Nhấn Enter để tiếp tục...{C.E}")
        return None
    
    # Hiển thị link
    print()
    print_msg(f"Link: {short_link}", '🔗', C.C)
    print()
    print_msg("Vượt link trên để lấy mã", 'ℹ️', C.W)
    print_msg("Sau khi vượt xong, nhập mã bên dưới", 'ℹ️', C.W)
    print()
    
    # Cho phép đổi link tối đa 3 lần
    attempts = 0
    max_attempts = 3
    
    while attempts < max_attempts:
        user_input = input(f"{C.Y}Mã (hoặc 'r' để đổi link): {C.E}").strip()
        
        if user_input.lower() == 'r':
            # Tạo key và link mới
            key = generate_key()
            print_msg("Đang tạo link mới...", '⏳', C.Y)
            
            short_link = None
            for i in range(len(LINK_SERVICES)):
                short_link = create_short_link(key, i)
                if short_link:
                    break
            
            if short_link:
                print()
                print_msg(f"Link mới: {short_link}", '🔗', C.C)
                print()
            else:
                print_msg("Không thể tạo link mới!", '❌', C.R)
            
            attempts += 1
            continue
        
        # Kiểm tra key
        if user_input.upper() == key:
            print_msg("✓ Mã hợp lệ!", '✓', C.G)
            time.sleep(0.5)
            return key
        else:
            remaining = max_attempts - attempts - 1
            if remaining > 0:
                print_msg(f"✗ Mã sai (còn {remaining} lần)", '✗', C.R)
                attempts += 1
                time.sleep(1)
            else:
                print_msg("✗ Hết lượt thử!", '✗', C.R)
                input(f"\n{C.Y}Nhấn Enter để thoát và thử lại...{C.E}")
                return None
    
    print_msg("Đã hết lượt thử!", '⛔', C.R)
    input(f"\n{C.Y}Nhấn Enter để tiếp tục...{C.E}")
    return None

# ========== LICENSE MANAGEMENT ==========
def get_current_ip():
    """Lấy IP hiện tại"""
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        return response.json()['ip']
    except:
        return None

def compute_signature(license_data):
    """Tính signature cho license"""
    sig_str = f"{license_data['mode']}{license_data['expire']}{license_data.get('ip', '')}{license_data.get('remain', 0)}"
    return hashlib.sha256(sig_str.encode()).hexdigest()[:16]

def save_license(mode, remain=4, username=""):
    """Lưu license"""
    expire_date = (datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y")
    current_ip = get_current_ip() if mode == 'FREE' else ""
    
    license_data = {
        'mode': mode,
        'remain': remain if mode == 'FREE' else -1,  # -1 = unlimited
        'expire': expire_date,
        'ip': current_ip,
        'username': username
    }
    
    license_data['sig'] = compute_signature(license_data)
    
    return save_file(LICENSE_FILE, license_data)

def load_license():
    """Đọc license"""
    data = load_file(LICENSE_FILE)
    
    if not data:
        return None
    
    # Verify signature
    expected_sig = compute_signature(data)
    if data.get('sig') != expected_sig:
        # File bị sửa
        try:
            os.remove(LICENSE_FILE)
        except:
            pass
        return None
    
    # Check expire
    try:
        expire_date = datetime.strptime(data['expire'], "%d/%m/%Y").date()
        if expire_date < datetime.now().date():
            return None
    except:
        return None
    
    # Check IP (FREE only)
    if data.get('mode') == 'FREE':
        current_ip = get_current_ip()
        if current_ip and data.get('ip') != current_ip:
            return None
    
    # Check remain
    remain = data.get('remain', 0)
    if data.get('mode') == 'FREE' and remain <= 0:
        return None
    
    return data

def update_license_remain(new_remain):
    """Cập nhật số lượt còn lại"""
    data = load_license()
    if data and data.get('mode') == 'FREE':
        data['remain'] = new_remain
        data['sig'] = compute_signature(data)
        save_file(LICENSE_FILE, data)

# ========== ACCOUNT LOCK ==========
def save_account_lock(username):
    """Lưu account lock"""
    return save_file(LOCK_FILE, {'username': username})

def load_account_lock():
    """Đọc account lock"""
    return load_file(LOCK_FILE)

def clear_account_lock():
    """Xóa account lock"""
    try:
        if os.path.exists(LOCK_FILE):
            os.remove(LOCK_FILE)
        return True
    except:
        return False

# ========== ACCOUNTS MANAGEMENT ==========
def save_accounts(accounts):
    """Lưu danh sách tài khoản"""
    return save_file(ACCOUNTS_FILE, accounts)

def load_accounts():
    """Đọc danh sách tài khoản"""
    data = load_file(ACCOUNTS_FILE)
    return data if data else {}

def select_account():
    """Chọn tài khoản"""
    accounts = load_accounts()
    
    if not accounts:
        return None, None
    
    print_header("TÀI KHOẢN ĐÃ LƯU")
    
    account_list = list(accounts.items())
    for idx, (name, data) in enumerate(account_list, 1):
        saved_time = data.get('saved_at', '')
        print(f"  {C.Y}{idx}.{C.E} {C.W}{name}{C.E} {C.C}({saved_time}){C.E}")
    
    print(f"  {C.Y}0.{C.E} {C.W}Đăng nhập mới{C.E}")
    print()
    
    choice = input(f"{C.Y}Chọn (0-{len(account_list)}): {C.E}").strip()
    
    if choice == '0':
        return None, None
    
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(account_list):
            name, data = account_list[idx]
            return data.get('username'), data.get('password')
    except:
        pass
    
    return None, None

def save_new_account(name, username, password):
    """Lưu tài khoản mới"""
    accounts = load_accounts()
    accounts[name] = {
        'username': username,
        'password': password,
        'saved_at': datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    return save_accounts(accounts)

# ========== OLM LOGIN ==========
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
        print_msg("Đang đăng nhập...", '⏳', C.Y)
        
        # Lấy CSRF
        session.get("https://olm.vn/dangnhap", headers=HEADERS, timeout=10)
        csrf = session.cookies.get('XSRF-TOKEN')
        
        # Payload
        payload = {
            '_token': csrf,
            'username': username,
            'password': password,
            'remember': 'true',
            'device_id': DEVICE_HASH,
            'platform': 'web'
        }
        
        h_login = HEADERS.copy()
        h_login['x-csrf-token'] = csrf
        
        # Login
        session.post("https://olm.vn/post-login", data=payload, headers=h_login, timeout=10)
        
        # Check
        check_res = session.get("https://olm.vn/thong-tin-tai-khoan/info", headers=HEADERS, timeout=10)
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

# ========== SESSION MANAGEMENT ==========
def save_session(session, user_id, user_name):
    """Lưu session"""
    session_data = {
        'cookies': session.cookies.get_dict(),
        'user_id': user_id,
        'user_name': user_name
    }
    return save_file(SESSION_FILE, session_data)

# ========== DOWNLOAD & RUN MAIN ==========
def download_main():
    """Download main.py từ GitHub"""
    try:
        print_msg("Đang tải main.py...", '⏳', C.Y)
        response = requests.get(GITHUB_MAIN, timeout=15)
        
        if response.status_code == 200:
            return response.text
        return None
    except:
        return None

def run_main(session, user_id, user_name):
    """Chạy main.py"""
    # Download main.py
    main_code = download_main()
    
    if not main_code:
        print_msg("Không thể tải main.py!", '❌', C.R)
        input(f"\n{C.Y}Nhấn Enter để tiếp tục...{C.E}")
        return
    
    # Lưu session
    save_session(session, user_id, user_name)
    
    # Chạy trong temp
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            f.write(main_code)
            temp_file = f.name
        
        # Chạy
        subprocess.run([sys.executable, temp_file], check=False)
        
        # Xóa temp file
        try:
            os.remove(temp_file)
        except:
            pass
            
    except Exception as e:
        print_msg(f"Lỗi chạy main.py: {str(e)}", '❌', C.R)
        input(f"\n{C.Y}Nhấn Enter để tiếp tục...{C.E}")

# ========== MAIN LAUNCHER ==========
def main():
    """Main launcher"""
    check_env()
    
    print_header()
    print_msg("Khởi động OLM Master Pro...", '🚀', C.G)
    time.sleep(1)
    
    # Bước 1: Chọn/đăng nhập tài khoản
    print_header("ĐĂNG NHẬP")
    
    saved_username, saved_password = select_account()
    
    if saved_username and saved_password:
        use_saved = input(f"\n{C.Y}Dùng tài khoản đã lưu? (y/n): {C.E}").strip().lower()
        if use_saved == 'y':
            username = saved_username
            password = saved_password
        else:
            username = input(f"\n👤 {C.Y}Tên đăng nhập: {C.E}").strip()
            password = input(f"🔑 {C.Y}Mật khẩu: {C.E}").strip()
    else:
        username = input(f"\n👤 {C.Y}Tên đăng nhập: {C.E}").strip()
        password = input(f"🔑 {C.Y}Mật khẩu: {C.E}").strip()
    
    if not username or not password:
        print_msg("Tên đăng nhập/mật khẩu trống!", '❌', C.R)
        input(f"\n{C.Y}Nhấn Enter để thoát...{C.E}")
        return
    
    # Bước 2: Đăng nhập
    session, user_id, user_name = login_olm(username, password)
    
    if not session:
        print_msg("Đăng nhập thất bại!", '❌', C.R)
        print_msg("Sai tên đăng nhập hoặc mật khẩu", 'ℹ️', C.W)
        input(f"\n{C.Y}Nhấn Enter để thoát...{C.E}")
        return
    
    print_msg(f"✓ Đăng nhập thành công!", '✓', C.G)
    print_msg(f"Xin chào: {user_name}", '👤', C.C)
    time.sleep(1)
    
    # Hỏi lưu tài khoản
    if not saved_username or saved_username != username:
        save_choice = input(f"\n{C.Y}Lưu tài khoản? (y/n): {C.E}").strip().lower()
        if save_choice == 'y':
            save_new_account(user_name, username, password)
            print_msg("✓ Đã lưu tài khoản", '✓', C.G)
            time.sleep(0.5)
    
    # Bước 3: Check VIP (ngầm)
    print()
    print_msg("Đang kiểm tra quyền truy cập...", '⏳', C.Y)
    
    is_vip = check_vip_status(username)
    
    if is_vip:
        # VIP - không cần vượt link
        print_msg("✓ Tài khoản VIP", '⭐', C.G)
        print_msg("• Không giới hạn lượt làm bài", 'ℹ️', C.C)
        save_license('VIP', username=username)
        time.sleep(1)
    else:
        # FREE - kiểm tra license
        print_msg("Tài khoản FREE", 'ℹ️', C.Y)
        
        license_data = load_license()
        
        if license_data and license_data.get('remain', 0) > 0:
            # Có license còn hiệu lực
            remain = license_data.get('remain', 0)
            print_msg(f"✓ Còn {remain} lượt làm bài", '💎', C.G)
            time.sleep(1)
        else:
            # Cần lấy key mới
            print_msg("• 4 lượt/ngày", 'ℹ️', C.C)
            print_msg("• Cần vượt link để lấy key", 'ℹ️', C.C)
            time.sleep(1)
            
            key = bypass_link_flow()
            
            if not key:
                print_msg("Không có key, thoát!", '❌', C.R)
                input(f"\n{C.Y}Nhấn Enter để thoát...{C.E}")
                return
            
            # Lưu license FREE
            save_license('FREE', remain=4, username=username)
            print_msg("✓ Đã kích hoạt key FREE", '✓', C.G)
            print_msg("• Còn 4 lượt làm bài", '💎', C.G)
            time.sleep(1)
    
    # Bước 4: Lưu account lock
    save_account_lock(username)
    
    # Bước 5: Chạy main.py
    print()
    print_msg("Đang khởi động tool...", '🚀', C.G)
    time.sleep(1)
    
    run_main(session, user_id, user_name)
    
    # Kết thúc
    print()
    print_msg("Đã thoát tool!", '👋', C.C)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{C.Y}Đã dừng chương trình{C.E}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{C.R}Lỗi: {str(e)}{C.E}")
        input(f"\n{C.Y}Nhấn Enter để thoát...{C.E}")
