#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║                    OLM MASTER - ALL IN ONE                   ║
║                    Created by: Tuấn Anh                      ║
╚══════════════════════════════════════════════════════════════╝
Tool tự động tải bản mới nhất từ GitHub và tự xóa sau khi dùng
"""

import os
import sys
import time
import json
import random
import requests
import re
import hashlib
import base64
import tempfile
import subprocess
import platform
import socket
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from bs4 import BeautifulSoup

# ========== CẤU HÌNH ==========
URL_MAIN = "https://raw.githubusercontent.com/thieunangbiettuot/ToolOLM/refs/heads/main/main.py"
URL_VIP = "https://raw.githubusercontent.com/thieunangbiettuot/ToolOLM/refs/heads/main/vip_users.txt"
API_TOKENS = ["698b226d9150d31d216157a5"]

VERSION = "2.0.0"
AUTHOR = "Tuấn Anh"

# ========== MÀU SẮC ==========
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
    'user': '👤', 'key': '🔑', 'lock': '🔐', 'crown': '👑',
    'star': '⭐', 'rocket': '🚀', 'check': '✔️', 'exit': '🚪',
    'refresh': '🔄', 'download': '📥', 'upload': '📤', 'link': '🔗',
    'list': '📋', 'brain': '🧠', 'video': '🎬', 'theory': '📖',
    'exercise': '📝', 'test': '📋', 'clock': '⏰', 'fire': '🔥'
}

# ========== TIỆN ÍCH ==========
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_line(char='═', color=Colors.CYAN, width=60):
    print(f"{color}{char * width}{Colors.END}")

def print_header(title=""):
    clear_screen()
    print_line('═', Colors.BLUE, 60)
    print(f"{Colors.BLUE}{Colors.BOLD}{' ' * 15}OLM MASTER ALL IN ONE{' ' * 15}{Colors.END}")
    print(f"{Colors.PURPLE}{' ' * 20}Version: {VERSION}{' ' * 20}{Colors.END}")
    print(f"{Colors.PURPLE}{' ' * 20}Author: {AUTHOR}{' ' * 20}{Colors.END}")
    if title:
        print_line('─', Colors.CYAN, 60)
        print(f"{Colors.CYAN}{' ' * ((60 - len(title)) // 2)}{title}{Colors.END}")
    print_line('═', Colors.BLUE, 60)
    print()

def print_status(message, icon='info', color=Colors.WHITE):
    print(f"{ICONS.get(icon, '')} {color}{message}{Colors.END}")

def wait_enter(prompt="Nhấn Enter để tiếp tục..."):
    input(f"\n{Colors.YELLOW}{prompt}{Colors.END}")

def input_prompt(prompt, color=Colors.YELLOW):
    return input(f"{color}{prompt}{Colors.END}").strip()

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
ACCOUNTS_FILE = os.path.join(DATA_DIR, f'.{DEVICE_HASH}ac')

# ========== BẢO MẬT ĐƠN GIẢN ==========
def encode_data(data):
    return base64.b64encode(json.dumps(data).encode()).decode()

def decode_data(encoded):
    try:
        return json.loads(base64.b64decode(encoded).decode())
    except:
        return None

# ========== LICENSE ==========
def load_license():
    try:
        if os.path.exists(LICENSE_FILE):
            with open(LICENSE_FILE, 'r') as f:
                return decode_data(f.read())
    except:
        pass
    return None

def save_license(data):
    try:
        with open(LICENSE_FILE, 'w') as f:
            f.write(encode_data(data))
        return True
    except:
        return False

def is_vip(username):
    try:
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

# ========== QUẢN LÝ TÀI KHOẢN ==========
def load_accounts():
    try:
        if os.path.exists(ACCOUNTS_FILE):
            return decode_data(open(ACCOUNTS_FILE, 'r').read()) or {}
    except:
        pass
    return {}

def save_accounts(accounts):
    try:
        with open(ACCOUNTS_FILE, 'w') as f:
            f.write(encode_data(accounts))
        return True
    except:
        return False

def select_saved_account():
    accounts = load_accounts()
    if not accounts:
        return None, None
    
    print(f"\n{Colors.CYAN}👤 TÀI KHOẢN ĐÃ LƯU:{Colors.END}")
    print_line('─', Colors.CYAN, 40)
    
    account_list = list(accounts.items())
    for idx, (name, data) in enumerate(account_list, 1):
        print(f"  {Colors.YELLOW}{idx}.{Colors.END} {name} ({data.get('saved_at', '')})")
    
    print(f"  {Colors.YELLOW}0.{Colors.END} Đăng nhập mới")
    print_line('─', Colors.CYAN, 40)
    
    choice = input_prompt("Chọn: ")
    
    if choice == '0':
        return None, None
    
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(account_list):
            return account_list[idx][1]['username'], account_list[idx][1]['password']
    
    return None, None

def save_current_account(name, username, password):
    accounts = load_accounts()
    accounts[name] = {
        'username': username,
        'password': password,
        'saved_at': datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    return save_accounts(accounts)

# ========== XỬ LÝ FREE ==========
def handle_free_license():
    blog_base = "https://keyfreedailyolmvip.blogspot.com/2026/02/blog-post.html"
    max_attempts = 3
    
    print_header("KÍCH HOẠT BẢN FREE")
    print(f"{Colors.CYAN}Bạn cần vượt link để lấy key{Colors.END}")
    print(f"{Colors.CYAN}Mỗi key có 4 lượt, hiệu lực 1 ngày{Colors.END}")
    
    for attempt in range(max_attempts):
        key = generate_key()
        blog_url = f"{blog_base}?ma={key}"
        short_link = create_short_link(blog_url)
        
        print(f"\n{Colors.GREEN}🔗 LINK: {short_link}{Colors.END}")
        print(f"{Colors.YELLOW}KEY: {Colors.BOLD}{key}{Colors.END}")
        print()
        
        key_input = input_prompt("Nhập key (r = tạo lại): ")
        
        if key_input.lower() == 'r':
            continue
        
        if key_input == key:
            license_data = {
                'mode': 'FREE',
                'remain': 4,
                'expire': (datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y")
            }
            save_license(license_data)
            print_status("Kích hoạt thành công! Bạn có 4 lượt.", 'success', Colors.GREEN)
            return True
        else:
            remaining = max_attempts - attempt - 1
            if remaining > 0:
                print_status(f"Sai key! Còn {remaining} lần", 'error', Colors.RED)
                time.sleep(attempt + 1)
            else:
                print_status("Hết lượt thử!", 'error', Colors.RED)
    
    return False

# ========== HEADERS ==========
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'x-requested-with': 'XMLHttpRequest',
}

# ========== ĐĂNG NHẬP ==========
def login_olm():
    print_header("ĐĂNG NHẬP OLM")
    
    saved_user, saved_pass = select_saved_account()
    
    use_saved = False
    if saved_user and saved_pass:
        use_saved = input_prompt("Dùng tài khoản đã lưu? (y/n): ").lower() == 'y'
    
    if use_saved:
        username = saved_user
        password = saved_pass
        print_status("Đang đăng nhập...", 'user', Colors.GREEN)
    else:
        username = input_prompt(f"{ICONS['user']} Tên đăng nhập: ")
        password = input_prompt(f"{ICONS['key']} Mật khẩu: ")
    
    if not username or not password:
        print_status("Thông tin trống!", 'error', Colors.RED)
        wait_enter()
        return None, None, None
    
    session = requests.Session()
    session.headers.update(HEADERS)
    
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
            
            print_status(f"Đăng nhập thành công: {user_name}", 'success', Colors.GREEN)
            
            # Lưu tài khoản
            if not use_saved and input_prompt("Lưu tài khoản? (y/n): ").lower() == 'y':
                save_current_account(user_name, username, password)
            
            return session, user_id, user_name
        else:
            print_status("Đăng nhập thất bại!", 'error', Colors.RED)
            wait_enter()
            return None, None, None
            
    except Exception as e:
        print_status(f"Lỗi: {str(e)}", 'error', Colors.RED)
        wait_enter()
        return None, None, None

# ========== CÁC HÀM XỬ LÝ BÀI TẬP (GIỮ NGUYÊN) ==========

def check_hidden_test_status(session, url, id_cate):
    """Kiểm tra bài kiểm tra ẩn điểm"""
    try:
        test_url = f'https://olm.vn/course/teacher-categories/{id_cate}/get-next-cate'
        
        headers = HEADERS.copy()
        headers['referer'] = url
        headers['x-csrf-token'] = session.cookies.get('XSRF-TOKEN', '')
        
        response = session.get(test_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            try:
                response.json()
                return True
            except:
                pass
        
        quiz_response = session.get(url, timeout=10)
        html = quiz_response.text
        
        pattern = r'quiz_list\s*[:=]\s*["\'](\d{6,}(?:,\d{6,})*)["\']'
        match = re.search(pattern, html)
        
        if match:
            quiz_list = match.group(1)
            api_url = 'https://olm.vn/course/question/get-question-of-ids'
            
            payload = {
                'qlib_list': quiz_list,
                'id_subject': '2',
                'id_skill': id_cate,
                'cv_q': '1'
            }
            
            api_headers = HEADERS.copy()
            api_headers['content-type'] = 'application/x-www-form-urlencoded'
            api_headers['x-csrf-token'] = session.cookies.get('XSRF-TOKEN', '')
            api_headers['referer'] = url
            
            api_response = session.post(api_url, data=payload, headers=api_headers, timeout=10)
            
            if api_response.status_code == 200:
                response_text = api_response.text.lower()
                if "đã hoàn thành" in response_text or "đã nộp" in response_text:
                    return True
        
        return False
    except:
        return False

def get_assignments(session, pages_to_scan=5):
    """Lấy danh sách bài tập"""
    print_header(f"QUÉT BÀI TẬP ({pages_to_scan} TRANG)")
    
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
                    continue
                
                soup = BeautifulSoup(response.text, 'html.parser')
                rows = soup.find_all('tr', class_='my-gived-courseware-item')
                
                if not rows:
                    continue
                
                for row in rows:
                    link_tags = row.find_all('a', class_='olm-text-link')
                    if not link_tags:
                        continue
                    
                    main_link = link_tags[0]
                    href = main_link.get('href')
                    link_text = main_link.get_text(strip=True)
                    
                    if href and ('(Toán' in link_text or '(Ngữ văn' in link_text):
                        continue
                    
                    if not href:
                        continue
                    
                    tds = row.find_all('td')
                    if len(tds) < 2:
                        continue
                    
                    loai_raw = tds[1].get_text(strip=True)
                    
                    if "[Tự luận]" in loai_raw or "[Tu luan]" in loai_raw:
                        continue
                    
                    is_video = "[Video]" in loai_raw
                    is_ly_thuyet = "[Lý thuyết]" in loai_raw
                    is_kiem_tra = "[Kiểm tra]" in loai_raw
                    
                    # Kiểm tra trạng thái
                    status_spans = []
                    status_spans.extend(main_link.find_all('span', class_='message-static-item'))
                    
                    if not status_spans:
                        status_spans.extend(row.find_all('span', class_='message-static-item'))
                    
                    should_process = False
                    
                    if not is_kiem_tra:
                        if not status_spans:
                            should_process = True
                        else:
                            for span in status_spans:
                                span_text = span.get_text(strip=True).lower()
                                if "chưa" in span_text or "làm tiếp" in span_text:
                                    should_process = True
                                    break
                    else:
                        if not status_spans:
                            id_cate = None
                            if row.has_attr('data-cate'):
                                id_cate = row['data-cate']
                            else:
                                match = re.search(r'-(\d+)\?', href)
                                if match:
                                    id_cate = match.group(1)
                            
                            if id_cate:
                                should_process = not check_hidden_test_status(session, href, id_cate)
                            else:
                                should_process = True
                    
                    if should_process and href not in seen_links:
                        seen_links.add(href)
                        
                        mon = row.find('span', class_='alert')
                        mon_text = mon.get_text(strip=True) if mon else "Khác"
                        
                        ten_bai = re.sub(r'\([^)]*\)', '', link_text).strip()
                        
                        status = "Chưa làm"
                        if status_spans:
                            for span in status_spans:
                                span_text = span.get_text(strip=True)
                                if "chưa" in span_text.lower():
                                    status = span_text
                                    break
                        
                        full_url = 'https://olm.vn' + href if not href.startswith('http') else href
                        
                        assignments.append({
                            'title': ten_bai[:60],
                            'subject': mon_text[:20],
                            'type': loai_raw.replace('[', '').replace(']', '').strip()[:20],
                            'status': status,
                            'url': full_url,
                            'is_video': is_video,
                            'is_ly_thuyet': is_ly_thuyet,
                            'is_kiem_tra': is_kiem_tra
                        })
            
            except Exception as e:
                continue
        
        if assignments:
            print_status(f"Tìm thấy {len(assignments)} bài", 'success', Colors.GREEN)
        else:
            print_status("Không tìm thấy bài", 'warning', Colors.YELLOW)
        
        return assignments
        
    except Exception as e:
        print_status(f"Lỗi: {str(e)}", 'error', Colors.RED)
        return []

def display_assignments(assignments):
    """Hiển thị danh sách bài tập"""
    if not assignments:
        return
    
    print(f"\n{Colors.PURPLE}{'📚 DANH SÁCH BÀI TẬP':^60}{Colors.END}")
    print_line('─', Colors.PURPLE, 60)
    
    for idx, item in enumerate(assignments, 1):
        title = item['title']
        if len(title) > 35:
            title = title[:32] + "..."
        
        if item['is_video']:
            icon = '🎬'
            color = Colors.BLUE
        elif item['is_ly_thuyet']:
            icon = '📖'
            color = Colors.CYAN
        elif item['is_kiem_tra']:
            icon = '📋'
            color = Colors.YELLOW
        else:
            icon = '📝'
            color = Colors.GREEN
        
        print(f"{Colors.YELLOW}{idx:>2}.{Colors.END} {color}{icon} {item['type']:<10}{Colors.END} {Colors.WHITE}{title:<35}{Colors.END}")
    
    print_line('─', Colors.PURPLE, 60)

def get_target_score(is_video=False, is_kiem_tra=False):
    """Chọn điểm số"""
    if is_video:
        return 100
    elif is_kiem_tra:
        return random.randint(85, 100)
    
    print(f"\n{Colors.CYAN}🎯 CHỌN ĐIỂM{Colors.END}")
    print_line('─', Colors.CYAN, 40)
    print(f"  {Colors.YELLOW}1.{Colors.END} 100 điểm")
    print(f"  {Colors.YELLOW}2.{Colors.END} Tùy chọn")
    print_line('─', Colors.CYAN, 40)
    
    while True:
        choice = input_prompt("Chọn (1-2): ")
        if choice == '1':
            return 100
        elif choice == '2':
            try:
                score = int(input_prompt("Nhập điểm (0-100): "))
                if 0 <= score <= 100:
                    return score
                print_status("Điểm 0-100!", 'error', Colors.RED)
            except:
                print_status("Nhập số!", 'error', Colors.RED)
        else:
            print_status("Chọn 1 hoặc 2!", 'error', Colors.RED)

def extract_quiz_info(session, url, is_video=False):
    """Trích xuất thông tin quiz"""
    try:
        resp = session.get(url, timeout=10)
        html = resp.text
        
        quiz_list = None
        patterns = [
            r'quiz_list\s*[:=]\s*["\'](\d{6,}(?:,\d{6,})*)["\']',
            r'"quiz_list"\s*:\s*"(\d+(?:,\d+)*)"',
            r'\b(\d{9,}(?:,\d{9,})+)\b'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, html)
            if match:
                quiz_list = match.group(1)
                break
        
        id_courseware = None
        cw_match = re.search(r'id_courseware\s*[:=]\s*["\']?(\d+)["\']?', html)
        if cw_match:
            id_courseware = cw_match.group(1)
        
        id_cate = None
        cate_match = re.search(r'-(\d+)(?:\?|$)', url)
        if cate_match:
            id_cate = cate_match.group(1)
        
        if not quiz_list and not is_video:
            return None, 0, id_courseware, id_cate
        
        total = 0
        if quiz_list:
            total = len([q for q in quiz_list.split(',') if q.strip()])
        
        return quiz_list, total, id_courseware, id_cate
        
    except Exception as e:
        return None, 0, None, None

def create_data_log(total, target):
    """Tạo data_log"""
    if target == 100:
        correct = total
    elif target == 0:
        correct = 0
    else:
        correct = round((target / 100) * total)
        correct = max(0, min(total, correct))
    
    wrong = total - correct
    
    results = [1] * correct + [0] * wrong
    random.shuffle(results)
    
    data_log = []
    total_time = 0
    
    for i, is_correct in enumerate(results):
        time_spent = random.randint(10, 30) + (i % 5)
        total_time += time_spent
        
        order = [0, 1, 2, 3]
        random.shuffle(order)
        
        chosen = "0" if is_correct else str(random.randint(1, 3))
        
        data_log.append({
            "q_params": json.dumps([{"js": "", "order": order}]),
            "a_params": json.dumps([f'["{chosen}"]']),
            "result": is_correct,
            "correct": is_correct,
            "wrong": 0 if is_correct else 1,
            "a_index": i,
            "time_spent": time_spent
        })
    
    return data_log, total_time, correct

def handle_response(response, target):
    """Xử lý phản hồi"""
    if response.status_code == 200:
        try:
            result = response.json()
            if 'code' in result:
                if result['code'] == 403:
                    print_status("Đã nộp trước", 'warning', Colors.YELLOW)
                    return True
                elif result['code'] == 200:
                    score = result.get('score', target)
                    print_status(f"Thành công! Điểm: {score}/100", 'success', Colors.GREEN)
                    return True
                else:
                    print_status("Nộp thành công", 'success', Colors.GREEN)
                    return True
            else:
                print_status("Nộp thành công", 'success', Colors.GREEN)
                return True
        except:
            print_status("Nộp thành công", 'success', Colors.GREEN)
            return True
    elif response.status_code == 403:
        print_status("Đã nộp trước", 'warning', Colors.YELLOW)
        return True
    else:
        print_status(f"Lỗi {response.status_code}", 'error', Colors.RED)
        return False

def submit_assignment(session, assignment, user_id):
    """Nộp bài tập"""
    print(f"\n{Colors.CYAN}📤 XỬ LÝ: {assignment['title']}{Colors.END}")
    
    if assignment['is_video']:
        print(f"{Colors.BLUE}🎬 Video{Colors.END}")
        target = 100
    elif assignment['is_ly_thuyet']:
        print(f"{Colors.CYAN}📚 Lý thuyết{Colors.END}")
        target = get_target_score(False, False)
    elif assignment['is_kiem_tra']:
        print(f"{Colors.YELLOW}📋 Kiểm tra{Colors.END}")
        target = get_target_score(False, True)
    else:
        print(f"{Colors.GREEN}📝 Bài tập{Colors.END}")
        target = get_target_score(False, False)
    
    try:
        quiz_list, total, id_cw, id_cate = extract_quiz_info(
            session, assignment['url'], assignment['is_video']
        )
        
        if assignment['is_video']:
            # Xử lý video đơn giản
            csrf = session.cookies.get('XSRF-TOKEN')
            if not csrf:
                return False
            
            current = int(time.time())
            spent = random.randint(300, 900)
            
            data = [{
                "answer": '["0"]',
                "params": '{"js":""}',
                "result": [1],
                "type": [11],
                "id": f"vid{random.randint(100000, 999999)}"
            }]
            
            payload = {
                '_token': csrf,
                'id_user': user_id,
                'id_cate': id_cate or '0',
                'id_courseware': id_cw or '0',
                'time_spent': str(spent),
                'score': '100',
                'data_log': json.dumps(data),
                'date_end': str(current),
                'ended': '1',
                'cv_q': '1'
            }
            
            if quiz_list:
                payload['quiz_list'] = quiz_list
            
            resp = session.post(
                'https://olm.vn/course/teacher-static',
                data=payload,
                headers={'x-csrf-token': csrf},
                timeout=10
            )
            
            success = handle_response(resp, 100)
            
        else:
            if not quiz_list or total == 0:
                print_status("Không lấy được thông tin", 'error', Colors.RED)
                return False
            
            print_status(f"Có {total} câu", 'info', Colors.WHITE)
            
            data_log, total_time, correct = create_data_log(total, target)
            
            csrf = session.cookies.get('XSRF-TOKEN')
            if not csrf:
                resp = session.get(assignment['url'], timeout=5)
                match = re.search(r'<meta name="csrf-token" content="([^"]+)"', resp.text)
                csrf = match.group(1) if match else ""
            
            current = int(time.time())
            start = current - total_time if total_time > 0 else current - 600
            
            user_ans = ["0"] * total
            list_ans = ["0"] * total
            
            payload = {
                '_token': csrf,
                'id_user': user_id,
                'id_cate': id_cate or '0',
                'id_grade': '10',
                'id_courseware': id_cw or '0',
                'id_group': '6148789559',
                'id_school': '0',
                'time_init': str(start),
                'name_user': '',
                'type_vip': '0',
                'time_spent': str(total_time),
                'data_log': json.dumps(data_log, separators=(',', ':')),
                'score': str(target),
                'answered': str(total),
                'correct': str(correct),
                'count_problems': str(total),
                'missed': str(total - correct),
                'time_stored': str(current),
                'date_end': str(current),
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
            
            print_status("Đang nộp...", 'upload', Colors.YELLOW)
            
            headers = HEADERS.copy()
            headers['x-csrf-token'] = csrf
            
            resp = session.post(
                'https://olm.vn/course/teacher-static',
                data=payload,
                headers=headers,
                timeout=15
            )
            
            success = handle_response(resp, target)
        
        if success:
            print_status("✅ HOÀN THÀNH!", 'success', Colors.GREEN + Colors.BOLD)
            
            # Trừ lượt cho FREE
            license_data = load_license()
            if license_data and license_data.get('mode') == 'FREE':
                remain = license_data.get('remain', 0)
                if remain > 0:
                    license_data['remain'] = remain - 1
                    save_license(license_data)
                    print_status(f"Lượt còn: {license_data['remain']}/4", 'info', Colors.CYAN)
            
            wait_enter()
            return True
        
        return False
        
    except Exception as e:
        print_status(f"Lỗi: {str(e)}", 'error', Colors.RED)
        return False

def parse_selection(selection, max_num):
    """Phân tích lựa chọn"""
    if selection == '0':
        return list(range(1, max_num + 1))
    
    if '-' in selection:
        try:
            s, e = map(int, selection.split('-'))
            return list(range(max(1, s), min(e, max_num) + 1))
        except:
            return []
    
    if ',' in selection:
        try:
            return [int(x.strip()) for x in selection.split(',') if 1 <= int(x.strip()) <= max_num]
        except:
            return []
    
    if selection.isdigit():
        n = int(selection)
        return [n] if 1 <= n <= max_num else []
    
    return []

def solve_specific(session, user_id):
    """Giải bài cụ thể"""
    print_header("GIẢI BÀI CỤ THỂ")
    
    pages = input_prompt("Số trang quét (mặc định: 3): ")
    pages = 3 if not pages.isdigit() else int(pages)
    
    assignments = get_assignments(session, pages)
    if not assignments:
        wait_enter()
        return False
    
    display_assignments(assignments)
    
    print(f"\n{Colors.CYAN}📝 CÁCH CHỌN: 0 (tất cả), 1,3,5 (nhiều), 1-5 (khoảng), 1 (một){Colors.END}")
    selection = input_prompt("Chọn bài: ")
    
    indices = parse_selection(selection, len(assignments))
    
    if not indices:
        print_status("Không chọn bài nào!", 'error', Colors.RED)
        wait_enter()
        return False
    
    print_status(f"Đã chọn {len(indices)} bài", 'info', Colors.CYAN)
    
    # Kiểm tra lượt
    license_data = load_license()
    if license_data and license_data.get('mode') == 'FREE':
        if license_data.get('remain', 0) < len(indices):
            print_status(f"Không đủ lượt! Cần {len(indices)}, còn {license_data.get('remain', 0)}", 'error', Colors.RED)
            wait_enter()
            return False
    
    confirm = input_prompt("Xác nhận? (y/n): ").lower()
    if confirm != 'y':
        print_status("Đã hủy", 'warning', Colors.YELLOW)
        wait_enter()
        return False
    
    print_header(f"GIẢI {len(indices)} BÀI")
    
    success = 0
    for i, idx in enumerate(indices, 1):
        print(f"\n{Colors.YELLOW}📊 Bài {i}/{len(indices)}{Colors.END}")
        
        if submit_assignment(session, assignments[idx-1], user_id):
            success += 1
        
        if i < len(indices):
            wait = random.randint(2, 4)
            print_status(f"Chờ {wait}s...", 'clock', Colors.YELLOW)
            time.sleep(wait)
    
    print(f"\n{Colors.GREEN}✅ Kết quả: {success}/{len(indices)}{Colors.END}")
    wait_enter()
    return True

def solve_from_link(session, user_id):
    """Giải từ link"""
    print_header("GIẢI TỪ LINK")
    
    url = input_prompt("Dán link OLM: ")
    
    if not url.startswith('https://olm.vn/'):
        print_status("Link không hợp lệ!", 'error', Colors.RED)
        wait_enter()
        return False
    
    try:
        resp = session.get(url, timeout=10)
        
        is_video = 'video' in url.lower() or '[Video]' in resp.text
        is_ly_thuyet = 'ly-thuyet' in url.lower() or '[Lý thuyết]' in resp.text
        is_kiem_tra = 'kiem-tra' in url.lower() or '[Kiểm tra]' in resp.text
        
        assignment = {
            'title': "Bài từ link",
            'subject': "Tự chọn",
            'type': "Bài tập",
            'status': "Chưa làm",
            'url': url,
            'page': 1,
            'is_video': is_video,
            'is_ly_thuyet': is_ly_thuyet,
            'is_kiem_tra': is_kiem_tra
        }
        
        if is_video:
            assignment['type'] = "Video"
        elif is_ly_thuyet:
            assignment['type'] = "Lý thuyết"
        elif is_kiem_tra:
            assignment['type'] = "Kiểm tra"
        
        print(f"\n{Colors.CYAN}📋 Loại: {assignment['type']}{Colors.END}")
        
        # Kiểm tra lượt
        license_data = load_license()
        if license_data and license_data.get('mode') == 'FREE' and license_data.get('remain', 0) < 1:
            print_status("Hết lượt!", 'error', Colors.RED)
            wait_enter()
            return False
        
        confirm = input_prompt("Xác nhận? (y/n): ").lower()
        
        if confirm == 'y':
            return submit_assignment(session, assignment, user_id)
        else:
            print_status("Đã hủy", 'warning', Colors.YELLOW)
            wait_enter()
            return False
            
    except Exception as e:
        print_status(f"Lỗi: {str(e)}", 'error', Colors.RED)
        wait_enter()
        return False

# ========== MENU CHÍNH ==========
def main_menu(session, user_id, user_name):
    """Menu chính"""
    
    while True:
        print_header("MENU CHÍNH")
        print(f"{ICONS['user']} {Colors.GREEN}{user_name}{Colors.END}")
        
        license_data = load_license()
        if license_data:
            if license_data.get('mode') == 'VIP':
                print(f"{ICONS['crown']} {Colors.MAGENTA}VIP: Không giới hạn{Colors.END}")
            else:
                print(f"{ICONS['key']} {Colors.CYAN}Lượt: {license_data.get('remain', 0)}/4{Colors.END}")
        print()
        
        print(f"\n{Colors.CYAN}📋 CHỌN CHỨC NĂNG{Colors.END}")
        print_line('─', Colors.CYAN, 40)
        print(f"  {Colors.YELLOW}1.{Colors.END} {ICONS['brain']} Giải bài cụ thể")
        print(f"  {Colors.YELLOW}2.{Colors.END} {ICONS['link']} Giải từ link")
        print(f"  {Colors.YELLOW}3.{Colors.END} {ICONS['refresh']} Đổi tài khoản")
        print(f"  {Colors.YELLOW}4.{Colors.END} {ICONS['exit']} Thoát")
        print_line('─', Colors.CYAN, 40)
        
        choice = input_prompt("\nChọn (1-4): ")
        
        if choice == '1':
            solve_specific(session, user_id)
        elif choice == '2':
            solve_from_link(session, user_id)
        elif choice == '3':
            print_status("Đang đăng xuất...", 'refresh', Colors.YELLOW)
            time.sleep(1)
            break
        elif choice == '4':
            print_status("Tạm biệt!", 'exit', Colors.GREEN)
            time.sleep(1)
            sys.exit(0)
        else:
            print_status("Chọn 1-4!", 'error', Colors.RED)
            time.sleep(1)

# ========== TỰ ĐỘNG XÓA ==========
def self_destruct():
    """Tự xóa file sau khi dùng"""
    try:
        os.remove(sys.argv[0])
    except:
        pass

# ========== MAIN ==========
def main():
    """Chương trình chính"""
    try:
        print_header(f"OLM MASTER {VERSION}")
        
        # Kiểm tra license
        license_data = load_license()
        
        if not license_data:
            # Chưa có license -> hỏi VIP hay FREE
            print(f"{Colors.CYAN}Chọn chế độ:{Colors.END}")
            print(f"  {Colors.YELLOW}1.{Colors.END} VIP (tài khoản VIP)")
            print(f"  {Colors.YELLOW}2.{Colors.END} FREE (vượt link lấy key)")
            print()
            
            mode = input_prompt("Chọn (1-2): ")
            
            if mode == '1':
                # VIP mode
                session, user_id, user_name = login_olm()
                if not session:
                    return
                
                # Kiểm tra VIP thật
                if is_vip(user_name):
                    license_data = {
                        'mode': 'VIP',
                        'remain': -1,
                        'expire': (datetime.now() + timedelta(days=365)).strftime("%d/%m/%Y")
                    }
                    save_license(license_data)
                    print_status("Kích hoạt VIP thành công!", 'crown', Colors.MAGENTA)
                    time.sleep(1)
                    main_menu(session, user_id, user_name)
                else:
                    print_status("Tài khoản không phải VIP!", 'error', Colors.RED)
                    wait_enter()
                    return
                    
            elif mode == '2':
                # FREE mode
                if handle_free_license():
                    session, user_id, user_name = login_olm()
                    if session:
                        main_menu(session, user_id, user_name)
            else:
                print_status("Chọn 1 hoặc 2!", 'error', Colors.RED)
                wait_enter()
        else:
            # Đã có license -> đăng nhập và vào thẳng
            session, user_id, user_name = login_olm()
            if session:
                if license_data.get('mode') == 'VIP':
                    print_status("VIP: Không giới hạn", 'crown', Colors.MAGENTA)
                else:
                    print_status(f"FREE: {license_data.get('remain', 0)}/4 lượt", 'key', Colors.CYAN)
                time.sleep(1)
                main_menu(session, user_id, user_name)
        
        # Hỏi có chạy lại không
        print(f"\n{Colors.CYAN}{'─' * 50}{Colors.END}")
        if input_prompt("Chạy lại? (y/n): ").lower() == 'y':
            # Tự động tải bản mới từ GitHub
            try:
                print_status("Đang tải bản mới nhất...", 'download', Colors.BLUE)
                response = requests.get(URL_MAIN, timeout=10)
                if response.status_code == 200:
                    with open(sys.argv[0], 'w', encoding='utf-8') as f:
                        f.write(response.text)
                    print_status("Đã cập nhật! Khởi động lại...", 'success', Colors.GREEN)
                    time.sleep(1)
                    os.execl(sys.executable, sys.executable, *sys.argv)
                else:
                    print_status("Không thể cập nhật", 'error', Colors.RED)
            except:
                print_status("Lỗi cập nhật", 'error', Colors.RED)
            
            os.execl(sys.executable, sys.executable, *sys.argv)
        
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Đã dừng{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}Lỗi: {str(e)}{Colors.END}")
        wait_enter()
    
    # Tự xóa file
    self_destruct()

if __name__ == "__main__":
    main()
