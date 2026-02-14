#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║              OLM MASTER PRO V1.0 - LAUNCHER                  ║
║                 🚀 Professional Edition 🚀                   ║
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
    print("🔧 Đang cài đặt thư viện...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "beautifulsoup4", "--quiet"])
    import requests
    from bs4 import BeautifulSoup

import re

# ==================== CẤU HÌNH ====================
GITHUB_MAIN_URL = "https://github.com/thieunangbiettuot/ToolOLM/raw/refs/heads/main/main.py"
GITHUB_VIP_URL = "https://raw.githubusercontent.com/thieunangbiettuot/ToolOLM/refs/heads/main/vip_users.txt"

LINK_SERVICES = [
    {"name": "link4m_1", "api": "https://link4m.co/api-shorten/v2", "token": "67e4dc9b4d2e04d44dc3be8f02f2c72b9e67a4b9"},
    {"name": "link4m_2", "api": "https://link4m.co/api-shorten/v2", "token": "backup_token_here"},
]

SECRET_KEY = b"OLM_MASTER_PRO_V1_SECURE_2026"

# ==================== BEAUTIFUL COLORS ====================
class C:
    # Basic colors
    R = '\033[91m'      # Red
    G = '\033[92m'      # Green
    Y = '\033[93m'      # Yellow
    B = '\033[94m'      # Blue
    M = '\033[95m'      # Magenta
    C = '\033[96m'      # Cyan
    W = '\033[97m'      # White
    
    # Bright colors
    BR = '\033[91;1m'   # Bright Red
    BG = '\033[92;1m'   # Bright Green
    BY = '\033[93;1m'   # Bright Yellow
    BB = '\033[94;1m'   # Bright Blue
    BM = '\033[95;1m'   # Bright Magenta
    BC = '\033[96;1m'   # Bright Cyan
    BW = '\033[97;1m'   # Bright White
    
    # Backgrounds
    BGB = '\033[44m'    # Blue background
    BGG = '\033[42m'    # Green background
    BGY = '\033[43m'    # Yellow background
    BGR = '\033[41m'    # Red background
    
    # Styles
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDER = '\033[4m'
    BLINK = '\033[5m'
    
    # Reset
    E = '\033[0m'

# ==================== BEAUTIFUL ICONS ====================
I = {
    'rocket': '🚀', 'fire': '🔥', 'star': '⭐', 'gem': '💎', 'crown': '👑',
    'check': '✅', 'cross': '❌', 'warn': '⚠️', 'info': 'ℹ️', 'question': '❓',
    'user': '👤', 'key': '🔑', 'lock': '🔐', 'unlock': '🔓',
    'heart': '❤️', 'sparkle': '✨', 'zap': '⚡', 'boom': '💥',
    'clock': '⏰', 'hourglass': '⏳', 'calendar': '📅',
    'link': '🔗', 'chain': '⛓️', 'shield': '🛡️', 'trophy': '🏆',
    'target': '🎯', 'dart': '🎲', 'magic': '🪄', 'crystal': '🔮',
    'scroll': '📜', 'book': '📚', 'pen': '✒️', 'brush': '🖌️',
    'upload': '📤', 'download': '📥', 'inbox': '📨', 'outbox': '📬',
    'bell': '🔔', 'loudspeaker': '📢', 'megaphone': '📣',
    'globe': '🌐', 'satellite': '🛰️', 'antenna': '📡',
    'laptop': '💻', 'desktop': '🖥️', 'phone': '📱', 'tablet': '📲',
    'gear': '⚙️', 'wrench': '🔧', 'hammer': '🔨', 'tool': '🛠️',
    'magnify': '🔍', 'microscope': '🔬', 'telescope': '🔭',
    'chart': '📊', 'graph': '📈', 'meter': '📉',
    'folder': '📁', 'file': '📄', 'page': '📃', 'doc': '📝',
    'art': '🎨', 'palette': '🎭', 'music': '🎵', 'note': '🎶',
    'movie': '🎬', 'camera': '📷', 'video': '📹',
    'bulb': '💡', 'candle': '🕯️', 'flashlight': '🔦',
    'battery': '🔋', 'plug': '🔌', 'power': '⚡',
    'sun': '☀️', 'moon': '🌙', 'cloud': '☁️', 'rain': '🌧️',
    'snow': '❄️', 'wind': '💨', 'rainbow': '🌈',
    'tree': '🌲', 'flower': '🌸', 'rose': '🌹', 'leaf': '🍃',
    'gift': '🎁', 'balloon': '🎈', 'party': '🎉', 'confetti': '🎊',
    'medal': '🏅', 'award': '🥇', 'flag': '🚩',
    'up': '⬆️', 'down': '⬇️', 'left': '⬅️', 'right': '➡️',
    'yes': '👍', 'no': '👎', 'ok': '👌', 'peace': '✌️',
    'wave': '👋', 'clap': '👏', 'pray': '🙏',
    'eye': '👁️', 'eyes': '👀', 'ear': '👂',
    'brain': '🧠', 'muscle': '💪', 'bone': '🦴',
    'pizza': '🍕', 'burger': '🍔', 'coffee': '☕', 'beer': '🍺',
    'money': '💰', 'coin': '🪙', 'dollar': '💵', 'yen': '💴',
    'home': '🏠', 'building': '🏢', 'school': '🏫', 'hospital': '🏥',
    'car': '🚗', 'bus': '🚌', 'train': '🚆', 'plane': '✈️',
    'ship': '🚢', 'boat': '⛵', 'anchor': '⚓',
}

# ==================== CROSS-PLATFORM PATHS ====================
def get_device_hash():
    hostname = platform.node()
    mac = uuid.getnode()
    unique_str = f"{hostname}{mac}".encode()
    return hashlib.md5(unique_str).hexdigest()[:8]

def get_app_data_dir():
    system = platform.system()
    device_hash = get_device_hash()
    
    if system == "Windows":
        base = os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Microsoft', 'Windows', 'INetCache', 'IE')
    elif system == "Darwin":
        base = os.path.expanduser('~/Library/Application Support/com.apple.Safari')
    elif 'ANDROID_ROOT' in os.environ or 'TERMUX_VERSION' in os.environ:
        base = os.path.expanduser('~/.cache/google-chrome')
    else:
        base = os.path.expanduser('~/.cache/mozilla/firefox')
    
    os.makedirs(base, exist_ok=True)
    
    return {
        'license': os.path.join(base, f'.{device_hash}sc'),
        'session': os.path.join(base, f'.{device_hash}ss'),
        'accounts': os.path.join(base, f'.{device_hash}ac'),
        'lock': os.path.join(base, f'.{device_hash}lk')
    }

PATHS = get_app_data_dir()

# ==================== ENCRYPTION ====================
def xor_encrypt(data, key):
    key_len = len(key)
    return bytes([data[i] ^ key[i % key_len] for i in range(len(data))])

def encrypt_data(data_dict):
    try:
        json_str = json.dumps(data_dict, separators=(',', ':'))
        json_bytes = json_str.encode('utf-8')
        encrypted = xor_encrypt(json_bytes, SECRET_KEY)
        b85_data = base64.b85encode(encrypted).decode('ascii')
        checksum = hashlib.sha256(b85_data.encode()).hexdigest()[:12]
        noise = hashlib.md5(str(time.time()).encode()).hexdigest()
        noise_prefix = noise[:8]
        noise_suffix = noise[-8:][::-1]
        result = f"{noise_prefix}{checksum}{b85_data}{noise_suffix}"
        return result
    except:
        return None

def decrypt_data(encrypted_str):
    try:
        if not encrypted_str or len(encrypted_str) < 28:
            return None
        data_part = encrypted_str[8:-8]
        checksum_received = data_part[:12]
        b85_data = data_part[12:]
        checksum_calculated = hashlib.sha256(b85_data.encode()).hexdigest()[:12]
        if checksum_received != checksum_calculated:
            return None
        encrypted = base64.b85decode(b85_data.encode('ascii'))
        decrypted = xor_encrypt(encrypted, SECRET_KEY)
        json_str = decrypted.decode('utf-8')
        data_dict = json.loads(json_str)
        return data_dict
    except:
        return None

def save_file(filepath, data_dict):
    encrypted = encrypt_data(data_dict)
    if encrypted:
        with open(filepath, 'w') as f:
            f.write(encrypted)
        return True
    return False

def load_file(filepath):
    if not os.path.exists(filepath):
        return None
    try:
        with open(filepath, 'r') as f:
            encrypted = f.read()
        return decrypt_data(encrypted)
    except:
        return None

# ==================== BEAUTIFUL UI ====================
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    print('\033[2J\033[H', end='')

def box(text, width=70, color=C.C, border='═', corners='╔╗╚╝'):
    lines = text.split('\n')
    print(f"{color}{corners[0]}{border * (width-2)}{corners[1]}{C.E}")
    for line in lines:
        padding = width - len(line) - 4
        print(f"{color}║ {C.E}{line}{' ' * padding}{color} ║{C.E}")
    print(f"{color}{corners[2]}{border * (width-2)}{corners[3]}{C.E}")

def gradient_text(text, colors):
    result = ""
    step = len(text) / len(colors)
    for i, char in enumerate(text):
        color_idx = min(int(i / step), len(colors) - 1)
        result += f"{colors[color_idx]}{char}"
    return result + C.E

def header(title=""):
    clear()
    
    # Animated banner
    banner = f"{I['rocket']} OLM MASTER PRO V1.0 {I['fire']}"
    colors = [C.BR, C.BY, C.BG, C.BC, C.BB, C.BM]
    
    print(f"\n{C.BB}{'═' * 72}{C.E}")
    print(gradient_text(f"{'█' * 72}", colors))
    print(f"{C.BW}{banner:^72}{C.E}")
    print(gradient_text(f"{'█' * 72}", colors[::-1]))
    print(f"{C.BB}{'═' * 72}{C.E}")
    
    if title:
        print(f"\n{C.BC}{'▬' * 72}{C.E}")
        print(f"{C.BY}{I['sparkle']} {title:^67} {I['sparkle']}{C.E}")
        print(f"{C.BC}{'▬' * 72}{C.E}")
    
    print()

def status(msg, icon='info', color=C.W):
    icons = {
        'success': (I['check'], C.BG),
        'error': (I['cross'], C.BR),
        'warn': (I['warn'], C.BY),
        'info': (I['info'], C.BC),
        'load': (I['hourglass'], C.BY),
        'vip': (I['crown'], C.BM),
        'gem': (I['gem'], C.BM),
    }
    
    icon_char, icon_color = icons.get(icon, (I['info'], C.W))
    print(f"{icon_color}{icon_char} {color}{msg}{C.E}")

def progress_bar(current, total, width=50, msg=""):
    percent = int((current / total) * 100)
    filled = int((current / total) * width)
    bar = '█' * filled + '░' * (width - filled)
    
    print(f"\r{C.BC}[{C.BG}{bar}{C.BC}] {C.BY}{percent}%{C.E} {C.W}{msg}{C.E}", end='', flush=True)
    
    if current == total:
        print()

def fancy_input(prompt, color=C.BY):
    return input(f"{color}{I['pen']} {prompt}{C.E}").strip()

def menu(title, options, width=60):
    print(f"\n{C.BC}┌{'─' * (width-2)}┐{C.E}")
    print(f"{C.BC}│ {C.BW}{I['gear']} {title:<{width-6}} {C.BC}│{C.E}")
    print(f"{C.BC}├{'─' * (width-2)}┤{C.E}")
    
    for key, value in options.items():
        print(f"{C.BC}│ {C.BY}[{key}]{C.E} {value:<{width-8}} {C.BC}│{C.E}")
    
    print(f"{C.BC}└{'─' * (width-2)}┘{C.E}")

def wait(prompt="Nhấn Enter để tiếp tục..."):
    input(f"\n{C.BY}{I['hand']} {prompt}{C.E}")

def loading_animation(duration=2, msg="Đang xử lý"):
    frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    end_time = time.time() + duration
    
    while time.time() < end_time:
        for frame in frames:
            print(f"\r{C.BC}{frame} {C.W}{msg}...{C.E}", end='', flush=True)
            time.sleep(0.1)
            if time.time() >= end_time:
                break
    
    print(f"\r{C.BG}{I['check']} {msg} hoàn tất!{C.E}" + " " * 20)

# ==================== VIP CHECK ====================
def check_vip_status(username):
    try:
        response = requests.get(GITHUB_VIP_URL, timeout=10)
        if response.status_code == 200:
            vip_list = response.text.lower().split('\n')
            vip_users = [line.strip() for line in vip_list 
                        if line.strip() and not line.strip().startswith('#')]
            return username.lower() in vip_users
    except:
        pass
    return False

# ==================== ACCOUNT MANAGEMENT ====================
def load_accounts():
    data = load_file(PATHS['accounts'])
    return data if data else {}

def save_accounts(accounts_dict):
    return save_file(PATHS['accounts'], accounts_dict)

def select_account():
    accounts = load_accounts()
    
    if accounts:
        print(f"\n{C.BC}┌{'─' * 68}┐{C.E}")
        print(f"{C.BC}│ {C.BM}{I['user']} TÀI KHOẢN ĐÃ LƯU{' ' * 49} {C.BC}│{C.E}")
        print(f"{C.BC}├{'─' * 68}┤{C.E}")
        
        acc_list = list(accounts.items())
        for idx, (name, data) in enumerate(acc_list, 1):
            saved_at = data.get('saved_at', '')
            print(f"{C.BC}│ {C.BY}[{idx}]{C.E} {name:<30} {C.DIM}{saved_at:<28}{C.E} {C.BC}│{C.E}")
        
        print(f"{C.BC}│ {C.BY}[0]{C.E} {C.BG}Đăng nhập mới{' ' * 51}{C.BC}│{C.E}")
        print(f"{C.BC}└{'─' * 68}┘{C.E}")
        
        choice = fancy_input(f"Chọn (0-{len(acc_list)}): ")
        
        if choice.isdigit():
            idx = int(choice)
            if idx == 0:
                return None, None
            elif 1 <= idx <= len(acc_list):
                name, data = acc_list[idx - 1]
                return data.get('username'), data.get('password')
    
    return None, None

def save_account(name, username, password):
    accounts = load_accounts()
    accounts[name] = {
        'username': username,
        'password': password,
        'saved_at': datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    if save_accounts(accounts):
        status(f"Đã lưu tài khoản: {name}", 'success', C.BG)
        return True
    return False

# ==================== LICENSE ====================
def get_current_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        return response.json()['ip']
    except:
        return "unknown"

def compute_signature(license_data):
    sig_str = f"{license_data.get('mode', '')}{license_data.get('expire', '')}{license_data.get('ip', '')}"
    return hashlib.sha256(sig_str.encode()).hexdigest()[:16]

def load_license():
    data = load_file(PATHS['license'])
    if not data:
        return None
    
    if data.get('sig') != compute_signature(data):
        os.remove(PATHS['license'])
        return None
    
    try:
        expire_date = datetime.strptime(data['expire'], "%d/%m/%Y").date()
        if expire_date < datetime.now().date():
            os.remove(PATHS['license'])
            return None
    except:
        return None
    
    if data.get('mode') == 'FREE':
        if data.get('ip') != get_current_ip():
            status("IP đã thay đổi, cần vượt link mới", 'warn', C.BY)
            os.remove(PATHS['license'])
            return None
    
    if data.get('remain', 0) <= 0:
        os.remove(PATHS['license'])
        if os.path.exists(PATHS['lock']):
            os.remove(PATHS['lock'])
        return None
    
    return data

def save_license(mode, key, expire_days, attempts):
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

# ==================== ACCOUNT LOCK ====================
def get_locked_account():
    data = load_file(PATHS['lock'])
    return data.get('username') if data else None

def set_locked_account(username):
    return save_file(PATHS['lock'], {'username': username})

def clear_locked_account():
    if os.path.exists(PATHS['lock']):
        os.remove(PATHS['lock'])

# ==================== KEY GENERATION ====================
def generate_unique_key():
    now = datetime.now()
    device_id = get_device_hash()
    unique_string = f"{device_id}{now.timestamp()}{random.randint(1000, 9999)}"
    hash_value = hashlib.sha256(unique_string.encode()).hexdigest()
    key = f"OLM-{now:%d%m}-{hash_value[:4].upper()}-{hash_value[4:8].upper()}"
    return key

def shorten_link(long_url):
    for service in LINK_SERVICES:
        try:
            response = requests.post(
                service['api'],
                json={'url': long_url},
                headers={'api-token': service['token'], 'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('status') == 'success':
                    return result.get('shortenedUrl')
        except:
            continue
    return None

def get_free_key():
    max_regenerate = 3
    
    for attempt in range(max_regenerate):
        key = generate_unique_key()
        base_url = "https://olm.vn"
        long_url = f"{base_url}?key={key}"
        
        loading_animation(1, "Đang tạo link rút gọn")
        short_url = shorten_link(long_url)
        
        if not short_url:
            status("Không thể tạo link, thử lại...", 'error', C.BR)
            time.sleep(1)
            continue
        
        # Beautiful link display
        print(f"\n{C.BG}{'═' * 70}{C.E}")
        print(f"{C.BY}{I['zap']} BƯỚC 1: VƯỢT LINK ĐỂ LẤY MÃ{' ' * 38}{C.E}")
        print(f"{C.BG}{'═' * 70}{C.E}")
        print(f"{C.BC}{I['link']} Link:{C.E} {C.BW}{short_url}{C.E}")
        print(f"{C.BG}{'═' * 70}{C.E}\n")
        
        fail_count = 0
        for i in range(3):
            user_input = fancy_input(f"{I['key']} BƯỚC 2 - Nhập mã (hoặc 'r' để tạo link mới): ")
            
            if user_input.lower() == 'r':
                if attempt < max_regenerate - 1:
                    loading_animation(1, "Đang tạo link mới")
                    break
                else:
                    status("Đã hết lượt tạo link mới", 'error', C.BR)
                    return None
            
            if user_input == key:
                status("Xác thực thành công!", 'success', C.BG)
                time.sleep(0.5)
                return key
            
            fail_count += 1
            time.sleep(fail_count)
            
            if i < 2:
                status(f"Sai mã ({2-i} lần còn lại)", 'error', C.BR)
        
        if user_input != key and user_input.lower() != 'r':
            status("Đã hết lượt thử", 'error', C.BR)
            return None
    
    status("Đã hết lượt tạo link", 'error', C.BR)
    return None

# ==================== LOGIN ====================
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'vi-VN,vi;q=0.9',
    'x-requested-with': 'XMLHttpRequest',
    'origin': 'https://olm.vn',
    'referer': 'https://olm.vn/'
}

def login_olm(username, password):
    session = requests.Session()
    session.headers.update(HEADERS)
    
    try:
        loading_animation(1, "Đang kết nối đến OLM")
        
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
        
        loading_animation(1, "Đang xác thực")
        session.post("https://olm.vn/post-login", data=payload, headers=h_login)
        
        check_res = session.get("https://olm.vn/thong-tin-tai-khoan/info", headers=HEADERS)
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
            
            return session, user_id, user_name
        
        return None, None, None
        
    except:
        return None, None, None

# ==================== SESSION ====================
def save_session(session, user_id, user_name):
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

# ==================== MAIN ====================
def main():
    header("LAUNCHER")
    
    # 1. CHỌN TÀI KHOẢN
    saved_username, saved_password = select_account()
    
    if saved_username and saved_password:
        username, password = saved_username, saved_password
        status(f"Sử dụng tài khoản: {saved_username}", 'success', C.BG)
    else:
        print(f"\n{C.BC}┌{'─' * 68}┐{C.E}")
        print(f"{C.BC}│ {C.BM}{I['user']} ĐĂNG NHẬP MỚI{' ' * 50} {C.BC}│{C.E}")
        print(f"{C.BC}└{'─' * 68}┘{C.E}\n")
        
        username = fancy_input(f"{I['user']} Tên đăng nhập: ")
        password = fancy_input(f"{I['key']} Mật khẩu: ")
    
    if not username or not password:
        status("Thông tin không hợp lệ!", 'error', C.BR)
        wait()
        sys.exit(1)
    
    # 2. ĐĂNG NHẬP
    session, user_id, user_name = login_olm(username, password)
    
    if not session:
        status("Đăng nhập thất bại!", 'error', C.BR)
        wait()
        sys.exit(1)
    
    # Success animation
    print(f"\n{C.BG}{'═' * 70}{C.E}")
    print(f"{C.BG}{I['check']} ĐĂNG NHẬP THÀNH CÔNG!{' ' * 45}{C.E}")
    print(f"{C.BC}{I['user']} Xin chào: {C.BW}{user_name}{' ' * (54 - len(user_name))}{C.E}")
    print(f"{C.BG}{'═' * 70}{C.E}\n")
    
    # Hỏi lưu tài khoản
    if not saved_username or saved_username != username:
        save_choice = fancy_input(f"{I['question']} Lưu tài khoản? (y/n): ").lower()
        if save_choice == 'y':
            save_account(user_name, username, password)
    
    # 3. CHECK VIP
    loading_animation(1, "Đang kiểm tra quyền")
    is_vip = check_vip_status(username)
    
    # 4. LICENSE
    existing_license = load_license()
    
    if is_vip:
        # VIP
        print(f"\n{C.BM}{'═' * 70}{C.E}")
        print(f"{C.BM}{I['crown']} CHÀO MỪNG VIP: {user_name}{' ' * (50 - len(user_name))}{C.E}")
        print(f"{C.BM}{I['sparkle']} Quyền: UNLIMITED{' ' * 51}{C.E}")
        print(f"{C.BM}{'═' * 70}{C.E}\n")
        
        save_license('VIP', 'VIP_' + username, 3650, 999999)
        
    elif existing_license and existing_license.get('remain', 0) > 0:
        # CÒN LƯỢT
        remain = existing_license['remain']
        print(f"\n{C.BG}{'═' * 70}{C.E}")
        print(f"{C.BG}{I['gem']} Còn {remain} lượt{' ' * (60 - len(str(remain)))}{C.E}")
        print(f"{C.BG}{'═' * 70}{C.E}\n")
        
        locked_acc = get_locked_account()
        if locked_acc and locked_acc != username:
            status(f"Key đang được sử dụng bởi: {locked_acc}", 'warn', C.BY)
            status("Tiếp tục sẽ chuyển sang tài khoản mới", 'info', C.BC)
        
        set_locked_account(username)
        
    else:
        # FREE
        print(f"\n{C.BC}{'═' * 70}{C.E}")
        print(f"{C.BC}{I['info']} Tài khoản FREE (4 lượt/ngày){' ' * 39}{C.E}")
        print(f"{C.BC}{'═' * 70}{C.E}\n")
        
        key = get_free_key()
        
        if not key:
            status("Không thể lấy key!", 'error', C.BR)
            wait()
            sys.exit(1)
        
        save_license('FREE', key, 1, 4)
        set_locked_account(username)
        
        print(f"\n{C.BG}{'═' * 70}{C.E}")
        print(f"{C.BG}{I['check']} Đã kích hoạt 4 lượt!{' ' * 47}{C.E}")
        print(f"{C.BG}{'═' * 70}{C.E}\n")
    
    # 5. LƯU SESSION
    if not save_session(session, user_id, user_name):
        status("Lỗi lưu session!", 'error', C.BR)
        wait()
        sys.exit(1)
    
    # 6. DOWNLOAD MAIN.PY
    loading_animation(2, "Đang tải main.py từ GitHub")
    
    try:
        response = requests.get(GITHUB_MAIN_URL, timeout=15)
        if response.status_code == 200:
            temp_dir = tempfile.gettempdir()
            main_path = os.path.join(temp_dir, f'olm_main_{get_device_hash()}.py')
            
            with open(main_path, 'wb') as f:
                f.write(response.content)
            
            print(f"\n{C.BG}{'═' * 70}{C.E}")
            print(f"{C.BG}{I['rocket']} KHỞI ĐỘNG TOOL...{' ' * 47}{C.E}")
            print(f"{C.BG}{'═' * 70}{C.E}\n")
            
            time.sleep(1)
            
            # 7. CHẠY
            subprocess.run([sys.executable, main_path])
            
            try:
                os.remove(main_path)
            except:
                pass
            
        else:
            status("Không thể tải main.py!", 'error', C.BR)
            wait()
            sys.exit(1)
            
    except Exception as e:
        status(f"Lỗi: {str(e)}", 'error', C.BR)
        wait()
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{I['wave']} {C.BY}Đã dừng{C.E}")
        sys.exit(0)
    except Exception as e:
        status(f"Lỗi: {str(e)}", 'error', C.BR)
        wait()
        sys.exit(1)
