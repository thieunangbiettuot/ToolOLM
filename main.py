#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║                 OLM MASTER PRO - MAIN V1.0                   ║
║                     Created by: Tuấn Anh                     ║
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
import base64
import hashlib
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
    'diamond': '💎'
}

# ========== TIỆN ÍCH HIỂN THỊ ==========
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def animate_text(text, color=Colors.WHITE, delay=0.05):
    for char in text:
        sys.stdout.write(f"{color}{char}{Colors.END}")
        sys.stdout.flush()
        time.sleep(delay)
    print()

def spinner_animation(message, duration=2, color=Colors.CYAN):
    spinner = ['|', '/', '-', '\\']
    end_time = time.time() + duration
    i = 0
    print(f"{color}{message}{Colors.END}", end='')
    while time.time() < end_time:
        sys.stdout.write(f"\r{color}{message} {spinner[i % 4]}{Colors.END}")
        sys.stdout.flush()
        i += 1
        time.sleep(0.2)
    print("\r" + " " * (len(message) + 2) + "\r", end='')

def print_centered(text, color=Colors.WHITE, width=60):
    padding = (width - len(text.strip())) // 2
    print(f"{color}{' ' * padding}{text}{Colors.END}")

def print_line(char='═', color=Colors.CYAN, width=60):
    print(f"{color}{char * width}{Colors.END}")

def print_header(title=""):
    clear_screen()
    print_line('═', Colors.BLUE, 60)
    print_centered(f"{ICONS['rocket']} OLM MASTER PRO V1.0 {ICONS['fire']}", Colors.BLUE + Colors.BOLD, 60)
    print_centered("Created by: Tuấn Anh", Colors.PURPLE, 60)
    if title:
        print_line('─', Colors.CYAN, 60)
        print_centered(title, Colors.CYAN, 60)
    print_line('═', Colors.BLUE, 60)
    print()

def print_menu(title, options):
    print(f"\n{Colors.CYAN}{ICONS['setting']} {title}{Colors.END}")
    print_line('─', Colors.CYAN, 40)
    for key, value in options.items():
        print(f" {Colors.YELLOW}{key}.{Colors.END} {value}")
    print_line('─', Colors.CYAN, 40)

def wait_enter(prompt="Nhấn Enter để tiếp tục..."):
    input(f"\n{Colors.YELLOW}{prompt}{Colors.END}")

def print_status(message, icon='info', color=Colors.WHITE):
    print(f"{ICONS.get(icon, '')} {color}{message}{Colors.END}")

# ========== BẢO MẬT ==========
SECRET_KEY = b'OLM_MASTER_PRO_2026_SECRET_KEY_42'

def encrypt_data(data):
    json_str = json.dumps(data)
    bytes_data = json_str.encode()
    xor_data = bytearray(b ^ SECRET_KEY[i % len(SECRET_KEY)] for i, b in enumerate(bytes_data))
    b85_data = base64.b85encode(xor_data).decode()
    checksum = hashlib.sha256(b85_data.encode()).hexdigest()[:12]
    noise_prefix = hashlib.md5(os.urandom(16)).hexdigest()[:8]
    noise_suffix = noise_prefix[::-1]
    return f"{noise_prefix}{checksum}{b85_data}{noise_suffix}"

def decrypt_data(encrypted_str):
    try:
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
        json_str = bytes_data.decode()
        return json.loads(json_str)
    except:
        return None

def verify_integrity(data):
    if not data:
        return False
    sig_expected = hashlib.sha256(f"{data.get('mode', '')}{data.get('expire', '')}{data.get('ip', '')}".encode()).hexdigest()
    return data.get('sig') == sig_expected

def compute_sig(data):
    return hashlib.sha256(f"{data['mode']}{data['expire']}{data['ip']}".encode()).hexdigest()

# ========== LOAD SESSION & LICENSE ==========
def load_session():
    session_file = os.environ.get('OLM_SESSION_FILE')
    if session_file and os.path.exists(session_file):
        with open(session_file, 'rb') as f:
            data = pickle.load(f)
        session = requests.Session()
        session.cookies.update(data['cookies'])
        session.headers.update({
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'vi-VN,vi;q=0.9,en-US;q=0.8',
            'x-requested-with': 'XMLHttpRequest',
            'origin': 'https://olm.vn',
            'referer': 'https://olm.vn/'
        })
        return session, data['user_id'], data['user_name']
    print_status("Không tìm thấy session!", 'error', Colors.RED)
    sys.exit(1)

def load_license():
    license_file = os.environ.get('OLM_LICENSE_FILE')
    if license_file and os.path.exists(license_file):
        with open(license_file, 'r') as f:
            encrypted = f.read()
        data = decrypt_data(encrypted)
        if data and verify_integrity(data):
            return data
    return None

def save_license_updated(data):
    encrypted = encrypt_data(data)
    license_file = os.environ.get('OLM_LICENSE_FILE')
    with open(license_file, 'w') as f:
        f.write(encrypted)

def get_remaining_credits(license_data):
    if license_data['mode'] == 'VIP':
        return 'Unlimited'
    return license_data.get('remain', 0)

def deduct_credit(license_data, success, is_theory=False):
    if license_data['mode'] == 'VIP':
        return True
    if success or is_theory:
        if license_data['remain'] > 0:
            license_data['remain'] -= 1
            license_data['sig'] = compute_sig(license_data)
            save_license_updated(license_data)
            print_status(f"{ICONS['diamond']} Còn: {license_data['remain']} lượt", 'diamond', Colors.CYAN)
            return True
    return False

# ========== PHẦN QUÉT BÀI TẬP ==========
def get_assignments_fixed(session, pages_to_scan=3):
    assignments = []
    seen_links = set()
    for page in range(1, pages_to_scan + 1):
        url = "https://olm.vn/lop-hoc-cua-toi?action=login" if page == 1 else f"https://olm.vn/lop-hoc-cua-toi/page-{page}?action=login"
        response = session.get(url, timeout=10)
        if response.status_code != 200:
            continue
        soup = BeautifulSoup(response.text, 'html.parser')
        rows = soup.find_all('tr', class_='my-gived-courseware-item')
        for row in rows:
            link_tags = row.find_all('a', class_='olm-text-link')
            if not link_tags:
                continue
            main_link = link_tags[0]
            href = main_link.get('href')
            link_text = main_link.get_text(strip=True)
            if not href or any(mon in link_text for mon in ['(Toán', '(Ngữ văn', '(Tiếng Anh', '(Tin học']):
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
            should_process = False
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
            if should_process and href not in seen_links:
                seen_links.add(href)
                mon = row.find('span', class_='alert')
                mon_text = mon.get_text(strip=True) if mon else "Khác"
                ten_bai = re.sub(r'\([^)]*\)', '', link_text).strip()
                status = "Chưa làm" if not status_spans else status_spans[0].get_text(strip=True)
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
                    'is_bai_tap': is_bai_tap,
                    'is_kiem_tra': is_kiem_tra,
                    'is_tu_luan': is_tu_luan
                })
    return assignments

def display_assignments_table(assignments):
    if not assignments:
        return
    print(f"\n{Colors.PURPLE}{'📚 DANH SÁCH BÀI TẬP CẦN LÀM 📚':^90}{Colors.END}")
    print_line('─', Colors.PURPLE, 90)
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
    print_line('─', Colors.PURPLE, 90)

# ========== PHẦN XỬ LÝ BÀI TẬP ==========
def get_target_score(is_video=False, is_kiem_tra=False):
    if is_video:
        print_status("Video: Tự động chọn 100 điểm", 'video', Colors.BLUE)
        return 100
    elif is_kiem_tra:
        print_status("Kiểm tra: Tự động chọn điểm cao", 'warning', Colors.YELLOW)
        return random.randint(85, 100)
    print(f"\n{Colors.CYAN}{ICONS['star']} CHỌN ĐIỂM SỐ{Colors.END}")
    print_line('─', Colors.CYAN, 40)
    print(f" {Colors.YELLOW}1.{Colors.END} {ICONS['star']} 100 điểm (Xuất sắc)")
    print(f" {Colors.YELLOW}2.{Colors.END} {ICONS['question']} Tùy chọn điểm số")
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
                return None, 0, id_courseware, id_cate
        question_ids = [qid.strip() for qid in quiz_list.split(',') if qid.strip()]
        total_questions = len(question_ids)
        return quiz_list, total_questions, id_courseware, id_cate
    except Exception as e:
        return None, 0, None, None

def create_data_log_for_normal(total_questions, target_score):
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

def submit_assignment(session, assignment, user_id, license_data):
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
        if assignment['is_video']:
            success = handle_video_submission(session, assignment, user_id, quiz_list, total_questions, id_courseware, id_cate)
        else:
            if not quiz_list or total_questions == 0:
                print_status("Không thể lấy thông tin bài", 'error', Colors.RED)
                success = False
            else:
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
                submit_headers = session.headers.copy()
                submit_headers['x-csrf-token'] = csrf_token
                response = session.post(
                    'https://olm.vn/course/teacher-static',
                    data=payload,
                    headers=submit_headers,
                    timeout=15
                )
                success = handle_submission_response(response, target_score)
        deduct_credit(license_data, success, assignment['is_ly_thuyet'])
        return success
    except Exception as e:
        print_status(f"Lỗi: {str(e)}", 'error', Colors.RED)
        return False

def handle_video_submission(session, assignment, user_id, quiz_list, total_questions, id_courseware, id_cate):
    # Giữ nguyên logic từ code gốc, che các method
    # Giả sử gọi try_video_simple_method, etc., nhưng che bằng cách không print chi tiết
    methods = [try_video_simple_method, try_video_with_quiz, try_video_complex_method]
    for method in methods:
        success = method(session, assignment, user_id, quiz_list, total_questions, id_courseware, id_cate)
        if success:
            return True
    return False

# Copy các hàm try_video_... từ code gốc

def submit_assignment(session, assignment, user_id, license_data):
    print_status(f"Đang xử lý: {assignment['title']}", 'upload', Colors.YELLOW)
    target_score = get_target_score(assignment['is_video'], assignment['is_kiem_tra'])
    quiz_list, total_questions, id_courseware, id_cate = extract_quiz_info(session, assignment['url'], assignment['is_video'])
    if assignment['is_video']:
        success = handle_video_submission(session, assignment, user_id, quiz_list, total_questions, id_courseware, id_cate)
    else:
        if not quiz_list or total_questions == 0:
            return False
        data_log, total_time, correct_needed = create_data_log_for_normal(total_questions, target_score)
        csrf_token = session.cookies.get('XSRF-TOKEN') or re.search(r'<meta name="csrf-token" content="([^"]+)"', session.get(assignment['url']).text).group(1)
        current_time = int(time.time())
        start_time = current_time - total_time
        payload = {  # Payload từ code gốc
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
            'user_ans': json.dumps(["0"] * total_questions),
            'list_quiz': quiz_list or '',
            'list_ans': ','.join(["0"] * total_questions),
            'result': '[]',
            'ans': '[]'
        }
        submit_headers = session.headers.copy()
        submit_headers['x-csrf-token'] = csrf_token
        response = session.post('https://olm.vn/course/teacher-static', data=payload, headers=submit_headers, timeout=15)
        success = handle_submission_response(response, target_score)
    deduct_credit(license_data, success, assignment['is_ly_thuyet'])
    return success

# Copy handle_submission_response từ code gốc

# ========== MENU CHÍNH ==========
def main():
    print_header("MENU CHÍNH")
    session, user_id, user_name = load_session()
    license_data = load_license()
    if not license_data:
        print_status("License hết hạn hoặc không hợp lệ!", 'error', Colors.RED)
        options = {
            '1': "Quay lại launcher lấy key mới",
            '2': "Thoát"
        }
        print_menu("LỰA CHỌN", options)
        choice = input(f"\n{Colors.YELLOW}Chọn: {Colors.END}").strip()
        if choice == '1':
            sys.exit(0)
        else:
            sys.exit(1)
    remaining = get_remaining_credits(license_data)
    print_status(f"Lượt còn lại: {remaining}", 'diamond', Colors.CYAN)
    while True:
        options = {
            '1': f"{ICONS['brain']} Giải bài cụ thể",
            '2': f"{ICONS['link']} Giải từ link",
            '3': f"{ICONS['refresh']} Đổi tài khoản",
            '4': f"{ICONS['exit']} Thoát"
        }
        print_menu("LỰA CHỌN", options)
        choice = input(f"\n{Colors.YELLOW}Chọn: {Colors.END}").strip()
        if choice == '1':
            pages = int(input_prompt("Số trang quét (mặc định 3): ") or 3)
            assignments = get_assignments_fixed(session, pages)
            display_assignments_table(assignments)
            selection = input_prompt("Chọn bài (0=tất cả, 1,3,5=nhiều, 1=một): ")
            selected = []
            if selection == '0':
                selected = assignments
            elif ',' in selection:
                indices = [int(i)-1 for i in selection.split(',')]
                selected = [assignments[i] for i in indices if 0 <= i < len(assignments)]
            else:
                idx = int(selection) - 1
                if 0 <= idx < len(assignments):
                    selected = [assignments[idx]]
            if selected:
                score = get_target_score()  # Chọn 1 lần
                confirm = input_prompt("Xác nhận? (y/n): ").lower() == 'y'
                if confirm:
                    success_count = 0
                    for idx, ass in enumerate(selected, 1):
                        print_status(f"Bài {idx}/{len(selected)}", 'info', Colors.BLUE)
                        if submit_assignment(session, ass, user_id, license_data):
                            success_count += 1
                    print_status(f"Hoàn thành {success_count}/{len(selected)} bài", 'success', Colors.GREEN)
        elif choice == '2':
            url = input_prompt("Dán link: ")
            assignment = {'url': url, 'title': 'Từ link', 'is_video': False, 'is_ly_thuyet': False, 'is_kiem_tra': False}  # Điều chỉnh dựa trên url
            submit_assignment(session, assignment, user_id, license_data)
        elif choice == '3':
            delete_lock()
            sys.exit(0)
        elif choice == '4':
            sys.exit(0)
        if get_remaining_credits(license_data) == 0:
            print_status("Hết lượt!", 'error', Colors.RED)
            options = {
                '1': "Quay lại launcher lấy key mới",
                '2': "Thoát"
            }
            print_menu("LỰA CHỌN", options)
            choice = input_prompt("Chọn: ")
            if choice == '1':
                sys.exit(0)
            else:
                sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{ICONS['exit']} {Colors.YELLOW}Đã dừng chương trình{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{ICONS['error']} {Colors.RED}Lỗi không mong muốn: {str(e)}{Colors.END}")
        wait_enter()
