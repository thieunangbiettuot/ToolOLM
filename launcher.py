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
import random
import requests
import re
import pickle
import tempfile
import hashlib
import uuid
import platform
import base64
import string
from datetime import datetime
from urllib.parse import quote

# ========== CẤU HÌNH MÀU SẮC VÀ KÝ TỰ ĐẶC BIỆT ==========
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

ICONS = {
    'success': '✅',
    'error': '❌',
    'warning': '⚠️',
    'info': 'ℹ️',
    'question': '❓',
    'lock': '🔐',
    'user': '👤',
    'key': '🔑',
    'book': '📚',
    'video': '🎬',
    'theory': '📖',
    'exercise': '📝',
    'search': '🔍',
    'clock': '⏰',
    'star': '⭐',
    'fire': '🔥',
    'rocket': '🚀',
    'check': '✔️',
    'setting': '⚙️',
    'home': '🏠',
    'exit': '🚪',
    'refresh': '🔄',
    'download': '📥',
    'upload': '📤',
    'link': '🔗',
    'list': '📋',
    'magic': '✨',
    'brain': '🧠',
    'back': '↩️'
}

# ========== TIỆN ÍCH HIỂN THỊ ==========
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_centered(text, color=Colors.WHITE, width=60):
    padding = (width - len(text.strip())) // 2
    print(f"{color}{' ' * padding}{text}{Colors.END}")

def print_line(char='═', color=Colors.CYAN, width=60):
    print(f"{color}{char * width}{Colors.END}")

def print_header(title=""):
    clear_screen()
    print_line('═', Colors.BLUE, 60)
    print_centered("🎯 OLM MASTER PRO - LAUNCHER 🎯", Colors.BLUE + Colors.BOLD, 60)
    print_centered("Premium Auto Solver Tool", Colors.PURPLE, 60)
    if title:
        print_line('─', Colors.CYAN, 60)
        print_centered(title, Colors.CYAN, 60)
    print_line('═', Colors.BLUE, 60)
    print()

def print_menu(title, options):
    print(f"\n{Colors.CYAN}{ICONS['setting']} {title}{Colors.END}")
    print_line('─', Colors.CYAN, 45)
    for key, value in options.items():
        print(f"  {Colors.YELLOW}{key}.{Colors.END} {value}")
    print_line('─', Colors.CYAN, 45)

def wait_enter(prompt="Press Enter to continue..."):
    input(f"\n{Colors.YELLOW}{prompt}{Colors.END}")

def print_status(message, icon='info', color=Colors.WHITE):
    print(f"{ICONS.get(icon, '')} {color}{message}{Colors.END}")

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
SECRET_KEY = "OLM_MASTER_PRO_SECRET_2024"

def encrypt_data(data):
    try:
        json_data = json.dumps(data).encode()
        xor_data = bytes(a ^ ord(SECRET_KEY[i % len(SECRET_KEY)]) for i, a in enumerate(json_data))
        encoded = base64.b85encode(xor_data).decode()
        checksum = hashlib.sha256(encoded.encode()).hexdigest()[:12]
        noise_prefix = ''.join(random.choices(string.ascii_letters, k=8))
        noise_suffix = ''.join(reversed(noise_prefix))
        return f"{noise_prefix}{checksum}{encoded}{noise_suffix}"
    except:
        return None

def decrypt_data(encrypted_str):
    try:
        if not encrypted_str or len(encrypted_str) < 36:
            return None
        encoded = encrypted_str[20:-8]
        decoded_bytes = base64.b85decode(encoded)
        decrypted = bytes(a ^ ord(SECRET_KEY[i % len(SECRET_KEY)]) for i, a in enumerate(decoded_bytes))
        return json.loads(decrypted.decode())
    except:
        return None

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
            
            expire_date = datetime.strptime(data['expire'], "%d/%m/%Y").date()
            if expire_date < datetime.now().date():
                return None
            
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
        if encrypted:
            with open(paths['license'], 'w', encoding='utf-8') as f:
                f.write(encrypted)
            return True
    except:
        pass
    return False

def get_public_ip():
    try:
        response = requests.get('https://httpbin.org/ip', timeout=5)
        return response.json()['origin'].split(',')[0].strip()
    except:
        return '127.0.0.1'

# ========== LINK4M INTEGRATION ==========
API_TOKEN = "698b226d9150d31d216157a5"
LINK4M_BASE = "https://link4m.co/api-shorten/v2"

def shorten_url(destination_url):
    """Shorten URL using Link4m API"""
    try:
        encoded_url = quote(destination_url)
        api_url = f"{LINK4M_BASE}?api={API_TOKEN}&url={encoded_url}"
        response = requests.get(api_url, timeout=10)
        if response.status_code == 200:
            result = response.json()
            if result.get("status") == "success":
                return result.get("shortenedUrl")
    except:
        pass
    return None

def generate_and_shorten_key():
    """Generate key and create shortened link"""
    # Generate key
    now = datetime.now()
    device_id = hashlib.md5(f"{uuid.getnode()}".encode()).hexdigest()[:16]
    unique_str = f"{device_id}{now.microsecond}{random.randint(1000, 9999)}"
    hash_val = hashlib.sha256(unique_str.encode()).hexdigest()
    key = f"OLMFREE-{now.strftime('%d%m')}-{hash_val[:4].upper()}-{hash_val[4:8].upper()}"
    
    # Create verification URL (you can customize this)
    verification_url = f"https://verify-key.com/check?key={key}"
    short_link = shorten_url(verification_url)
    
    return key, short_link

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
        if encrypted:
            with open(paths['accounts'], 'w', encoding='utf-8') as f:
                f.write(encrypted)
            return True
    except:
        pass
    return False

def select_saved_account():
    accounts = load_saved_accounts()
    if not accounts:
        return None, None
    
    print(f"\n{Colors.CYAN}{ICONS['user']} SAVED ACCOUNTS:{Colors.END}")
    print_line('─', Colors.CYAN, 45)
    
    account_list = list(accounts.items())
    for idx, (name, data) in enumerate(account_list, 1):
        saved_time = data.get('saved_at', '')
        print(f"  {Colors.YELLOW}{idx}.{Colors.END} {name} {Colors.CYAN}({saved_time}){Colors.END}")
    
    print(f"  {Colors.YELLOW}0.{Colors.END} New Login")
    print_line('─', Colors.CYAN, 45)
    
    choice = input(f"{Colors.YELLOW}Select account (0-{len(account_list)}): {Colors.END}").strip()
    
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
    
    if save_accounts(accounts):
        print_status(f"Account saved: {name}", 'success', Colors.GREEN)
        return True
    else:
        print_status("Failed to save account", 'error', Colors.RED)
        return False

# ========== VIP CHECK ==========
def check_vip(username):
    try:
        url = "https://raw.githubusercontent.com/thieunangbiettuot/ToolOLM/refs/heads/main/vip_users.txt"
        response = requests.get(url, timeout=10)
        if response.status_code == 200 and username.lower() in response.text.lower():
            return True
    except:
        pass
    return False

# ========== LOGIN FUNCTIONS ==========
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'vi-VN,vi;q=0.9,en-US;q=0.8',
    'x-requested-with': 'XMLHttpRequest',
    'origin': 'https://olm.vn',
    'referer': 'https://olm.vn/'
}

def login_olm():
    print_header("OLM LOGIN")
    
    saved_username, saved_password = select_saved_account()
    
    if saved_username and saved_password:
        use_saved = input(f"{Colors.YELLOW}Use saved account? (y/n): {Colors.END}").strip().lower()
        if use_saved == 'y':
            username = saved_username
            password = saved_password
            print_status("Logging in with saved account...", 'user', Colors.GREEN)
        else:
            username = input(f"{ICONS['user']} {Colors.YELLOW}Username: {Colors.END}").strip()
            password = input(f"{ICONS['key']} {Colors.YELLOW}Password: {Colors.END}").strip()
    else:
        username = input(f"{ICONS['user']} {Colors.YELLOW}Username: {Colors.END}").strip()
        password = input(f"{ICONS['key']} {Colors.YELLOW}Password: {Colors.END}").strip()
    
    if not username or not password:
        print_status("Username and password required!", 'error', Colors.RED)
        wait_enter()
        return None, None, None
    
    session = requests.Session()
    session.headers.update(HEADERS)
    
    try:
        print_status("Authenticating...", 'clock', Colors.YELLOW)
        
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
            print_status(f"LOGIN SUCCESSFUL!", 'success', Colors.GREEN + Colors.BOLD)
            print_status(f"User: {user_name}", 'user', Colors.CYAN)
            
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
            
            if not saved_username or saved_username != username:
                save_choice = input(f"\n{Colors.YELLOW}Save this account? (y/n): {Colors.END}").strip().lower()
                if save_choice == 'y':
                    save_current_account(user_name, username, password)
            
            wait_enter()
            return session, user_id, user_name
            
        else:
            print_status("LOGIN FAILED!", 'error', Colors.RED)
            print_status("Invalid username or password", 'error', Colors.RED)
            wait_enter()
            return None, None, None
            
    except Exception as e:
        print_status(f"Login error: {str(e)}", 'error', Colors.RED)
        wait_enter()
        return None, None, None

# ========== MAIN FUNCTION ==========
def main():
    print_header("OLM MASTER PRO LAUNCHER")
    
    license_data = load_license()
    if license_data:
        print_status("Checking license...", 'info', Colors.YELLOW)
        time.sleep(1)
        
        remain = license_data.get('remain', 0)
        expire = license_data.get('expire')
        mode = license_data.get('mode')
        
        if remain > 0 and datetime.strptime(expire, "%d/%m/%Y").date() >= datetime.now().date():
            if mode == 'FREE':
                current_ip = get_public_ip()
                if license_data.get('ip') != current_ip:
                    print_status("IP changed - new key required", 'warning', Colors.YELLOW)
                    license_data = None
            print_status(f"Found {mode} license with {remain} uses", 'success', Colors.GREEN)
        else:
            print_status("License expired or used up", 'warning', Colors.YELLOW)
            license_data = None
    
    if not license_data:
        saved_username, saved_password = select_saved_account()
        session, user_id, user_name = login_olm()
        if not session:
            print_status("Login failed!", 'error', Colors.RED)
            return
        
        print_status("Checking VIP status...", 'info', Colors.YELLOW)
        is_vip = check_vip(user_name)
        
        if is_vip:
            print_status("VIP Account - Unlimited Access", 'success', Colors.GREEN + Colors.BOLD)
            save_license('VIP', '31/12/2099', remain=-1)
            license_data = {'mode': 'VIP', 'remain': -1}
        else:
            print_status("FREE Account - Key Required", 'warning', Colors.YELLOW)
            
            # Generate key and create link
            free_key, short_link = generate_and_shorten_key()
            
            if short_link:
                print(f"\n{Colors.CYAN}🔑 YOUR ACCESS LINK:{Colors.END}")
                print(f"{Colors.YELLOW}{short_link}{Colors.END}")
                print(f"{Colors.RED}Note: Key expires in 1 day with 4 uses{Colors.END}")
                
                # Show key for manual entry (fallback)
                print(f"\n{Colors.PURPLE}Backup Key (if link fails):{Colors.END}")
                print(f"{Colors.WHITE}{free_key}{Colors.END}")
                
                user_input = input(f"\n{Colors.YELLOW}Enter the key you received: {Colors.END}").strip()
                if user_input == free_key:
                    save_license('FREE', datetime.now().strftime("%d/%m/%Y"), get_public_ip(), 4)
                    license_data = {'mode': 'FREE', 'remain': 4}
                    print_status("Key verified - Starting tool!", 'success', Colors.GREEN)
                else:
                    print_status("Invalid key!", 'error', Colors.RED)
                    return
            else:
                print_status("Failed to generate link - using direct key", 'error', Colors.RED)
                print(f"\n{Colors.CYAN}YOUR KEY:{Colors.END}")
                print(f"{Colors.YELLOW}{free_key}{Colors.END}")
                
                user_input = input(f"\n{Colors.YELLOW}Enter key: {Colors.END}").strip()
                if user_input == free_key:
                    save_license('FREE', datetime.now().strftime("%d/%m/%Y"), get_public_ip(), 4)
                    license_data = {'mode': 'FREE', 'remain': 4}
                    print_status("Key accepted!", 'success', Colors.GREEN)
                else:
                    print_status("Invalid key!", 'error', Colors.RED)
                    return
    
    # Save session and run main.py
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
        
        print_status("Downloading main.py from GitHub...", 'download', Colors.CYAN)
        
        main_url = "https://github.com/thieunangbiettuot/ToolOLM/raw/refs/heads/main/main.py"
        main_file = os.path.join(temp_dir, 'main.py')
        
        try:
            response = requests.get(main_url, timeout=15)
            if response.status_code == 200:
                with open(main_file, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                
                print_status("Launching main.py...", 'rocket', Colors.GREEN)
                time.sleep(2)
                
                os.system(f'{sys.executable} "{main_file}" "{session_file}"')
                
            else:
                print_status("Failed to download main.py!", 'error', Colors.RED)
        except Exception as e:
            print_status(f"Download error: {str(e)}", 'error', Colors.RED)
            
    except Exception as e:
        print_status(f"Session save error: {str(e)}", 'error', Colors.RED)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{ICONS['exit']} {Colors.YELLOW}Program terminated{Colors.END}")
    except Exception as e:
        print(f"\n{ICONS['error']} {Colors.RED}Unexpected error: {str(e)}{Colors.END}")
