#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║                    OLM MASTER PRO - MAIN                     ║
║                    Created by: Tuấn Anh                      ║
╚══════════════════════════════════════════════════════════════╝
"""

import os
import sys
import time
import json
import random
import pickle
import hashlib
import base64
import requests
import re
from datetime import datetime, timedelta
from pathlib import Path

# ========== CẤU HÌNH MÀU SẮC SIÊU RỰC RỠ ==========
class Colors:
    # Màu cơ bản
    BLACK = '\033[30m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    
    # Màu đậm
    BOLD = '\033[1m'
    DIM = '\033[2m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    
    # Màu nền
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    
    # Kết thúc
    END = '\033[0m'

# Bộ icon đẹp lung linh
ICONS = {
    # Trạng thái
    'success': '✅',
    'error': '❌',
    'warning': '⚠️',
    'info': 'ℹ️',
    'question': '❓',
    'waiting': '⏳',
    
    # Đối tượng
    'user': '👤',
    'key': '🔑',
    'lock': '🔐',
    'crown': '👑',
    'star': '⭐',
    'diamond': '💎',
    'heart': '❤️',
    'fire': '🔥',
    'rocket': '🚀',
    'magic': '✨',
    'brain': '🧠',
    'robot': '🤖',
    
    # Hành động
    'download': '📥',
    'upload': '📤',
    'refresh': '🔄',
    'exit': '🚪',
    'back': '↩️',
    'next': '➡️',
    'check': '✔️',
    'cross': '✖️',
    'plus': '➕',
    'minus': '➖',
    
    # Nội dung
    'video': '🎬',
    'book': '📚',
    'theory': '📖',
    'exercise': '📝',
    'test': '📋',
    'link': '🔗',
    'list': '📊',
    'clock': '⏰',
    'calendar': '📅',
    'trophy': '🏆',
    
    # Trang trí
    'flower': '🌸',
    'sparkle': '✨',
    'zap': '⚡',
    'gear': '⚙️',
    'search': '🔍',
    'home': '🏠'
}

# ========== TIỆN ÍCH HIỂN THỊ SIÊU ĐẸP ==========
def clear_screen():
    """Xóa màn hình đẹp"""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_terminal_width():
    """Lấy chiều rộng terminal"""
    try:
        cols = os.get_terminal_size().columns
        return min(cols, 80)
    except:
        return 70

def print_separator(char='═', color=Colors.CYAN, width=None):
    """In đường kẻ đẹp"""
    if width is None:
        width = get_terminal_width()
    print(f"{color}{char * width}{Colors.END}")

def print_centered(text, color=Colors.WHITE, width=None):
    """In text căn giữa có màu"""
    if width is None:
        width = get_terminal_width()
    clean_text = re.sub(r'\033\[[0-9;]*m', '', text)
    padding = max(0, (width - len(clean_text)) // 2)
    print(f"{color}{' ' * padding}{text}{Colors.END}")

def print_double_line():
    """In đường kẻ đôi đẹp"""
    width = get_terminal_width()
    print(f"{Colors.MAGENTA}╔{'═' * (width - 2)}╗{Colors.END}")

def print_header(title=""):
    """In header siêu đẹp"""
    clear_screen()
    width = get_terminal_width()
    
    # Header trên
    print(f"{Colors.CYAN}{Colors.BOLD}╔{'═' * (width - 2)}╗{Colors.END}")
    
    # Dòng 1 - Logo
    logo = f"{ICONS['rocket']}  OLM MASTER PRO  {ICONS['crown']}"
    padding1 = (width - 2 - len(logo)) // 2
    padding2 = width - 2 - len(logo) - padding1
    print(f"{Colors.CYAN}║{Colors.END}{Colors.YELLOW}{Colors.BOLD}{' ' * padding1}{logo}{' ' * padding2}{Colors.END}{Colors.CYAN}║{Colors.END}")
    
    # Dòng 2 - Creator
    creator = "Created by: Tuấn Anh"
    padding1 = (width - 2 - len(creator)) // 2
    padding2 = width - 2 - len(creator) - padding1
    print(f"{Colors.CYAN}║{Colors.END}{Colors.MAGENTA}{' ' * padding1}{creator}{' ' * padding2}{Colors.END}{Colors.CYAN}║{Colors.END}")
    
    # Dòng 3 - Thời gian
    current_time = datetime.now().strftime("%H:%M:%S %d/%m/%Y")
    padding1 = (width - 2 - len(current_time)) // 2
    padding2 = width - 2 - len(current_time) - padding1
    print(f"{Colors.CYAN}║{Colors.END}{Colors.CYAN}{' ' * padding1}{current_time}{' ' * padding2}{Colors.END}{Colors.CYAN}║{Colors.END}")
    
    # Header dưới
    if title:
        print(f"{Colors.CYAN}╠{'═' * (width - 2)}╣{Colors.END}")
        padding1 = (width - 2 - len(title)) // 2
        padding2 = width - 2 - len(title) - padding1
        print(f"{Colors.CYAN}║{Colors.END}{Colors.GREEN}{Colors.BOLD}{' ' * padding1}{title}{' ' * padding2}{Colors.END}{Colors.CYAN}║{Colors.END}")
    
    print(f"{Colors.CYAN}╚{'═' * (width - 2)}╝{Colors.END}")
    print()

def print_menu(title, options):
    """In menu đẹp"""
    width = get_terminal_width()
    print(f"\n{Colors.YELLOW}{Colors.BOLD}╔{'═' * (width - 10)}╗{Colors.END}")
    print(f"{Colors.YELLOW}{Colors.BOLD}║{Colors.END}{Colors.CYAN}{Colors.BOLD}  {ICONS['list']} {title.upper():^{width-15}}{Colors.END}{Colors.YELLOW}{Colors.BOLD}║{Colors.END}")
    print(f"{Colors.YELLOW}{Colors.BOLD}╠{'═' * (width - 10)}╣{Colors.END}")
    
    for key, value in options.items():
        print(f"{Colors.YELLOW}{Colors.BOLD}║{Colors.END}  {Colors.GREEN}{key}.{Colors.END} {value:<{width-17}} {Colors.YELLOW}{Colors.BOLD}║{Colors.END}")
    
    print(f"{Colors.YELLOW}{Colors.BOLD}╚{'═' * (width - 10)}╝{Colors.END}")

def print_status(message, icon='info', color=Colors.WHITE, bold=False):
    """In thông báo trạng thái đẹp"""
    bold_tag = Colors.BOLD if bold else ''
    print(f"{bold_tag}{color}{ICONS.get(icon, '•')} {message}{Colors.END}")

def print_progress(current, total, prefix='Đang xử lý', suffix='Hoàn thành', length=40):
    """In progress bar đẹp"""
    percent = (current / total) * 100
    filled_length = int(length * current // total)
    bar = '█' * filled_length + '░' * (length - filled_length)
    
    # Màu theo tiến độ
    if percent < 30:
        color = Colors.RED
    elif percent < 70:
        color = Colors.YELLOW
    else:
        color = Colors.GREEN
    
    print(f"\r{color}{prefix} |{bar}| {current}/{total} ({percent:.1f}%) {suffix}{Colors.END}", end='')
    if current == total:
        print()

def input_prompt(prompt, icon='question', color=Colors.YELLOW):
    """Input có icon đẹp"""
    return input(f"{color}{Colors.BOLD}{ICONS.get(icon, '•')} {prompt}{Colors.END} ").strip()

def wait_enter():
    """Chờ nhấn Enter"""
    input_prompt("Nhấn Enter để tiếp tục...", 'info')

def animate_text(text, color=Colors.CYAN, delay=0.03):
    """Hiệu ứng chữ chạy"""
    for char in text:
        print(f"{color}{char}{Colors.END}", end='', flush=True)
        time.sleep(delay)
    print()

def spinner_animation(message, duration=2):
    """Hiệu ứng spinner"""
    spinner = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    end_time = time.time() + duration
    i = 0
    print(f"{Colors.CYAN}{message}{Colors.END} ", end='', flush=True)
    while time.time() < end_time:
        print(f"\r{Colors.MAGENTA}{message} {spinner[i % len(spinner)]}{Colors.END}", end='', flush=True)
        i += 1
        time.sleep(0.1)
    print(f"\r{Colors.GREEN}{message} {ICONS['check']}{Colors.END}" + ' ' * 20)

# ========== QUẢN LÝ SESSION VÀ LICENSE ==========
def load_session():
    """Tải session từ file"""
    session_file = os.environ.get('OLM_SESSION_FILE')
    if not session_file or not os.path.exists(session_file):
        print_status("Không tìm thấy session!", 'error', Colors.RED, True)
        sys.exit(1)
    
    try:
        with open(session_file, 'rb') as f:
            session_data = pickle.load(f)
        
        session = requests.Session()
        session.cookies.update(session_data.get('cookies', {}))
        session.headers.update({
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'x-requested-with': 'XMLHttpRequest',
        })
        
        return session, session_data.get('user_id'), session_data.get('user_name')
    except Exception as e:
        print_status(f"Lỗi tải session: {e}", 'error', Colors.RED, True)
        sys.exit(1)

def load_license():
    """Tải thông tin license"""
    license_file = os.environ.get('OLM_LICENSE_FILE')
    if not license_file or not os.path.exists(license_file):
        print_status("Không tìm thấy license!", 'error', Colors.RED, True)
        return None
    
    try:
        with open(license_file, 'r') as f:
            encrypted = f.read()
        
        # Giải mã
        data = decrypt_data(encrypted)
        if data and verify_license(data):
            return data
    except:
        pass
    
    return None

def decrypt_data(encrypted_str):
    """Giải mã dữ liệu"""
    try:
        SECRET_KEY = b'OLM_MASTER_PRO_2026_SECRET_KEY_42'
        noise_len = 8
        prefix = encrypted_str[:noise_len]
        suffix = encrypted_str[-noise_len:]
        if suffix != prefix[::-1]:
            return None
        content = encrypted_str[noise_len:-noise_len]
        checksum = content[:12]
        b85_data = content[12:]
        if hashlib.sha256(b85_data.encode()).hexdigest()[:12] != checksum:
            return None
        xor_data = base64.b85decode(b85_data)
        bytes_data = bytes(b ^ SECRET_KEY[i % len(SECRET_KEY)] for i, b in enumerate(xor_data))
        return json.loads(bytes_data.decode())
    except:
        return None

def verify_license(data):
    """Xác thực license"""
    try:
        sig_expected = hashlib.sha256(f"{data.get('mode', '')}{data.get('expire', '')}{data.get('ip', '')}".encode()).hexdigest()
        return data.get('sig') == sig_expected
    except:
        return False

def is_vip():
    """Kiểm tra VIP"""
    license_data = load_license()
    return license_data and license_data.get('mode') == 'VIP'

def get_remaining_attempts():
    """Lấy số lượt còn lại"""
    license_data = load_license()
    if not license_data:
        return 0
    if license_data.get('mode') == 'VIP':
        return float('inf')
    return license_data.get('remain', 0)

def decrement_attempts():
    """Giảm số lượt (FREE)"""
    license_data = load_license()
    if not license_data or license_data.get('mode') == 'VIP':
        return True
    
    remain = license_data.get('remain', 0)
    if remain <= 0:
        return False
    
    license_data['remain'] = remain - 1
    
    # Mã hóa lại
    SECRET_KEY = b'OLM_MASTER_PRO_2026_SECRET_KEY_42'
    json_str = json.dumps(license_data)
    bytes_data = json_str.encode()
    xor_data = bytearray(b ^ SECRET_KEY[i % len(SECRET_KEY)] for i, b in enumerate(bytes_data))
    b85_data = base64.b85encode(xor_data).decode()
    checksum = hashlib.sha256(b85_data.encode()).hexdigest()[:12]
    noise_prefix = hashlib.md5(os.urandom(16)).hexdigest()[:8]
    noise_suffix = noise_prefix[::-1]
    encrypted = f"{noise_prefix}{checksum}{b85_data}{noise_suffix}"
    
    license_file = os.environ.get('OLM_LICENSE_FILE')
    if license_file:
        with open(license_file, 'w') as f:
            f.write(encrypted)
    
    return True

def display_license_info():
    """Hiển thị thông tin license"""
    license_data = load_license()
    if not license_data:
        print_status("Không có thông tin license!", 'warning', Colors.YELLOW)
        return
    
    mode = license_data.get('mode', 'UNKNOWN')
    remain = license_data.get('remain', 0)
    expire = license_data.get('expire', 'N/A')
    
    width = get_terminal_width()
    print(f"\n{Colors.CYAN}╔{'═' * (width - 10)}╗{Colors.END}")
    print(f"{Colors.CYAN}║{Colors.END}{Colors.YELLOW}{Colors.BOLD}  {ICONS['lock']} THÔNG TIN LICENSE{' ' * (width - 30)}{Colors.END}{Colors.CYAN}║{Colors.END}")
    print(f"{Colors.CYAN}╠{'═' * (width - 10)}╣{Colors.END}")
    
    if mode == 'VIP':
        print(f"{Colors.CYAN}║{Colors.END}  {Colors.MAGENTA}Loại:{Colors.END} {Colors.GREEN}{Colors.BOLD}VIP UNLIMITED {ICONS['crown']}{Colors.END}{' ' * (width - 30)}{Colors.CYAN}║{Colors.END}")
        print(f"{Colors.CYAN}║{Colors.END}  {Colors.MAGENTA}Hạn dùng:{Colors.END} {Colors.CYAN}{expire}{Colors.END}{' ' * (width - 30)}{Colors.CYAN}║{Colors.END}")
        print(f"{Colors.CYAN}║{Colors.END}  {Colors.MAGENTA}Lượt còn:{Colors.END} {Colors.GREEN}{ICONS['infinity']} Không giới hạn{Colors.END}{' ' * (width - 38)}{Colors.CYAN}║{Colors.END}")
    else:
        print(f"{Colors.CYAN}║{Colors.END}  {Colors.MAGENTA}Loại:{Colors.END} {Colors.YELLOW}FREE (4 lượt){Colors.END}{' ' * (width - 28)}{Colors.CYAN}║{Colors.END}")
        print(f"{Colors.CYAN}║{Colors.END}  {Colors.MAGENTA}Hạn dùng:{Colors.END} {Colors.CYAN}{expire}{Colors.END}{' ' * (width - 25)}{Colors.CYAN}║{Colors.END}")
        print(f"{Colors.CYAN}║{Colors.END}  {Colors.MAGENTA}Lượt còn:{Colors.END} {Colors.GREEN if remain > 0 else Colors.RED}{remain}/4{Colors.END}{' ' * (width - 28)}{Colors.CYAN}║{Colors.END}")
    
    print(f"{Colors.CYAN}╚{'═' * (width - 10)}╝{Colors.END}")

# ========== KIỂM TRA BÀI KIỂM TRA ẨN ĐIỂM ==========
def check_hidden_test_status(session, url, id_cate):
    """Kiểm tra bài kiểm tra đã làm chưa (ẩn điểm)"""
    try:
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'x-csrf-token': session.cookies.get('XSRF-TOKEN', ''),
            'referer': url
        }
        
        # Thử API get-next-cate
        test_url = f'https://olm.vn/course/teacher-categories/{id_cate}/get-next-cate'
        response = session.get(test_url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            try:
                response.json()
                return True  # Đã làm
            except:
                pass
        
        # Thử API get-question-of-ids
        quiz_response = session.get(url, timeout=5)
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
            
            api_response = session.post(api_url, data=payload, headers=headers, timeout=5)
            
            if api_response.status_code == 200:
                response_text = api_response.text.lower()
                if "đã hoàn thành" in response_text or "đã nộp" in response_text:
                    return True
        
        return False
        
    except Exception:
        return False

# ========== QUÉT BÀI TẬP ==========
def get_assignments(session, pages_to_scan=5):
    """Lấy danh sách bài tập cần làm"""
    print_header(f"QUÉT BÀI TẬP ({pages_to_scan} TRANG)")
    print_status("Đang quét danh sách bài tập...", 'search', Colors.CYAN)
    
    assignments = []
    seen_links = set()
    
    # Progress bar
    for page in range(1, pages_to_scan + 1):
        print_progress(page, pages_to_scan, f"Trang {page}/{pages_to_scan}")
        
        if page == 1:
            url = "https://olm.vn/lop-hoc-cua-toi?action=login"
        else:
            url = f"https://olm.vn/lop-hoc-cua-toi/page-{page}?action=login"
        
        try:
            response = session.get(url, timeout=8)
            if response.status_code != 200:
                continue
            
            soup = BeautifulSoup(response.text, 'html.parser')
            rows = soup.find_all('tr', class_='my-gived-courseware-item')
            
            for row in rows:
                # Tìm link bài tập
                link_tags = row.find_all('a', class_='olm-text-link')
                if not link_tags:
                    continue
                
                main_link = link_tags[0]
                href = main_link.get('href')
                link_text = main_link.get_text(strip=True)
                
                # Bỏ qua link môn học
                if href and ('(Toán' in link_text or '(Ngữ văn' in link_text):
                    continue
                
                if not href:
                    continue
                
                # Lấy loại bài
                tds = row.find_all('td')
                if len(tds) < 2:
                    continue
                
                loai_raw = tds[1].get_text(strip=True)
                
                # Xác định loại
                is_video = "[Video]" in loai_raw or "Video" in loai_raw
                is_ly_thuyet = "[Lý thuyết]" in loai_raw or "Ly thuyet" in loai_raw
                is_kiem_tra = "[Kiểm tra]" in loai_raw or "[Kiem tra]" in loai_raw
                is_tu_luan = "[Tự luận]" in loai_raw or "[Tu luan]" in loai_raw
                
                # Bỏ qua bài tự luận
                if is_tu_luan:
                    continue
                
                # Kiểm tra trạng thái
                status_spans = row.find_all('span', class_='message-static-item')
                if not status_spans:
                    status_spans = row.find_all('span', class_='alert-warning')
                
                should_process = False
                
                if is_kiem_tra:
                    # Bài kiểm tra (có thể ẩn điểm)
                    id_cate = row.get('data-cate')
                    if not id_cate:
                        match = re.search(r'-(\d+)\?', href)
                        id_cate = match.group(1) if match else None
                    
                    if id_cate:
                        is_done = check_hidden_test_status(session, href, id_cate)
                        should_process = not is_done
                    else:
                        should_process = True
                else:
                    # Bài thường
                    if not status_spans:
                        should_process = True
                    else:
                        for span in status_spans:
                            span_text = span.get_text(strip=True).lower()
                            if "chưa" in span_text or "làm tiếp" in span_text:
                                should_process = True
                                break
                            elif "điểm" in span_text and "đúng" in span_text:
                                should_process = False
                                break
                
                if should_process and href not in seen_links:
                    seen_links.add(href)
                    
                    # Lấy môn học
                    mon = row.find('span', class_='alert')
                    mon_text = mon.get_text(strip=True) if mon else "Khác"
                    
                    ten_bai = re.sub(r'\([^)]*\)', '', link_text).strip()
                    
                    # Xác định trạng thái
                    status = "Chưa làm"
                    if status_spans:
                        for span in status_spans:
                            span_text = span.get_text(strip=True)
                            if "chưa" in span_text.lower() or "làm tiếp" in span_text.lower():
                                status = span_text
                                break
                    
                    # Xây dựng URL đầy đủ
                    full_url = 'https://olm.vn' + href if not href.startswith('http') else href
                    
                    assignments.append({
                        'title': ten_bai[:60],
                        'subject': mon_text[:20],
                        'type': loai_raw.replace('[', '').replace(']', '').strip()[:20],
                        'status': status,
                        'url': full_url,
                        'page': page,
                        'is_video': is_video,
                        'is_ly_thuyet': is_ly_thuyet,
                        'is_kiem_tra': is_kiem_tra
                    })
        
        except Exception as e:
            print_status(f"Lỗi trang {page}: {str(e)}", 'error', Colors.RED)
            continue
    
    print()  # Xuống dòng sau progress bar
    
    if assignments:
        # Thống kê
        video_count = sum(1 for a in assignments if a['is_video'])
        theory_count = sum(1 for a in assignments if a['is_ly_thuyet'])
        test_count = sum(1 for a in assignments if a['is_kiem_tra'])
        exercise_count = len(assignments) - video_count - theory_count - test_count
        
        print(f"\n{Colors.GREEN}{Colors.BOLD}📊 THỐNG KÊ:{Colors.END}")
        print(f"  {ICONS['video']} Video: {video_count}")
        print(f"  {ICONS['theory']} Lý thuyết: {theory_count}")
        print(f"  {ICONS['exercise']} Bài tập: {exercise_count}")
        print(f"  {ICONS['test']} Kiểm tra: {test_count}")
        print(f"  {Colors.CYAN}Tổng cộng: {len(assignments)} bài{Colors.END}")
    else:
        print_status("Không tìm thấy bài tập nào cần làm!", 'warning', Colors.YELLOW)
    
    return assignments

def display_assignments_table(assignments):
    """Hiển thị danh sách bài tập dạng bảng đẹp"""
    if not assignments:
        return
    
    width = get_terminal_width()
    
    print(f"\n{Colors.MAGENTA}{Colors.BOLD}╔{'═' * (width - 10)}╗{Colors.END}")
    print(f"{Colors.MAGENTA}{Colors.BOLD}║{Colors.END}{Colors.YELLOW}{Colors.BOLD}  {ICONS['list']} DANH SÁCH BÀI TẬP{' ' * (width - 35)}{Colors.END}{Colors.MAGENTA}{Colors.BOLD}║{Colors.END}")
    print(f"{Colors.MAGENTA}{Colors.BOLD}╠{'═' * (width - 10)}╣{Colors.END}")
    
    for idx, item in enumerate(assignments, 1):
        # Rút gọn title
        title = item['title']
        if len(title) > 30:
            title = title[:27] + "..."
        
        # Icon theo loại
        if item['is_video']:
            icon = ICONS['video']
            type_color = Colors.BLUE
        elif item['is_ly_thuyet']:
            icon = ICONS['theory']
            type_color = Colors.CYAN
        elif item['is_kiem_tra']:
            icon = ICONS['test']
            type_color = Colors.YELLOW
        else:
            icon = ICONS['exercise']
            type_color = Colors.GREEN
        
        # Màu trạng thái
        if "Chưa làm" in item['status']:
            status_color = Colors.RED
        elif "làm tiếp" in item['status'].lower():
            status_color = Colors.YELLOW
        else:
            status_color = Colors.WHITE
        
        # In dòng
        line = f"  {Colors.YELLOW}{idx:>2}.{Colors.END} "
        line += f"{type_color}{icon} {item['type']:<10}{Colors.END} "
        line += f"{Colors.WHITE}{item['subject']:<12}{Colors.END} "
        line += f"{Colors.WHITE}{title:<30}{Colors.END} "
        line += f"{status_color}{item['status']:<15}{Colors.END}"
        
        print(line)
    
    print(f"{Colors.MAGENTA}{Colors.BOLD}╚{'═' * (width - 10)}╝{Colors.END}")

# ========== XỬ LÝ BÀI TẬP ==========
def get_target_score(is_video=False, is_kiem_tra=False):
    """Chọn điểm số"""
    if is_video:
        print_status("Video: Tự động chọn 100 điểm", 'video', Colors.BLUE)
        return 100
    
    if is_kiem_tra:
        print_status("Kiểm tra: Tự động chọn điểm cao", 'test', Colors.YELLOW)
        return random.randint(85, 100)
    
    print(f"\n{Colors.CYAN}{Colors.BOLD}╔{'═' * 38}╗{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}║{Colors.END}{Colors.YELLOW}{Colors.BOLD}  {ICONS['star']} CHỌN ĐIỂM SỐ{' ' * 25}{Colors.END}{Colors.CYAN}{Colors.BOLD}║{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}╠{'═' * 38}╣{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}║{Colors.END}  {Colors.GREEN}1.{Colors.END} 100 điểm (Xuất sắc)       {Colors.CYAN}{Colors.BOLD}║{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}║{Colors.END}  {Colors.GREEN}2.{Colors.END} Tùy chọn điểm số         {Colors.CYAN}{Colors.BOLD}║{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}╚{'═' * 38}╝{Colors.END}")
    
    while True:
        choice = input_prompt("Chọn (1-2): ", 'question')
        
        if choice == '1':
            return 100
        elif choice == '2':
            try:
                score = int(input_prompt("Nhập điểm (0-100): ", 'key'))
                if 0 <= score <= 100:
                    return score
                print_status("Điểm phải từ 0-100!", 'error', Colors.RED)
            except:
                print_status("Vui lòng nhập số!", 'error', Colors.RED)
        else:
            print_status("Lựa chọn không hợp lệ!", 'error', Colors.RED)

def extract_quiz_info(session, url, is_video=False):
    """Trích xuất thông tin quiz"""
    try:
        resp = session.get(url, timeout=8)
        html = resp.text
        
        # Tìm quiz_list
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
        
        # Tìm id_courseware
        id_courseware = None
        cw_patterns = [
            r'id_courseware\s*[:=]\s*["\']?(\d+)["\']?',
            r'data-courseware\s*=\s*["\'](\d+)["\']'
        ]
        
        for pattern in cw_patterns:
            match = re.search(pattern, html)
            if match:
                id_courseware = match.group(1)
                break
        
        # Tìm id_cate
        id_cate = None
        cate_match = re.search(r'-(\d+)(?:\?|$)', url)
        if cate_match:
            id_cate = cate_match.group(1)
        
        if not quiz_list and not is_video:
            print_status("Không tìm thấy danh sách câu hỏi!", 'warning', Colors.YELLOW)
            return None, 0, id_courseware, id_cate
        
        # Đếm số câu
        total_questions = 0
        if quiz_list:
            question_ids = [qid.strip() for qid in quiz_list.split(',') if qid.strip()]
            total_questions = len(question_ids)
        
        return quiz_list, total_questions, id_courseware, id_cate
        
    except Exception as e:
        print_status(f"Lỗi trích xuất: {str(e)}", 'error', Colors.RED)
        return None, 0, None, None

def create_data_log(total_questions, target_score):
    """Tạo data_log cho bài tập"""
    if target_score == 100:
        correct_needed = total_questions
    elif target_score == 0:
        correct_needed = 0
    else:
        correct_needed = round((target_score / 100) * total_questions)
        correct_needed = max(1, min(total_questions, correct_needed))
    
    wrong_needed = total_questions - correct_needed
    
    # Tạo kết quả
    results = [1] * correct_needed + [0] * wrong_needed
    random.shuffle(results)
    
    data_log = []
    total_time = 0
    
    for i, is_correct in enumerate(results):
        time_spent = random.randint(8, 25) + (i % 4)
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
    print(f"\n{Colors.CYAN}{Colors.BOLD}╔{'═' * 48}╗{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}║{Colors.END}{Colors.YELLOW}{Colors.BOLD}  {ICONS['upload']} ĐANG XỬ LÝ BÀI TẬP{' ' * 30}{Colors.END}{Colors.CYAN}{Colors.BOLD}║{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}╠{'═' * 48}╣{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}║{Colors.END}  {Colors.WHITE}📖 {assignment['title']:<44}{Colors.END}{Colors.CYAN}{Colors.BOLD}║{Colors.END}")
    
    if assignment['is_video']:
        print(f"{Colors.CYAN}{Colors.BOLD}║{Colors.END}  {Colors.BLUE}{ICONS['video']} Loại: Video{' ' * 36}{Colors.END}{Colors.CYAN}{Colors.BOLD}║{Colors.END}")
        target_score = 100
    elif assignment['is_ly_thuyet']:
        print(f"{Colors.CYAN}{Colors.BOLD}║{Colors.END}  {Colors.CYAN}{ICONS['theory']} Loại: Lý thuyết{' ' * 32}{Colors.END}{Colors.CYAN}{Colors.BOLD}║{Colors.END}")
        target_score = get_target_score(False, False)
    elif assignment['is_kiem_tra']:
        print(f"{Colors.CYAN}{Colors.BOLD}║{Colors.END}  {Colors.YELLOW}{ICONS['test']} Loại: Kiểm tra{' ' * 33}{Colors.END}{Colors.CYAN}{Colors.BOLD}║{Colors.END}")
        target_score = get_target_score(False, True)
    else:
        print(f"{Colors.CYAN}{Colors.BOLD}║{Colors.END}  {Colors.GREEN}{ICONS['exercise']} Loại: Bài tập{' ' * 34}{Colors.END}{Colors.CYAN}{Colors.BOLD}║{Colors.END}")
        target_score = get_target_score(False, False)
    
    print(f"{Colors.CYAN}{Colors.BOLD}╚{'═' * 48}╝{Colors.END}")
    
    try:
        # Trích xuất thông tin
        spinner_animation("Đang trích xuất thông tin bài tập...", 1)
        quiz_list, total_questions, id_courseware, id_cate = extract_quiz_info(
            session, assignment['url'], assignment['is_video']
        )
        
        # Xử lý video
        if assignment['is_video']:
            success = handle_video_submission(session, assignment, user_id, quiz_list, id_courseware, id_cate)
            if success:
                print_status(f"{ICONS['success']} HOÀN THÀNH VIDEO!", 'success', Colors.GREEN, True)
            return success
        
        # Bài tập thường
        if not quiz_list or total_questions == 0:
            print_status("Không thể lấy thông tin bài tập!", 'error', Colors.RED)
            return False
        
        print_status(f"Tìm thấy {total_questions} câu hỏi", 'info', Colors.CYAN)
        
        # Tạo dữ liệu
        spinner_animation("Đang tạo dữ liệu bài làm...", 1)
        data_log, total_time, correct_needed = create_data_log(total_questions, target_score)
        
        # Lấy CSRF token
        csrf_token = session.cookies.get('XSRF-TOKEN')
        if not csrf_token:
            resp = session.get(assignment['url'], timeout=5)
            csrf_match = re.search(r'<meta name="csrf-token" content="([^"]+)"', resp.text)
            csrf_token = csrf_match.group(1) if csrf_match else ""
        
        # Tạo payload
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
        
        # Gửi request
        print_status("Đang nộp bài...", 'upload', Colors.YELLOW)
        
        submit_headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'x-csrf-token': csrf_token,
            'x-requested-with': 'XMLHttpRequest'
        }
        
        response = session.post(
            'https://olm.vn/course/teacher-static',
            data=payload,
            headers=submit_headers,
            timeout=15
        )
        
        # Xử lý kết quả
        success = handle_response(response, target_score)
        
        if success:
            # TRỪ LƯỢT CHO FREE (luôn trừ lý thuyết)
            if not is_vip():
                decrement_attempts()
                remaining = get_remaining_attempts()
                if remaining == float('inf'):
                    print_status("Lượt còn: VIP (Không giới hạn)", 'crown', Colors.MAGENTA)
                else:
                    print_status(f"Lượt còn: {remaining}/4", 'info', Colors.CYAN)
            
            print_status(f"{ICONS['success']} HOÀN THÀNH BÀI!", 'success', Colors.GREEN, True)
            
            # Hiệu ứng hoàn thành
            for _ in range(3):
                print(f"{Colors.GREEN}{ICONS['sparkle']}{Colors.END}", end=' ', flush=True)
                time.sleep(0.2)
            print()
        
        return success
        
    except Exception as e:
        print_status(f"Lỗi: {str(e)}", 'error', Colors.RED)
        return False

def handle_video_submission(session, assignment, user_id, quiz_list, id_courseware, id_cate):
    """Xử lý nộp video"""
    methods = [
        submit_video_simple,
        submit_video_with_quiz,
        submit_video_complex
    ]
    
    for i, method in enumerate(methods, 1):
        print_status(f"Thử phương pháp {i}/3...", 'video', Colors.BLUE)
        success = method(session, assignment, user_id, quiz_list, id_courseware, id_cate)
        if success:
            return True
        time.sleep(1)
    
    print_status("Không thể xử lý video!", 'error', Colors.RED)
    return False

def submit_video_simple(session, assignment, user_id, quiz_list, id_courseware, id_cate):
    """Phương pháp đơn giản cho video"""
    try:
        csrf_token = session.cookies.get('XSRF-TOKEN')
        if not csrf_token:
            resp = session.get(assignment['url'], timeout=5)
            csrf_match = re.search(r'<meta name="csrf-token" content="([^"]+)"', resp.text)
            csrf_token = csrf_match.group(1) if csrf_match else ""
        
        current_time = int(time.time())
        time_spent = random.randint(300, 900)
        
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
        
        if quiz_list:
            payload['quiz_list'] = quiz_list
        
        submit_headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'x-csrf-token': csrf_token
        }
        
        response = session.post(
            'https://olm.vn/course/teacher-static',
            data=payload,
            headers=submit_headers,
            timeout=10
        )
        
        return handle_response(response, 100)
        
    except Exception:
        return False

def submit_video_with_quiz(session, assignment, user_id, quiz_list, id_courseware, id_cate):
    """Phương pháp video có quiz_list"""
    try:
        if not quiz_list:
            return False
        
        csrf_token = session.cookies.get('XSRF-TOKEN')
        if not csrf_token:
            return False
        
        current_time = int(time.time())
        time_spent = random.randint(300, 900)
        
        # Tách quiz_list để đếm
        qids = quiz_list.split(',')
        num_questions = min(len(qids), 3)
        
        data_log = []
        for i in range(num_questions):
            data_log.append({
                "answer": '["0"]',
                "params": '{"js":""}',
                "result": [1],
                "wrong_skill": [],
                "correct_skill": [],
                "type": [1],
                "id": qids[i],
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
            'correct': str(num_questions),
            'count_problems': str(num_questions)
        }
        
        submit_headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'x-csrf-token': csrf_token
        }
        
        response = session.post(
            'https://olm.vn/course/teacher-static',
            data=payload,
            headers=submit_headers,
            timeout=10
        )
        
        return handle_response(response, 100)
        
    except Exception:
        return False

def submit_video_complex(session, assignment, user_id, quiz_list, id_courseware, id_cate):
    """Phương pháp phức tạp cho video"""
    try:
        csrf_token = session.cookies.get('XSRF-TOKEN')
        if not csrf_token:
            return False
        
        current_time = int(time.time())
        time_spent = random.randint(600, 1200)
        
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
        
        if quiz_list:
            qids = quiz_list.split(',')
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
                "id": qids[0] if qids else f"q{random.randint(100000, 999999)}",
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
        
        submit_headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'x-csrf-token': csrf_token
        }
        
        response = session.post(
            'https://olm.vn/course/teacher-static',
            data=payload,
            headers=submit_headers,
            timeout=10
        )
        
        return handle_response(response, 100)
        
    except Exception:
        return False

def handle_response(response, target_score):
    """Xử lý phản hồi từ server"""
    if response.status_code == 200:
        try:
            result = response.json()
            
            if 'code' in result:
                if result['code'] == 403:
                    print_status("Bài đã được nộp trước đó!", 'warning', Colors.YELLOW)
                    return True
                elif result['code'] == 400:
                    print_status(f"Lỗi: {result.get('message', '')}", 'error', Colors.RED)
                    return False
                else:
                    actual_score = result.get('score', target_score)
                    print_status(f"Thành công! Điểm: {actual_score}/100", 'success', Colors.GREEN)
                    return True
            else:
                print_status("Nộp bài thành công!", 'success', Colors.GREEN)
                return True
                
        except:
            if "success" in response.text.lower():
                print_status("Nộp bài thành công!", 'success', Colors.GREEN)
                return True
            print_status("Nộp bài thành công (HTTP 200)", 'success', Colors.GREEN)
            return True
            
    elif response.status_code == 403:
        print_status("Bài đã được nộp trước đó!", 'warning', Colors.YELLOW)
        return True
    else:
        print_status(f"Lỗi HTTP {response.status_code}", 'error', Colors.RED)
        return False

# ========== GIẢI BÀI CỤ THỂ ==========
def solve_specific(session, user_id):
    """Giải bài cụ thể từ danh sách"""
    print_header("GIẢI BÀI CỤ THỂ")
    
    # Nhập số trang
    pages_input = input_prompt("Số trang cần quét (mặc định: 5): ", 'search')
    pages_to_scan = 5
    if pages_input.isdigit() and int(pages_input) > 0:
        pages_to_scan = int(pages_input)
    
    # Quét bài
    assignments = get_assignments(session, pages_to_scan)
    if not assignments:
        wait_enter()
        return False
    
    # Hiển thị danh sách
    display_assignments_table(assignments)
    
    # Chọn bài
    print(f"\n{Colors.CYAN}{Colors.BOLD}📝 CÁCH CHỌN:{Colors.END}")
    print(f"  - Nhập số bài: {Colors.GREEN}1,3,5{Colors.END} (nhiều bài)")
    print(f"  - Nhập khoảng: {Colors.GREEN}1-5{Colors.END} (từ 1 đến 5)")
    print(f"  - Nhập {Colors.GREEN}0{Colors.END} để chọn tất cả")
    
    selection = input_prompt("Chọn bài: ", 'question')
    
    # Xử lý lựa chọn
    selected_indices = []
    
    if selection == '0':
        selected_indices = list(range(1, len(assignments) + 1))
    elif '-' in selection:
        try:
            start, end = map(int, selection.split('-'))
            selected_indices = list(range(max(1, start), min(end, len(assignments)) + 1))
        except:
            print_status("Định dạng không hợp lệ!", 'error', Colors.RED)
            wait_enter()
            return False
    elif ',' in selection:
        try:
            selected_indices = [int(x.strip()) for x in selection.split(',') if x.strip().isdigit()]
            selected_indices = [x for x in selected_indices if 1 <= x <= len(assignments)]
        except:
            print_status("Định dạng không hợp lệ!", 'error', Colors.RED)
            wait_enter()
            return False
    elif selection.isdigit():
        idx = int(selection)
        if 1 <= idx <= len(assignments):
            selected_indices = [idx]
        else:
            print_status("Số bài không hợp lệ!", 'error', Colors.RED)
            wait_enter()
            return False
    
    if not selected_indices:
        print_status("Không có bài nào được chọn!", 'warning', Colors.YELLOW)
        wait_enter()
        return False
    
    # Xác nhận
    print(f"\n{Colors.CYAN}Đã chọn {len(selected_indices)} bài:{Colors.END}")
    for idx in selected_indices[:5]:  # Chỉ hiển thị 5 bài đầu
        print(f"  {Colors.YELLOW}{idx}.{Colors.END} {assignments[idx-1]['title'][:50]}")
    if len(selected_indices) > 5:
        print(f"  ... và {len(selected_indices) - 5} bài khác")
    
    confirm = input_prompt("Xác nhận giải? (y/n): ", 'question')
    if confirm.lower() != 'y':
        print_status("Đã hủy", 'warning', Colors.YELLOW)
        wait_enter()
        return False
    
    # Giải từng bài
    print_header(f"GIẢI {len(selected_indices)} BÀI")
    
    success_count = 0
    total = len(selected_indices)
    
    for i, idx in enumerate(selected_indices, 1):
        print(f"\n{Colors.YELLOW}{Colors.BOLD}📊 Bài {i}/{total}{Colors.END}")
        
        # Kiểm tra lượt (chỉ FREE)
        if not is_vip():
            remaining = get_remaining_attempts()
            if remaining <= 0:
                print_status("HẾT LƯỢT! Vui lòng đổi tài khoản hoặc thoát.", 'error', Colors.RED, True)
                print_status("Chọn [3] Đổi tài khoản để tiếp tục", 'info', Colors.CYAN)
                break
        
        # Xử lý bài
        success = submit_assignment(session, assignments[idx-1], user_id)
        if success:
            success_count += 1
        
        # Chờ giữa các bài
        if i < total:
            wait_time = random.randint(2, 4)
            print_status(f"Chờ {wait_time}s trước bài tiếp theo...", 'clock', Colors.YELLOW)
            time.sleep(wait_time)
    
    # Kết quả
    print(f"\n{Colors.GREEN}{Colors.BOLD}╔{'═' * 40}╗{Colors.END}")
    print(f"{Colors.GREEN}{Colors.BOLD}║{Colors.END}{Colors.YELLOW}{Colors.BOLD}  {ICONS['trophy']} KẾT QUẢ{' ' * 30}{Colors.END}{Colors.GREEN}{Colors.BOLD}║{Colors.END}")
    print(f"{Colors.GREEN}{Colors.BOLD}╠{'═' * 40}╣{Colors.END}")
    print(f"{Colors.GREEN}{Colors.BOLD}║{Colors.END}  Thành công: {Colors.GREEN}{success_count}/{total}{Colors.END}{' ' * 21}{Colors.GREEN}{Colors.BOLD}║{Colors.END}")
    print(f"{Colors.GREEN}{Colors.BOLD}╚{'═' * 40}╝{Colors.END}")
    
    wait_enter()
    return success_count > 0

# ========== GIẢI TỪ LINK ==========
def solve_from_link(session, user_id):
    """Giải bài từ link"""
    print_header("GIẢI BÀI TỪ LINK")
    
    print(f"{Colors.CYAN}{ICONS['link']} NHẬP LINK BÀI TẬP:{Colors.END}")
    print("Ví dụ: https://olm.vn/chu-de/bai-tap-123456")
    print()
    
    url = input_prompt("Dán link: ", 'link')
    
    if not url.startswith('https://olm.vn/'):
        print_status("Link không hợp lệ! Phải là link OLM", 'error', Colors.RED)
        wait_enter()
        return False
    
    try:
        # Kiểm tra loại bài
        resp = session.get(url, timeout=8)
        html = resp.text
        
        is_video = 'video' in url.lower() or '[Video]' in html
        is_ly_thuyet = 'ly-thuyet' in url.lower() or 'lý-thuyết' in url.lower() or '[Lý thuyết]' in html
        is_kiem_tra = 'kiem-tra' in url.lower() or 'kiểm-tra' in url.lower() or '[Kiểm tra]' in html
        
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
            'is_kiem_tra': is_kiem_tra
        }
        
        if is_video:
            assignment['type'] = "Video"
        elif is_ly_thuyet:
            assignment['type'] = "Lý thuyết"
        elif is_kiem_tra:
            assignment['type'] = "Kiểm tra"
        
        # Hiển thị thông tin
        print(f"\n{Colors.CYAN}╔{'═' * 50}╗{Colors.END}")
        print(f"{Colors.CYAN}║{Colors.END}{Colors.YELLOW}{Colors.BOLD}  {ICONS['info']} THÔNG TIN BÀI TẬP{' ' * 32}{Colors.END}{Colors.CYAN}║{Colors.END}")
        print(f"{Colors.CYAN}╠{'═' * 50}╣{Colors.END}")
        print(f"{Colors.CYAN}║{Colors.END}  📖 Link: {Colors.CYAN}{url[:40]}...{Colors.END}{' ' * 5}{Colors.CYAN}║{Colors.END}")
        print(f"{Colors.CYAN}║{Colors.END}  📝 Loại: {Colors.GREEN}{assignment['type']}{Colors.END}{' ' * 35}{Colors.CYAN}║{Colors.END}")
        print(f"{Colors.CYAN}╚{'═' * 50}╝{Colors.END}")
        
        confirm = input_prompt("Xác nhận giải bài này? (y/n): ", 'question')
        
        if confirm.lower() == 'y':
            # Kiểm tra lượt
            if not is_vip():
                remaining = get_remaining_attempts()
                if remaining <= 0:
                    print_status("HẾT LƯỢT! Vui lòng đổi tài khoản.", 'error', Colors.RED, True)
                    wait_enter()
                    return False
            
            success = submit_assignment(session, assignment, user_id)
            return success
        else:
            print_status("Đã hủy", 'warning', Colors.YELLOW)
            wait_enter()
            return False
            
    except Exception as e:
        print_status(f"Lỗi: {str(e)}", 'error', Colors.RED)
        wait_enter()
        return False

# ========== ĐỔI TÀI KHOẢN ==========
def change_account():
    """Đổi tài khoản (quay lại launcher)"""
    print_header("ĐỔI TÀI KHOẢN")
    
    print(f"{Colors.YELLOW}{Colors.BOLD}{ICONS['warning']} Bạn sắp đăng xuất để đổi tài khoản.{Colors.END}")
    print(f"{Colors.CYAN}Lưu ý: License hiện tại sẽ được giữ nguyên nếu còn lượt.{Colors.END}")
    print()
    
    confirm = input_prompt("Xác nhận đổi tài khoản? (y/n): ", 'question')
    
    if confirm.lower() == 'y':
        print_status("Đang đăng xuất...", 'refresh', Colors.YELLOW)
        time.sleep(1)
        return True
    
    return False

# ========== MENU CHÍNH ==========
def main_menu(session, user_id, user_name):
    """Menu chính"""
    
    while True:
        print_header("MENU CHÍNH")
        
        # Hiển thị thông tin user và license
        print(f"{Colors.CYAN}┌{'─' * 48}┐{Colors.END}")
        print(f"{Colors.CYAN}│{Colors.END}{Colors.YELLOW}{Colors.BOLD}  {ICONS['user']} Xin chào: {user_name}{' ' * (30 - len(user_name))}{Colors.END}{Colors.CYAN}│{Colors.END}")
        
        if is_vip():
            print(f"{Colors.CYAN}│{Colors.END}{Colors.MAGENTA}  {ICONS['crown']} VIP: Không giới hạn lượt{' ' * 21}{Colors.END}{Colors.CYAN}│{Colors.END}")
        else:
            remaining = get_remaining_attempts()
            remain_str = f"{remaining}/4" if remaining != float('inf') else "Không giới hạn"
            print(f"{Colors.CYAN}│{Colors.END}{Colors.GREEN}  {ICONS['key']} Lượt còn: {remain_str}{' ' * (33 - len(remain_str))}{Colors.END}{Colors.CYAN}│{Colors.END}")
        
        print(f"{Colors.CYAN}└{'─' * 48}┘{Colors.END}")
        print()
        
        menu_options = {
            '1': f"{ICONS['brain']} Giải bài cụ thể từ danh sách",
            '2': f"{ICONS['link']} Giải bài từ link OLM",
            '3': f"{ICONS['refresh']} Đổi tài khoản",
            '4': f"{ICONS['exit']} Thoát"
        }
        
        print_menu("CHỌN CHỨC NĂNG", menu_options)
        
        choice = input_prompt("Chọn (1-4): ", 'question')
        
        if choice == '1':
            # Giải bài cụ thể
            solve_specific(session, user_id)
        
        elif choice == '2':
            # Giải từ link
            solve_from_link(session, user_id)
        
        elif choice == '3':
            # Đổi tài khoản
            if change_account():
                break
        
        elif choice == '4':
            # Thoát
            print_header("TẠM BIỆT")
            animate_text("Cảm ơn bạn đã sử dụng OLM MASTER PRO!", Colors.GREEN, 0.03)
            animate_text("Hẹn gặp lại!", Colors.CYAN, 0.03)
            time.sleep(1)
            sys.exit(0)
        
        else:
            print_status("Lựa chọn không hợp lệ!", 'error', Colors.RED)
            time.sleep(1)

# ========== CHƯƠNG TRÌNH CHÍNH ==========
def main():
    """Chương trình chính"""
    try:
        # Import BeautifulSoup ở đây để tránh lỗi nếu chưa cài
        try:
            from bs4 import BeautifulSoup
        except ImportError:
            print_status("Đang cài đặt BeautifulSoup...", 'download', Colors.YELLOW)
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "beautifulsoup4", "--quiet"])
            from bs4 import BeautifulSoup
        
        # Load session
        session, user_id, user_name = load_session()
        
        # Hiệu ứng chào mừng
        print_banner_small()
        animate_text("KẾT NỐI THÀNH CÔNG!", Colors.GREEN, 0.05)
        time.sleep(1)
        
        # Hiển thị thông tin license
        display_license_info()
        time.sleep(2)
        
        # Vào menu chính
        main_menu(session, user_id, user_name)
        
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}{ICONS['exit']} Đã dừng chương trình{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}{ICONS['error']} Lỗi: {str(e)}{Colors.END}")
        wait_enter()

def print_banner_small():
    """In banner nhỏ"""
    width = get_terminal_width()
    clear_screen()
    print(f"{Colors.MAGENTA}{Colors.BOLD}╔{'═' * (width - 2)}╗{Colors.END}")
    print(f"{Colors.MAGENTA}{Colors.BOLD}║{Colors.END}{Colors.CYAN}{Colors.BOLD}  {ICONS['rocket']} OLM MASTER PRO - READY {ICONS['fire']}{' ' * (width - 32)}{Colors.END}{Colors.MAGENTA}{Colors.BOLD}║{Colors.END}")
    print(f"{Colors.MAGENTA}{Colors.BOLD}╚{'═' * (width - 2)}╝{Colors.END}")

if __name__ == "__main__":
    main()
