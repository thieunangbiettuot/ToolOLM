#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║                    OLM MASTER - AUTO SOLVER                  ║
║                    Created by: Tuấn Anh                      ║
║                    VIP Edition - v2.0                       ║
╚══════════════════════════════════════════════════════════════╝
"""

import os
import sys
import time
import json
import random
import requests
import re
import socket
import uuid
import hashlib
import base64
from bs4 import BeautifulSoup
from datetime import datetime

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
    GRAY = '\033[90m'

# Ký tự icon
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
    'back': '↩️',
    'vip': '👑',
    'help': '❓'
}

# ========== TIỆN ÍCH HIỂN THỊ ==========
def clear_screen():
    """Xóa màn hình"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_centered(text, color=Colors.WHITE, width=60):
    """In text căn giữa"""
    padding = (width - len(text.strip())) // 2
    print(f"{color}{' ' * padding}{text}{Colors.END}")

def print_line(char='═', color=Colors.CYAN, width=60):
    """In đường kẻ"""
    print(f"{color}{char * width}{Colors.END}")

def print_header(title=""):
    """In header tool"""
    clear_screen()
    print_line('═', Colors.BLUE, 60)
    print_centered(f"{ICONS['rocket']} OLM MASTER - AUTO SOLVER {ICONS['fire']}", Colors.BLUE + Colors.BOLD, 60)
    print_centered("Created by: Tuấn Anh", Colors.PURPLE, 60)
    if title:
        print_line('─', Colors.CYAN, 60)
        print_centered(title, Colors.CYAN, 60)
    print_line('═', Colors.BLUE, 60)
    print()

def print_menu(title, options):
    """In menu"""
    print(f"\n{Colors.CYAN}{ICONS['setting']} {title}{Colors.END}")
    print_line('─', Colors.CYAN, 40)
    for key, value in options.items():
        print(f"  {Colors.YELLOW}{key}.{Colors.END} {value}")
    print_line('─', Colors.CYAN, 40)

def wait_enter(prompt="Nhấn Enter để tiếp tục..."):
    """Chờ nhấn Enter"""
    input(f"\n{Colors.YELLOW}{prompt}{Colors.END}")

def print_status(message, icon='info', color=Colors.WHITE):
    """In thông báo trạng thái"""
    print(f"{ICONS.get(icon, '')} {color}{message}{Colors.END}")

def print_tutorial():
    """In hướng dẫn chi tiết"""
    clear_screen()
    print_line('═', Colors.PURPLE, 60)
    print_centered(f"{ICONS['help']} HƯỚNG DẪN SỬ DỤNG {ICONS['help']}", Colors.PURPLE + Colors.BOLD, 60)
    print_line('═', Colors.PURPLE, 60)
    print()
    
    print(f"{Colors.YELLOW}1. TÀI KHOẢN VIP{Colors.END}")
    print(f"  • Kiểm tra tự động từ file GitHub: {Colors.CYAN}https://raw.githubusercontent.com/thieunangbiettuot/ToolOLM/main/vip_users.txt{Colors.END}")
    print(f"  • Tài khoản VIP: {Colors.GREEN}KHÔNG GIỚI HẠN LƯỢT{Colors.END}")
    print(f"  • Dấu hiệu: Hiển thị {ICONS['vip']} {Colors.GREEN}Tài khoản VIP - Không giới hạn lượt sử dụng{Colors.END}")
    
    print(f"\n{Colors.YELLOW}2. TÀI KHOẢN FREE{Colors.END}")
    print(f"  • Số lượt: {Colors.YELLOW}4 lượt/ngày{Colors.END} (tính từ lúc tạo key)")
    print(f"  • Khi hết lượt: {Colors.RED}Vào lại tool và lấy key mới{Colors.END}")
    print(f"  • IP thay đổi: Phải lấy key mới")
    
    print(f"\n{Colors.YELLOW}3. LÀM BÀI TẬP{Colors.END}")
    print(f"  • Chọn bài: {Colors.CYAN}0{Colors.END} (tất cả) hoặc {Colors.CYAN}1,2,3{Colors.END} (nhiều bài)")
    print(f"  • Làm xong: {Colors.GREEN}Số lượt tự động trừ{Colors.END}")
    print(f"  • Khi hết lượt: {Colors.RED}Tự động quay lại tạo key mới{Colors.END}")
    
    print(f"\n{Colors.YELLOW}4. LỖI THƯỜNG GẶP{Colors.END}")
    print(f"  • Lỗi 403: {Colors.GRAY}Bài đã được nộp trước đó{Colors.END}")
    print(f"  • Lỗi link: {Colors.GRAY}Thử lại hoặc đổi IP{Colors.END}")
    print(f"  • Lỗi key: {Colors.GRAY}Vui lòng kiểm tra lại key{Colors.END}")
    
    print()
    print_line('═', Colors.PURPLE, 60)
    wait_enter()

# ========== XỬ LÝ TÀI KHOẢN ==========
def get_appdata_dir():
    """Lấy thư mục lưu dữ liệu theo hệ điều hành"""
    if os.name == 'nt':
        return os.path.join(os.getenv('LOCALAPPDATA', 
                       os.path.expanduser('~/AppData/Local')),
                       'Microsoft', 'Windows', 'INetCache', 'IE')
    elif sys.platform == 'darwin':
        return os.path.expanduser('~/Library/Application Support/com.apple.Safari')
    elif 'ANDROID_ROOT' in os.environ:
        return os.path.expanduser('~/.cache/google-chrome')
    else:  # Linux
        return os.path.expanduser('~/.cache/mozilla/firefox')

def get_device_hash():
    """Tạo hash thiết bị duy nhất"""
    hostname = socket.gethostname()
    mac = uuid.getnode()
    return hashlib.sha256(f"{hostname}{mac}".encode()).hexdigest()[:8]

def get_license_path():
    """Trả về đường dẫn file license"""
    os.makedirs(get_appdata_dir(), exist_ok=True)
    return os.path.join(get_appdata_dir(), f'.{get_device_hash()}sc')

def encrypt_data(data):
    """Mã hóa dữ liệu theo chuẩn bảo mật"""
    json_data = json.dumps(data)
    key = "OLMSECURE2024"  # Secret key (không thay đổi)
    
    # XOR với key
    encrypted = bytes(
        b ^ key[i % len(key)].encode()[0] 
        for i, b in enumerate(json_data.encode())
    )
    
    # Base85 encode
    base85 = base64.b85encode(encrypted).decode()
    
    # Tạo checksum và noise
    checksum = hashlib.sha256(json_data.encode()).hexdigest()[:12]
    noise = hashlib.md5(os.urandom(8)).hexdigest()[:8]
    
    return f"{noise}{checksum}{base85}{noise[::-1]}"

def decrypt_data(encrypted):
    """Giải mã dữ liệu"""
    try:
        # Tách noise, checksum, base85
        noise = encrypted[:8]
        checksum = encrypted[8:20]
        base85 = encrypted[20:-8]
        noise_rev = encrypted[-8:]
        
        if noise[::-1] != noise_rev:
            return None
            
        # Giải mã Base85
        decoded = base64.b85decode(base85)
        key = "OLMSECURE2024"
        
        # XOR ngược
        decrypted = bytes(
            b ^ key[i % len(key)].encode()[0] 
            for i, b in enumerate(decoded)
        )
        
        return json.loads(decrypted.decode())
    except:
        return None

def load_license():
    """Tải license từ file"""
    path = get_license_path()
    if not os.path.exists(path):
        return None
    
    try:
        with open(path, 'r') as f:
            encrypted = f.read()
        
        data = decrypt_data(encrypted)
        if data:
            return data
    except:
        pass
    return None

def save_license(data):
    """Lưu license vào file"""
    path = get_license_path()
    try:
        # Mã hóa và lưu
        encrypted = encrypt_data(data)
        with open(path, 'w') as f:
            f.write(encrypted)
        return True
    except:
        return False

# ========== XỬ LÝ VIP & KEY ==========
def check_vip(user_name):
    """Kiểm tra tài khoản VIP (realtime)"""
    vip_url = "https://raw.githubusercontent.com/thieunangbiettuot/ToolOLM/refs/heads/main/vip_users.txt"
    try:
        response = requests.get(vip_url, timeout=5)
        if response.status_code == 200:
            vip_list = [line.strip() for line in response.text.splitlines() if line.strip()]
            return user_name in vip_list
        else:
            print_status(f"Không thể kiểm tra VIP (HTTP {response.status_code})", 'error', Colors.RED)
    except Exception as e:
        print_status(f"Kết nối lỗi: {str(e)}", 'error', Colors.RED)
    return False

def generate_olm_key():
    """Tạo key với định dạng OLMFREE-DDMM-XXXX-YYYY"""
    now = datetime.now()
    device_id = hashlib.md5(f"{socket.gethostname()}{uuid.getnode()}".encode()).hexdigest()[:16]
    unique_str = f"{device_id}{now.timestamp()}{random.randint(1000, 9999)}"
    hash_val = hashlib.sha256(unique_str.encode()).hexdigest()
    return f"OLMFREE-{now:%d%m}-{hash_val[:4].upper()}-{hash_val[4:8].upper()}"

LINK_SERVICES = [
    {"api": "https://link4m.co/api-shorten/v2", "token": "698b226d9150d31d216157a5"},
    {"api": "https://link4m.co/api-shorten/v2", "token": "698b226d9150d31d216157a5"},
]

def create_short_link(url):
    """Tạo link rút gọn qua link4m (nhiều service)"""
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }
    for service in LINK_SERVICES:
        try:
            # Sử dụng params thay vì nối chuỗi URL
            params = {
                'api': service['token'],
                'url': url
            }
            
            response = requests.get(
                service['api'],
                params=params,
                headers=headers,
                timeout=8
            )
            
            if response.status_code != 200:
                continue
                
            data = response.json()
            if data.get("status") == "success":
                return data.get("shortenedUrl")
                
        except Exception as e:
            continue
        time.sleep(random.uniform(0.5, 1.2))
    return None

def get_public_ip():
    """Lấy IP public của người dùng"""
    try:
        return requests.get('https://api.ipify.org', timeout=5).text
    except:
        return "127.0.0.1"

def handle_key_generation():
    """Xử lý tạo key cho tài khoản FREE"""
    key = generate_olm_key()
    # Đổi URL đích theo yêu cầu
    real_url = f"https://keyfreedailyolmvip.blogspot.com/2026/02/blog-post.html?ma={key}"
    
    print(f"\n{Colors.YELLOW}Đang tạo liên kết bảo mật...{Colors.END}")
    
    short_link = create_short_link(real_url)
    
    if not short_link:
        print_status("Không thể tạo link. Vui lòng thử lại.", 'error', Colors.RED)
        return None
    
    print()
    print(Colors.PURPLE + "════════════════════════════════════" + Colors.END)
    print(Colors.CYAN + "🔗 LIÊN KẾT XÁC THỰC:" + Colors.END)
    print(Colors.BOLD + short_link + Colors.END)
    print(Colors.PURPLE + "════════════════════════════════════" + Colors.END)
    print()
    
    user_key = input(f"{Colors.YELLOW}Nhập key: {Colors.END}").strip()
    if user_key != key:
        print_status("Key không hợp lệ!", 'error', Colors.RED)
        return None
    
    return {
        'key': key,
        'remain': 4,
        'expire': datetime.now().strftime("%Y-%m-%d"),
        'ip': get_public_ip()
    }

# ========== QUẢN LÝ TÀI KHOẢN ==========
def load_saved_accounts():
    """Tải danh sách tài khoản đã lưu"""
    if os.path.exists('accounts.json'):
        try:
            with open('accounts.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_accounts(accounts):
    """Lưu danh sách tài khoản"""
    try:
        with open('accounts.json', 'w', encoding='utf-8') as f:
            json.dump(accounts, f, ensure_ascii=False, indent=2)
        return True
    except:
        return False

def select_saved_account():
    """Chọn tài khoản đã lưu"""
    accounts = load_saved_accounts()
    if not accounts:
        return None, None
    
    print(f"\n{Colors.CYAN}{ICONS['user']} TÀI KHOẢN ĐÃ LƯU:{Colors.END}")
    print_line('─', Colors.CYAN, 40)
    
    account_list = list(accounts.items())
    for idx, (name, data) in enumerate(account_list, 1):
        saved_time = data.get('saved_at', '')
        print(f"  {Colors.YELLOW}{idx}.{Colors.END} {name} {Colors.CYAN}({saved_time}){Colors.END}")
    
    print(f"  {Colors.YELLOW}0.{Colors.END} Đăng nhập mới")
    print_line('─', Colors.CYAN, 40)
    
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
    """Lưu tài khoản hiện tại"""
    accounts = load_saved_accounts()
    accounts[name] = {
        'username': username,
        'password': password,
        'saved_at': datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    
    if save_accounts(accounts):
        print_status(f"Đã lưu tài khoản: {name}", 'success', Colors.GREEN)
        return True
    else:
        print_status("Không thể lưu tài khoản", 'error', Colors.RED)
        return False

# ========== PHẦN ĐĂNG NHẬP ==========
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'vi-VN,vi;q=0.9,en-US;q=0.8',
    'x-requested-with': 'XMLHttpRequest',
    'origin': 'https://olm.vn',
    'referer': 'https://olm.vn/'
}

def login_olm():
    """Đăng nhập OLM"""
    print_header("ĐĂNG NHẬP OLM")
    
    # Chọn tài khoản đã lưu
    saved_username, saved_password = select_saved_account()
    
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
        wait_enter()
        return None, None, None
    
    session = requests.Session()
    session.headers.update(HEADERS)
    
    try:
        print_status("Đang đăng nhập...", 'clock', Colors.YELLOW)
        
        # Lấy trang đăng nhập
        session.get("https://olm.vn/dangnhap", headers=HEADERS)
        csrf = session.cookies.get('XSRF-TOKEN')
        
        # Tạo payload đăng nhập
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
        
        # Đăng nhập
        session.post("https://olm.vn/post-login", data=payload, headers=h_login)
        
        # Kiểm tra đăng nhập thành công
        check_res = session.get("https://olm.vn/thong-tin-tai-khoan/info", headers=HEADERS)
        match = re.search(r'name="name".*?value="(.*?)"', check_res.text)
        
        if match and match.group(1).strip() != "":
            user_name = match.group(1).strip()
            print_status(f"ĐĂNG NHẬP THÀNH CÔNG!", 'success', Colors.GREEN + Colors.BOLD)
            print_status(f"Tên người dùng: {user_name}", 'user', Colors.CYAN)
            
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
            
            # Hỏi lưu tài khoản
            if not saved_username or saved_username != username:
                save_choice = input(f"\n{Colors.YELLOW}Lưu tài khoản này? (y/n): {Colors.END}").strip().lower()
                if save_choice == 'y':
                    save_current_account(user_name, username, password)
            
            wait_enter()
            return session, user_id, user_name
            
        else:
            print_status("ĐĂNG NHẬP THẤT BẠI!", 'error', Colors.RED)
            print_status("Sai tên đăng nhập hoặc mật khẩu", 'error', Colors.RED)
            wait_enter()
            return None, None, None
            
    except Exception as e:
        print_status(f"Lỗi đăng nhập: {str(e)}", 'error', Colors.RED)
        wait_enter()
        return None, None, None

# ========== PHẦN QUÉT BÀI TẬP (PHIÊN BẢN ĐÃ SỬA) ==========
def get_assignments_fixed(session, pages_to_scan=5):
    """Lấy danh sách bài tập - BẢN ĐÃ SỬA LỖI"""
    print_header(f"QUÉT BÀI TẬP ({pages_to_scan} trang)")
    
    assignments = []
    seen_links = set()
    
    try:
        for page in range(1, pages_to_scan + 1):
            if page == 1:
                url = "https://olm.vn/lop-hoc-cua-toi?action=login"
            else:
                url = f"https://olm.vn/lop-hoc-cua-toi/page-{page}?action=login"
            
            print_status(f"Đang quét trang {page}/{pages_to_scan}...", 'search', Colors.YELLOW)
            
            try:
                response = session.get(url, headers=HEADERS, timeout=10)
                
                if response.status_code != 200:
                    print_status(f"Lỗi HTTP {response.status_code}", 'error', Colors.RED)
                    continue
                
                soup = BeautifulSoup(response.text, 'html.parser')
                rows = soup.find_all('tr', class_='my-gived-courseware-item')
                
                if not rows: 
                    print_status(f"Trang {page} không có bài tập", 'warning', Colors.YELLOW)
                    continue
                
                page_count = 0
                for row in rows:
                    # Tìm link bài tập chính
                    link_tags = row.find_all('a', class_='olm-text-link')
                    if not link_tags:
                        continue
                    
                    main_link = link_tags[0]
                    href = main_link.get('href')
                    link_text = main_link.get_text(strip=True)
                    
                    # Bỏ qua link parenthetical (môn học)
                    if href and ('(Toán' in link_text or '(Ngữ văn' in link_text or 
                                '(Tiếng Anh' in link_text or '(Tin học' in link_text):
                        continue
                    
                    if not href:
                        continue
                    
                    # Lấy loại bài
                    tds = row.find_all('td')
                    if len(tds) < 2:
                        continue
                    
                    loai_raw = tds[1].get_text(strip=True)
                    
                    # Xác định loại bài
                    is_video = "[Video]" in loai_raw or "Video" in loai_raw
                    is_ly_thuyet = "[Lý thuyết]" in loai_raw or "Ly thuyet" in loai_raw
                    is_kiem_tra = "[Kiểm tra]" in loai_raw or "[Kiem tra]" in loai_raw
                    is_bai_tap = not (is_video or is_ly_thuyet or is_kiem_tra)
                    
                    # BỎ QUA BÀI TỰ LUẬN (không xử lý được)
                    is_tu_luan = "[Tự luận]" in loai_raw or "[Tu luan]" in loai_raw
                    if is_tu_luan:
                        continue
                    
                    # BỎ QUA BÀI KIỂM TRA (theo yêu cầu)
                    if is_kiem_tra:
                        continue
                    
                    # ====== LOGIC KIỂM TRA TRẠNG THÁI ======
                    should_process = False
                    
                    # Tìm span trạng thái (kiểm tra cả trong và ngoài thẻ a)
                    status_spans = []
                    
                    # 1. Tìm trong thẻ a
                    status_spans.extend(main_link.find_all('span', class_='message-static-item'))
                    
                    # 2. Tìm trong hàng
                    if not status_spans:
                        status_spans.extend(row.find_all('span', class_='message-static-item'))
                    
                    # 3. Tìm span có class alert-warning (trạng thái "Chưa nộp")
                    if not status_spans:
                        warning_spans = row.find_all('span', class_='alert-warning')
                        # Chỉ thêm nếu span không phải là môn học
                        for span in warning_spans:
                            span_text = span.get_text(strip=True)
                            if span_text not in ['Hóa học', 'Toán', 'Ngữ văn', 'Tiếng Anh', 'Tin học', 'Lịch sử', 'Địa lý', 'Giáo dục công dân']:
                                status_spans.append(span)
                    
                    # ====== XỬ LÝ KHÁC NHAU CHO TỪNG LOẠI BÀI ======
                    
                    # A. BÀI LUYỆN TẬP THƯỜNG (Video, Lý thuyết, Bài tập)
                    if not is_kiem_tra:
                        # Bài luyện tập LUÔN HIỆN ĐIỂM -> kiểm tra span như bình thường
                        if not status_spans:
                            # KHÔNG CÓ SPAN -> XÉT LÀ CHƯA LÀM
                            should_process = True
                        else:
                            # Có span -> kiểm tra nội dung
                            for span in status_spans:
                                span_text = span.get_text(strip=True).lower()
                                if "chưa" in span_text or "chưa nộp" in span_text or "làm tiếp" in span_text:
                                    should_process = True
                                    break
                                elif "điểm" in span_text and "đúng" in span_text:
                                    # Đã có điểm -> đã làm
                                    should_process = False
                                    break
                                elif "đã xem" in span_text:
                                    # Lý thuyết đã xem -> bỏ qua
                                    should_process = False
                                    break
                    
                    # Xử lý bài tập
                    if should_process and href not in seen_links:
                        seen_links.add(href)
                        
                        # Lấy thông tin bài
                        mon = row.find('span', class_='alert')
                        mon_text = mon.get_text(strip=True) if mon else "Khác"
                        
                        ten_bai = link_text
                        # Làm sạch title
                        ten_bai = re.sub(r'\([^)]*\)', '', ten_bai).strip()
                        
                        # Xác định trạng thái
                        status = "Chưa làm"
                        if status_spans:
                            for span in status_spans:
                                span_text = span.get_text(strip=True)
                                if "chưa" in span_text.lower() or "làm tiếp" in span_text.lower():
                                    status = span_text
                                    break
                        
                        # Xây dựng URL đầy đủ
                        if not href.startswith('http'):
                            full_url = 'https://olm.vn' + href
                        else:
                            full_url = href
                        
                        # Thêm vào danh sách
                        assignments.append({
                            'title': ten_bai[:60],
                            'subject': mon_text[:20],
                            'type': loai_raw.replace('[', '').replace(']', '').strip()[:20],
                            'status': status,
                            'url': full_url,
                            'page': page,
                            'is_video': is_video,
                            'is_ly_thuyet': is_ly_thuyet,
                            'is_bai_tap': is_bai_tap,
                            'is_kiem_tra': is_kiem_tra,
                            'is_tu_luan': is_tu_luan
                        })
                        page_count += 1
                
                if page_count > 0:
                    print_status(f"Trang {page}: {page_count} bài cần làm", 'success', Colors.GREEN)
                else:
                    print_status(f"Trang {page}: không có bài cần làm", 'warning', Colors.YELLOW)
                    
            except Exception as e:
                print_status(f"Lỗi trang {page}: {str(e)}", 'error', Colors.RED)
                continue
        
        # Tổng kết
        if assignments:
            print_status(f"Tổng cộng: {len(assignments)} bài cần xử lý", 'success', Colors.GREEN + Colors.BOLD)
            
            # Thống kê loại bài
            video_count = sum(1 for a in assignments if a['is_video'])
            ly_thuyet_count = sum(1 for a in assignments if a['is_ly_thuyet'])
            bai_tap_count = sum(1 for a in assignments if a['is_bai_tap'])
            
            print(f"\n{Colors.CYAN}📊 THỐNG KÊ LOẠI BÀI:{Colors.END}")
            if video_count > 0:
                print(f"  {ICONS['video']} Video: {video_count} bài")
            if ly_thuyet_count > 0:
                print(f"  {ICONS['theory']} Lý thuyết: {ly_thuyet_count} bài")
            if bai_tap_count > 0:
                print(f"  {ICONS['exercise']} Bài tập: {bai_tap_count} bài")
            
            return assignments
        else:
            print_status("Không tìm thấy bài tập nào cần làm", 'warning', Colors.YELLOW)
            return []
            
    except Exception as e:
        print_status(f"Lỗi khi quét bài tập: {str(e)}", 'error', Colors.RED)
        return []

def display_assignments_table(assignments):
    """Hiển thị danh sách bài tập dạng bảng"""
    if not assignments:
        return
    
    print(f"\n{Colors.PURPLE}{'📚 DANH SÁCH BÀI TẬP CẦN LÀM 📚':^90}{Colors.END}")
    print_line('─', Colors.PURPLE, 90)
    
    for idx, item in enumerate(assignments, 1):
        title = item['title']
        if len(title) > 38:
            title = title[:35] + "..."
        
        # Màu sắc theo loại bài
        if item['is_video']:
            loai_color = Colors.BLUE
            icon = ICONS['video']
        elif item['is_ly_thuyet']:
            loai_color = Colors.CYAN
            icon = ICONS['theory']
        else:
            loai_color = Colors.GREEN
            icon = ICONS['exercise']
        
        # Màu sắc theo trạng thái
        status = item['status']
        if "Chưa làm" in status or "chưa nộp" in status.lower():
            status_color = Colors.RED
        elif "làm tiếp" in status.lower():
            status_color = Colors.YELLOW
        else:
            status_color = Colors.WHITE
        
        print(f"{Colors.YELLOW}{idx:>2}.{Colors.END} ", end="")
        print(f"{icon} ", end="")
        print(f"{loai_color}{item['type']:<10}{Colors.END} ", end="")
        print(f"{Colors.WHITE}{item['subject']:<15}{Colors.END} ", end="")
        print(f"{Colors.WHITE}{title:<40}{Colors.END} ", end="")
        print(f"{status_color}{status:<15}{Colors.END}")
    
    print_line('─', Colors.PURPLE, 90)

# ========== PHẦN XỬ LÝ BÀI TẬP ==========
def get_target_score(is_video=False, is_kiem_tra=False):
    """Menu chọn điểm số"""
    if is_video:
        return 100
    elif is_kiem_tra:
        return random.randint(85, 100)  # Điểm kiểm tra thường cao
    
    return 100

def extract_quiz_info(session, url, is_video=False):
    """Trích xuất thông tin quiz"""
    try:
        resp = session.get(url, timeout=10)
        html = resp.text
        
        # Tìm quiz_list
        quiz_list = None
        
        # Cách 1: Tìm trong script
        pattern1 = r'quiz_list\s*[:=]\s*["\'](\d{6,}(?:,\d{6,})*)["\']'
        match1 = re.search(pattern1, html)
        if match1:
            quiz_list = match1.group(1)
        
        # Cách 2: Tìm pattern số
        if not quiz_list:
            pattern2 = r'\b\d{9,}(?:,\d{9,})+\b'
            matches = re.findall(pattern2, html)
            if matches:
                quiz_list = max(matches, key=len)
        
        # Cách 3: Tìm trong JSON
        if not quiz_list:
            pattern3 = r'"quiz_list"\s*:\s*"(\d+(?:,\d+)*)"'
            match3 = re.search(pattern3, html)
            if match3:
                quiz_list = match3.group(1)
        
        # Tìm id_courseware
        id_courseware = None
        cw_match = re.search(r'id_courseware\s*[:=]\s*["\']?(\d+)["\']?', html)
        if cw_match:
            id_courseware = cw_match.group(1)
        else:
            # Thử cách khác
            cw_match = re.search(r'data-courseware\s*=\s*["\'](\d+)["\']', html)
            if cw_match:
                id_courseware = cw_match.group(1)
        
        # Tìm id_cate từ URL
        id_cate = None
        cate_match = re.search(r'-(\d+)(?:\?|$)', url)
        if cate_match:
            id_cate = cate_match.group(1)
        
        if not quiz_list:
            if is_video:
                return "", 0, id_courseware, id_cate
            else:
                return None, 0, id_courseware, id_cate
        
        # Tách danh sách câu hỏi
        question_ids = [qid.strip() for qid in quiz_list.split(',') if qid.strip()]
        total_questions = len(question_ids)
        
        return quiz_list, total_questions, id_courseware, id_cate
        
    except Exception as e:
        return None, 0, None, None

def create_data_log_for_normal(total_questions, target_score):
    """Tạo data_log CHO BÀI TẬP THƯỜNG"""
    if target_score == 100:
        correct_needed = total_questions
    elif target_score == 0:
        correct_needed = 0
    else:
        correct_needed = round((target_score / 100) * total_questions)
        correct_needed = max(0, min(total_questions, correct_needed))
    
    wrong_needed = total_questions - correct_needed
    
    results = [1] * correct_needed + [0] * wrong_needed
    random.shuffle(results)
    
    data_log = []
    total_time = 0
    
    for i, is_correct in enumerate(results):
        time_spent = random.randint(10, 30) + (i % 5)
        total_time += time_spent
        
        order = [0, 1, 2, 3]
        random.shuffle(order)
        
        chosen_answer = "0" if is_correct else str(random.randint(1, 3))
        
        data_log.append({
            "q_params": json.dumps([{"js": "", "order": order}]),
            "a_params": json.dumps([f'["{chosen_answer}"]']),
            "result": is_correct,
            "correct": is_correct,
            "wrong": 0 if is_correct else 1,
            "a_index": i,
            "time_spent": time_spent
        })
    
    return data_log, total_time, correct_needed

def submit_assignment(session, assignment, user_id):
    """Nộp bài tập"""
    try:
        # TRÍCH XUẤT THÔNG TIN
        quiz_list, total_questions, id_courseware, id_cate = extract_quiz_info(
            session, assignment['url'], assignment['is_video']
        )
        
        # XỬ LÝ VIDEO
        if assignment['is_video']:
            success = handle_video_submission(session, assignment, user_id, quiz_list, total_questions, id_courseware, id_cate)
            return success
        
        # BÀI TẬP THƯỜNG & LÝ THUYẾT & KIỂM TRA
        if not quiz_list or total_questions == 0:
            return False
        
        data_log, total_time, correct_needed = create_data_log_for_normal(total_questions, 100)
        
        # LẤY CSRF TOKEN
        csrf_token = session.cookies.get('XSRF-TOKEN')
        
        if not csrf_token:
            resp = session.get(assignment['url'], timeout=10)
            csrf_match = re.search(r'<meta name="csrf-token" content="([^"]+)"', resp.text)
            csrf_token = csrf_match.group(1) if csrf_match else ""
        
        # TẠO PAYLOAD
        current_time = int(time.time())
        start_time = current_time - total_time if total_time > 0 else current_time - 600
        
        user_ans = ["0"] * total_questions
        list_ans = ["0"] * total_questions
        
        payload = {
            '_token': csrf_token,
            'id_user': user_id,
            'id_cate': id_cate or '0',
            'id_grade': '10',
            'id_courseware': id_courseware or '0',
            'id_group': '6148789559',
            'id_school': '0',
            'time_init': str(start_time),
            'name_user': '',
            'type_vip': '0',
            'time_spent': str(total_time),
            'data_log': json.dumps(data_log, separators=(',', ':')),
            'score': '100',
            'answered': str(total_questions),
            'correct': str(correct_needed),
            'count_problems': str(total_questions),
            'missed': str(total_questions - correct_needed),
            'time_stored': str(current_time),
            'date_end': str(current_time),
            'ended': '1',
            'save_star': '0',
            'cv_q': '1',
            'quiz_list': quiz_list or '',
            'choose_log': json.dumps(data_log, separators=(',', ':')),
            'user_ans': json.dumps(user_ans),
            'list_quiz': quiz_list or '',
            'list_ans': ','.join(list_ans),
            'result': '[]',
            'ans': '[]'
        }
        
        # GỬI REQUEST
        submit_headers = HEADERS.copy()
        submit_headers['x-csrf-token'] = csrf_token
        
        response = session.post(
            'https://olm.vn/course/teacher-static',
            data=payload,
            headers=submit_headers,
            timeout=15
        )
        
        return response.status_code == 200
            
    except Exception as e:
        return False

def handle_video_submission(session, assignment, user_id, quiz_list, total_questions, id_courseware, id_cate):
    """Xử lý nộp video"""
    
    # THỬ NHIỀU PHƯƠNG PHÁP
    methods = [
        try_video_simple_method,
        try_video_with_quiz,
        try_video_complex_method,
    ]
    
    for i, method in enumerate(methods, 1):
        success = method(session, assignment, user_id, quiz_list, total_questions, id_courseware, id_cate)
        if success:
            return True
        time.sleep(0.5)
    
    return False

def try_video_simple_method(session, assignment, user_id, quiz_list, total_questions, id_courseware, id_cate):
    """Phương pháp đơn giản cho video"""
    try:
        csrf_token = session.cookies.get('XSRF-TOKEN')
        if not csrf_token:
            resp = session.get(assignment['url'], timeout=5)
            csrf_match = re.search(r'<meta name="csrf-token" content="([^"]+)"', resp.text)
            csrf_token = csrf_match.group(1) if csrf_match else ""
        
        current_time = int(time.time())
        time_spent = random.randint(300, 900)
        
        # Tạo data_log đơn giản
        data_log = [{
            "answer": '["0"]',
            "params": '{"js":""}',
            "result": [1],
            "wrong_skill": [],
            "correct_skill": [],
            "type": [11],
            "id": f"vid{random.randint(100000, 999999)}",
            "marker": 1
        }]
        
        # Tạo payload
        payload = {
            '_token': csrf_token,
            'id_user': user_id,
            'id_cate': id_cate or '0',
            'id_grade': '10',
            'id_courseware': id_courseware or '0',
            'time_spent': str(time_spent),
            'score': '100',
            'data_log': json.dumps(data_log, separators=(',', ':')),
            'date_end': str(current_time),
            'ended': '1',
            'cv_q': '1'
        }
        
        submit_headers = HEADERS.copy()
        submit_headers['x-csrf-token'] = csrf_token
        
        response = session.post(
            'https://olm.vn/course/teacher-static',
            data=payload,
            headers=submit_headers,
            timeout=10
        )
        
        return response.status_code == 200
        
    except Exception as e:
        return False

def try_video_with_quiz(session, assignment, user_id, quiz_list, total_questions, id_courseware, id_cate):
    """Phương pháp video có quiz_list"""
    try:
        if not quiz_list or total_questions == 0:
            return False
        
        csrf_token = session.cookies.get('XSRF-TOKEN')
        if not csrf_token:
            resp = session.get(assignment['url'], timeout=5)
            csrf_match = re.search(r'<meta name="csrf-token" content="([^"]+)"', resp.text)
            csrf_token = csrf_match.group(1) if csrf_match else ""
        
        current_time = int(time.time())
        time_spent = random.randint(300, 900)
        
        # Tạo data_log với số câu hỏi thực tế
        data_log = []
        for i in range(min(total_questions, 5)):
            data_log.append({
                "answer": '["0"]',
                "params": '{"js":""}',
                "result": [1],
                "wrong_skill": [],
                "correct_skill": [],
                "type": [11],
                "id": f"vid{random.randint(100000, 999999)}",
                "marker": i + 1
            })
        
        payload = {
            '_token': csrf_token,
            'id_user': user_id,
            'id_cate': id_cate or '0',
            'id_grade': '10',
            'id_courseware': id_courseware or '0',
            'time_spent': str(time_spent),
            'score': '100',
            'data_log': json.dumps(data_log, separators=(',', ':')),
            'date_end': str(current_time),
            'ended': '1',
            'cv_q': '1',
            'quiz_list': quiz_list,
            'correct': str(len(data_log)),
            'count_problems': str(len(data_log))
        }
        
        submit_headers = HEADERS.copy()
        submit_headers['x-csrf-token'] = csrf_token
        
        response = session.post(
            'https://olm.vn/course/teacher-static',
            data=payload,
            headers=submit_headers,
            timeout=10
        )
        
        return response.status_code == 200
        
    except Exception as e:
        return False

def try_video_complex_method(session, assignment, user_id, quiz_list, total_questions, id_courseware, id_cate):
    """Phương pháp phức tạp cho video"""
    try:
        csrf_token = session.cookies.get('XSRF-TOKEN')
        if not csrf_token:
            resp = session.get(assignment['url'], timeout=5)
            csrf_match = re.search(r'<meta name="csrf-token" content="([^"]+)"', resp.text)
            csrf_token = csrf_match.group(1) if csrf_match else ""
        
        current_time = int(time.time())
        time_spent = random.randint(600, 1200)
        
        # Tạo data_log kết hợp
        data_log = []
        
        # Câu hỏi video
        data_log.append({
            "answer": '["0"]',
            "params": '{"js":""}',
            "result": [1],
            "wrong_skill": [],
            "correct_skill": [],
            "type": [11],
            "id": f"vid{random.randint(100000, 999999)}",
            "marker": 1
        })
        
        # Thêm câu hỏi trắc nghiệm
        if quiz_list and total_questions > 0:
            order = [0, 1, 2, 3]
            random.shuffle(order)
            data_log.append({
                "answer": '["0"]',
                "label": ["A"],
                "params": json.dumps({"js": "", "order": order}),
                "result": [1],
                "wrong_skill": [],
                "correct_skill": [],
                "type": [1],
                "id": f"q{random.randint(100000, 999999)}",
                "marker": 2
            })
        
        payload = {
            '_token': csrf_token,
            'id_user': user_id,
            'id_cate': id_cate or '0',
            'id_grade': '10',
            'id_courseware': id_courseware or '0',
            'id_group': '6148789559',
            'id_school': '30494',
            'time_init': '',
            'name_user': '',
            'type_vip': '530',
            'time_spent': str(time_spent),
            'score': '100',
            'data_log': json.dumps(data_log, separators=(',', ':')),
            'total_time': str(time_spent),
            'current_time': '3',
            'correct': str(len(data_log)),
            'totalq': '0',
            'count_problems': str(len(data_log)),
            'date_end': str(current_time),
            'ended': '1',
            'save_star': '1',
            'cv_q': '1'
        }
        
        if quiz_list:
            payload['quiz_list'] = quiz_list
        
        submit_headers = HEADERS.copy()
        submit_headers['x-csrf-token'] = csrf_token
        
        response = session.post(
            'https://olm.vn/course/teacher-static',
            data=payload,
            headers=submit_headers,
            timeout=10
        )
        
        return response.status_code == 200
        
    except Exception as e:
        return False

# ========== GIẢI BÀI TỪ LINK ==========
def solve_from_link(session, user_id, is_vip, remaining_uses):
    """Giải bài từ link"""
    print_header("GIẢI BÀI TỪ LINK")
    
    print(f"{Colors.CYAN}{ICONS['link']} NHẬP LINK BÀI TẬP:{Colors.END}")
    print("Ví dụ: https://olm.vn/chu-de/...")
    print()
    
    url = input(f"{ICONS['link']} {Colors.YELLOW}Dán link bài tập: {Colors.END}").strip()
    
    if not url.startswith('https://olm.vn/'):
        print_status("Link không hợp lệ! Phải là link OLM", 'error', Colors.RED)
        wait_enter()
        return False, remaining_uses
    
    try:
        # Kiểm tra loại bài
        resp = session.get(url, timeout=10)
        is_video = 'video' in url.lower() or '[Video]' in resp.text
        is_ly_thuyet = 'ly-thuyet' in url.lower() or 'lý-thuyết' in url.lower() or '[Lý thuyết]' in resp.text
        
        # Tạo assignment object
        assignment = {
            'title': "Bài từ link",
            'subject': "Tự chọn",
            'type': "Bài tập",
            'status': "Chưa làm",
            'url': url,
            'page': 1,
            'is_video': is_video,
            'is_ly_thuyet': is_ly_thuyet,
            'is_bai_tap': not (is_video or is_ly_thuyet),
            'is_kiem_tra': False,
            'is_tu_luan': False
        }
        
        # Điều chỉnh loại bài
        if assignment['is_video']:
            assignment['type'] = "Video"
        elif assignment['is_ly_thuyet']:
            assignment['type'] = "Lý thuyết"
        
        print(f"\n{Colors.CYAN}📋 THÔNG TIN BÀI TẬP:{Colors.END}")
        print(f"  {Colors.WHITE}📖 Link: {url}{Colors.END}")
        print(f"  {Colors.CYAN}📝 Loại: {assignment['type']}{Colors.END}")
        
        confirm = input(f"\n{Colors.YELLOW}Xác nhận giải bài này? (y/n): {Colors.END}").strip().lower()
        
        if confirm == 'y':
            success = submit_assignment(session, assignment, user_id)
            if success:
                print_status("Thành công!", 'success', Colors.GREEN)
                wait_enter()
                if not is_vip:
                    remaining_uses -= 1
                    save_license({
                        'key': license_data['key'],
                        'remain': remaining_uses,
                        'expire': license_data['expire'],
                        'ip': license_data['ip']
                    })
                    print(f"{Colors.YELLOW}Số lượt còn lại: {remaining_uses}{Colors.END}")
                return True, remaining_uses
            else:
                print_status("Thất bại!", 'error', Colors.RED)
                wait_enter()
                return False, remaining_uses
        else:
            print_status("Đã hủy", 'warning', Colors.YELLOW)
            return False, remaining_uses
            
    except Exception as e:
        print_status(f"Lỗi: {str(e)}", 'error', Colors.RED)
        return False, remaining_uses

# ========== GIẢI BÀI CỤ THỂ TỪ DANH SÁCH ==========
def solve_specific_from_list(session, user_id, is_vip, remaining_uses):
    """Giải bài cụ thể từ danh sách"""
    print_header("GIẢI BÀI CỤ THỂ")
    
    # Hỏi số trang
    pages_input = input(f"{Colors.YELLOW}Số trang cần quét (mặc định: 3): {Colors.END}").strip()
    pages_to_scan = 3
    if pages_input.isdigit() and int(pages_input) > 0:
        pages_to_scan = int(pages_input)
    
    assignments = get_assignments_fixed(session, pages_to_scan)
    if not assignments:
        wait_enter()
        return False, remaining_uses
    
    display_assignments_table(assignments)
    
    # Chọn bài để giải
    try:
        selection = input(f"\n{Colors.YELLOW}Chọn số bài để giải (1-{len(assignments)}): {Colors.END}").strip()
        
        # Xử lý trường hợp "0" (giải tất cả)
        if selection == '0':
            indices = list(range(len(assignments)))
        else:
            indices = []
            for part in selection.split(','):
                if part.strip().isdigit():
                    idx = int(part.strip()) - 1
                    if 0 <= idx < len(assignments):
                        indices.append(idx)
            
            if not indices:
                print_status("Lựa chọn không hợp lệ", 'error', Colors.RED)
                wait_enter()
                return False, remaining_uses
        
        # Lấy điểm số 1 lần cho tất cả bài
        all_success = True
        
        for idx, assignment_idx in enumerate(indices, 1):
            print(f"\n{Colors.YELLOW}📊 Bài {idx}/{len(indices)}{Colors.END}")
            assignment = assignments[assignment_idx]
            
            # Kiểm tra lượt sử dụng
            if not is_vip and remaining_uses <= 0:
                print_status("Hết lượt sử dụng! Vui lòng lấy key mới.", 'error', Colors.RED)
                all_success = False
                break
            
            success = submit_assignment(session, assignment, user_id)
            
            if success:
                print_status("Thành công!", 'success', Colors.GREEN)
                if not is_vip:
                    remaining_uses -= 1
                    save_license({
                        'key': license_data['key'],
                        'remain': remaining_uses,
                        'expire': license_data['expire'],
                        'ip': license_data['ip']
                    })
                    print(f"{Colors.YELLOW}Số lượt còn lại: {remaining_uses}{Colors.END}")
            else:
                print_status("Thất bại!", 'error', Colors.RED)
                all_success = False
            
            # Chờ giữa các bài
            if idx < len(indices):
                wait_time = random.randint(2, 5)
                print_status(f"Chờ {wait_time}s...", 'clock', Colors.YELLOW)
                time.sleep(wait_time)
        
        wait_enter()
        return all_success, remaining_uses
        
    except Exception as e:
        print_status(f"Lỗi chọn bài: {str(e)}", 'error', Colors.RED)
        wait_enter()
        return False, remaining_uses

# ========== MENU CHÍNH ==========
def main_menu(session, user_id, user_name, is_vip, remaining_uses):
    """Menu chính"""
    
    while True:
        print_header("MENU CHÍNH")
        print(f"{ICONS['user']} {Colors.GREEN}Xin chào: {user_name}{Colors.END}")
        
        if not is_vip:
            print(f"{Colors.YELLOW}Số lượt còn lại: {remaining_uses}{Colors.END}")
        
        # Nếu hết lượt, yêu cầu lấy key mới
        if not is_vip and remaining_uses <= 0:
            print(f"\n{Colors.RED}Hết lượt sử dụng! Vui lòng lấy key mới{Colors.END}")
            new_license = handle_key_generation()
            if new_license:
                save_license(new_license)
                print(f"{Colors.GREEN}Đăng ký thành công! Bạn có {new_license['remain']} lượt{Colors.END}")
                return True, new_license['remain']
            else:
                print_status("Không thể đăng ký key", 'error', Colors.RED)
                return False, remaining_uses
        
        menu_options = {
            '1': f"{ICONS['rocket']} Tự động hoàn thành bài",
            '2': f"{ICONS['link']} Giải bài từ link OLM",
            '3': f"{ICONS['refresh']} Đăng xuất",
            '4': f"{ICONS['exit']} Thoát",
            '5': f"{ICONS['help']} Hướng dẫn sử dụng"
        }
        
        print_menu("LỰA CHỌN", menu_options)
        
        choice = input(f"\n{Colors.YELLOW}Chọn chức năng (1-5): {Colors.END}").strip()
        
        if choice == '1':
            pages_input = input(f"{Colors.YELLOW}Số trang cần quét (mặc định: 3): {Colors.END}").strip()
            pages_to_scan = 3
            if pages_input.isdigit() and int(pages_input) > 0:
                pages_to_scan = int(pages_input)
            
            assignments = get_assignments_fixed(session, pages_to_scan)
            if assignments:
                display_assignments_table(assignments)
                
                selection = input(f"\n{Colors.YELLOW}Chọn bài (0 cho tất cả, hoặc 1,2,3...): {Colors.END}").strip()
                if selection == '0':
                    _, remaining_uses = solve_specific_from_list(session, user_id, is_vip, remaining_uses)
                else:
                    _, remaining_uses = solve_specific_from_list(session, user_id, is_vip, remaining_uses)
        
        elif choice == '2':
            _, remaining_uses = solve_from_link(session, user_id, is_vip, remaining_uses)
        
        elif choice == '3':
            print_status("Đang đăng xuất...", 'refresh', Colors.YELLOW)
            time.sleep(1)
            return False, remaining_uses
        
        elif choice == '4':
            print_status("Cảm ơn đã sử dụng!", 'exit', Colors.GREEN)
            time.sleep(1)
            sys.exit(0)
        
        elif choice == '5':
            print_tutorial()
        
        else:
            print_status("Lựa chọn không hợp lệ!", 'error', Colors.RED)
            time.sleep(1)
    
    return True, remaining_uses

# ========== CHƯƠNG TRÌNH CHÍNH ==========
def main():
    """Chương trình chính"""
    
    # Hiển thị tutorial khi chạy lần đầu
    print_tutorial()
    
    while True:
        # Đăng nhập
        session, user_id, user_name = login_olm()
        
        if session and user_id and user_name:
            # Kiểm tra VIP
            is_vip = check_vip(user_name)
            
            if is_vip:
                print(f"{Colors.GREEN}{ICONS['vip']} TÀI KHOẢN VIP - KHÔNG GIỚI HẠN LƯỢT SỬ DỤNG{Colors.END}")
                main_menu(session, user_id, user_name, True, float('inf'))
            else:
                # Tải license tồn tại
                global license_data
                license_data = load_license()
                today = datetime.now().strftime("%Y-%m-%d")
                current_ip = get_public_ip()
                
                # Kiểm tra license hợp lệ
                if (license_data and 
                    license_data.get('expire') == today and 
                    license_data.get('ip') == current_ip and 
                    license_data.get('remain', 0) > 0):
                    
                    remaining_uses = license_data['remain']
                    print(f"{Colors.YELLOW}Tài khoản FREE - Còn {remaining_uses} lượt{Colors.END}")
                    # Gọi main_menu và cập nhật remaining_uses
                    _, remaining_uses = main_menu(session, user_id, user_name, False, remaining_uses)
                else:
                    # Tạo key mới
                    print(f"{Colors.YELLOW}Tài khoản FREE - Vui lòng lấy key mới{Colors.END}")
                    new_license = handle_key_generation()
                    if new_license:
                        save_license(new_license)
                        print(f"{Colors.GREEN}Đăng ký thành công! Còn {new_license['remain']} lượt{Colors.END}")
                        _, remaining_uses = main_menu(session, user_id, user_name, False, new_license['remain'])
                    else:
                        print_status("Không thể đăng ký key", 'error', Colors.RED)
        else:
            retry = input(f"\n{Colors.YELLOW}Thử lại? (y/n): {Colors.END}").strip().lower()
            if retry != 'y':
                print_status("Tạm biệt!", 'exit', Colors.GREEN)
                time.sleep(1)
                break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{ICONS['exit']} {Colors.YELLOW}Đã dừng chương trình{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{ICONS['error']} {Colors.RED}Lỗi không mong muốn: {str(e)}{Colors.END}")
        wait_enter()
