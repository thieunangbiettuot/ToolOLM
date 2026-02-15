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
from datetime import datetime
import uuid
import random
import string

# ========== CẤU HÌNH ==========
LAUNCHER_VERSION = "1.0"
GITHUB_RAW = "https://raw.githubusercontent.com/thieunangbiettuot/ToolOLM/refs/heads/main/"
VIP_LIST_URL = GITHUB_RAW + "vip_users.txt"
MAIN_PY_URL = GITHUB_RAW + "main.py"

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

def print_header(title="OLM MASTER PRO", subtitle="LAUNCHER V1.0"):
    """In header"""
    clear_screen()
    width = min(get_terminal_width() - 4, 80)
    
    print_box(title, [
        f"{ICONS['rocket']} {subtitle}",
        f"{ICONS['crown']} Premium Auto Solver for OLM",
        f"Created by: Tuấn Anh"
    ], Colors.BLUE, width)

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

def get_device_hash():
    """Lấy device hash"""
    try:
        # Tạo hash từ hostname + MAC address
        hostname = platform.node()
        mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0, 2*6, 2)][::-1])
        device_string = f"{hostname}{mac}"
        return hashlib.md5(device_string.encode()).hexdigest()[:16]
    except:
        return hashlib.md5(str(uuid.getnode()).encode()).hexdigest()[:16]

def get_data_dir():
    """Lấy thư mục dữ liệu"""
    device_hash = get_device_hash()
    
    if platform.system() == "Windows":
        data_dir = os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Microsoft', 'Windows', 'INetCache', 'IE')
    elif platform.system() == "Darwin":  # macOS
        data_dir = os.path.expanduser('~/Library/Application Support/com.apple.Safari')
    elif platform.system() == "Linux":
        data_dir = os.path.expanduser('~/.cache/mozilla/firefox')
    else:  # Android/Termux
        data_dir = os.path.expanduser('~/.cache/google-chrome')
    
    # Tạo thư mục nếu không tồn tại
    if not os.path.exists(data_dir):
        try:
            os.makedirs(data_dir, exist_ok=True)
        except:
            data_dir = tempfile.gettempdir()
    
    return data_dir

def get_data_file(extension):
    """Lấy đường dẫn file dữ liệu"""
    device_hash = get_device_hash()
    data_dir = get_data_dir()
    filename = f".{device_hash}{extension}"
    return os.path.join(data_dir, filename)

# ========== MÃ HÓA ==========
def encrypt_data(data):
    """Mã hóa dữ liệu"""
    try:
        # Secret key
        secret = "OLM_MASTER_PRO_2026"
        secret_bytes = secret.encode()
        
        # Chuyển data thành JSON string
        json_str = json.dumps(data)
        data_bytes = json_str.encode()
        
        # XOR encryption
        encrypted = bytearray()
        for i, byte in enumerate(data_bytes):
            encrypted.append(byte ^ secret_bytes[i % len(secret_bytes)])
        
        # Base85 encoding
        encoded = encrypted.decode('utf-8', errors='ignore').encode('utf-8')
        base85_data = encoded.decode('utf-8', errors='ignore')
        
        # Tạo checksum
        checksum = hashlib.sha256(json_str.encode()).hexdigest()[:12]
        
        # Tạo noise
        noise_prefix = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        noise_suffix = noise_prefix[::-1]
        
        # Kết hợp
        result = f"{noise_prefix}{checksum}{base85_data}{noise_suffix}"
        return result
    except:
        return None

def decrypt_data(encrypted_str):
    """Giải mã dữ liệu"""
    try:
        # Secret key
        secret = "OLM_MASTER_PRO_2026"
        secret_bytes = secret.encode()
        
        # Tách các phần
        if len(encrypted_str) < 28:  # 8 + 12 + 8
            return None
            
        noise_prefix = encrypted_str[:8]
        checksum = encrypted_str[8:20]
        base85_data = encrypted_str[20:-8]
        noise_suffix = encrypted_str[-8:]
        
        # Kiểm tra noise
        if noise_prefix != noise_suffix[::-1]:
            return None
        
        # Base85 decode
        try:
            encrypted_bytes = base85_data.encode('utf-8')
            encrypted = bytearray(encrypted_bytes.decode('utf-8', errors='ignore'), 'latin-1')
        except:
            return None
        
        # XOR decryption
        decrypted = bytearray()
        for i, byte in enumerate(encrypted):
            decrypted.append(byte ^ secret_bytes[i % len(secret_bytes)])
        
        # Parse JSON
        json_str = decrypted.decode('utf-8')
        data = json.loads(json_str)
        
        # Verify checksum
        expected_checksum = hashlib.sha256(json_str.encode()).hexdigest()[:12]
        if checksum != expected_checksum:
            return None
        
        return data
    except:
        return None

# ========== QUẢN LÝ FILE ==========
def save_file(data, extension):
    """Lưu file dữ liệu"""
    try:
        file_path = get_data_file(extension)
        encrypted = encrypt_data(data)
        if encrypted:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(encrypted)
            return True
    except:
        pass
    return False

def load_file(extension):
    """Tải file dữ liệu"""
    try:
        file_path = get_data_file(extension)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                encrypted_str = f.read()
            return decrypt_data(encrypted_str)
    except:
        pass
    return None

def delete_file(extension):
    """Xóa file dữ liệu"""
    try:
        file_path = get_data_file(extension)
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
    except:
        pass
    return False

# ========== QUẢN LÝ TÀI KHOẢN ==========
def load_accounts():
    """Tải danh sách tài khoản"""
    return load_file('ac') or {}

def save_accounts(accounts):
    """Lưu danh sách tài khoản"""
    return save_file(accounts, 'ac')

def select_account():
    """Chọn tài khoản"""
    accounts = load_accounts()
    if not accounts:
        return None, None, None
    
    account_list = list(accounts.items())
    
    options = [f"{Colors.GREEN}{ICONS['user']} TÀI KHOẢN ĐÃ LƯU{Colors.RESET}"]
    for idx, (name, data) in enumerate(account_list, 1):
        saved_time = data.get('saved_at', 'N/A')
        options.append(f"{Colors.YELLOW}[{idx}]{Colors.RESET} {name} {Colors.CYAN}({saved_time}){Colors.RESET}")
    
    options.append(f"{Colors.YELLOW}[0]{Colors.RESET} Đăng nhập mới")
    
    print_menu("LỰA CHỌN TÀI KHOẢN", options)
    
    choice = input(f"\n{Colors.YELLOW}Chọn tài khoản (0-{len(account_list)}): {Colors.RESET}").strip()
    
    if choice == '0':
        return None, None, None
    
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(account_list):
            name, data = account_list[idx]
            return data.get('username'), data.get('password'), name
    
    return None, None, None

def save_account(name, username, password):
    """Lưu tài khoản"""
    accounts = load_accounts()
    accounts[name] = {
        'username': username,
        'password': password,
        'saved_at': datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    return save_accounts(accounts)

# ========== ĐĂNG NHẬP OLM ==========
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'vi-VN,vi;q=0.9,en-US;q=0.8',
    'x-requested-with': 'XMLHttpRequest',
    'origin': 'https://olm.vn',
    'referer': 'https://olm.vn/'
}

def login_olm(username, password):
    """Đăng nhập OLM"""
    session = requests.Session()
    session.headers.update(HEADERS)
    
    try:
        print_status("Đang đăng nhập...", 'info', Colors.YELLOW)
        
        # Lấy trang đăng nhập
        session.get("https://olm.vn/dangnhap")
        csrf = session.cookies.get('XSRF-TOKEN')
        
        # Tạo payload
        payload = {
            '_token': csrf,
            'username': username,
            'password': password,
            'remember': 'true',
            'device_id': '0b48f4d6204591f83dc40b07f07af7d4',
            'platform': 'web'
        }
        
        headers = HEADERS.copy()
        headers['x-csrf-token'] = csrf
        
        # Đăng nhập
        session.post("https://olm.vn/post-login", data=payload, headers=headers)
        
        # Kiểm tra thành công
        check_res = session.get("https://olm.vn/thong-tin-tai-khoan/info")
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
        
    except:
        return None, None, None

# ========== CHECK VIP ==========
def check_vip(username):
    """Check VIP từ GitHub"""
    try:
        print_status("Đang kiểm tra tài khoản VIP...", 'info', Colors.YELLOW)
        
        # Tải danh sách VIP
        response = requests.get(VIP_LIST_URL, timeout=10)
        if response.status_code == 200:
            vip_list = response.text.lower().split('\n')
            # Bỏ dòng comment và trống
            vip_list = [line.strip() for line in vip_list if line.strip() and not line.strip().startswith('#')]
            
            if username.lower() in vip_list:
                print_status(f"{ICONS['crown']} Tài khoản VIP!", 'success', Colors.GREEN + Colors.BOLD)
                return True
            else:
                print_status("Tài khoản FREE", 'info', Colors.CYAN)
                return False
        else:
            print_status("Không thể kiểm tra VIP, mặc định là FREE", 'warning', Colors.YELLOW)
            return False
    except:
        print_status("Lỗi kiểm tra VIP, mặc định là FREE", 'error', Colors.RED)
        return False

# ========== KEY GENERATION ==========
def generate_key():
    """Tạo key độc nhất"""
    now = datetime.now()
    
    # DDMM format
    ddmm = now.strftime("%d%m")
    
    # Tạo unique string
    device_id = get_device_hash()
    timestamp = str(int(now.timestamp() * 1000))  # milliseconds
    random_str = str(random.randint(1000, 9999))
    
    unique_string = f"{device_id}{timestamp}{random_str}"
    
    # Hash
    hash_value = hashlib.sha256(unique_string.encode()).hexdigest().upper()
    
    # Format key: OLMFREE-DDMM-XXXX-YYYY
    key = f"OLMFREE-{ddmm}-{hash_value[:4]}-{hash_value[4:8]}"
    
    return key

# ========== RÚT GỌN LINK (LINK4M) ==========
LINK_SERVICES = [
    {"name": "link4m_1", "api": "https://link4m.co/api-shorten/v2", "token": "TOKEN_1"},
    {"name": "link4m_2", "api": "https://link4m.co/api-shorten/v2", "token": "TOKEN_2"}
]

def shorten_link(original_url, max_retries=2):
    """Rút gọn link với link4m"""
    for i in range(max_retries):
        service = random.choice(LINK_SERVICES)
        try:
            print_status("Đang tạo link rút gọn...", 'info', Colors.YELLOW)
            
            payload = {
                'url': original_url,
                'alias': '',
                'password': '',
                'token': service['token']
            }
            
            response = requests.post(service['api'], data=payload, timeout=15)
            
            if response.status_code == 200:
                result = response.json()
                if 'shorturl' in result:
                    short_url = result['shorturl']
                    print_status("Tạo link thành công!", 'success', Colors.GREEN)
                    return short_url
            
        except:
            continue
    
    print_status("Không thể tạo link rút gọn", 'error', Colors.RED)
    return None

def get_key_from_user(expected_key=None):
    """Nhập key từ người dùng"""
    if expected_key:
        print_status(f"Dự phòng: {expected_key}", 'info', Colors.CYAN)
    
    for i in range(3):
        key = input(f"{Colors.YELLOW}{ICONS['key']} Nhập key: {Colors.RESET}").strip()
        
        if key == expected_key:
            print_status("Key hợp lệ!", 'success', Colors.GREEN)
            return True
        
        if i < 2:
            remaining = 2 - i
            print_status(f"Key sai! Còn {remaining} lần thử", 'error', Colors.RED)
            time.sleep(1)
    
    print_status("Nhập sai key quá 3 lần!", 'error', Colors.RED)
    return False

# ========== QUẢN LÝ LICENSE ==========
def load_license():
    """Tải license"""
    return load_file('sc')

def save_license(license_data):
    """Lưu license"""
    return save_file(license_data, 'sc')

def delete_license():
    """Xóa license"""
    return delete_file('sc')

def get_current_ip():
    """Lấy IP hiện tại"""
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        if response.status_code == 200:
            return response.json()['ip']
    except:
        pass
    return "127.0.0.1"

def is_license_valid():
    """Kiểm tra license có còn hiệu lực không"""
    license_data = load_license()
    if not license_data:
        return None
    
    # Kiểm tra expire
    try:
        expire_date = datetime.strptime(license_data['expire'], "%d/%m/%Y").date()
        if expire_date < datetime.now().date():
            print_status("License đã hết hạn!", 'warning', Colors.YELLOW)
            delete_license()
            return None
    except:
        print_status("License lỗi!", 'error', Colors.RED)
        delete_license()
        return None
    
    # Kiểm tra IP (chỉ cho FREE)
    if license_data.get('mode') == 'FREE':
        current_ip = get_current_ip()
        if license_data.get('ip') != current_ip:
            print_status("IP đã thay đổi!", 'warning', Colors.YELLOW)
            delete_license()
            return None
    
    # Kiểm tra lượt
    if license_data.get('mode') == 'FREE':
        if license_data.get('remain', 0) <= 0:
            print_status("Đã hết lượt!", 'warning', Colors.YELLOW)
            delete_license()
            return None
    
    return license_data

def process_free_license():
    """Xử lý license FREE"""
    key = generate_key()
    
    # Tạo link vượt link
    original_url = f"https://olm.vn/get-key?key={key}"
    short_url = shorten_link(original_url)
    
    if not short_url:
        print_status("Không thể tạo link vượt link", 'error', Colors.RED)
        return False
    
    # Hiển thị link
    print_box("VƯỚT LINK ĐỂ LẤY KEY", [
        f"Link: {short_url}",
        f"Vui lòng vượt link và nhập key bên dưới"
    ], Colors.YELLOW)
    
    # Cho phép đổi link
    for attempt in range(3):
        user_input = input(f"{Colors.YELLOW}Key (r=link mới): {Colors.RESET}").strip()
        
        if user_input.lower() == 'r':
            # Tạo key và link mới
            key = generate_key()
            original_url = f"https://olm.vn/get-key?key={key}"
            short_url = shorten_link(original_url)
            
            if short_url:
                print_box("LINK MỚI", [f"Link: {short_url}"], Colors.CYAN)
                continue
            else:
                print_status("Không thể tạo link mới", 'error', Colors.RED)
                continue
        
        if user_input == key:
            print_status("Key hợp lệ!", 'success', Colors.GREEN)
            
            # Tạo license
            today = datetime.now()
            expire_date = today.strftime("%d/%m/%Y")
            
            license_data = {
                'mode': 'FREE',
                'key': key,
                'expire': expire_date,
                'ip': get_current_ip(),
                'remain': 4,
                'created_at': today.strftime("%d/%m/%Y %H:%M:%S")
            }
            
            # Lưu license
            if save_license(license_data):
                print_status(f"{ICONS['diamond']} Còn: 4 lượt", 'info', Colors.GREEN)
                return True
            else:
                print_status("Không thể lưu license", 'error', Colors.RED)
                return False
        else:
            remaining = 2 - attempt
            if remaining > 0:
                print_status(f"Key sai! Còn {remaining} lần thử", 'error', Colors.RED)
    
    print_status("Nhập sai key quá 3 lần!", 'error', Colors.RED)
    return False

def process_vip_license():
    """Xử lý license VIP"""
    # Tạo license VIP
    today = datetime.now()
    
    license_data = {
        'mode': 'VIP',
        'expire': '31/12/2099',  # Không bao giờ hết hạn
        'unlimited': True,
        'created_at': today.strftime("%d/%m/%Y %H:%M:%S")
    }
    
    # Lưu license
    if save_license(license_data):
        print_status(f"{ICONS['crown']} VIP Activated! Unlimited lượt", 'success', Colors.GREEN + Colors.BOLD)
        return True
    else:
        print_status("Không thể lưu license VIP", 'error', Colors.RED)
        return False

# ========== CHẠY MAIN.PY ==========
def download_and_run_main(session, user_id):
    """Tải và chạy main.py"""
    try:
        print_status("Đang tải main.py...", 'download', Colors.YELLOW)
        
        # Tải file
        response = requests.get(MAIN_PY_URL, timeout=15)
        if response.status_code != 200:
            print_status("Không thể tải main.py", 'error', Colors.RED)
            return False
        
        # Lưu vào temp
        temp_dir = tempfile.gettempdir()
        main_path = os.path.join(temp_dir, "main_olm.py")
        
        with open(main_path, 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        print_status("Đang khởi động...", 'rocket', Colors.GREEN)
        time.sleep(1)
        
        # Truyền session và user_id qua file tạm
        session_file = os.path.join(temp_dir, "session_olm.pkl")
        with open(session_file, 'wb') as f:
            pickle.dump((session, user_id), f)
        
        # Chạy main.py
        subprocess.run([sys.executable, main_path])
        
        # Xóa file tạm
        try:
            os.remove(main_path)
            os.remove(session_file)
        except:
            pass
        
        return True
        
    except:
        print_status("Lỗi khi chạy main.py", 'error', Colors.RED)
        return False

# ========== MAIN ==========
def main():
    """Hàm chính"""
    # Anti-debug
    if hasattr(sys, 'gettrace') and sys.gettrace():
        sys.exit(0)
    
    print_header()
    
    # Chọn tài khoản
    username, password, account_name = select_account()
    
    if not username:
        # Đăng nhập mới
        username = input(f"{Colors.YELLOW}{ICONS['user']} Tên đăng nhập: {Colors.RESET}").strip()
        password = input(f"{Colors.YELLOW}{ICONS['key']} Mật khẩu: {Colors.RESET}").strip()
    
    if not username or not password:
        print_status("Tên đăng nhập và mật khẩu không được để trống!", 'error', Colors.RED)
        wait_enter()
        return
    
    # Đăng nhập
    session, user_id, user_name = login_olm(username, password)
    
    if not session or not user_id or not user_name:
        print_status("Đăng nhập thất bại!", 'error', Colors.RED)
        wait_enter()
        return
    
    print_status(f"Đăng nhập thành công: {user_name}", 'success', Colors.GREEN)
    
    # Lưu tài khoản
    if not account_name:
        save_choice = input(f"{Colors.YELLOW}Lưu tài khoản này? (y/n): {Colors.RESET}").strip().lower()
        if save_choice == 'y':
            save_account(user_name, username, password)
    
    # Kiểm tra license
    license_data = is_license_valid()
    
    if license_data:
        # License còn hiệu lực
        if license_data.get('mode') == 'VIP':
            print_status(f"{ICONS['crown']} VIP Activated!", 'success', Colors.GREEN)
        else:
            remain = license_data.get('remain', 0)
            print_status(f"{ICONS['diamond']} Còn: {remain} lượt", 'info', Colors.CYAN)
    else:
        # Check VIP
        is_vip = check_vip(username)
        
        if is_vip:
            # Kích hoạt VIP
            if not process_vip_license():
                print_status("Không thể kích hoạt VIP", 'error', Colors.RED)
                wait_enter()
                return
        else:
            # Cần key FREE
            print_box("TÀI KHOẢN FREE", [
                f"{ICONS['info']} Cần vượt link để lấy key",
                f"{ICONS['diamond']} 4 lượt / key",
                f"{ICONS['lock']} IP Lock"
            ], Colors.YELLOW)
            
            if not process_free_license():
                wait_enter()
                return
    
    # Chạy main.py
    time.sleep(2)
    download_and_run_main(session, user_id)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}{ICONS['exit']} Đã dừng chương trình{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}{ICONS['error']} Lỗi: {str(e)}{Colors.RESET}")
        wait_enter()
