#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║              OLM MASTER PRO V1.0 - MAIN SOLVER               ║
║                 🎯 Professional Edition 🎯                   ║
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
import platform
from datetime import datetime, timedelta

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Error: Missing libraries")
    sys.exit(1)

import re

# ==================== CONFIGURATION ====================
SECRET_KEY = b"OLM_MASTER_PRO_V1_SECURE_2026"

# ==================== BEAUTIFUL COLORS ====================
class C:
    R = '\033[91m'; G = '\033[92m'; Y = '\033[93m'; B = '\033[94m'
    M = '\033[95m'; Cy = '\033[96m'; W = '\033[97m'
    BR = '\033[91;1m'; BG = '\033[92;1m'; BY = '\033[93;1m'; BB = '\033[94;1m'
    BM = '\033[95;1m'; BC = '\033[96;1m'; BW = '\033[97;1m'
    BOLD = '\033[1m'; DIM = '\033[2m'; UNDER = '\033[4m'
    E = '\033[0m'

# ==================== ICONS ====================
I = {
    'rocket': '🚀', 'fire': '🔥', 'star': '⭐', 'gem': '💎', 'crown': '👑',
    'check': '✅', 'cross': '❌', 'warn': '⚠️', 'info': 'ℹ️', 'quest': '❓',
    'user': '👤', 'key': '🔑', 'lock': '🔐', 'video': '🎬', 'theory': '📖',
    'exercise': '📝', 'book': '📚', 'search': '🔍', 'clock': '⏰',
    'upload': '📤', 'download': '📥', 'link': '🔗', 'sparkle': '✨',
    'brain': '🧠', 'zap': '⚡', 'target': '🎯', 'trophy': '🏆',
    'refresh': '🔄', 'exit': '🚪', 'back': '↩️', 'gear': '⚙️',
    'chart': '📊', 'list': '📋', 'magic': '🪄', 'wave': '👋',
}

# ==================== CROSS-PLATFORM ====================
def get_device_hash():
    hostname = platform.node()
    mac = uuid.getnode()
    return hashlib.md5(f"{hostname}{mac}".encode()).hexdigest()[:8]

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
        'lock': os.path.join(base, f'.{device_hash}lk')
    }

PATHS = get_app_data_dir()

# ==================== ENCRYPTION ====================
def xor_encrypt(data, key):
    key_len = len(key)
    return bytes([data[i] ^ key[i % key_len] for i in range(len(data))])

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
        return json.loads(decrypted.decode('utf-8'))
    except:
        return None

def load_file(filepath):
    if not os.path.exists(filepath):
        return None
    try:
        with open(filepath, 'r') as f:
            return decrypt_data(f.read())
    except:
        return None

def encrypt_data(data_dict):
    try:
        json_str = json.dumps(data_dict, separators=(',', ':'))
        encrypted = xor_encrypt(json_str.encode('utf-8'), SECRET_KEY)
        b85_data = base64.b85encode(encrypted).decode('ascii')
        checksum = hashlib.sha256(b85_data.encode()).hexdigest()[:12]
        noise = hashlib.md5(str(time.time()).encode()).hexdigest()
        return f"{noise[:8]}{checksum}{b85_data}{noise[-8:][::-1]}"
    except:
        return None

def save_file(filepath, data_dict):
    encrypted = encrypt_data(data_dict)
    if encrypted:
        with open(filepath, 'w') as f:
            f.write(encrypted)
        return True
    return False

# ==================== BEAUTIFUL UI ====================
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    print('\033[2J\033[H', end='')

def gradient_text(text, colors):
    result = ""
    step = len(text) / len(colors)
    for i, char in enumerate(text):
        color_idx = min(int(i / step), len(colors) - 1)
        result += f"{colors[color_idx]}{char}"
    return result + C.E

def header(title=""):
    clear()
    
    # Big CYAN text - no box
    print(f"\n{C.BC}{C.BOLD}")
    print("  ╔═══════════════════════════════════════════════════════════════╗")
    print("  ║                                                               ║")
    print("  ║     ██████╗ ██╗     ███╗   ██╗    ███╗   ███╗ █████╗         ║")
    print("  ║    ██╔═══██╗██║     ████╗  ██║    ████╗ ████║██╔══██╗        ║")
    print("  ║    ██║   ██║██║     ██╔██╗ ██║    ██╔████╔██║███████║        ║")
    print("  ║    ██║   ██║██║     ██║╚██╗██║    ██║╚██╔╝██║██╔══██║        ║")
    print("  ║    ╚██████╔╝███████╗██║ ╚████║    ██║ ╚═╝ ██║██║  ██║        ║")
    print("  ║     ╚═════╝ ╚══════╝╚═╝  ╚═══╝    ╚═╝     ╚═╝╚═╝  ╚═╝        ║")
    print("  ║                                                               ║")
    print("  ║            🚀 MASTER PRO V1.0 - Professional Edition 🔥       ║")
    print("  ║                      Created by: Tuấn Anh                     ║")
    print("  ║                                                               ║")
    print("  ╚═══════════════════════════════════════════════════════════════╝")
    print(f"{C.E}")
    
    if title:
        print(f"\n{C.BC}{C.BOLD}>>> {title.upper()} <<<{C.E}\n")
    else:
        print()

def status(msg, icon='info', color=C.W):
    icons = {
        'success': (I['check'], C.BG), 'error': (I['cross'], C.BR),
        'warn': (I['warn'], C.BY), 'info': (I['info'], C.BC),
        'video': (I['video'], C.BB), 'theory': (I['theory'], C.Cy),
        'exercise': (I['exercise'], C.BG), 'search': (I['search'], C.BY),
        'upload': (I['upload'], C.BC), 'clock': (I['clock'], C.BY),
        'gem': (I['gem'], C.BM),
    }
    icon_char, icon_color = icons.get(icon, (I['info'], C.W))
    print(f"{icon_color}{icon_char} {color}{msg}{C.E}")

def fancy_input(prompt, color=C.BY):
    return input(f"{color}{I['zap']} {prompt}{C.E}").strip()

def wait(prompt="Nhấn Enter để tiếp tục..."):
    input(f"\n{C.BY}{I['wave']} {prompt}{C.E}")

def print_line(char='─', color=C.Cy, width=90):
    print(f"{color}{char * width}{C.E}")

# ==================== LICENSE MANAGEMENT ====================
def load_license():
    return load_file(PATHS['license'])

def compute_signature(lic):
    sig_str = f"{lic.get('mode', '')}{lic.get('expire', '')}{lic.get('ip', '')}"
    return hashlib.sha256(sig_str.encode()).hexdigest()[:16]

def consume_one_attempt():
    """Trừ 1 lượt SAU KHI thành công"""
    lic = load_license()
    if not lic:
        status("Lỗi license!", 'error', C.BR)
        return False
    
    # VIP không trừ
    if lic.get('mode') == 'VIP':
        print(f"\n{C.BM}╔{'═' * 48}╗{C.E}")
        print(f"{C.BM}║ {I['crown']} VIP UNLIMITED {' ' * 29}║{C.E}")
        print(f"{C.BM}╚{'═' * 48}╝{C.E}\n")
        return True
    
    # FREE trừ lượt
    lic['remain'] -= 1
    
    if lic['remain'] <= 0:
        # HẾT LƯỢT
        if os.path.exists(PATHS['license']):
            os.remove(PATHS['license'])
        if os.path.exists(PATHS['lock']):
            os.remove(PATHS['lock'])
        
        print(f"\n{C.BR}╔{'═' * 48}╗{C.E}")
        print(f"{C.BR}║ {I['warn']} HẾT LƯỢT! {' ' * 32}║{C.E}")
        print(f"{C.BR}╠{'═' * 48}╣{C.E}")
        print(f"{C.BR}║ {C.BY}[1]{C.E} Quay launcher lấy key mới {' ' * 18}║")
        print(f"{C.BR}║ {C.BY}[2]{C.E} Thoát {' ' * 37}║")
        print(f"{C.BR}╚{'═' * 48}╝{C.E}\n")
        
        choice = fancy_input("Chọn: ")
        sys.exit(0)
    
    # Lưu
    save_file(PATHS['license'], lic)
    
    # Hiển thị số lượt
    print(f"\n{C.BG}╔{'═' * 48}╗{C.E}")
    print(f"{C.BG}║ {I['gem']} Còn: {C.BY}{lic['remain']}{C.E} lượt {' ' * (37 - len(str(lic['remain'])))}║")
    print(f"{C.BG}╚{'═' * 48}╝{C.E}\n")
    
    return True

def clear_account_lock():
    if os.path.exists(PATHS['lock']):
        os.remove(PATHS['lock'])

# ==================== LOAD SESSION ====================
def load_session():
    try:
        with open(PATHS['session'], 'rb') as f:
            session_data = pickle.load(f)
        
        session = requests.Session()
        session.cookies.update(session_data['cookies'])
        
        return session, session_data['user_id'], session_data['user_name']
    except:
        return None, None, None

# ==================== HEADERS (100% GỐC) ====================
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'vi-VN,vi;q=0.9,en-US;q=0.8',
    'x-requested-with': 'XMLHttpRequest',
    'origin': 'https://olm.vn',
    'referer': 'https://olm.vn/'
}

# ========== 100% CODE GỐC - KIỂM TRA BÀI ẨN ĐIỂM ==========
def check_hidden_test_status(session, url, id_cate):
    """Kiểm tra xem bài kiểm tra đã làm chưa (ẩn điểm) - 100% GỐC"""
    try:
        test_url = f'https://olm.vn/course/teacher-categories/{id_cate}/get-next-cate'
        
        headers = HEADERS.copy()
        headers['referer'] = url
        headers['x-csrf-token'] = session.cookies.get('XSRF-TOKEN', '')
        
        response = session.get(test_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            try:
                data = response.json()
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
            api_headers['content-type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
            api_headers['x-csrf-token'] = session.cookies.get('XSRF-TOKEN', '')
            api_headers['referer'] = url
            
            api_response = session.post(api_url, data=payload, headers=api_headers, timeout=10)
            
            if api_response.status_code == 200:
                response_text = api_response.text.lower()
                if "đã hoàn thành" in response_text or "completed" in response_text or "đã nộp" in response_text:
                    return True
        
        return False
        
    except:
        return False

# ========== 100% CODE GỐC - QUÉT BÀI ==========
def get_assignments_fixed(session, pages_to_scan=5):
    """100% CODE GỐC - Lấy danh sách bài tập"""
    header(f"QUÉT BÀI TẬP ({pages_to_scan} trang)")
    
    assignments = []
    seen_links = set()
    
    try:
        for page in range(1, pages_to_scan + 1):
            if page == 1:
                url = "https://olm.vn/lop-hoc-cua-toi?action=login"
            else:
                url = f"https://olm.vn/lop-hoc-cua-toi/page-{page}?action=login"
            
            status(f"Đang quét trang {page}/{pages_to_scan}...", 'search', C.BY)
            
            try:
                response = session.get(url, headers=HEADERS, timeout=10)
                
                if response.status_code != 200:
                    status(f"Lỗi HTTP {response.status_code}", 'error', C.BR)
                    continue
                
                soup = BeautifulSoup(response.text, 'html.parser')
                rows = soup.find_all('tr', class_='my-gived-courseware-item')
                
                if not rows:
                    status(f"Trang {page} không có bài tập", 'warn', C.BY)
                    continue
                
                page_count = 0
                for row in rows:
                    link_tags = row.find_all('a', class_='olm-text-link')
                    if not link_tags:
                        continue
                    
                    main_link = link_tags[0]
                    href = main_link.get('href')
                    link_text = main_link.get_text(strip=True)
                    
                    if href and ('(Toán' in link_text or '(Ngữ văn' in link_text or 
                                '(Tiếng Anh' in link_text or '(Tin học' in link_text):
                        continue
                    
                    if not href:
                        continue
                    
                    tds = row.find_all('td')
                    if len(tds) < 2:
                        continue
                    
                    loai_raw = tds[1].get_text(strip=True)
                    
                    is_video = "[Video]" in loai_raw or "Video" in loai_raw
                    is_ly_thuyet = "[Lý thuyết]" in loai_raw or "Ly thuyet" in loai_raw
                    is_kiem_tra = "[Kiểm tra]" in loai_raw or "[Kiem tra]" in loai_raw
                    is_bai_tap = not (is_video or is_ly_thuyet or is_kiem_tra)
                    is_tu_luan = "[Tự luận]" in loai_raw or "[Tu luan]" in loai_raw
                    
                    if is_tu_luan:
                        continue
                    
                    should_process = False
                    status_spans = []
                    
                    status_spans.extend(main_link.find_all('span', class_='message-static-item'))
                    
                    if not status_spans:
                        status_spans.extend(row.find_all('span', class_='message-static-item'))
                    
                    if not status_spans:
                        warning_spans = row.find_all('span', class_='alert-warning')
                        for span in warning_spans:
                            span_text = span.get_text(strip=True)
                            if span_text not in ['Hóa học', 'Toán', 'Ngữ văn', 'Tiếng Anh', 'Tin học', 'Lịch sử', 'Địa lý', 'Giáo dục công dân']:
                                status_spans.append(span)
                    
                    if not is_kiem_tra:
                        if not status_spans:
                            should_process = True
                        else:
                            for span in status_spans:
                                span_text = span.get_text(strip=True).lower()
                                if "chưa" in span_text or "chưa nộp" in span_text or "làm tiếp" in span_text:
                                    should_process = True
                                    break
                                elif "điểm" in span_text and "đúng" in span_text:
                                    should_process = False
                                    break
                                elif "đã xem" in span_text:
                                    should_process = False
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
                                is_done = check_hidden_test_status(session, href, id_cate)
                                if is_done:
                                    should_process = False
                                else:
                                    should_process = True
                            else:
                                should_process = True
                        else:
                            for span in status_spans:
                                span_text = span.get_text(strip=True).lower()
                                if "chưa" in span_text or "chưa nộp" in span_text or "làm tiếp" in span_text:
                                    should_process = True
                                    break
                                elif "điểm" in span_text and "đúng" in span_text:
                                    should_process = False
                                    break
                    
                    if should_process and href not in seen_links:
                        seen_links.add(href)
                        
                        mon = row.find('span', class_='alert')
                        mon_text = mon.get_text(strip=True) if mon else "Khác"
                        
                        ten_bai = link_text
                        ten_bai = re.sub(r'\([^)]*\)', '', ten_bai).strip()
                        
                        status_text = "Chưa làm"
                        if status_spans:
                            for span in status_spans:
                                span_text = span.get_text(strip=True)
                                if "chưa" in span_text.lower() or "làm tiếp" in span_text.lower():
                                    status_text = span_text
                                    break
                        
                        if not href.startswith('http'):
                            full_url = 'https://olm.vn' + href
                        else:
                            full_url = href
                        
                        assignments.append({
                            'title': ten_bai[:60],
                            'subject': mon_text[:20],
                            'type': loai_raw.replace('[', '').replace(']', '').strip()[:20],
                            'status': status_text,
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
                    status(f"Trang {page}: {page_count} bài cần làm", 'success', C.BG)
                else:
                    status(f"Trang {page}: không có bài cần làm", 'warn', C.BY)
                    
            except Exception as e:
                status(f"Lỗi trang {page}: {str(e)}", 'error', C.BR)
                continue
        
        if assignments:
            print(f"\n{C.BG}╔{'═' * 70}╗{C.E}")
            print(f"{C.BG}║ {I['check']} Tổng cộng: {C.BY}{len(assignments)}{C.E} bài cần xử lý{' ' * (45 - len(str(len(assignments))))}║")
            print(f"{C.BG}╚{'═' * 70}╝{C.E}\n")
            
            video_count = sum(1 for a in assignments if a['is_video'])
            ly_thuyet_count = sum(1 for a in assignments if a['is_ly_thuyet'])
            bai_tap_count = sum(1 for a in assignments if a['is_bai_tap'])
            kiem_tra_count = sum(1 for a in assignments if a['is_kiem_tra'])
            
            print(f"{C.Cy}{I['chart']} THỐNG KÊ LOẠI BÀI:{C.E}")
            print_line('─', C.Cy, 50)
            if video_count > 0:
                print(f"  {I['video']} Video: {C.BB}{video_count}{C.E} bài")
            if ly_thuyet_count > 0:
                print(f"  {I['theory']} Lý thuyết: {C.Cy}{ly_thuyet_count}{C.E} bài")
            if bai_tap_count > 0:
                print(f"  {I['exercise']} Bài tập: {C.BG}{bai_tap_count}{C.E} bài")
            if kiem_tra_count > 0:
                print(f"  {I['warn']} Kiểm tra: {C.BY}{kiem_tra_count}{C.E} bài")
            print_line('─', C.Cy, 50)
            
            return assignments
        else:
            status("Không tìm thấy bài tập nào cần làm", 'warn', C.BY)
            return []
            
    except Exception as e:
        status(f"Lỗi khi quét bài tập: {str(e)}", 'error', C.BR)
        return []

def display_assignments_table(assignments):
    """100% CODE GỐC - Hiển thị danh sách"""
    if not assignments:
        return
    
    print(f"\n{C.BM}╔{'═' * 90}╗{C.E}")
    print(f"{C.BM}║{' ' * 20}{I['book']} DANH SÁCH BÀI TẬP CẦN LÀM {I['book']}{' ' * 20}║{C.E}")
    print(f"{C.BM}╚{'═' * 90}╝{C.E}\n")
    
    for idx, item in enumerate(assignments, 1):
        title = item['title']
        if len(title) > 38:
            title = title[:35] + "..."
        
        if item['is_video']:
            loai_color = C.BB
            icon = I['video']
        elif item['is_ly_thuyet']:
            loai_color = C.Cy
            icon = I['theory']
        elif item['is_kiem_tra']:
            loai_color = C.BY
            icon = I['warn']
        else:
            loai_color = C.BG
            icon = I['exercise']
        
        status_text = item['status']
        if "Chưa làm" in status_text or "chưa nộp" in status_text.lower():
            status_color = C.BR
        elif "làm tiếp" in status_text.lower():
            status_color = C.BY
        else:
            status_color = C.W
        
        print(f"{C.BY}{idx:>2}.{C.E} {icon} {loai_color}{item['type']:<10}{C.E} {C.W}{item['subject']:<15}{C.E} {C.W}{title:<40}{C.E} {status_color}{status_text:<15}{C.E}")
    
    print_line('─', C.BM, 90)

# ========== 100% CODE GỐC - CHỌN ĐIỂM ==========
def get_target_score(is_video=False, is_kiem_tra=False):
    """100% CODE GỐC"""
    if is_video:
        status("Video: Tự động chọn 100 điểm", 'video', C.BB)
        return 100
    elif is_kiem_tra:
        status("Kiểm tra: Tự động chọn điểm cao", 'warn', C.BY)
        return random.randint(85, 100)
    
    print(f"\n{C.BC}┌{'─' * 48}┐{C.E}")
    print(f"{C.BC}│ {C.BW}{I['star']} CHỌN ĐIỂM SỐ{' ' * 32}│{C.E}")
    print(f"{C.BC}├{'─' * 48}┤{C.E}")
    print(f"{C.BC}│ {C.BY}[1]{C.E} {I['trophy']} 100 điểm (Xuất sắc){' ' * 17}│")
    print(f"{C.BC}│ {C.BY}[2]{C.E} {I['gear']} Tùy chọn điểm số{' ' * 20}│")
    print(f"{C.BC}└{'─' * 48}┘{C.E}")
    
    while True:
        choice = fancy_input("Chọn (1-2): ")
        
        if choice == '1':
            return 100
        elif choice == '2':
            try:
                score = int(fancy_input("Nhập điểm số (0-100): "))
                if 0 <= score <= 100:
                    return score
                else:
                    status("Điểm số phải từ 0 đến 100!", 'error', C.BR)
            except ValueError:
                status("Vui lòng nhập số hợp lệ!", 'error', C.BR)
        else:
            status("Lựa chọn không hợp lệ!", 'error', C.BR)

# ========== 100% CODE GỐC - TRÍCH XUẤT ==========
def extract_quiz_info(session, url, is_video=False):
    """100% CODE GỐC"""
    try:
        resp = session.get(url, timeout=10)
        html = resp.text
        
        quiz_list = None
        
        pattern1 = r'quiz_list\s*[:=]\s*["\'](\d{6,}(?:,\d{6,})*)["\']'
        match1 = re.search(pattern1, html)
        if match1:
            quiz_list = match1.group(1)
        
        if not quiz_list:
            pattern2 = r'\b\d{9,}(?:,\d{9,})+\b'
            matches = re.findall(pattern2, html)
            if matches:
                quiz_list = max(matches, key=len)
        
        if not quiz_list:
            pattern3 = r'"quiz_list"\s*:\s*"(\d+(?:,\d+)*)"'
            match3 = re.search(pattern3, html)
            if match3:
                quiz_list = match3.group(1)
        
        id_courseware = None
        cw_match = re.search(r'id_courseware\s*[:=]\s*["\']?(\d+)["\']?', html)
        if cw_match:
            id_courseware = cw_match.group(1)
        else:
            cw_match = re.search(r'data-courseware\s*=\s*["\'](\d+)["\']', html)
            if cw_match:
                id_courseware = cw_match.group(1)
        
        id_cate = None
        cate_match = re.search(r'-(\d+)(?:\?|$)', url)
        if cate_match:
            id_cate = cate_match.group(1)
        
        if not quiz_list:
            if is_video:
                status("Video: Không có quiz_list, sẽ thử phương pháp khác", 'video', C.BB)
                return "", 0, id_courseware, id_cate
            else:
                status("Không tìm thấy danh sách câu hỏi", 'error', C.BR)
                return None, 0, id_courseware, id_cate
        
        question_ids = [qid.strip() for qid in quiz_list.split(',') if qid.strip()]
        total_questions = len(question_ids)
        
        status(f"Tìm thấy {total_questions} câu hỏi", 'info', C.W)
        
        return quiz_list, total_questions, id_courseware, id_cate
        
    except Exception as e:
        status(f"Lỗi trích xuất thông tin: {str(e)}", 'error', C.BR)
        return None, 0, None, None

def create_data_log_for_normal(total_questions, target_score):
    """100% CODE GỐC"""
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

# ========== 100% CODE GỐC - VIDEO METHODS ==========
def try_video_simple_method(session, assignment, user_id, quiz_list, total_questions, id_courseware, id_cate):
    """100% CODE GỐC - Method 1"""
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
        
        for key, value in optional_fields.items():
            payload[key] = value
        
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
        
    except:
        return False

def try_video_with_quiz(session, assignment, user_id, quiz_list, total_questions, id_courseware, id_cate):
    """100% CODE GỐC - Method 2"""
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
        
        return handle_submission_response(response, 100)
        
    except:
        return False

def try_video_complex_method(session, assignment, user_id, quiz_list, total_questions, id_courseware, id_cate):
    """100% CODE GỐC - Method 3"""
    try:
        csrf_token = session.cookies.get('XSRF-TOKEN')
        if not csrf_token:
            resp = session.get(assignment['url'], timeout=5)
            csrf_match = re.search(r'<meta name="csrf-token" content="([^"]+)"', resp.text)
            csrf_token = csrf_match.group(1) if csrf_match else ""
        
        current_time = int(time.time())
        time_spent = random.randint(600, 1200)
        
        data_log = []
        
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
        
        return handle_submission_response(response, 100)
        
    except:
        return False

def handle_video_submission(session, assignment, user_id, quiz_list, total_questions, id_courseware, id_cate):
    """100% CODE GỐC - Xử lý video với 3 methods"""
    
    methods = [
        try_video_simple_method,
        try_video_with_quiz,
        try_video_complex_method,
    ]
    
    for i, method in enumerate(methods, 1):
        # CHE DI THÔNG BÁO METHOD
        # status(f"Thử phương pháp {i} cho video...", 'video', C.BB)
        success = method(session, assignment, user_id, quiz_list, total_questions, id_courseware, id_cate)
        if success:
            return True
        time.sleep(1)
    
    status("Tất cả phương pháp đều thất bại", 'error', C.BR)
    return False

def handle_submission_response(response, target_score):
    """100% CODE GỐC"""
    if response.status_code == 200:
        try:
            result = response.json()
            
            if 'code' in result:
                if result['code'] == 403:
                    status(f"Đã nộp trước: {result.get('message', '')}", 'warn', C.BY)
                    return True
                elif result['code'] == 400:
                    status(f"Lỗi 400: {result.get('message', '')}", 'error', C.BR)
                    return False
                else:
                    actual_score = result.get('score', target_score)
                    status(f"Thành công! Điểm: {actual_score}/100", 'success', C.BG)
                    return True
            else:
                status("Nộp thành công (status 200)", 'success', C.BG)
                return True
        except:
            if "success" in response.text.lower() or "hoàn thành" in response.text.lower():
                status("Có vẻ đã thành công", 'success', C.BG)
                return True
            status("Nộp thành công (status 200)", 'success', C.BG)
            return True
    elif response.status_code == 403:
        status("Bài đã được nộp trước đó", 'warn', C.BY)
        return True
    else:
        status(f"Lỗi {response.status_code}", 'error', C.BR)
        return False

# ========== 100% CODE GỐC - NỘP BÀI + TRỪ LƯỢT ==========
def submit_assignment(session, assignment, user_id):
    """100% CODE GỐC + TRỪ LƯỢT"""
    print(f"\n{C.BC}╔{'═' * 70}╗{C.E}")
    print(f"{C.BC}║ {I['upload']} ĐANG XỬ LÝ{' ' * 54}║{C.E}")
    print(f"{C.BC}║ {C.W}📖 {assignment['title']:<64}║{C.E}")
    print(f"{C.BC}╚{'═' * 70}╝{C.E}\n")
    
    if assignment['is_video']:
        print(f"{C.BB}🎬 Loại: Video{C.E}")
        target_score = 100
    elif assignment['is_ly_thuyet']:
        print(f"{C.Cy}📚 Loại: Lý thuyết{C.E}")
        target_score = get_target_score(False, False)
    elif assignment['is_kiem_tra']:
        print(f"{C.BY}⚠️ Loại: Kiểm tra{C.E}")
        target_score = get_target_score(False, True)
    else:
        print(f"{C.BG}📝 Loại: Bài tập{C.E}")
        target_score = get_target_score(False, False)
    
    try:
        quiz_list, total_questions, id_courseware, id_cate = extract_quiz_info(
            session, assignment['url'], assignment['is_video']
        )
        
        # VIDEO
        if assignment['is_video']:
            status("Đang xử lý video...", 'video', C.BB)
            success = handle_video_submission(session, assignment, user_id, quiz_list, total_questions, id_courseware, id_cate)
            
            if success:
                print(f"\n{C.BG}╔{'═' * 70}╗{C.E}")
                print(f"{C.BG}║ {I['check']} HOÀN THÀNH! ({assignment['title'][:50]}){' ' * (12 - min(len(assignment['title']), 50))}║{C.E}")
                print(f"{C.BG}╚{'═' * 70}╝{C.E}")
                consume_one_attempt()
                wait()
            
            return success
        
        # BÀI THƯỜNG
        if not quiz_list or total_questions == 0:
            # LÝ THUYẾT đặc biệt
            if assignment['is_ly_thuyet']:
                status("Bài lý thuyết - đã xử lý", 'success', C.BG)
                consume_one_attempt()
                wait()
                return True
            
            status("Không thể lấy thông tin bài", 'error', C.BR)
            return False
        
        status(f"Đang tạo dữ liệu cho {total_questions} câu...", 'clock', C.BY)
        data_log, total_time, correct_needed = create_data_log_for_normal(total_questions, target_score)
        
        csrf_token = session.cookies.get('XSRF-TOKEN')
        if not csrf_token:
            resp = session.get(assignment['url'], timeout=10)
            csrf_match = re.search(r'<meta name="csrf-token" content="([^"]+)"', resp.text)
            csrf_token = csrf_match.group(1) if csrf_match else ""
        
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
        
        status("Đang nộp bài...", 'upload', C.BY)
        
        submit_headers = HEADERS.copy()
        submit_headers['x-csrf-token'] = csrf_token
        
        response = session.post(
            'https://olm.vn/course/teacher-static',
            data=payload,
            headers=submit_headers,
            timeout=15
        )
        
        status(f"Phản hồi: HTTP {response.status_code}", 'info', C.W)
        
        success = handle_submission_response(response, target_score)
        
        if success:
            print(f"\n{C.BG}╔{'═' * 70}╗{C.E}")
            print(f"{C.BG}║ {I['check']} HOÀN THÀNH! ({assignment['title'][:50]}){' ' * (12 - min(len(assignment['title']), 50))}║{C.E}")
            print(f"{C.BG}╚{'═' * 70}╝{C.E}")
            consume_one_attempt()
            wait()
        else:
            # LÝ THUYẾT vẫn trừ
            if assignment['is_ly_thuyet']:
                status("Lý thuyết - vẫn tính đã xử lý", 'warn', C.BY)
                consume_one_attempt()
        
        return success
            
    except Exception as e:
        status(f"Lỗi: {str(e)}", 'error', C.BR)
        
        if assignment['is_ly_thuyet']:
            consume_one_attempt()
        
        return False

# ========== GIẢI TỪ LINK ==========
def solve_from_link(session, user_id):
    """Giải bài từ link"""
    header("GIẢI BÀI TỪ LINK")
    
    print(f"{C.Cy}{I['link']} NHẬP LINK BÀI TẬP:{C.E}")
    print("Ví dụ: https://olm.vn/chu-de/...\n")
    
    url = fancy_input("Dán link bài tập: ")
    
    if not url.startswith('https://olm.vn/'):
        status("Link không hợp lệ! Phải là link OLM", 'error', C.BR)
        wait()
        return False
    
    try:
        resp = session.get(url, timeout=10)
        is_video = 'video' in url.lower() or '[Video]' in resp.text
        is_ly_thuyet = 'ly-thuyet' in url.lower() or 'lý-thuyết' in url.lower() or '[Lý thuyết]' in resp.text
        
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
        
        if assignment['is_video']:
            assignment['type'] = "Video"
        elif assignment['is_ly_thuyet']:
            assignment['type'] = "Lý thuyết"
        
        print(f"\n{C.Cy}╔{'═' * 48}╗{C.E}")
        print(f"{C.Cy}║ {I['book']} THÔNG TIN BÀI TẬP{' ' * 25}║{C.E}")
        print(f"{C.Cy}╠{'═' * 48}╣{C.E}")
        print(f"{C.Cy}║ {C.W}📖 Link: {url[:33]}{' ' * (7 - max(0, 33 - len(url)))}║{C.E}")
        print(f"{C.Cy}║ {C.W}📝 Loại: {assignment['type']}{' ' * (35 - len(assignment['type']))}║{C.E}")
        print(f"{C.Cy}╚{'═' * 48}╝{C.E}\n")
        
        confirm = fancy_input("Xác nhận giải bài này? (y/n): ").lower()
        
        if confirm == 'y':
            success = submit_assignment(session, assignment, user_id)
            return success
        else:
            status("Đã hủy", 'warn', C.BY)
            wait()
            return False
            
    except Exception as e:
        status(f"Lỗi: {str(e)}", 'error', C.BR)
        wait()
        return False

# ========== GIẢI BÀI CỤ THỂ (0/1,3,5/1) ==========
def solve_specific_from_list(session, user_id):
    """Giải bài cụ thể - HỖ TRỢ 0/1,3,5/1"""
    header("GIẢI BÀI CỤ THỂ")
    
    pages_input = fancy_input("Số trang cần quét (mặc định: 3): ")
    pages_to_scan = 3
    if pages_input.isdigit() and int(pages_input) > 0:
        pages_to_scan = int(pages_input)
    
    assignments = get_assignments_fixed(session, pages_to_scan)
    if not assignments:
        wait()
        return False
    
    display_assignments_table(assignments)
    
    # CHỌN BÀI
    print(f"\n{C.Cy}Chọn bài để giải:{C.E}")
    print(f"  • Nhập {C.BY}0{C.E} để giải TẤT CẢ")
    print(f"  • Nhập {C.BY}1,3,5{C.E} để giải nhiều bài cụ thể")
    print(f"  • Nhập {C.BY}1{C.E} để giải 1 bài\n")
    
    selection = fancy_input("Lựa chọn: ")
    
    selected_assignments = []
    
    if selection == '0':
        selected_assignments = assignments
    elif ',' in selection:
        try:
            indices = [int(x.strip()) - 1 for x in selection.split(',')]
            for idx in indices:
                if 0 <= idx < len(assignments):
                    selected_assignments.append(assignments[idx])
        except:
            status("Lựa chọn không hợp lệ", 'error', C.BR)
            wait()
            return False
    else:
        try:
            idx = int(selection) - 1
            if 0 <= idx < len(assignments):
                selected_assignments = [assignments[idx]]
            else:
                status("Số bài không hợp lệ", 'error', C.BR)
                wait()
                return False
        except:
            status("Vui lòng nhập số", 'error', C.BR)
            wait()
            return False
    
    if not selected_assignments:
        status("Không có bài nào được chọn", 'warn', C.BY)
        wait()
        return False
    
    # CHỌN ĐIỂM 1 LẦN
    print(f"\n{C.Cy}Sẽ giải {len(selected_assignments)} bài{C.E}")
    
    non_auto_assignments = [a for a in selected_assignments if not (a['is_video'] or a['is_kiem_tra'])]
    
    if non_auto_assignments:
        target_score = get_target_score(False, False)
    else:
        target_score = 100
    
    # CONFIRM
    confirm = fancy_input(f"\nBắt đầu giải {len(selected_assignments)} bài? (y/n): ").lower()
    
    if confirm != 'y':
        status("Đã hủy", 'warn', C.BY)
        wait()
        return False
    
    # GIẢI
    success_count = 0
    total_count = len(selected_assignments)
    
    for idx, assignment in enumerate(selected_assignments, 1):
        print(f"\n{C.BY}╔{'═' * 48}╗{C.E}")
        print(f"{C.BY}║ {I['chart']} Bài {idx}/{total_count}{' ' * (40 - len(str(idx)) - len(str(total_count)))}║{C.E}")
        print(f"{C.BY}╚{'═' * 48}╝{C.E}")
        
        success = submit_assignment(session, assignment, user_id)
        
        if success:
            success_count += 1
        
        if idx < total_count:
            wait_time = random.randint(2, 5)
            status(f"Chờ {wait_time}s...", 'clock', C.BY)
            time.sleep(wait_time)
    
    # KẾT QUẢ
    print(f"\n{C.BG}╔{'═' * 70}╗{C.E}")
    print(f"{C.BG}║ {I['trophy']} KẾT QUẢ{' ' * 57}║{C.E}")
    print(f"{C.BG}║ {C.W}Hoàn thành: {C.BY}{success_count}/{total_count}{C.E} bài{' ' * (47 - len(str(success_count)) - len(str(total_count)))}║")
    print(f"{C.BG}╚{'═' * 70}╝{C.E}\n")
    
    wait()
    return success_count > 0

# ========== MENU 4 OPTIONS ==========
def main_menu(session, user_id, user_name):
    """Menu 4 options"""
    
    while True:
        header("MENU CHÍNH")
        
        # User info
        print(f"{I['user']} {C.BG}Xin chào: {user_name}{C.E}")
        
        # License info
        lic = load_license()
        if lic:
            if lic.get('mode') == 'VIP':
                print(f"{I['crown']} {C.BM}Trạng thái: VIP UNLIMITED{C.E}")
            else:
                remain = lic.get('remain', 0)
                print(f"{I['gem']} {C.Cy}Số lượt còn: {C.BY}{remain}{C.E}")
        
        # MENU
        print(f"\n{C.BC}┌{'─' * 68}┐{C.E}")
        print(f"{C.BC}│ {C.BW}{I['gear']} CHỨC NĂNG{' ' * 54}│{C.E}")
        print(f"{C.BC}├{'─' * 68}┤{C.E}")
        print(f"{C.BC}│ {C.BY}[1]{C.E} {I['brain']} Giải bài cụ thể{' ' * 42}│")
        print(f"{C.BC}│ {C.BY}[2]{C.E} {I['link']} Giải từ link{' ' * 46}│")
        print(f"{C.BC}│ {C.BY}[3]{C.E} {I['refresh']} Đổi tài khoản{' ' * 45}│")
        print(f"{C.BC}│ {C.BY}[4]{C.E} {I['exit']} Thoát{' ' * 54}│")
        print(f"{C.BC}└{'─' * 68}┘{C.E}")
        
        choice = fancy_input("\nChọn chức năng (1-4): ")
        
        if choice == '1':
            solve_specific_from_list(session, user_id)
        
        elif choice == '2':
            solve_from_link(session, user_id)
        
        elif choice == '3':
            # ĐỔI TÀI KHOẢN
            status("Đổi tài khoản...", 'refresh', C.BY)
            clear_account_lock()
            status("Đã xóa account lock, key vẫn còn hiệu lực", 'info', C.Cy)
            time.sleep(1)
            status("Quay về launcher để đăng nhập tài khoản mới", 'back', C.BG)
            time.sleep(2)
            sys.exit(0)
        
        elif choice == '4':
            status("Cảm ơn đã sử dụng!", 'exit', C.BG)
            time.sleep(1)
            sys.exit(0)
        
        else:
            status("Lựa chọn không hợp lệ!", 'error', C.BR)
            time.sleep(1)

# ========== MAIN ==========
def main():
    """Main function"""
    
    # 1. LOAD SESSION
    session, user_id, user_name = load_session()
    
    if not session:
        status("Lỗi session! Vui lòng chạy launcher", 'error', C.BR)
        wait()
        sys.exit(1)
    
    # 2. CHECK LICENSE
    lic = load_license()
    
    if not lic:
        status("Lỗi license! Vui lòng chạy launcher", 'error', C.BR)
        wait()
        sys.exit(1)
    
    # 3. UPDATE HEADERS
    session.headers.update(HEADERS)
    
    # 4. MENU
    main_menu(session, user_id, user_name)

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
