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
                print_status("Video: Không có quiz_list, sẽ thử phương pháp khác", 'video', Colors.BLUE)
                return "", 0, id_courseware, id_cate
            else:
                print_status("Không tìm thấy danh sách câu hỏi", 'error', Colors.RED)
                return None, 0, id_courseware, id_cate
        question_ids = [qid.strip() for qid in quiz_list.split(',') if qid.strip()]
        total_questions = len(question_ids)
        print_status(f"Tìm thấy {total_questions} câu hỏi", 'info', Colors.WHITE)
        return quiz_list, total_questions, id_courseware, id_cate
    except Exception as e:
        print_status(f"Lỗi trích xuất thông tin: {str(e)}", 'error', Colors.RED)
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
            print_status("Đang xử lý video...", 'video', Colors.BLUE)
            success = handle_video_submission(session, assignment, user_id, quiz_list, total_questions, id_courseware, id_cate)
        else:
            if not quiz_list or total_questions == 0:
                print_status("Không thể lấy thông tin bài", 'error', Colors.RED)
                success = False
            else:
                print_status(f"Đang tạo dữ liệu cho {total_questions} câu...", 'clock', Colors.YELLOW)
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
                print_status("Đang nộp bài...", 'upload', Colors.YELLOW)
                response = session.post(
                    'https://olm.vn/course/teacher-static',
                    data=payload,
                    headers=submit_headers,
                    timeout=15
                )
                print_status(f"Phản hồi: HTTP {response.status_code}", 'info', Colors.WHITE)
                success = handle_submission_response(response, target_score)
        if success:
            print_status(f"{ICONS['success']} HOÀN THÀNH BÀI ({assignment['title']})", 'success', Colors.GREEN + Colors.BOLD)
            wait_enter()
        deduct_credit(license_data, success, assignment['is_ly_thuyet'])
        return success
    except Exception as e:
        print_status(f"Lỗi: {str(e)}", 'error', Colors.RED)
        return False

def handle_video_submission(session, assignment, user_id, quiz_list, total_questions, id_courseware, id_cate):
    methods = [
        try_video_simple_method,
        try_video_with_quiz,
        try_video_complex_method,
    ]
    for i, method in enumerate(methods, 1):
        print_status(f"Thử phương pháp {i} cho video...", 'video', Colors.BLUE)
        success = method(session, assignment, user_id, quiz_list, total_questions, id_courseware, id_cate)
        if success:
            return True
        time.sleep(1)
    print_status("Tất cả phương pháp đều thất bại", 'error', Colors.RED)
    return False

def try_video_simple_method(session, assignment, user_id, quiz_list, total_questions, id_courseware, id_cate):
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
            'cv_q': '1',
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
        if quiz_list:
            payload['quiz_list'] = quiz_list
        submit_headers = session.headers.copy()
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
        submit_headers = session.headers.copy()
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
        submit_headers = session.headers.copy()
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

def handle_submission_response(response, target_score):
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
        except:
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
def solve_from_link(session, user_id, license_data):
    print_header("GIẢI BÀI TỪ LINK")
    url = input(f"{ICONS['link']} {Colors.YELLOW}Dán link bài tập: {Colors.END}").strip()
    if not url.startswith('https://olm.vn/'):
        print_status("Link không hợp lệ! Phải là link OLM", 'error', Colors.RED)
        wait_enter()
        return
    try:
        resp = session.get(url, timeout=10)
        is_video = 'video' in url.lower() or '[Video]' in resp.text
        is_ly_thuyet = 'ly-thuyet' in url.lower() or 'lý-thuyết' in url.lower() or '[Lý thuyết]' in resp.text
        is_kiem_tra = '[Kiểm tra]' in resp.text or 'kiem-tra' in url.lower()
        assignment = {
            'title': "Bài từ link",
            'subject': "Tự chọn",
            'type': "Bài tập",
            'status': "Chưa làm",
            'url': url,
            'page': 1,
            'is_video': is_video,
            'is_ly_thuyet': is_ly_thuyet,
            'is_bai_tap': not (is_video or is_ly_thuyet or is_kiem_tra),
            'is_kiem_tra': is_kiem_tra,
            'is_tu_luan': False
        }
        if assignment['is_video']:
            assignment['type'] = "Video"
        elif assignment['is_ly_thuyet']:
            assignment['type'] = "Lý thuyết"
        elif assignment['is_kiem_tra']:
            assignment['type'] = "Kiểm tra"
        print(f"\n{Colors.CYAN}📋 THÔNG TIN BÀI TẬP:{Colors.END}")
        print(f" {Colors.WHITE}📖 Link: {url}{Colors.END}")
        print(f" {Colors.CYAN}📝 Loại: {assignment['type']}{Colors.END}")
        confirm = input(f"\n{Colors.YELLOW}Xác nhận giải bài này? (y/n): {Colors.END}").strip().lower()
        if confirm == 'y':
            submit_assignment(session, assignment, user_id, license_data)
        else:
            print_status("Đã hủy", 'warning', Colors.YELLOW)
    except Exception as e:
        print_status(f"Lỗi: {str(e)}", 'error', Colors.RED)

# ========== GIẢI BÀI CỤ THỂ ==========
def solve_specific(session, user_id, license_data):
    print_header("GIẢI BÀI CỤ THỂ")
    pages_input = input(f"{Colors.YELLOW}Số trang cần quét (mặc định: 3): {Colors.END}").strip()
    pages_to_scan = 3 if not pages_input.isdigit() else int(pages_input)
    assignments = get_assignments_fixed(session, pages_to_scan)
    if not assignments:
        wait_enter()
        return
    display_assignments_table(assignments)
    selection = input(f"\n{Colors.YELLOW}Chọn số bài để giải (0=tất cả, 1,3,5=nhiều, 1=1 bài): {Colors.END}").strip()
    selected_indices = []
    if selection == '0':
        selected_indices = list(range(len(assignments)))
    elif ',' in selection:
        selected_indices = [int(i.strip()) - 1 for i in selection.split(',') if i.strip().isdigit()]
    elif selection.isdigit():
        selected_indices = [int(selection) - 1]
    selected = [assignments[i] for i in selected_indices if 0 <= i < len(assignments)]
    if not selected:
        print_status("Số bài không hợp lệ", 'error', Colors.RED)
        wait_enter()
        return
    target_score = get_target_score()
    confirm = input(f"\n{Colors.YELLOW}Xác nhận? (y/n): {Colors.END}").strip().lower()
    if confirm != 'y':
        return
    success_count = 0
    total_count = len(selected)
    for idx, assignment in enumerate(selected, 1):
        print(f"\n{Colors.YELLOW}📊 Bài {idx}/{total_count}{Colors.END}")
        success = submit_assignment(session, assignment, user_id, license_data)
        if success:
            success_count += 1
        else:
            print_status(f"Không thể xử lý bài {idx}", 'error', Colors.RED)
        if idx < total_count:
            wait_time = random.randint(2, 5)
            print_status(f"Chờ {wait_time}s...", 'clock', Colors.YELLOW)
            time.sleep(wait_time)
    print_status(f"Hoàn thành {success_count}/{total_count} bài", 'success', Colors.GREEN)
    wait_enter()

# ========== MENU CHÍNH ==========
def main_menu(session, user_id, user_name, license_data):
    while True:
        print_header("MENU CHÍNH")
        print(f"{ICONS['user']} {Colors.GREEN}Xin chào: {user_name}{Colors.END}")
        remaining = get_remaining_credits(license_data)
        print_status(f"{ICONS['diamond']} Còn: {remaining} lượt", 'diamond', Colors.CYAN)
        menu_options = {
            '1': f"{ICONS['brain']} Giải bài cụ thể",
            '2': f"{ICONS['link']} Giải từ link",
            '3': f"{ICONS['refresh']} Đổi tài khoản",
            '4': f"{ICONS['exit']} Thoát"
        }
        print_menu("LỰA CHỌN", menu_options)
        choice = input(f"\n{Colors.YELLOW}Chọn chức năng (1-4): {Colors.END}").strip()
        if choice == '1':
            solve_specific(session, user_id, license_data)
        elif choice == '2':
            solve_from_link(session, user_id, license_data)
        elif choice == '3':
            print_status("Đang đổi tài khoản...", 'refresh', Colors.YELLOW)
            time.sleep(1)
            sys.exit(0)  # Quay launcher
        elif choice == '4':
            print_status("Cảm ơn đã sử dụng!", 'exit', Colors.GREEN)
            time.sleep(1)
            sys.exit(0)
        else:
            print_status("Lựa chọn không hợp lệ!", 'error', Colors.RED)
            time.sleep(1)
        if get_remaining_credits(license_data) == 0:
            print_status("⛔ HẾT LƯỢT", 'error', Colors.RED)
            options = {
                '1': "Quay launcher lấy key mới",
                '2': "Thoát"
            }
            print_menu("LỰA CHỌN", options)
            choice = input(f"\n{Colors.YELLOW}Chọn: {Colors.END}").strip()
            if choice == '1':
                sys.exit(0)
            else:
                sys.exit(1)

# ========== CHƯƠNG TRÌNH CHÍNH ==========
def main():
    session, user_id, user_name = load_session()
    license_data = load_license()
    if not license_data:
        print_status("License hết hạn hoặc không hợp lệ!", 'error', Colors.RED)
        options = {
            '1': "Quay launcher lấy key mới",
            '2': "Thoát"
        }
        print_menu("LỰA CHỌN", options)
        choice = input(f"\n{Colors.YELLOW}Chọn: {Colors.END}").strip()
        if choice == '1':
            sys.exit(0)
        else:
            sys.exit(1)
    main_menu(session, user_id, user_name, license_data)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{ICONS['exit']} {Colors.YELLOW}Đã dừng chương trình{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{ICONS['error']} {Colors.RED}Lỗi không mong muốn: {str(e)}{Colors.END}")
        wait_enter()
