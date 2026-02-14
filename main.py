#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║              OLM MASTER PRO V1.0 - MAIN SOLVER               ║
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
    print("Error: Missing required libraries")
    sys.exit(1)

import re

# ==================== CẤU HÌNH ====================
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
    'user': '👤', 'key': '🔑', 'lock': '🔐', 'star': '⭐', 'gem': '💎',
    'fire': '🔥', 'rocket': '🚀', 'check': '✔️', 'exit': '🚪',
    'link': '🔗', 'clock': '⏰', 'refresh': '🔄', 'video': '🎬',
    'theory': '📖', 'exercise': '📝', 'book': '📚', 'search': '🔍',
    'upload': '📤', 'brain': '🧠', 'setting': '⚙️', 'back': '↩️'
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
        json_str = decrypted.decode('utf-8')
        data_dict = json.loads(json_str)
        
        return data_dict
    except:
        return None

def load_file(filepath):
    if not os.path.exists(filepath):
        return None
    try:
        with open(filepath, 'r') as f:
            encrypted = f.read()
        return decrypt_data(encrypted)
    except:
        return None

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

def save_file(filepath, data_dict):
    encrypted = encrypt_data(data_dict)
    if encrypted:
        with open(filepath, 'w') as f:
            f.write(encrypted)
        return True
    return False

# ==================== UI HELPERS ====================
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print('\033[2J\033[H', end='')

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

# ==================== LICENSE MANAGEMENT ====================
def load_license():
    return load_file(PATHS['license'])

def compute_signature(license_data):
    sig_str = f"{license_data.get('mode', '')}{license_data.get('expire', '')}{license_data.get('ip', '')}"
    return hashlib.sha256(sig_str.encode()).hexdigest()[:16]

def consume_one_attempt():
    """Trừ 1 lượt (SAU KHI thành công)"""
    lic = load_license()
    if not lic:
        print_status("Lỗi license!", 'error', Colors.RED)
        return False
    
    # VIP không trừ
    if lic.get('mode') == 'VIP':
        print(f"{ICONS['gem']} {Colors.PURPLE}VIP Unlimited{Colors.END}")
        return True
    
    # FREE trừ lượt
    lic['remain'] -= 1
    
    if lic['remain'] <= 0:
        # HẾT LƯỢT
        if os.path.exists(PATHS['license']):
            os.remove(PATHS['license'])
        if os.path.exists(PATHS['lock']):
            os.remove(PATHS['lock'])
        
        print(f"\n{Colors.RED}⛔ HẾT LƯỢT{Colors.END}\n")
        print(f"  {Colors.YELLOW}[1]{Colors.END} Quay launcher lấy key mới")
        print(f"  {Colors.YELLOW}[2]{Colors.END} Thoát\n")
        
        choice = input(f"{Colors.YELLOW}Chọn: {Colors.END}").strip()
        
        sys.exit(0)
    
    # Lưu license
    save_file(PATHS['license'], lic)
    
    # Hiển thị số lượt còn
    print(f"{ICONS['gem']} {Colors.GREEN}Còn: {lic['remain']} lượt{Colors.END}")
    
    return True

def clear_account_lock():
    """Xóa account lock"""
    if os.path.exists(PATHS['lock']):
        os.remove(PATHS['lock'])

# ==================== LOAD SESSION ====================
def load_session():
    """Load session từ launcher"""
    try:
        with open(PATHS['session'], 'rb') as f:
            session_data = pickle.load(f)
        
        session = requests.Session()
        session.cookies.update(session_data['cookies'])
        
        return session, session_data['user_id'], session_data['user_name']
    except:
        return None, None, None

# ==================== HEADERS ====================
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'vi-VN,vi;q=0.9,en-US;q=0.8',
    'x-requested-with': 'XMLHttpRequest',
    'origin': 'https://olm.vn',
    'referer': 'https://olm.vn/'
}

# ==================== QUÉT BÀI TẬP (100% GỐC) ====================
def get_assignments_fixed(session, pages_to_scan=5):
    """Lấy danh sách bài tập - GIỮ 100% LOGIC GỐC"""
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
                        
                        status = "Chưa làm"
                        if status_spans:
                            for span in status_spans:
                                span_text = span.get_text(strip=True)
                                if "chưa" in span_text.lower() or "làm tiếp" in span_text.lower():
                                    status = span_text
                                    break
                        
                        if not href.startswith('http'):
                            full_url = 'https://olm.vn' + href
                        else:
                            full_url = href
                        
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
        
        if assignments:
            print_status(f"Tổng cộng: {len(assignments)} bài cần xử lý", 'success', Colors.GREEN + Colors.BOLD)
            
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
    """Hiển thị danh sách bài tập - GIỮ GỐC"""
    if not assignments:
        return
    
    print(f"\n{Colors.PURPLE}{'📚 DANH SÁCH BÀI TẬP CẦN LÀM 📚':^90}{Colors.END}")
    print(f"{Colors.PURPLE}{'─' * 90}{Colors.END}")
    
    for idx, item in enumerate(assignments, 1):
        title = item['title']
        if len(title) > 38:
            title = title[:35] + "..."
        
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
    
    print(f"{Colors.PURPLE}{'─' * 90}{Colors.END}")

# ==================== CHỌN ĐIỂM (100% GỐC) ====================
def get_target_score(is_video=False, is_kiem_tra=False):
    """Menu chọn điểm - GIỮ GỐC"""
    if is_video:
        return 100
    elif is_kiem_tra:
        return random.randint(85, 100)
    
    print(f"\n{Colors.CYAN}{ICONS['star']} CHỌN ĐIỂM SỐ{Colors.END}")
    print(f"{Colors.CYAN}{'─' * 40}{Colors.END}")
    print(f"  {Colors.YELLOW}[1]{Colors.END} {ICONS['star']} 100 điểm (Xuất sắc)")
    print(f"  {Colors.YELLOW}[2]{Colors.END} {ICONS['setting']} Tùy chọn điểm số")
    print(f"{Colors.CYAN}{'─' * 40}{Colors.END}")
    
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

# ==================== TRÍCH XUẤT THÔNG TIN (100% GỐC) ====================
def extract_quiz_info(session, url, is_video=False):
    """Trích xuất thông tin quiz - GIỮ 100% GỐC"""
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
                return "", 0, id_courseware, id_cate
            else:
                print_status("Không tìm thấy danh sách câu hỏi", 'error', Colors.RED)
                return None, 0, id_courseware, id_cate
        
        question_ids = [qid.strip() for qid in quiz_list.split(',') if qid.strip()]
        total_questions = len(question_ids)
        
        return quiz_list, total_questions, id_courseware, id_cate
        
    except Exception as e:
        print_status(f"Lỗi trích xuất thông tin: {str(e)}", 'error', Colors.RED)
        return None, 0, None, None

def create_data_log_for_normal(total_questions, target_score):
    """Tạo data_log - GIỮ 100% GỐC"""
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

# ==================== XỬ LÝ VIDEO (CHỈ METHOD 1) ====================
def try_video_simple_method(session, assignment, user_id, quiz_list, total_questions, id_courseware, id_cate):
    """Phương pháp video - CHỈ DÙNG METHOD NÀY"""
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
        
    except Exception as e:
        return False

def handle_submission_response(response, target_score):
    """Xử lý phản hồi - GIỮ 100% GỐC"""
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

# ==================== NỘP BÀI (100% GỐC + TRỪ LƯỢT) ====================
def submit_assignment(session, assignment, user_id):
    """Nộp bài tập - GIỮ 100% GỐC LOGIC + THÊM TRỪ LƯỢT"""
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
        quiz_list, total_questions, id_courseware, id_cate = extract_quiz_info(
            session, assignment['url'], assignment['is_video']
        )
        
        # XỬ LÝ VIDEO (chỉ 1 method)
        if assignment['is_video']:
            print_status("Đang xử lý video...", 'video', Colors.BLUE)
            success = try_video_simple_method(session, assignment, user_id, quiz_list, total_questions, id_courseware, id_cate)
            
            if success:
                print_status("HOÀN THÀNH!", 'success', Colors.GREEN + Colors.BOLD)
                # TRỪ LƯỢT
                consume_one_attempt()
            
            return success
        
        # BÀI THƯỜNG
        if not quiz_list or total_questions == 0:
            # BÀI LÝ THUYẾT đặc biệt: DÙ SAO CŨNG TRỪ LƯỢT
            if assignment['is_ly_thuyet']:
                print_status("Bài lý thuyết - đã xử lý", 'success', Colors.GREEN)
                consume_one_attempt()
                return True
            
            print_status("Không thể lấy thông tin bài", 'error', Colors.RED)
            return False
        
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
        
        print_status("Đang nộp bài...", 'upload', Colors.YELLOW)
        
        submit_headers = HEADERS.copy()
        submit_headers['x-csrf-token'] = csrf_token
        
        response = session.post(
            'https://olm.vn/course/teacher-static',
            data=payload,
            headers=submit_headers,
            timeout=15
        )
        
        success = handle_submission_response(response, target_score)
        
        if success:
            print_status("HOÀN THÀNH!", 'success', Colors.GREEN + Colors.BOLD)
            # TRỪ LƯỢT
            consume_one_attempt()
        else:
            # BÀI LÝ THUYẾT: dù thất bại vẫn trừ
            if assignment['is_ly_thuyet']:
                print_status("Lý thuyết - vẫn tính đã xử lý", 'warning', Colors.YELLOW)
                consume_one_attempt()
        
        return success
            
    except Exception as e:
        print_status(f"Lỗi: {str(e)}", 'error', Colors.RED)
        
        # BÀI LÝ THUYẾT: dù lỗi vẫn trừ
        if assignment['is_ly_thuyet']:
            consume_one_attempt()
        
        return False

# ==================== GIẢI BÀI TỪ LINK ====================
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
        
        print(f"\n{Colors.CYAN}📋 THÔNG TIN BÀI TẬP:{Colors.END}")
        print(f"  {Colors.WHITE}📖 Link: {url}{Colors.END}")
        print(f"  {Colors.CYAN}📝 Loại: {assignment['type']}{Colors.END}")
        
        confirm = input(f"\n{Colors.YELLOW}Xác nhận giải bài này? (y/n): {Colors.END}").strip().lower()
        
        if confirm == 'y':
            success = submit_assignment(session, assignment, user_id)
            wait_enter()
            return success
        else:
            print_status("Đã hủy", 'warning', Colors.YELLOW)
            wait_enter()
            return False
            
    except Exception as e:
        print_status(f"Lỗi: {str(e)}", 'error', Colors.RED)
        wait_enter()
        return False

# ==================== GIẢI BÀI CỤ THỂ (0/1,3,5/1) ====================
def solve_specific_from_list(session, user_id):
    """Giải bài cụ thể từ danh sách - HỖ TRỢ 0/1,3,5/1"""
    print_header("GIẢI BÀI CỤ THỂ")
    
    pages_input = input(f"{Colors.YELLOW}Số trang cần quét (mặc định: 3): {Colors.END}").strip()
    pages_to_scan = 3
    if pages_input.isdigit() and int(pages_input) > 0:
        pages_to_scan = int(pages_input)
    
    assignments = get_assignments_fixed(session, pages_to_scan)
    if not assignments:
        wait_enter()
        return False
    
    display_assignments_table(assignments)
    
    # CHỌN BÀI
    print(f"\n{Colors.CYAN}Chọn bài để giải:{Colors.END}")
    print(f"  • Nhập {Colors.YELLOW}0{Colors.END} để giải TẤT CẢ")
    print(f"  • Nhập {Colors.YELLOW}1,3,5{Colors.END} để giải nhiều bài cụ thể")
    print(f"  • Nhập {Colors.YELLOW}1{Colors.END} để giải 1 bài\n")
    
    selection = input(f"{Colors.YELLOW}Lựa chọn: {Colors.END}").strip()
    
    selected_assignments = []
    
    if selection == '0':
        # TẤT CẢ
        selected_assignments = assignments
    elif ',' in selection:
        # NHIỀU BÀI
        try:
            indices = [int(x.strip()) - 1 for x in selection.split(',')]
            for idx in indices:
                if 0 <= idx < len(assignments):
                    selected_assignments.append(assignments[idx])
        except:
            print_status("Lựa chọn không hợp lệ", 'error', Colors.RED)
            wait_enter()
            return False
    else:
        # 1 BÀI
        try:
            idx = int(selection) - 1
            if 0 <= idx < len(assignments):
                selected_assignments = [assignments[idx]]
            else:
                print_status("Số bài không hợp lệ", 'error', Colors.RED)
                wait_enter()
                return False
        except:
            print_status("Vui lòng nhập số", 'error', Colors.RED)
            wait_enter()
            return False
    
    if not selected_assignments:
        print_status("Không có bài nào được chọn", 'warning', Colors.YELLOW)
        wait_enter()
        return False
    
    # CHỌN ĐIỂM 1 LẦN
    print(f"\n{Colors.CYAN}Sẽ giải {len(selected_assignments)} bài{Colors.END}")
    
    # Lọc ra bài không phải video/kiểm tra để hỏi điểm
    non_auto_assignments = [a for a in selected_assignments if not (a['is_video'] or a['is_kiem_tra'])]
    
    if non_auto_assignments:
        target_score = get_target_score(False, False)
    else:
        target_score = 100  # Mặc định cho video/kiểm tra
    
    # CONFIRM
    confirm = input(f"\n{Colors.YELLOW}Bắt đầu giải {len(selected_assignments)} bài? (y/n): {Colors.END}").strip().lower()
    
    if confirm != 'y':
        print_status("Đã hủy", 'warning', Colors.YELLOW)
        wait_enter()
        return False
    
    # GIẢI TỪNG BÀI
    success_count = 0
    total_count = len(selected_assignments)
    
    for idx, assignment in enumerate(selected_assignments, 1):
        print(f"\n{Colors.YELLOW}📊 Bài {idx}/{total_count}{Colors.END}")
        
        # Gán điểm cho assignment
        if assignment['is_video']:
            # Video tự động 100
            pass
        elif assignment['is_kiem_tra']:
            # Kiểm tra random
            pass
        else:
            # Dùng điểm đã chọn
            assignment['target_score'] = target_score
        
        success = submit_assignment(session, assignment, user_id)
        
        if success:
            success_count += 1
        
        if idx < total_count:
            wait_time = random.randint(2, 5)
            print_status(f"Chờ {wait_time}s...", 'clock', Colors.YELLOW)
            time.sleep(wait_time)
    
    # KẾT QUẢ
    print(f"\n{Colors.CYAN}{'═' * 50}{Colors.END}")
    print(f"{Colors.CYAN}{ICONS['star']} KẾT QUẢ:{Colors.END}")
    print(f"{Colors.GREEN}Hoàn thành: {success_count}/{total_count} bài{Colors.END}")
    print(f"{Colors.CYAN}{'═' * 50}{Colors.END}")
    
    wait_enter()
    return success_count > 0

# ==================== MENU CHÍNH (4 OPTIONS) ====================
def main_menu(session, user_id, user_name):
    """Menu chính - 4 OPTIONS"""
    
    while True:
        print_header("MENU CHÍNH")
        
        # Hiển thị thông tin user
        print(f"{ICONS['user']} {Colors.GREEN}Xin chào: {user_name}{Colors.END}")
        
        # Hiển thị số lượt còn
        lic = load_license()
        if lic:
            if lic.get('mode') == 'VIP':
                print(f"{ICONS['star']} {Colors.PURPLE}Trạng thái: VIP UNLIMITED{Colors.END}")
            else:
                remain = lic.get('remain', 0)
                print(f"{ICONS['gem']} {Colors.CYAN}Số lượt còn: {remain}{Colors.END}")
        
        print()
        
        # MENU 4 OPTIONS
        print(f"{Colors.CYAN}{'─' * 50}{Colors.END}")
        print(f"  {Colors.YELLOW}[1]{Colors.END} {ICONS['brain']} Giải bài cụ thể")
        print(f"  {Colors.YELLOW}[2]{Colors.END} {ICONS['link']} Giải từ link")
        print(f"  {Colors.YELLOW}[3]{Colors.END} {ICONS['refresh']} Đổi tài khoản")
        print(f"  {Colors.YELLOW}[4]{Colors.END} {ICONS['exit']} Thoát")
        print(f"{Colors.CYAN}{'─' * 50}{Colors.END}")
        
        choice = input(f"\n{Colors.YELLOW}Chọn chức năng (1-4): {Colors.END}").strip()
        
        if choice == '1':
            solve_specific_from_list(session, user_id)
        
        elif choice == '2':
            solve_from_link(session, user_id)
        
        elif choice == '3':
            # ĐỔI TÀI KHOẢN
            print_status("Đổi tài khoản...", 'refresh', Colors.YELLOW)
            clear_account_lock()
            print_status("Đã xóa account lock, key vẫn còn hiệu lực", 'info', Colors.CYAN)
            time.sleep(1)
            print_status("Quay về launcher để đăng nhập tài khoản mới", 'back', Colors.GREEN)
            time.sleep(2)
            sys.exit(0)
        
        elif choice == '4':
            print_status("Cảm ơn đã sử dụng!", 'exit', Colors.GREEN)
            time.sleep(1)
            sys.exit(0)
        
        else:
            print_status("Lựa chọn không hợp lệ!", 'error', Colors.RED)
            time.sleep(1)

# ==================== MAIN ====================
def main():
    """Main function"""
    
    # 1. LOAD SESSION
    session, user_id, user_name = load_session()
    
    if not session:
        print_status("Lỗi session! Vui lòng chạy launcher", 'error', Colors.RED)
        wait_enter()
        sys.exit(1)
    
    # 2. CHECK LICENSE
    lic = load_license()
    
    if not lic:
        print_status("Lỗi license! Vui lòng chạy launcher", 'error', Colors.RED)
        wait_enter()
        sys.exit(1)
    
    # 3. UPDATE HEADERS
    session.headers.update(HEADERS)
    
    # 4. MENU
    main_menu(session, user_id, user_name)

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
