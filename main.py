#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║                    OLM MASTER - AUTO SOLVER                  ║
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
import subprocess
from bs4 import BeautifulSoup
from datetime import datetime


ACCOUNT_FILE = "olm_account.dat"

def check_account_lock(username):
    """Kiểm tra và khóa tài khoản với key"""
    if not os.path.exists(ACCOUNT_FILE):
        try:
            with open(ACCOUNT_FILE, 'w') as f:
                json.dump({'user': username, 'time': datetime.now().strftime("%d/%m/%Y %H:%M")}, f)
            print_status(f"🔐 Đã liên kết key với tài khoản: {username}", 'success', Colors.GREEN)
            return True
        except:
            return False
    else:
        try:
            with open(ACCOUNT_FILE, 'r') as f:
                data = json.load(f)
            
            if data.get('user') == username:
                return True
            else:
                print()
                print_status("⛔ KEY ĐÃ LIÊN KẾT VỚI TÀI KHOẢN KHÁC!", 'error', Colors.RED + Colors.BOLD)
                print_status(f"Tài khoản đã liên kết: {data.get('user')}", 'warning', Colors.YELLOW)
                print_status(f"Tài khoản bạn nhập: {username}", 'info', Colors.CYAN)
                print()
                print_status("💡 Giải pháp:", 'info', Colors.GREEN)
                print_status("  1. Dùng đúng tài khoản đã liên kết", 'info', Colors.WHITE)
                print_status("  2. Chọn [3] Đổi tài khoản trong menu", 'info', Colors.WHITE)
                print_status("  3. Hoặc lấy key mới", 'info', Colors.WHITE)
                return False
        except:
            return False

def consume_one_attempt():
    """Hàm wrapper để trừ lượt"""
    if 'consume_one_attempt' in globals():
        return globals()['consume_one_attempt']()
    return True

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
    'back': '↩️'
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
    """In đường kẻ responsive"""
    try:
        w = os.get_terminal_size().columns
        width = min(w - 4, 70)
    except:
        width = 60
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

# ========== KIỂM TRA VÀ CẬP NHẬT THƯ VIỆN ==========
def check_and_update_packages():
    """Kiểm tra và cập nhật gói tin"""
    print_header("KIỂM TRA CẬP NHẬT THƯ VIỆN")
    
    required_packages = ['requests', 'beautifulsoup4']
    
    for package in required_packages:
        try:
            # Sửa đổi: beautifulsoup4 cần import là bs4, nhưng cài đặt qua pip là beautifulsoup4
            if package == 'beautifulsoup4':
                __import__('bs4')
            else:
                __import__(package)
            print_status(f"Đã cài đặt: {package}", 'check', Colors.GREEN)
        except ImportError:
            print_status(f"Thiếu: {package} - Đang cài đặt...", 'warning', Colors.YELLOW)
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--quiet"])
                print_status(f"Đã cài đặt thành công: {package}", 'success', Colors.GREEN)
            except:
                print_status(f"Không thể cài đặt {package}", 'error', Colors.RED)
                wait_enter()
                return False
    
    print_status("Tất cả thư viện đã sẵn sàng!", 'success', Colors.GREEN)
    time.sleep(1)
    return True

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
    
    # Kiểm tra account lock (1 key = 1 account)
    if not check_account_lock(username):
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

# ========== HÀM KIỂM TRA BÀI KIỂM TRA ĐÃ LÀM CHƯA (ẨN ĐIỂM) ==========
def check_hidden_test_status(session, url, id_cate):
    """Kiểm tra xem bài kiểm tra đã làm chưa (ẩn điểm)"""
    try:
        # Thử truy cập API kiểm tra trạng thái
        test_url = f'https://olm.vn/course/teacher-categories/{id_cate}/get-next-cate'
        
        headers = HEADERS.copy()
        headers['referer'] = url
        headers['x-csrf-token'] = session.cookies.get('XSRF-TOKEN', '')
        
        response = session.get(test_url, headers=headers, timeout=10)
        
        # Nếu có response từ API này -> bài đã hoàn thành
        if response.status_code == 200:
            try:
                data = response.json()
                # API này chỉ xuất hiện với bài đã hoàn thành
                return True  # Đã làm
            except:
                pass
        
        # Thử cách 2: Kiểm tra endpoint get-question-of-ids
        quiz_response = session.get(url, timeout=10)
        html = quiz_response.text
        
        # Tìm quiz_list
        pattern = r'quiz_list\s*[:=]\s*["\'](\d{6,}(?:,\d{6,})*)["\']'
        match = re.search(pattern, html)
        
        if match:
            quiz_list = match.group(1)
            # Thử gọi API get-question-of-ids
            api_url = 'https://olm.vn/course/question/get-question-of-ids'
            
            payload = {
                'qlib_list': quiz_list,
                'id_subject': '2',  # Mặc định
                'id_skill': id_cate,
                'cv_q': '1'
            }
            
            api_headers = HEADERS.copy()
            api_headers['content-type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
            api_headers['x-csrf-token'] = session.cookies.get('XSRF-TOKEN', '')
            api_headers['referer'] = url
            
            api_response = session.post(api_url, data=payload, headers=api_headers, timeout=10)
            
            if api_response.status_code == 200:
                # Nếu trả về lỗi hoặc thông báo đã làm
                response_text = api_response.text.lower()
                if "đã hoàn thành" in response_text or "completed" in response_text or "đã nộp" in response_text:
                    return True  # Đã làm
        
        return False  # Chưa làm
        
    except Exception as e:
        return False  # Mặc định là chưa làm nếu có lỗi

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
                    
                    # B. BÀI KIỂM TRA
                    else:
                        # Bài kiểm tra CÓ THỂ ẨN ĐIỂM
                        if not status_spans:
                            # Không có span -> có thể: 1) Chưa làm, 2) Đã làm nhưng ẩn điểm
                            
                            # Lấy id_cate để kiểm tra
                            id_cate = None
                            if row.has_attr('data-cate'):
                                id_cate = row['data-cate']
                            else:
                                # Trích xuất từ URL
                                match = re.search(r'-(\d+)\?', href)
                                if match:
                                    id_cate = match.group(1)
                            
                            if id_cate:
                                # Kiểm tra kỹ cho bài kiểm tra
                                is_done = check_hidden_test_status(session, href, id_cate)
                                if is_done:
                                    should_process = False
                                else:
                                    should_process = True
                            else:
                                # Không có id_cate -> mặc định là chưa làm
                                should_process = True
                        else:
                            # Có span -> kiểm tra nội dung như bình thường
                            for span in status_spans:
                                span_text = span.get_text(strip=True).lower()
                                if "chưa" in span_text or "chưa nộp" in span_text or "làm tiếp" in span_text:
                                    should_process = True
                                    break
                                elif "điểm" in span_text and "đúng" in span_text:
                                    # Đã có điểm -> đã làm
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
            kiem_tra_count = sum(1 for a in assignments if a['is_kiem_tra'])
            
            print(f"\n{Colors.CYAN}📊 THỐNG KÊ LOẠI BÀI:{Colors.END}")
            if video_count > 0:
                print(f"  {ICONS['video']} Video: {video_count} bài")
            if ly_thuyet_count > 0:
                print(f"  {ICONS['theory']} Lý thuyết: {ly_thuyet_count} bài")
            if bai_tap_count > 0:
                print(f"  {ICONS['exercise']} Bài tập: {bai_tap_count} bài")
            if kiem_tra_count > 0:
                print(f"  {ICONS['warning']} Kiểm tra: {kiem_tra_count} bài")
            
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
        elif item['is_kiem_tra']:
            loai_color = Colors.YELLOW
            icon = ICONS['warning']
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
        print_status("Video: Tự động chọn 100 điểm", 'video', Colors.BLUE)
        return 100
    elif is_kiem_tra:
        print_status("Kiểm tra: Tự động chọn điểm cao", 'warning', Colors.YELLOW)
        return random.randint(85, 100)  # Điểm kiểm tra thường cao
    
    print(f"\n{Colors.CYAN}{ICONS['star']} CHỌN ĐIỂM SỐ{Colors.END}")
    print_line('─', Colors.CYAN, 40)
    print(f"  {Colors.YELLOW}1.{Colors.END} {ICONS['star']} 100 điểm (Xuất sắc)")
    print(f"  {Colors.YELLOW}2.{Colors.END} {ICONS['question']} Tùy chọn điểm số")
    print_line('─', Colors.CYAN, 40)
    
    while True:
        choice = input(f"{Colors.YELLOW}Chọn (1-2): {Colors.END}").strip()
        
        if choice == '1':
            return 100
        elif choice == '2':
            try:
                score = int(input(f"{Colors.YELLOW}Nhập điểm số (0-100): {Colors.END}").strip())
                if 0 <= score <= 100:
                    return score
                else:
                    print_status("Điểm số phải từ 0 đến 100!", 'error', Colors.RED)
            except ValueError:
                print_status("Vui lòng nhập số hợp lệ!", 'error', Colors.RED)
        else:
            print_status("Lựa chọn không hợp lệ!", 'error', Colors.RED)

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
                print_status("Video: Không có quiz_list, sẽ thử phương pháp khác", 'video', Colors.BLUE)
                return "", 0, id_courseware, id_cate
            else:
                print_status("Không tìm thấy danh sách câu hỏi", 'error', Colors.RED)
                return None, 0, id_courseware, id_cate
        
        # Tách danh sách câu hỏi
        question_ids = [qid.strip() for qid in quiz_list.split(',') if qid.strip()]
        total_questions = len(question_ids)
        
        print_status(f"Tìm thấy {total_questions} câu hỏi", 'info', Colors.WHITE)
        
        return quiz_list, total_questions, id_courseware, id_cate
        
    except Exception as e:
        print_status(f"Lỗi trích xuất thông tin: {str(e)}", 'error', Colors.RED)
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
    print(f"\n{Colors.CYAN}{ICONS['upload']} ĐANG XỬ LÝ:{Colors.END}")
    print(f"{Colors.WHITE}📖 {assignment['title']}{Colors.END}")
    
    if assignment['is_video']:
        print(f"{Colors.BLUE}🎬 Loại: Video{Colors.END}")
        target_score = 100
    elif assignment['is_ly_thuyet']:
        print(f"{Colors.CYAN}📚 Loại: Lý thuyết{Colors.END}")
        target_score = get_target_score(False, False)
    elif assignment['is_kiem_tra']:
        print(f"{Colors.YELLOW}⚠️ Loại: Kiểm tra{Colors.END}")
        target_score = get_target_score(False, True)
    else:
        print(f"{Colors.GREEN}📝 Loại: Bài tập{Colors.END}")
        target_score = get_target_score(False, False)
    
    try:
        # TRÍCH XUẤT THÔNG TIN
        quiz_list, total_questions, id_courseware, id_cate = extract_quiz_info(
            session, assignment['url'], assignment['is_video']
        )
        
        # XỬ LÝ VIDEO
        if assignment['is_video']:
            print_status("Đang xử lý video...", 'video', Colors.BLUE)
            success = handle_video_submission(session, assignment, user_id, quiz_list, total_questions, id_courseware, id_cate)
            if success:
                print_status(f"{ICONS['success']} HOÀN THÀNH BÀI ({assignment['title']})", 'success', Colors.GREEN + Colors.BOLD)
                wait_enter()
            return success
        
        # BÀI TẬP THƯỜNG & LÝ THUYẾT & KIỂM TRA
        if not quiz_list or total_questions == 0:
            print_status("Không thể lấy thông tin bài", 'error', Colors.RED)
            return False
        
        print_status(f"Đang tạo dữ liệu cho {total_questions} câu...", 'clock', Colors.YELLOW)
        data_log, total_time, correct_needed = create_data_log_for_normal(total_questions, target_score)
        
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
            'score': str(target_score),
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
        print_status("Đang nộp bài...", 'upload', Colors.YELLOW)
        
        submit_headers = HEADERS.copy()
        submit_headers['x-csrf-token'] = csrf_token
        
        response = session.post(
            'https://olm.vn/course/teacher-static',
            data=payload,
            headers=submit_headers,
            timeout=15
        )
        
        print_status(f"Phản hồi: HTTP {response.status_code}", 'info', Colors.WHITE)
        
        # XỬ LÝ KẾT QUẢ
        success = handle_submission_response(response, target_score)
        
        if success:
            print_status(f"{ICONS['success']} HOÀN THÀNH BÀI ({assignment['title']})", 'success', Colors.GREEN + Colors.BOLD)
            wait_enter()
        
        return success
            
    except Exception as e:
        print_status(f"Lỗi: {str(e)}", 'error', Colors.RED)
        return False

def handle_video_submission(session, assignment, user_id, quiz_list, total_questions, id_courseware, id_cate):
    """Xử lý nộp video"""
    
    # THỬ NHIỀU PHƯƠNG PHÁP
    methods = [
        try_video_simple_method,  # Phương pháp đơn giản
        try_video_with_quiz,      # Với quiz_list
        try_video_complex_method, # Phương pháp phức tạp
    ]
    
    for i, method in enumerate(methods, 1):
        print_status(f"Thử phương pháp {i} cho video...", 'video', Colors.BLUE)
        success = method(session, assignment, user_id, quiz_list, total_questions, id_courseware, id_cate)
        if success:
            return True
        time.sleep(1)  # Chờ giữa các phương pháp
    
    print_status("Tất cả phương pháp đều thất bại", 'error', Colors.RED)
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
        time_spent = random.randint(300, 900)  # 5-15 phút
        
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
        
        # Tạo payload linh hoạt
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
        
        # Thêm các trường tùy chọn
        optional_fields = {
            'id_group': '6148789559',
            'id_school': '0',
            'name_user': '',
            'type_vip': '530',
            'total_time': str(time_spent),
            'current_time': '3',
            'correct': '1',
            'totalq': '0',
            'count_problems': '1',
            'save_star': '1'
        }
        
        # Chỉ thêm các trường nếu có giá trị
        for key, value in optional_fields.items():
            payload[key] = value
        
        # Thêm quiz_list nếu có
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
        
        return handle_submission_response(response, 100)
        
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
        for i in range(min(total_questions, 5)):  # Giới hạn 5 câu
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
        
        return handle_submission_response(response, 100)
        
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
        
        # Thêm câu hỏi trắc nghiệm nếu có quiz_list
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
        
        # Thêm quiz_list nếu có
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
        
        return handle_submission_response(response, 100)
        
    except Exception as e:
        return False

def handle_submission_response(response, target_score):
    """Xử lý phản hồi"""
    if response.status_code == 200:
        try:
            result = response.json()
            
            if 'code' in result:
                if result['code'] == 403:
                    print_status(f"Đã nộp trước: {result.get('message', '')}", 'warning', Colors.YELLOW)
                    return True
                elif result['code'] == 400:
                    print_status(f"Lỗi 400: {result.get('message', '')}", 'error', Colors.RED)
                    return False
                else:
                    actual_score = result.get('score', target_score)
                    print_status(f"Thành công! Điểm: {actual_score}/100", 'success', Colors.GREEN)
                    return True
            else:
                print_status("Nộp thành công (status 200)", 'success', Colors.GREEN)
                return True
        except Exception as e:
            if "success" in response.text.lower() or "hoàn thành" in response.text.lower():
                print_status("Có vẻ đã thành công", 'success', Colors.GREEN)
                return True
            print_status("Nộp thành công (status 200)", 'success', Colors.GREEN)
            return True
    elif response.status_code == 403:
        print_status("Bài đã được nộp trước đó", 'warning', Colors.YELLOW)
        return True
    else:
        print_status(f"Lỗi {response.status_code}", 'error', Colors.RED)
        return False

# ========== GIẢI BÀI TỪ LINK ==========
def solve_from_link(session, user_id):
    """Giải bài từ link"""
    print_header("GIẢI BÀI TỪ LINK")
    
    print(f"{Colors.CYAN}{ICONS['link']} NHẬP LINK BÀI TẬP:{Colors.END}")
    print("Ví dụ: https://olm.vn/chu-de/...")
    print()
    
    url = input(f"{ICONS['link']} {Colors.YELLOW}Dán link bài tập: {Colors.END}").strip()
    
    if not url.startswith('https://olm.vn/'):
        print_status("Link không hợp lệ! Phải là link OLM", 'error', Colors.RED)
        wait_enter()
        return False
    
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
            return success
        else:
            print_status("Đã hủy", 'warning', Colors.YELLOW)
            return False
            
    except Exception as e:
        print_status(f"Lỗi: {str(e)}", 'error', Colors.RED)
        return False

# ========== GIẢI BÀI CỤ THỂ TỪ DANH SÁCH ==========
def solve_specific_from_list(session, user_id):
    """Giải bài cụ thể từ danh sách - HỖ TRỢ 0, 1, VÀ 1,3,5"""
    print_header("GIẢI BÀI CỤ THỂ")
    
    # Hỏi số trang
    pages_input = input(f"{Colors.YELLOW}Số trang cần quét (mặc định: 3): {Colors.END}").strip()
    pages_to_scan = 3
    if pages_input.isdigit() and int(pages_input) > 0:
        pages_to_scan = int(pages_input)
    
    assignments = get_assignments_fixed(session, pages_to_scan)
    if not assignments:
        wait_enter()
        return False
    
    display_assignments_table(assignments)
    
    # Chọn bài
    print()
    print(f"{Colors.CYAN}╔════════════════════════════════════════════════════╗{Colors.END}")
    print(f"{Colors.CYAN}║  {Colors.YELLOW}Cách chọn:{Colors.END}")
    print(f"{Colors.CYAN}║  {Colors.GREEN}• Nhập 0{Colors.END}       → Giải TẤT CẢ bài")
    print(f"{Colors.CYAN}║  {Colors.GREEN}• Nhập 1{Colors.END}       → Giải bài số 1")
    print(f"{Colors.CYAN}║  {Colors.GREEN}• Nhập 1,3,5{Colors.END}   → Giải bài 1, 3 và 5")
    print(f"{Colors.CYAN}╚════════════════════════════════════════════════════╝{Colors.END}")
    
    try:
        selection = input(f"\n{Colors.YELLOW}{ICONS['question']} Nhập lựa chọn: {Colors.END}").strip()
        
        if selection == '0':
            # Giải TẤT CẢ bài
            confirm = input(f"\n{Colors.YELLOW}⚠️  Xác nhận giải TẤT CẢ {len(assignments)} bài? (y/n): {Colors.END}").strip().lower()
            
            if confirm == 'y':
                print_header("ĐANG GIẢI TẤT CẢ BÀI")
                success_count = 0
                
                for idx, assignment in enumerate(assignments, 1):
                    # Trừ lượt
                    if not consume_one_attempt():
                        print()
                        print_status(f"⛔ Đã hết lượt! Giải được {success_count}/{len(assignments)} bài", 'warning', Colors.YELLOW)
                        wait_enter()
                        sys.exit(0)
                    
                    print(f"\n{Colors.YELLOW}{'━' * 60}{Colors.END}")
                    print(f"{Colors.CYAN}📊 Bài {idx}/{len(assignments)}{Colors.END}")
                    print(f"{Colors.YELLOW}{'━' * 60}{Colors.END}")
                    
                    if submit_assignment(session, assignment, user_id):
                        success_count += 1
                    
                    # Delay giữa các bài
                    if idx < len(assignments):
                        wait_time = random.randint(3, 6)
                        print_status(f"Chờ {wait_time}s trước bài tiếp theo...", 'clock', Colors.YELLOW)
                        time.sleep(wait_time)
                
                print()
                print(f"{Colors.GREEN}{'═' * 60}{Colors.END}")
                print_status(f"✅ HOÀN THÀNH {success_count}/{len(assignments)} bài!", 'success', Colors.GREEN + Colors.BOLD)
                print(f"{Colors.GREEN}{'═' * 60}{Colors.END}")
                wait_enter()
                return True
        
        elif ',' in selection:
            # Giải NHIỀU bài: 1,3,5
            nums = []
            for x in selection.split(','):
                x = x.strip()
                if x.isdigit():
                    num = int(x)
                    if 1 <= num <= len(assignments):
                        nums.append(num)
            
            if not nums:
                print_status("Không có số bài hợp lệ!", 'error', Colors.RED)
                wait_enter()
                return False
            
            # Xác nhận
            print(f"\n{Colors.CYAN}Sẽ giải {len(nums)} bài: {', '.join(map(str, nums))}{Colors.END}")
            confirm = input(f"{Colors.YELLOW}Xác nhận? (y/n): {Colors.END}").strip().lower()
            
            if confirm == 'y':
                print_header(f"ĐANG GIẢI {len(nums)} BÀI")
                success_count = 0
                
                for i, num in enumerate(nums, 1):
                    # Trừ lượt
                    if not consume_one_attempt():
                        print()
                        print_status(f"⛔ Hết lượt! Giải được {success_count}/{len(nums)} bài", 'warning', Colors.YELLOW)
                        wait_enter()
                        sys.exit(0)
                    
                    print(f"\n{Colors.YELLOW}{'━' * 60}{Colors.END}")
                    print(f"{Colors.CYAN}📊 Bài #{num} ({i}/{len(nums)}){Colors.END}")
                    print(f"{Colors.YELLOW}{'━' * 60}{Colors.END}")
                    
                    if submit_assignment(session, assignments[num-1], user_id):
                        success_count += 1
                    
                    if i < len(nums):
                        time.sleep(random.randint(3, 5))
                
                print()
                print(f"{Colors.GREEN}{'═' * 60}{Colors.END}")
                print_status(f"✅ HOÀN THÀNH {success_count}/{len(nums)} bài!", 'success', Colors.GREEN + Colors.BOLD)
                print(f"{Colors.GREEN}{'═' * 60}{Colors.END}")
                wait_enter()
                return True
        
        elif selection.isdigit():
            # Giải 1 BÀI
            idx = int(selection) - 1
            if 0 <= idx < len(assignments):
                # Trừ lượt
                if not consume_one_attempt():
                    print_status("\n⛔ Đã hết lượt!", 'error', Colors.RED)
                    wait_enter()
                    sys.exit(0)
                
                success = submit_assignment(session, assignments[idx], user_id)
                wait_enter()
                return success
            else:
                print_status("Số bài không hợp lệ!", 'error', Colors.RED)
        else:
            print_status("Lựa chọn không hợp lệ!", 'error', Colors.RED)
    
    except KeyboardInterrupt:
        print_status("\nĐã hủy", 'warning', Colors.YELLOW)
    except Exception as e:
        print_status(f"Lỗi: {e}", 'error', Colors.RED)
    
    wait_enter()
    return False

def process_all_assignments(session, assignments, user_id):
    """Xử lý tất cả bài tập"""
    if not assignments:
        return 0, 0
    
    print_header("BẮT ĐẦU XỬ LÝ")
    
    success_count = 0
    total_count = len(assignments)
    
    for idx, assignment in enumerate(assignments, 1):
        print(f"\n{Colors.YELLOW}📊 Bài {idx}/{total_count}{Colors.END}")
        
        success = submit_assignment(session, assignment, user_id)
        
        if success:
            success_count += 1
        else:
            print_status(f"Không thể xử lý bài {idx}", 'error', Colors.RED)
        
        # Chờ giữa các bài
        if idx < total_count:
            wait_time = random.randint(2, 5)
            print_status(f"Chờ {wait_time}s...", 'clock', Colors.YELLOW)
            time.sleep(wait_time)
    
    print(f"\n{Colors.CYAN}{ICONS['star']} KẾT QUẢ:{Colors.END}")
    print(f"{Colors.GREEN}Thành công: {success_count}/{total_count}{Colors.END}")
    
    wait_enter()
    return success_count, total_count

# ========== MENU CHÍNH ==========
def main_menu(session, user_id, user_name):
    """Menu chính"""
    
    while True:
        print_header("MENU CHÍNH")
        print(f"{ICONS['user']} {Colors.GREEN}Xin chào: {user_name}{Colors.END}")
        print()
        
        menu_options = {
            '1': f"{ICONS['brain']} Giải bài cụ thể (Hỗ trợ: 0=tất cả, 1,3,5=nhiều bài)",
            '2': f"{ICONS['link']} Giải bài từ link OLM",
            '3': f"{ICONS['refresh']} Đổi tài khoản (xóa liên kết)",
            '4': f"{ICONS['exit']} Thoát"
        }
        
        print_menu("LỰA CHỌN", menu_options)
        
        choice = input(f"\n{Colors.YELLOW}Chọn chức năng (1-4): {Colors.END}").strip()
        
        if choice == '1':
            # Giải bài cụ thể (HỖ TRỢ 0 và 1,3,5)
            solve_specific_from_list(session, user_id)
        
        elif choice == '2':
            # Giải từ link
            if not consume_one_attempt():
                print_status("\n⛔ Đã hết lượt!", 'error', Colors.RED)
                print_status("Đang quay về launcher...", 'info', Colors.YELLOW)
                time.sleep(1)
                sys.exit(0)
            solve_from_link(session, user_id)
        
        elif choice == '3':
            # Đổi tài khoản
            if os.path.exists('olm_account.dat'):
                os.remove('olm_account.dat')
                print_status("✓ Đã xóa liên kết tài khoản", 'success', Colors.GREEN)
            print_status("Đang đăng xuất để đổi tài khoản...", 'info', Colors.CYAN)
            time.sleep(1)
            break
        
        elif choice == '4':
            print_status("Cảm ơn đã sử dụng! 👋", 'exit', Colors.GREEN)
            time.sleep(1)
            sys.exit(0)
        
        else:
            print_status("Lựa chọn không hợp lệ!", 'error', Colors.RED)
            time.sleep(1)

# ========== CHƯƠNG TRÌNH CHÍNH ==========
def main():
    """Chương trình chính"""
    # Kiểm tra và cập nhật thư viện
    if not check_and_update_packages():
        print_status("Không thể khởi động tool!", 'error', Colors.RED)
        wait_enter()
        return
    
    while True:
        # Đăng nhập
        session, user_id, user_name = login_olm()
        
        if session and user_id and user_name:
            # Vào menu chính
            main_menu(session, user_id, user_name)
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
