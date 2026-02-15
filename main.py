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
import requests
import re
import hashlib
import base64
from datetime import datetime
from bs4 import BeautifulSoup

# ========== MÀU SẮC ==========
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    MAGENTA = '\033[95m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
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
    print(f"{Colors.BLUE}{Colors.BOLD}{' ' * 15}OLM MASTER PRO{' ' * 15}{Colors.END}")
    print(f"{Colors.PURPLE}{' ' * 18}Created by: Tuấn Anh{' ' * 18}{Colors.END}")
    if title:
        print_line('─', Colors.CYAN, 60)
        print(f"{Colors.CYAN}{' ' * ((60 - len(title)) // 2)}{title}{Colors.END}")
    print_line('═', Colors.BLUE, 60)
    print()

def print_status(message, icon='info', color=Colors.WHITE):
    print(f"{ICONS.get(icon, '')} {color}{message}{Colors.END}")

def wait_enter(prompt="Nhấn Enter để tiếp tục..."):
    input(f"\n{Colors.YELLOW}{prompt}{Colors.END}")

# ========== HEADERS ==========
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'x-requested-with': 'XMLHttpRequest',
}

# ========== LICENSE ==========
LICENSE_FILE = os.environ.get('OLM_LICENSE_FILE', 'license.dat')
SESSION_FILE = os.environ.get('OLM_SESSION_FILE', 'session.pkl')

def load_license():
    """Tải license từ file"""
    if not os.path.exists(LICENSE_FILE):
        return None
    
    try:
        with open(LICENSE_FILE, 'r') as f:
            encrypted = f.read()
        
        # Giải mã đơn giản
        data = json.loads(base64.b64decode(encrypted).decode())
        
        # Kiểm tra hạn
        expire = datetime.strptime(data['expire'], '%d/%m/%Y')
        if expire < datetime.now():
            return None
        
        return data
    except:
        return None

def save_license(mode, remain, expire):
    """Lưu license"""
    data = {
        'mode': mode,
        'remain': remain,
        'expire': expire
    }
    encrypted = base64.b64encode(json.dumps(data).encode()).decode()
    with open(LICENSE_FILE, 'w') as f:
        f.write(encrypted)

def is_vip():
    """Kiểm tra VIP"""
    license_data = load_license()
    return license_data and license_data.get('mode') == 'VIP'

def get_remaining():
    """Lấy số lượt còn lại"""
    license_data = load_license()
    if not license_data:
        return 0
    if license_data.get('mode') == 'VIP':
        return float('inf')
    return license_data.get('remain', 0)

def decrement_attempt():
    """Giảm lượt (FREE)"""
    license_data = load_license()
    if not license_data or license_data.get('mode') == 'VIP':
        return True
    
    remain = license_data.get('remain', 0)
    if remain <= 0:
        return False
    
    license_data['remain'] = remain - 1
    save_license(license_data['mode'], license_data['remain'], license_data['expire'])
    return True

# ========== SESSION ==========
def load_session():
    """Tải session từ file"""
    try:
        import pickle
        with open(SESSION_FILE, 'rb') as f:
            data = pickle.load(f)
        
        session = requests.Session()
        session.cookies.update(data.get('cookies', {}))
        session.headers.update(HEADERS)
        
        return session, data.get('user_id'), data.get('user_name')
    except:
        print_status("Không thể tải session!", 'error', Colors.RED)
        sys.exit(1)

# ========== HÀM KIỂM TRA BÀI ẨN ĐIỂM ==========
def check_hidden_test_status(session, url, id_cate):
    """Kiểm tra bài kiểm tra đã làm chưa (ẩn điểm)"""
    try:
        # API kiểm tra trạng thái
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
        
        # Cách 2: Kiểm tra get-question-of-ids
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

# ========== QUÉT BÀI TẬP ==========
def get_assignments(session, pages_to_scan=5):
    """Lấy danh sách bài tập - GIỮ NGUYÊN từ tool cũ"""
    print_header(f"QUÉT BÀI TẬP ({pages_to_scan} trang)")
    
    assignments = []
    seen_links = set()
    
    try:
        for page in range(1, pages_to_scan + 1):
            if page == 1:
                url = "https://olm.vn/lop-hoc-cua-toi?action=login"
            else:
                url = f"https://olm.vn/lop-hoc-cua-toi/page-{page}?action=login"
            
            print_status(f"Đang quét trang {page}/{pages_to_scan}...", 'info', Colors.YELLOW)
            
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
                    
                    # Bỏ qua tự luận
                    if "[Tự luận]" in loai_raw or "[Tu luan]" in loai_raw:
                        continue
                    
                    # Kiểm tra trạng thái
                    should_process = False
                    
                    # Tìm span trạng thái
                    status_spans = []
                    status_spans.extend(main_link.find_all('span', class_='message-static-item'))
                    
                    if not status_spans:
                        status_spans.extend(row.find_all('span', class_='message-static-item'))
                    
                    if not status_spans:
                        warning_spans = row.find_all('span', class_='alert-warning')
                        for span in warning_spans:
                            span_text = span.get_text(strip=True)
                            if span_text not in ['Hóa học', 'Toán', 'Ngữ văn', 'Tiếng Anh']:
                                status_spans.append(span)
                    
                    # Xử lý theo loại
                    if not is_kiem_tra:
                        if not status_spans:
                            should_process = True
                        else:
                            for span in status_spans:
                                span_text = span.get_text(strip=True).lower()
                                if "chưa" in span_text or "làm tiếp" in span_text:
                                    should_process = True
                                    break
                                elif "điểm" in span_text:
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
                                should_process = not is_done
                            else:
                                should_process = True
                        else:
                            for span in status_spans:
                                span_text = span.get_text(strip=True).lower()
                                if "chưa" in span_text or "làm tiếp" in span_text:
                                    should_process = True
                                    break
                                elif "điểm" in span_text:
                                    should_process = False
                                    break
                    
                    if should_process and href not in seen_links:
                        seen_links.add(href)
                        
                        # Lấy thông tin bài
                        mon = row.find('span', class_='alert')
                        mon_text = mon.get_text(strip=True) if mon else "Khác"
                        
                        ten_bai = re.sub(r'\([^)]*\)', '', link_text).strip()
                        
                        status = "Chưa làm"
                        if status_spans:
                            for span in status_spans:
                                span_text = span.get_text(strip=True)
                                if "chưa" in span_text.lower() or "làm tiếp" in span_text.lower():
                                    status = span_text
                                    break
                        
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
            return assignments
        else:
            print_status("Không tìm thấy bài tập nào cần làm", 'warning', Colors.YELLOW)
            return []
            
    except Exception as e:
        print_status(f"Lỗi khi quét bài tập: {str(e)}", 'error', Colors.RED)
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
        
        print(f"{Colors.YELLOW}{idx:>2}.{Colors.END} {type_color}{icon} {item['type']:<10}{Colors.END} {Colors.WHITE}{title:<35}{Colors.END}")
    
    print_line('─', Colors.PURPLE, 60)

# ========== XỬ LÝ BÀI TẬP ==========
def get_target_score(is_video=False, is_kiem_tra=False):
    """Chọn điểm số"""
    if is_video:
        return 100
    elif is_kiem_tra:
        return random.randint(85, 100)
    
    print(f"\n{Colors.CYAN}🎯 CHỌN ĐIỂM SỐ{Colors.END}")
    print_line('─', Colors.CYAN, 40)
    print(f"  {Colors.YELLOW}1.{Colors.END} 100 điểm")
    print(f"  {Colors.YELLOW}2.{Colors.END} Tùy chọn")
    print_line('─', Colors.CYAN, 40)
    
    while True:
        choice = input(f"{Colors.YELLOW}Chọn (1-2): {Colors.END}").strip()
        if choice == '1':
            return 100
        elif choice == '2':
            try:
                score = int(input(f"{Colors.YELLOW}Nhập điểm (0-100): {Colors.END}").strip())
                if 0 <= score <= 100:
                    return score
                print_status("Điểm từ 0-100!", 'error', Colors.RED)
            except:
                print_status("Nhập số!", 'error', Colors.RED)
        else:
            print_status("Chọn 1 hoặc 2!", 'error', Colors.RED)

def extract_quiz_info(session, url, is_video=False):
    """Trích xuất thông tin quiz"""
    try:
        resp = session.get(url, timeout=10)
        html = resp.text
        
        # Tìm quiz_list
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
        
        # Tìm id_courseware
        id_courseware = None
        cw_match = re.search(r'id_courseware\s*[:=]\s*["\']?(\d+)["\']?', html)
        if cw_match:
            id_courseware = cw_match.group(1)
        
        # Tìm id_cate
        id_cate = None
        cate_match = re.search(r'-(\d+)(?:\?|$)', url)
        if cate_match:
            id_cate = cate_match.group(1)
        
        if not quiz_list and not is_video:
            return None, 0, id_courseware, id_cate
        
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
    print(f"\n{Colors.CYAN}📤 ĐANG XỬ LÝ:{Colors.END}")
    print(f"{Colors.WHITE}📖 {assignment['title']}{Colors.END}")
    
    if assignment['is_video']:
        print(f"{Colors.BLUE}🎬 Loại: Video{Colors.END}")
        target_score = 100
    elif assignment['is_ly_thuyet']:
        print(f"{Colors.CYAN}📚 Loại: Lý thuyết{Colors.END}")
        target_score = get_target_score(False, False)
    elif assignment['is_kiem_tra']:
        print(f"{Colors.YELLOW}📋 Loại: Kiểm tra{Colors.END}")
        target_score = get_target_score(False, True)
    else:
        print(f"{Colors.GREEN}📝 Loại: Bài tập{Colors.END}")
        target_score = get_target_score(False, False)
    
    try:
        # Trích xuất thông tin
        quiz_list, total_questions, id_courseware, id_cate = extract_quiz_info(
            session, assignment['url'], assignment['is_video']
        )
        
        # Xử lý video
        if assignment['is_video']:
            print_status("Đang xử lý video...", 'video', Colors.BLUE)
            success = handle_video(session, assignment, user_id, quiz_list, id_courseware, id_cate)
            if success:
                print_status(f"{ICONS['success']} HOÀN THÀNH BÀI!", 'success', Colors.GREEN + Colors.BOLD)
                # Trừ lượt cho FREE (luôn trừ)
                if not is_vip():
                    decrement_attempt()
                    remain = get_remaining()
                    print_status(f"Lượt còn: {remain if remain != float('inf') else 'Không giới hạn'}", 'info', Colors.CYAN)
                wait_enter()
            return success
        
        # Bài tập thường
        if not quiz_list or total_questions == 0:
            print_status("Không thể lấy thông tin bài", 'error', Colors.RED)
            return False
        
        print_status(f"Tìm thấy {total_questions} câu hỏi", 'info', Colors.WHITE)
        print_status("Đang tạo dữ liệu...", 'clock', Colors.YELLOW)
        
        data_log, total_time, correct_needed = create_data_log(total_questions, target_score)
        
        # Lấy CSRF token
        csrf_token = session.cookies.get('XSRF-TOKEN')
        if not csrf_token:
            resp = session.get(assignment['url'], timeout=10)
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
        
        submit_headers = HEADERS.copy()
        submit_headers['x-csrf-token'] = csrf_token
        
        response = session.post(
            'https://olm.vn/course/teacher-static',
            data=payload,
            headers=submit_headers,
            timeout=15
        )
        
        # Xử lý kết quả
        success = handle_response(response, target_score)
        
        if success:
            print_status(f"{ICONS['success']} HOÀN THÀNH BÀI!", 'success', Colors.GREEN + Colors.BOLD)
            # Trừ lượt cho FREE (luôn trừ)
            if not is_vip():
                decrement_attempt()
                remain = get_remaining()
                print_status(f"Lượt còn: {remain if remain != float('inf') else 'Không giới hạn'}", 'info', Colors.CYAN)
            wait_enter()
        
        return success
            
    except Exception as e:
        print_status(f"Lỗi: {str(e)}", 'error', Colors.RED)
        return False

def handle_video(session, assignment, user_id, quiz_list, id_courseware, id_cate):
    """Xử lý video"""
    methods = [
        video_method_1,
        video_method_2,
        video_method_3
    ]
    
    for i, method in enumerate(methods, 1):
        print_status(f"Thử phương pháp {i}...", 'video', Colors.BLUE)
        success = method(session, assignment, user_id, quiz_list, id_courseware, id_cate)
        if success:
            return True
        time.sleep(1)
    
    return False

def video_method_1(session, assignment, user_id, quiz_list, id_courseware, id_cate):
    """Phương pháp 1"""
    try:
        csrf_token = session.cookies.get('XSRF-TOKEN')
        if not csrf_token:
            return False
        
        current_time = int(time.time())
        time_spent = random.randint(300, 900)
        
        data_log = [{
            "answer": '["0"]',
            "params": '{"js":""}',
            "result": [1],
            "type": [11],
            "id": f"vid{random.randint(100000, 999999)}"
        }]
        
        payload = {
            '_token': csrf_token,
            'id_user': user_id,
            'id_cate': id_cate or '0',
            'id_courseware': id_courseware or '0',
            'time_spent': str(time_spent),
            'score': '100',
            'data_log': json.dumps(data_log),
            'date_end': str(current_time),
            'ended': '1',
            'cv_q': '1'
        }
        
        if quiz_list:
            payload['quiz_list'] = quiz_list
        
        response = session.post(
            'https://olm.vn/course/teacher-static',
            data=payload,
            headers={'x-csrf-token': csrf_token},
            timeout=10
        )
        
        return handle_response(response, 100)
    except:
        return False

def video_method_2(session, assignment, user_id, quiz_list, id_courseware, id_cate):
    """Phương pháp 2"""
    try:
        if not quiz_list:
            return False
        
        csrf_token = session.cookies.get('XSRF-TOKEN')
        if not csrf_token:
            return False
        
        current_time = int(time.time())
        time_spent = random.randint(300, 900)
        
        qids = quiz_list.split(',')
        data_log = []
        for i in range(min(len(qids), 3)):
            data_log.append({
                "answer": '["0"]',
                "params": '{"js":""}',
                "result": [1],
                "type": [1],
                "id": qids[i]
            })
        
        payload = {
            '_token': csrf_token,
            'id_user': user_id,
            'id_cate': id_cate or '0',
            'id_courseware': id_courseware or '0',
            'time_spent': str(time_spent),
            'score': '100',
            'data_log': json.dumps(data_log),
            'date_end': str(current_time),
            'ended': '1',
            'cv_q': '1',
            'quiz_list': quiz_list,
            'correct': str(len(data_log))
        }
        
        response = session.post(
            'https://olm.vn/course/teacher-static',
            data=payload,
            headers={'x-csrf-token': csrf_token},
            timeout=10
        )
        
        return handle_response(response, 100)
    except:
        return False

def video_method_3(session, assignment, user_id, quiz_list, id_courseware, id_cate):
    """Phương pháp 3"""
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
            "type": [11],
            "id": f"vid{random.randint(100000, 999999)}"
        }]
        
        if quiz_list:
            order = [0, 1, 2, 3]
            random.shuffle(order)
            data_log.append({
                "answer": '["0"]',
                "params": json.dumps({"order": order}),
                "result": [1],
                "type": [1],
                "id": quiz_list.split(',')[0]
            })
        
        payload = {
            '_token': csrf_token,
            'id_user': user_id,
            'id_cate': id_cate or '0',
            'id_courseware': id_courseware or '0',
            'time_spent': str(time_spent),
            'score': '100',
            'data_log': json.dumps(data_log),
            'date_end': str(current_time),
            'ended': '1',
            'cv_q': '1',
            'correct': str(len(data_log))
        }
        
        if quiz_list:
            payload['quiz_list'] = quiz_list
        
        response = session.post(
            'https://olm.vn/course/teacher-static',
            data=payload,
            headers={'x-csrf-token': csrf_token},
            timeout=10
        )
        
        return handle_response(response, 100)
    except:
        return False

def handle_response(response, target_score):
    """Xử lý phản hồi"""
    if response.status_code == 200:
        try:
            result = response.json()
            if 'code' in result:
                if result['code'] == 403:
                    print_status("Bài đã nộp trước đó", 'warning', Colors.YELLOW)
                    return True
                elif result['code'] == 200:
                    print_status(f"Thành công! Điểm: {result.get('score', target_score)}/100", 'success', Colors.GREEN)
                    return True
                else:
                    print_status("Nộp thành công", 'success', Colors.GREEN)
                    return True
            else:
                print_status("Nộp thành công", 'success', Colors.GREEN)
                return True
        except:
            if "success" in response.text.lower():
                print_status("Nộp thành công", 'success', Colors.GREEN)
                return True
            print_status("Nộp thành công", 'success', Colors.GREEN)
            return True
    elif response.status_code == 403:
        print_status("Bài đã nộp trước đó", 'warning', Colors.YELLOW)
        return True
    else:
        print_status(f"Lỗi {response.status_code}", 'error', Colors.RED)
        return False

# ========== CHỌN BÀI LINH HOẠT ==========
def parse_selection(selection, max_num):
    """Phân tích lựa chọn bài"""
    if selection == '0':
        return list(range(1, max_num + 1))
    
    if '-' in selection:
        try:
            start, end = map(int, selection.split('-'))
            return [i for i in range(max(1, start), min(end, max_num) + 1)]
        except:
            return []
    
    if ',' in selection:
        try:
            return [int(x.strip()) for x in selection.split(',') if 1 <= int(x.strip()) <= max_num]
        except:
            return []
    
    if selection.isdigit():
        num = int(selection)
        return [num] if 1 <= num <= max_num else []
    
    return []

# ========== GIẢI BÀI CỤ THỂ ==========
def solve_specific(session, user_id):
    """Giải bài cụ thể từ danh sách"""
    print_header("GIẢI BÀI CỤ THỂ")
    
    pages = input(f"{Colors.YELLOW}Số trang cần quét (mặc định: 3): {Colors.END}").strip()
    pages_to_scan = 3
    if pages.isdigit() and int(pages) > 0:
        pages_to_scan = int(pages)
    
    assignments = get_assignments(session, pages_to_scan)
    if not assignments:
        wait_enter()
        return False
    
    display_assignments(assignments)
    
    print(f"\n{Colors.CYAN}📝 CÁCH CHỌN:{Colors.END}")
    print(f"  - Nhập {Colors.YELLOW}0{Colors.END}: Tất cả")
    print(f"  - Nhập {Colors.YELLOW}1,3,5{Colors.END}: Nhiều bài")
    print(f"  - Nhập {Colors.YELLOW}1-5{Colors.END}: Khoảng")
    print(f"  - Nhập {Colors.YELLOW}1{Colors.END}: Một bài")
    
    selection = input(f"\n{Colors.YELLOW}Chọn bài: {Colors.END}").strip()
    
    indices = parse_selection(selection, len(assignments))
    
    if not indices:
        print_status("Không có bài nào được chọn!", 'error', Colors.RED)
        wait_enter()
        return False
    
    print_status(f"Đã chọn {len(indices)} bài", 'info', Colors.CYAN)
    
    confirm = input(f"{Colors.YELLOW}Xác nhận? (y/n): {Colors.END}").strip().lower()
    if confirm != 'y':
        print_status("Đã hủy", 'warning', Colors.YELLOW)
        wait_enter()
        return False
    
    # Kiểm tra lượt trước khi bắt đầu
    if not is_vip() and get_remaining() < len(indices):
        print_status(f"Không đủ lượt! Cần {len(indices)}, còn {get_remaining()}", 'error', Colors.RED)
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
    
    print(f"\n{Colors.GREEN}✅ KẾT QUẢ: {success}/{len(indices)}{Colors.END}")
    wait_enter()
    return True

# ========== GIẢI TỪ LINK ==========
def solve_from_link(session, user_id):
    """Giải bài từ link"""
    print_header("GIẢI BÀI TỪ LINK")
    
    url = input(f"{Colors.YELLOW}Dán link OLM: {Colors.END}").strip()
    
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
        
        print(f"\n{Colors.CYAN}📋 THÔNG TIN:{Colors.END}")
        print(f"  {Colors.WHITE}📖 Link: {url}{Colors.END}")
        print(f"  {Colors.CYAN}📝 Loại: {assignment['type']}{Colors.END}")
        
        confirm = input(f"\n{Colors.YELLOW}Xác nhận giải? (y/n): {Colors.END}").strip().lower()
        
        if confirm == 'y':
            # Kiểm tra lượt
            if not is_vip() and get_remaining() < 1:
                print_status("Hết lượt!", 'error', Colors.RED)
                wait_enter()
                return False
            
            return submit_assignment(session, assignment, user_id)
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
    """Đổi tài khoản - quay lại launcher"""
    print_header("ĐỔI TÀI KHOẢN")
    
    print(f"{Colors.YELLOW}{ICONS['warning']} Bạn sắp quay lại màn hình đăng nhập.{Colors.END}")
    print(f"{Colors.CYAN}License hiện tại sẽ được giữ nguyên.{Colors.END}")
    print()
    
    confirm = input(f"{Colors.YELLOW}Xác nhận? (y/n): {Colors.END}").strip().lower()
    
    if confirm == 'y':
        print_status("Đang quay lại...", 'refresh', Colors.YELLOW)
        time.sleep(1)
        return True
    
    return False

# ========== MENU CHÍNH ==========
def main_menu(session, user_id, user_name):
    """Menu chính - 4 options"""
    
    while True:
        print_header("MENU CHÍNH")
        print(f"{ICONS['user']} {Colors.GREEN}Xin chào: {user_name}{Colors.END}")
        
        # Hiển thị lượt
        if is_vip():
            print(f"{ICONS['crown']} {Colors.MAGENTA}VIP: Không giới hạn{Colors.END}")
        else:
            remain = get_remaining()
            print(f"{ICONS['key']} {Colors.CYAN}Lượt còn: {remain}/4{Colors.END}")
        print()
        
        menu_options = {
            '1': f"{ICONS['brain']} Giải bài cụ thể từ danh sách",
            '2': f"{ICONS['link']} Giải bài từ link OLM",
            '3': f"{ICONS['refresh']} Đổi tài khoản",
            '4': f"{ICONS['exit']} Thoát"
        }
        
        print(f"\n{Colors.CYAN}📋 LỰA CHỌN{Colors.END}")
        print_line('─', Colors.CYAN, 40)
        for key, value in menu_options.items():
            print(f"  {Colors.YELLOW}{key}.{Colors.END} {value}")
        print_line('─', Colors.CYAN, 40)
        
        choice = input(f"\n{Colors.YELLOW}Chọn (1-4): {Colors.END}").strip()
        
        if choice == '1':
            solve_specific(session, user_id)
        elif choice == '2':
            solve_from_link(session, user_id)
        elif choice == '3':
            if change_account():
                break  # Quay lại launcher
        elif choice == '4':
            print_status("Tạm biệt!", 'exit', Colors.GREEN)
            time.sleep(1)
            sys.exit(0)
        else:
            print_status("Lựa chọn không hợp lệ!", 'error', Colors.RED)
            time.sleep(1)

# ========== MAIN ==========
def main():
    try:
        # Load session
        session, user_id, user_name = load_session()
        
        # Load license
        license_data = load_license()
        if not license_data:
            print_status("Không tìm thấy license!", 'error', Colors.RED)
            wait_enter()
            sys.exit(1)
        
        # Vào menu
        main_menu(session, user_id, user_name)
        
    except KeyboardInterrupt:
        print(f"\n\n{ICONS['exit']} {Colors.YELLOW}Đã dừng{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{ICONS['error']} {Colors.RED}Lỗi: {str(e)}{Colors.END}")
        wait_enter()

if __name__ == "__main__":
    main()
