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
from bs4 import BeautifulSoup
from datetime import datetime

# Colors and Icons (giữ giống launcher cho nhất quán)
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

ICONS = {
    'success': '✅',
    'error': '❌',
    'warning': '⚠️',
    'info': 'ℹ️',
    'lock': '🔐',
    'user': '👤',
    'key': '🔑',
    'star': '⭐',
    'rocket': '🚀',
    'diamond': '💎',
    'crown': '👑',
    'check': '✔️',
    'exit': '🚪',
    'refresh': '🔄',
    'download': '📥',
    'upload': '📤',
    'link': '🔗',
    'list': '📋',
    'magic': '✨',
    'brain': '🧠',
    'heart': '❤️',
    'video': '🎥',
    'book': '📖',
    'fire': '🔥',
    'clock': '⏰'
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

def print_banner(title=""):
    clear_screen()
    animate_text(f"{Colors.BLUE}{Colors.BOLD}╔══════════════════════════════════════════════════════════════╗{Colors.END}", delay=0.01)
    animate_text(f"{Colors.BLUE}{Colors.BOLD}║{Colors.MAGENTA}               OLM MASTER PRO V1.0                            {Colors.BLUE}║{Colors.END}", delay=0.01)
    animate_text(f"{Colors.BLUE}{Colors.BOLD}║{Colors.CYAN}                  Created by: Tuấn Anh                        {Colors.BLUE}║{Colors.END}", delay=0.01)
    animate_text(f"{Colors.BLUE}{Colors.BOLD}╚══════════════════════════════════════════════════════════════╝{Colors.END}", delay=0.01)
    if title:
        print(f"{Colors.CYAN}{Colors.BOLD}{title.center(60)}{Colors.END}")
    print()

def print_status(message, icon='info', color=Colors.WHITE):
    print(f"{ICONS.get(icon, '•')} {color}{message}{Colors.END}")

def print_menu(options):
    print(f"{Colors.CYAN}{'─' * 40}{Colors.END}")
    for key, value in options.items():
        print(f" {Colors.YELLOW}{key}.{Colors.END} {value}")
    print(f"{Colors.CYAN}{'─' * 40}{Colors.END}")

def input_prompt(prompt, color=Colors.YELLOW):
    return input(f"{color}{prompt}{Colors.END}").strip()

def wait_enter():
    input_prompt(f"{ICONS['info']} Nhấn Enter để tiếp tục...")

# ========== LOAD SESSION & LICENSE ==========
def load_session():
    session_file = os.environ.get('OLM_SESSION_FILE')
    if session_file and os.path.exists(session_file):
        with open(session_file, 'rb') as f:
            data = pickle.load(f)
        session = requests.Session()
        session.cookies.update(data['cookies'])
        session.headers.update({
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'x-requested-with': 'XMLHttpRequest',
        })
        return session, data['user_id'], data['user_name']
    print_status("Không tìm thấy session!", 'error', Colors.RED)
    sys.exit(1)

def load_license():
    license_file = os.environ.get('OLM_LICENSE_FILE')
    if license_file and os.path.exists(license_file):
        with open(license_file, 'r') as f:
            encrypted = f.read()
        data = decrypt_data(encrypted)  # Sử dụng hàm decrypt từ launcher (giả sử import hoặc copy)
        if data and verify_integrity(data):
            return data
    return None

def save_license_updated(data):
    encrypted = encrypt_data(data)  # Tương tự
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
    if is_theory or success:
        remain = license_data['remain']
        if remain > 0:
            license_data['remain'] -= 1
            license_data['sig'] = compute_sig(license_data)
            save_license_updated(license_data)
            print_status(f"{ICONS['diamond']} Còn: {license_data['remain']} lượt", 'diamond', Colors.CYAN)
            return True
    return False

# ========== QUÉT BÀI TẬP (ĐÃ SỬA, BỎ DÒ KIỂM TRA) ==========
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
            is_video = "Video" in loai_raw
            is_ly_thuyet = "Lý thuyết" in loai_raw
            is_kiem_tra = "Kiểm tra" in loai_raw
            is_tu_luan = "Tự luận" in loai_raw
            if is_tu_luan:
                continue
            status_spans = row.find_all('span', class_='message-static-item') or row.find_all('span', class_='alert-warning')
            should_process = not status_spans or any("chưa" in span.text.lower() for span in status_spans)
            if should_process and href not in seen_links:
                seen_links.add(href)
                full_url = 'https://olm.vn' + href if not href.startswith('http') else href
                assignments.append({
                    'title': re.sub(r'\([^)]*\)', '', link_text).strip()[:60],
                    'subject': tds[0].get_text(strip=True) if len(tds) > 0 else "Khác",
                    'type': loai_raw.replace('[', '').replace(']', '').strip(),
                    'status': "Chưa làm" if not status_spans else status_spans[0].text.strip(),
                    'url': full_url,
                    'is_video': is_video,
                    'is_ly_thuyet': is_ly_thuyet,
                    'is_bai_tap': not (is_video or is_ly_thuyet or is_kiem_tra),
                    'is_kiem_tra': is_kiem_tra,
                    'is_tu_luan': is_tu_luan
                })
    return assignments

def display_assignments(assignments):
    print(f"{Colors.PURPLE}{ICONS['book']} DANH SÁCH BÀI TẬP{Colors.END}")
    for idx, item in enumerate(assignments, 1):
        print(f"{Colors.YELLOW}{idx}.{Colors.END} {item['title']} ({item['type']}) - {item['status']}")

# ========== XỬ LÝ BÀI ==========
def get_target_score(is_video=False, is_kiem_tra=False):
    if is_video:
        return 100
    options = {
        '1': "100 điểm",
        '2': "Tùy chọn (1-100)"
    }
    print_menu(options)
    choice = input_prompt("Chọn: ")
    if choice == '1':
        return 100
    elif choice == '2':
        score = int(input_prompt("Nhập điểm: "))
        return max(1, min(100, score))
    return 100

def extract_quiz_info(session, url, is_video=False):
    # Giữ nguyên logic từ code gốc
    # (Copy hàm extract_quiz_info từ code gốc)
    try:
        resp = session.get(url, timeout=10)
        html = resp.text
        quiz_list = None
        patterns = [
            r'quiz_list\s*[:=]\s*["\'](\d{6,}(?:,\d{6,})*)["\']',
            r'\b\d{9,}(?:,\d{9,})+\b',
            r'"quiz_list"\s*:\s*"(\d+(?:,\d+)*)"'
        ]
        for pattern in patterns:
            match = re.search(pattern, html)
            if match:
                quiz_list = match.group(1)
                break
        id_courseware = re.search(r'id_courseware\s*[:=]\s*["\']?(\d+)["\']?', html).group(1) if re.search(r'id_courseware\s*[:=]\s*["\']?(\d+)["\']?', html) else None
        id_cate = re.search(r'-(\d+)(?:\?|$)', url).group(1) if re.search(r'-(\d+)(?:\?|$)', url) else None
        if not quiz_list and not is_video:
            return None, 0, id_courseware, id_cate
        question_ids = [q.strip() for q in quiz_list.split(',')] if quiz_list else []
        total_questions = len(question_ids)
        return quiz_list, total_questions, id_courseware, id_cate
    except:
        return None, 0, None, None

def create_data_log_for_normal(total_questions, target_score):
    # Giữ nguyên từ code gốc
    correct_needed = round((target_score / 100) * total_questions)
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
    print_banner("MENU CHÍNH")
    session, user_id, user_name = load_session()
    license_data = load_license()
    if not license_data:
        print_status("License hết hạn hoặc không hợp lệ!", 'error', Colors.RED)
        options = {
            '1': "Quay lại launcher lấy key mới",
            '2': "Thoát"
        }
        print_menu(options)
        choice = input_prompt("Chọn: ")
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
        print_menu(options)
        choice = input_prompt("Chọn: ")
        if choice == '1':
            pages = int(input_prompt("Số trang quét (mặc định 3): ") or 3)
            assignments = get_assignments_fixed(session, pages)
            display_assignments(assignments)
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
            print_menu(options)
            choice = input_prompt("Chọn: ")
            if choice == '1':
                sys.exit(0)
            else:
                sys.exit(1)

if __name__ == "__main__":
    main()
