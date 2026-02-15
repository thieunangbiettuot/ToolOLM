#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║                OLM MASTER PRO V4.0 - MAIN                    ║
║                  Ultimate Edition                            ║
╚══════════════════════════════════════════════════════════════╝
"""

import os
import sys
import time
import json
import requests
import hashlib
import base64
import re
import random
import socket
import uuid
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from pathlib import Path

# URLs
URL_VIP = "https://raw.githubusercontent.com/thieunangbiettuot/ToolOLM/refs/heads/main/vip_users.txt"

# Headers
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'vi-VN,vi;q=0.9',
    'x-requested-with': 'XMLHttpRequest',
    'origin': 'https://olm.vn',
    'referer': 'https://olm.vn/'
}

# ==================== COLORS ====================
class Color:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    HIDDEN = '\033[8m'
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    RESET = '\033[0m'
    END = '\033[0m'

# ==================== FILE PATHS ====================
def get_data_dir():
    p = sys.platform
    if p == 'win32':
        d = Path(os.getenv('LOCALAPPDATA', os.path.expanduser('~'))) / 'Microsoft' / 'Windows' / 'INetCache' / 'IE'
    elif p == 'darwin':
        d = Path.home() / 'Library' / 'Application Support' / 'com.apple.Safari'
    elif 'ANDROID_ROOT' in os.environ or 'TERMUX_VERSION' in os.environ:
        d = Path(os.getenv('HOME', '/data/data/com.termux/files/home')) / '.cache' / 'google-chrome'
    else:
        d = Path.home() / '.cache' / 'mozilla' / 'firefox'
    d.mkdir(parents=True, exist_ok=True)
    return str(d)

DATA = get_data_dir()
_h = hashlib.md5(f"{socket.gethostname()}{uuid.getnode()}".encode()).hexdigest()[:8]

# Get from environment or default
LIC = os.getenv('OLM_LICENSE_FILE', os.path.join(DATA, f'.{_h}sc'))
SESS = os.getenv('OLM_SESSION_FILE', os.path.join(DATA, f'.{_h}ss'))
LOCK = os.getenv('OLM_LOCK_FILE', os.path.join(DATA, f'.{_h}lk'))

KEY = b'OLM_ULTRA_SECRET_2026'

# ==================== ENCRYPTION ====================
def enc(obj):
    txt = json.dumps(obj, separators=(',', ':')).encode()
    xor = bytearray(txt[i] ^ KEY[i % len(KEY)] for i in range(len(txt)))
    b85 = base64.b85encode(bytes(xor)).decode()
    chk = hashlib.sha256(b85.encode()).hexdigest()[:12]
    noise = hashlib.md5(chk.encode()).hexdigest()[:8]
    return f"{noise}{chk}{b85}{noise[::-1]}"

def dec(s):
    try:
        s = s[8:-8]
        chk, b85 = s[:12], s[12:]
        if hashlib.sha256(b85.encode()).hexdigest()[:12] != chk:
            return None
        xor = base64.b85decode(b85)
        txt = bytes(xor[i] ^ KEY[i % len(KEY)] for i in range(len(xor)))
        return json.loads(txt)
    except:
        return None

# ==================== UI UTILITIES ====================
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_terminal_width():
    try:
        return os.get_terminal_size().columns
    except:
        return 80

def center_text(text, width=None):
    if width is None:
        width = get_terminal_width()
    clean_text = re.sub(r'\033\[[0-9;]+m', '', text)
    padding = (width - len(clean_text)) // 2
    return ' ' * padding + text

def print_center(text, color=''):
    print(center_text(f"{color}{text}{Color.RESET}"))

def print_gradient_line(char='═', width=None):
    if width is None:
        width = get_terminal_width()
    colors = [Color.CYAN, Color.BRIGHT_CYAN, Color.BLUE, Color.BRIGHT_BLUE]
    segment_width = width // len(colors)
    line = ''
    for i, color in enumerate(colors):
        segment = char * segment_width
        line += f"{color}{segment}"
    line += Color.RESET
    print(line)

def loading_animation(text, duration=1.0):
    frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        print(f"\r{Color.YELLOW}{frames[i % len(frames)]} {text}...{Color.RESET}", end='', flush=True)
        time.sleep(0.1)
        i += 1
    print(f"\r{' ' * (len(text) + 10)}\r", end='', flush=True)

def progress_bar(current, total, width=40, prefix=''):
    percent = int((current / total) * 100)
    filled = int((current / total) * width)
    bar = '█' * filled + '░' * (width - filled)
    
    if percent < 33:
        color = Color.RED
    elif percent < 66:
        color = Color.YELLOW
    else:
        color = Color.GREEN
    
    print(f"\r{prefix} {color}{bar}{Color.RESET} {Color.BOLD}{percent}%{Color.RESET} ({current}/{total})", end='', flush=True)

def box_print(text, color=Color.CYAN, width=None):
    if width is None:
        width = min(get_terminal_width() - 4, 70)
    
    lines = text.split('\n')
    max_len = max(len(line) for line in lines)
    box_width = min(max_len + 4, width)
    
    print(f"{color}╔{'═' * (box_width - 2)}╗{Color.RESET}")
    for line in lines:
        padding = box_width - len(line) - 4
        left_pad = padding // 2
        right_pad = padding - left_pad
        print(f"{color}║{Color.RESET} {' ' * left_pad}{Color.BOLD}{line}{Color.RESET}{' ' * right_pad} {color}║{Color.RESET}")
    print(f"{color}╚{'═' * (box_width - 2)}╝{Color.RESET}")

def banner():
    clear()
    width = get_terminal_width()
    print_gradient_line('═', width)
    print()
    print_center(f"{Color.BRIGHT_CYAN}{Color.BOLD}OLM MASTER PRO{Color.RESET}")
    print_center(f"{Color.BRIGHT_MAGENTA}V 4.0 ULTIMATE{Color.RESET}")
    print()
    print_center(f"{Color.DIM}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Color.RESET}")
    print_center(f"{Color.BRIGHT_YELLOW}Created by: Tuấn Anh{Color.RESET}")
    print_center(f"{Color.DIM}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Color.RESET}")
    print()
    print_gradient_line('═', width)
    print()

def success_box(message):
    print()
    box_print(f"✓ {message}", Color.GREEN)
    print()

def error_box(message):
    print()
    box_print(f"✗ {message}", Color.RED)
    print()

def info_box(message):
    print()
    box_print(f"ℹ {message}", Color.CYAN)
    print()

def warning_box(message):
    print()
    box_print(f"⚠ {message}", Color.YELLOW)
    print()
# ==================== LICENSE MANAGEMENT ====================
def sig(d):
    return hashlib.sha256(f"{d['mode']}{d['expire']}{d['ip']}".encode()).hexdigest()[:16]

def load_lic():
    if not os.path.exists(LIC):
        return None
    try:
        with open(LIC) as f:
            d = dec(f.read())
        if not d or d.get('sig') != sig(d):
            return None
        if datetime.strptime(d['expire'], "%d/%m/%Y").date() < datetime.now().date():
            return None
        if d.get('remain', 0) > 0 or d.get('mode') == 'VIP':
            return d
        return None
    except:
        return None

def update_lic_remain(new_remain):
    d = load_lic()
    if d and d.get('mode') == 'FREE':
        d['remain'] = new_remain
        d['sig'] = sig(d)
        with open(LIC, 'w') as f:
            f.write(enc(d))

def deduct_license():
    lic = load_lic()
    if not lic:
        return False
    
    if lic.get('mode') == 'VIP':
        return True
    
    remain = lic.get('remain', 0)
    if remain > 0:
        new_remain = remain - 1
        update_lic_remain(new_remain)
        
        if new_remain > 0:
            print(f"\n{Color.BRIGHT_GREEN}💎 Còn lại: {new_remain} lượt{Color.RESET}")
        else:
            print(f"\n{Color.BRIGHT_RED}⛔ HẾT LƯỢT{Color.RESET}")
        
        return True
    return False

def clear_lock():
    if os.path.exists(LOCK):
        os.remove(LOCK)

# ==================== SESSION MANAGEMENT ====================
def load_session():
    if not os.path.exists(SESS):
        return None, None, None
    try:
        import pickle
        with open(SESS, 'rb') as f:
            data = pickle.load(f)
        
        session = requests.Session()
        cookies_dict = data.get('cookies', {})
        for name, value in cookies_dict.items():
            session.cookies.set(name, value)
        session.headers.update(HEADERS)
        
        return session, data.get('user_id'), data.get('user_name')
    except:
        return None, None, None

def check_vip_realtime(user_id):
    try:
        loading_animation("Checking VIP status", 0.5)
        r = requests.get(URL_VIP, timeout=5)
        if r.status_code == 200:
            vip_users = []
            for line in r.text.strip().split('\n'):
                line = line.strip()
                if line and not line.startswith('#'):
                    vip_users.append(line.lower())
            return str(user_id).lower() in vip_users
    except:
        pass
    return False
# ==================== SCANNING ASSIGNMENTS ====================
def get_assignments(session, pages=3):
    print()
    print(f"{Color.CYAN}╔{'═' * 60}╗{Color.RESET}")
    print(f"{Color.CYAN}║{Color.BRIGHT_YELLOW}{Color.BOLD}{'QUÉT BÀI TẬP'.center(60)}{Color.RESET}{Color.CYAN}║{Color.RESET}")
    print(f"{Color.CYAN}╚{'═' * 60}╝{Color.RESET}")
    print()
    
    assignments = []
    seen_links = set()
    
    for page in range(1, pages + 1):
        url = f"https://olm.vn/lop-hoc-cua-toi/page-{page}?action=login" if page > 1 else "https://olm.vn/lop-hoc-cua-toi?action=login"
        
        loading_animation(f"Quét trang {page}/{pages}", 0.8)
        
        try:
            resp = session.get(url, headers=HEADERS, timeout=10)
            if resp.status_code != 200:
                continue
            
            soup = BeautifulSoup(resp.text, 'html.parser')
            rows = soup.find_all('tr', class_='my-gived-courseware-item')
            
            if not rows:
                continue
            
            page_count = 0
            for row in rows:
                link_tags = row.find_all('a', class_='olm-text-link')
                if not link_tags:
                    continue
                
                main_link = link_tags[0]
                href = main_link.get('href')
                link_text = main_link.get_text(strip=True)
                
                if href and ('(Toán' in link_text or '(Ngữ văn' in link_text or '(Tiếng Anh' in link_text):
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
                is_tu_luan = "[Tự luận]" in loai_raw or "[Tu luan]" in loai_raw
                is_bai_tap = not (is_video or is_ly_thuyet or is_kiem_tra)
                
                if is_tu_luan or is_kiem_tra:
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
                        if span_text not in ['Hóa học', 'Toán', 'Ngữ văn', 'Tiếng Anh', 'Tin học']:
                            status_spans.append(span)
                
                if not status_spans:
                    should_process = True
                else:
                    for span in status_spans:
                        span_text = span.get_text(strip=True).lower()
                        if "chưa" in span_text or "làm tiếp" in span_text:
                            should_process = True
                            break
                        elif "điểm" in span_text or "đã xem" in span_text:
                            should_process = False
                            break
                
                if should_process and href not in seen_links:
                    seen_links.add(href)
                    
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
                    
                    if not href.startswith('http'):
                        full_url = 'https://olm.vn' + href
                    else:
                        full_url = href
                    
                    assignments.append({
                        'title': ten_bai[:50],
                        'subject': mon_text[:15],
                        'type': loai_raw.replace('[', '').replace(']', '').strip()[:15],
                        'status': status,
                        'url': full_url,
                        'page': page,
                        'is_video': is_video,
                        'is_ly_thuyet': is_ly_thuyet,
                        'is_bai_tap': is_bai_tap
                    })
                    page_count += 1
            
            if page_count > 0:
                print(f"{Color.GREEN}✓ Trang {page}: {page_count} bài{Color.RESET}")
            
        except Exception as e:
            print(f"{Color.RED}✗ Trang {page}: Lỗi{Color.RESET}")
            continue
    
    if assignments:
        print()
        success_box(f"Tìm thấy {len(assignments)} bài cần làm")
        
        video_count = sum(1 for a in assignments if a['is_video'])
        ly_thuyet_count = sum(1 for a in assignments if a['is_ly_thuyet'])
        bai_tap_count = sum(1 for a in assignments if a['is_bai_tap'])
        
        print(f"{Color.CYAN}📊 Thống kê:{Color.RESET}")
        if video_count > 0:
            print(f"   🎬 Video: {video_count}")
        if ly_thuyet_count > 0:
            print(f"   📖 Lý thuyết: {ly_thuyet_count}")
        if bai_tap_count > 0:
            print(f"   📝 Bài tập: {bai_tap_count}")
        
        return assignments
    else:
        warning_box("Không tìm thấy bài nào")
        return []

def display_assignments(assignments):
    if not assignments:
        return
    
    print()
    print(f"{Color.MAGENTA}╔{'═' * 70}╗{Color.RESET}")
    print(f"{Color.MAGENTA}║{Color.BRIGHT_YELLOW}{Color.BOLD}{'DANH SÁCH BÀI TẬP'.center(70)}{Color.RESET}{Color.MAGENTA}║{Color.RESET}")
    print(f"{Color.MAGENTA}╠{'═' * 70}╣{Color.RESET}")
    
    for idx, item in enumerate(assignments, 1):
        title = item['title']
        if len(title) > 35:
            title = title[:32] + "..."
        
        if item['is_video']:
            icon = '🎬'
            type_color = Color.BLUE
        elif item['is_ly_thuyet']:
            icon = '📖'
            type_color = Color.CYAN
        else:
            icon = '📝'
            type_color = Color.GREEN
        
        num_color = Color.BRIGHT_YELLOW if idx % 2 == 0 else Color.YELLOW
        
        line = f"  {num_color}{idx:2}.{Color.RESET} {icon} {type_color}{item['type']:<12}{Color.RESET} {Color.WHITE}{title}{Color.RESET}"
        print(f"{Color.MAGENTA}║{Color.RESET} {line:<64} {Color.MAGENTA}║{Color.RESET}")
    
    print(f"{Color.MAGENTA}╚{'═' * 70}╝{Color.RESET}")
    print()
# ==================== SOLVING LOGIC ====================
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
    except:
        return None, 0, None, None

def create_data_log(total_questions, target_score):
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

def try_video_simple(session, assignment, user_id, quiz_list, total_questions, id_courseware, id_cate):
    try:
        csrf_token = session.cookies.get('XSRF-TOKEN')
        if not csrf_token:
            resp = session.get(assignment['url'], timeout=10)
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
        
        submit_headers = HEADERS.copy()
        submit_headers['x-csrf-token'] = csrf_token
        
        response = session.post('https://olm.vn/course/teacher-static', data=payload, headers=submit_headers, timeout=10)
        
        if response.status_code == 200:
            return True
        elif response.status_code == 403:
            return True
    except:
        pass
    return False

def handle_video(session, assignment, user_id, quiz_list, total_questions, id_courseware, id_cate):
    methods = [try_video_simple]
    for method in methods:
        if method(session, assignment, user_id, quiz_list, total_questions, id_courseware, id_cate):
            return True
        time.sleep(0.5)
    return False

def submit_assignment(session, assignment, user_id, target_score):
    print(f"\n{Color.CYAN}{'─' * 60}{Color.RESET}")
    print(f"{Color.BRIGHT_WHITE}📝 {assignment['title'][:45]}{Color.RESET}")
    
    if assignment['is_video']:
        print(f"{Color.BLUE}🎬 Video{Color.RESET}")
    elif assignment['is_ly_thuyet']:
        print(f"{Color.CYAN}📖 Lý thuyết{Color.RESET}")
    else:
        print(f"{Color.GREEN}📝 Bài tập{Color.RESET}")
    
    try:
        loading_animation("Đang xử lý", 1.0)
        
        quiz_list, total_questions, id_courseware, id_cate = extract_quiz_info(session, assignment['url'], assignment['is_video'])
        
        if assignment['is_video']:
            success = handle_video(session, assignment, user_id, quiz_list, total_questions, id_courseware, id_cate)
            return success
        
        if not quiz_list or total_questions == 0:
            print(f"{Color.RED}✗ Không lấy được thông tin bài{Color.RESET}")
            return False
        
        data_log, total_time, correct_needed = create_data_log(total_questions, target_score)
        
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
        
        submit_headers = HEADERS.copy()
        submit_headers['x-csrf-token'] = csrf_token
        
        response = session.post('https://olm.vn/course/teacher-static', data=payload, headers=submit_headers, timeout=15)
        
        if response.status_code == 200:
            print(f"{Color.GREEN}✓ Thành công!{Color.RESET}")
            return True
        elif response.status_code == 403:
            print(f"{Color.YELLOW}⚠ Đã nộp trước đó{Color.RESET}")
            return True
        else:
            print(f"{Color.RED}✗ Lỗi {response.status_code}{Color.RESET}")
            return False
    except Exception as e:
        print(f"{Color.RED}✗ Lỗi: {str(e)}{Color.RESET}")
        return False

# ==================== SOLVE SPECIFIC ====================
def solve_specific(session, user_id):
    banner()
    
    print(f"{Color.YELLOW}Số trang quét (mặc định 3): {Color.RESET}", end='')
    pages_input = input().strip()
    pages = 3
    if pages_input.isdigit() and int(pages_input) > 0:
        pages = min(int(pages_input), 10)
    
    assignments = get_assignments(session, pages)
    if not assignments:
        input(f"\n{Color.YELLOW}Enter để tiếp tục...{Color.RESET}")
        return
    
    display_assignments(assignments)
    
    print(f"{Color.CYAN}Chọn bài:{Color.RESET}")
    print(f"  • {Color.YELLOW}0{Color.RESET} = Tất cả")
    print(f"  • {Color.YELLOW}1,3,5{Color.RESET} = Nhiều bài")
    print(f"  • {Color.YELLOW}1{Color.RESET} = 1 bài")
    print()
    
    selection = input(f"{Color.BRIGHT_YELLOW}➤ Chọn: {Color.RESET}").strip()
    
    selected = []
    if selection == '0':
        selected = assignments
    elif ',' in selection:
        try:
            indices = [int(x.strip()) - 1 for x in selection.split(',')]
            selected = [assignments[i] for i in indices if 0 <= i < len(assignments)]
        except:
            error_box("Định dạng không hợp lệ")
            input(f"\n{Color.YELLOW}Enter...{Color.RESET}")
            return
    else:
        try:
            idx = int(selection) - 1
            if 0 <= idx < len(assignments):
                selected = [assignments[idx]]
        except:
            error_box("Số không hợp lệ")
            input(f"\n{Color.YELLOW}Enter...{Color.RESET}")
            return
    
    if not selected:
        error_box("Không có bài nào được chọn")
        input(f"\n{Color.YELLOW}Enter...{Color.RESET}")
        return
    
    print()
    print(f"{Color.CYAN}⭐ CHỌN ĐIỂM:{Color.RESET}")
    print(f"  {Color.YELLOW}1.{Color.RESET} 100 điểm")
    print(f"  {Color.YELLOW}2.{Color.RESET} Tùy chọn")
    print()
    
    target_score = 100
    score_choice = input(f"{Color.BRIGHT_YELLOW}➤ Chọn: {Color.RESET}").strip()
    
    if score_choice == '2':
        try:
            score = int(input(f"{Color.YELLOW}Nhập điểm (0-100): {Color.RESET}").strip())
            target_score = max(0, min(100, score))
        except:
            target_score = 100
    
    print()
    print(f"{Color.CYAN}╔{'═' * 40}╗{Color.RESET}")
    print(f"{Color.CYAN}║{Color.RESET} {Color.BRIGHT_WHITE}Số bài: {len(selected)}{Color.RESET}{' ' * (31 - len(str(len(selected))))} {Color.CYAN}║{Color.RESET}")
    print(f"{Color.CYAN}║{Color.RESET} {Color.BRIGHT_WHITE}Điểm: {target_score}{Color.RESET}{' ' * (32 - len(str(target_score)))} {Color.CYAN}║{Color.RESET}")
    print(f"{Color.CYAN}╚{'═' * 40}╝{Color.RESET}")
    print()
    
    confirm = input(f"{Color.YELLOW}Xác nhận? (y/n): {Color.RESET}").strip().lower()
    if confirm != 'y':
        info_box("Đã hủy")
        input(f"\n{Color.YELLOW}Enter...{Color.RESET}")
        return
    
    success_count = 0
    total_count = len(selected)
    
    print()
    print(f"{Color.GREEN}{'═' * 60}{Color.RESET}")
    print(f"{Color.GREEN}{Color.BOLD}BẮT ĐẦU XỬ LÝ{Color.RESET}")
    print(f"{Color.GREEN}{'═' * 60}{Color.RESET}")
    
    for idx, assignment in enumerate(selected, 1):
        print(f"\n{Color.YELLOW}[{idx}/{total_count}]{Color.RESET}")
        
        lic = load_lic()
        if not lic:
            error_box("HẾT LƯỢT")
            break
        
        if lic.get('mode') == 'FREE' and lic.get('remain', 0) <= 0:
            error_box("HẾT LƯỢT")
            break
        
        success = submit_assignment(session, assignment, user_id, target_score)
        
        if success:
            success_count += 1
            if assignment['is_ly_thuyet']:
                deduct_license()
            else:
                deduct_license()
        else:
            if assignment['is_ly_thuyet']:
                print(f"{Color.YELLOW}⚠ Lý thuyết vẫn trừ lượt{Color.RESET}")
                deduct_license()
        
        if idx < total_count:
            time.sleep(random.randint(2, 4))
    
    print()
    print(f"{Color.GREEN}{'═' * 60}{Color.RESET}")
    print(f"{Color.GREEN}✓ Hoàn thành: {success_count}/{total_count}{Color.RESET}")
    print(f"{Color.GREEN}{'═' * 60}{Color.RESET}")
    
    input(f"\n{Color.YELLOW}Enter...{Color.RESET}")

# ==================== SOLVE FROM LINK ====================
def solve_from_link(session, user_id):
    banner()
    
    print(f"{Color.CYAN}╔{'═' * 60}╗{Color.RESET}")
    print(f"{Color.CYAN}║{Color.BRIGHT_YELLOW}{Color.BOLD}{'GIẢI BÀI TỪ LINK'.center(60)}{Color.RESET}{Color.CYAN}║{Color.RESET}")
    print(f"{Color.CYAN}╚{'═' * 60}╝{Color.RESET}")
    print()
    
    url = input(f"{Color.YELLOW}🔗 Dán link: {Color.RESET}").strip()
    
    if not url.startswith('https://olm.vn/'):
        error_box("Link không hợp lệ")
        input(f"\n{Color.YELLOW}Enter...{Color.RESET}")
        return
    
    try:
        resp = session.get(url, timeout=10)
        is_video = 'video' in url.lower() or '[Video]' in resp.text
        is_ly_thuyet = 'ly-thuyet' in url.lower() or '[Lý thuyết]' in resp.text
        
        assignment = {
            'title': "Bài từ link",
            'subject': "Tự chọn",
            'type': "Video" if is_video else ("Lý thuyết" if is_ly_thuyet else "Bài tập"),
            'status': "Chưa làm",
            'url': url,
            'page': 1,
            'is_video': is_video,
            'is_ly_thuyet': is_ly_thuyet,
            'is_bai_tap': not (is_video or is_ly_thuyet)
        }
        
        target_score = 100
        if not is_video:
            print()
            print(f"{Color.CYAN}⭐ CHỌN ĐIỂM:{Color.RESET}")
            print(f"  {Color.YELLOW}1.{Color.RESET} 100 điểm")
            print(f"  {Color.YELLOW}2.{Color.RESET} Tùy chọn")
            print()
            
            score_choice = input(f"{Color.BRIGHT_YELLOW}➤ Chọn: {Color.RESET}").strip()
            
            if score_choice == '2':
                try:
                    score = int(input(f"{Color.YELLOW}Nhập điểm (0-100): {Color.RESET}").strip())
                    target_score = max(0, min(100, score))
                except:
                    target_score = 100
        
        print()
        print(f"{Color.CYAN}╔{'═' * 40}╗{Color.RESET}")
        print(f"{Color.CYAN}║{Color.RESET} {Color.BRIGHT_WHITE}Link: ...{url[-30:]}{Color.RESET}")
        print(f"{Color.CYAN}║{Color.RESET} {Color.BRIGHT_WHITE}Loại: {assignment['type']}{Color.RESET}{' ' * (33 - len(assignment['type']))} {Color.CYAN}║{Color.RESET}")
        print(f"{Color.CYAN}║{Color.RESET} {Color.BRIGHT_WHITE}Điểm: {target_score}{Color.RESET}{' ' * (32 - len(str(target_score)))} {Color.CYAN}║{Color.RESET}")
        print(f"{Color.CYAN}╚{'═' * 40}╝{Color.RESET}")
        print()
        
        confirm = input(f"{Color.YELLOW}Xác nhận? (y/n): {Color.RESET}").strip().lower()
        
        if confirm == 'y':
            lic = load_lic()
            if not lic:
                error_box("HẾT LƯỢT")
                input(f"\n{Color.YELLOW}Enter...{Color.RESET}")
                return
            
            if lic.get('mode') == 'FREE' and lic.get('remain', 0) <= 0:
                error_box("HẾT LƯỢT")
                input(f"\n{Color.YELLOW}Enter...{Color.RESET}")
                return
            
            success = submit_assignment(session, assignment, user_id, target_score)
            
            if success:
                if assignment['is_ly_thuyet']:
                    deduct_license()
                else:
                    deduct_license()
            else:
                if assignment['is_ly_thuyet']:
                    print(f"{Color.YELLOW}⚠ Lý thuyết vẫn trừ lượt{Color.RESET}")
                    deduct_license()
            
            input(f"\n{Color.YELLOW}Enter...{Color.RESET}")
        else:
            info_box("Đã hủy")
            input(f"\n{Color.YELLOW}Enter...{Color.RESET}")
    
    except Exception as e:
        error_box(f"Lỗi: {str(e)}")
        input(f"\n{Color.YELLOW}Enter...{Color.RESET}")

# ==================== MAIN MENU ====================
def main_menu(session, user_id, user_name):
    while True:
        banner()
        
        print(f"{Color.BRIGHT_WHITE}👤 {user_name}{Color.RESET}")
        
        lic = load_lic()
        if lic:
            mode = lic.get('mode', 'FREE')
            if mode == 'VIP':
                print(f"{Color.BRIGHT_GREEN}⭐ VIP - UNLIMITED{Color.RESET}")
            else:
                remain = lic.get('remain', 0)
                if remain > 0:
                    print(f"{Color.BRIGHT_YELLOW}💎 FREE - {remain} lượt{Color.RESET}")
                else:
                    print(f"{Color.BRIGHT_RED}⛔ HẾT LƯỢT{Color.RESET}")
        else:
            print(f"{Color.BRIGHT_RED}⛔ Không có license{Color.RESET}")
        
        print()
        print(f"{Color.CYAN}╔{'═' * 60}╗{Color.RESET}")
        print(f"{Color.CYAN}║{Color.BRIGHT_YELLOW}{Color.BOLD}{'MENU CHÍNH'.center(60)}{Color.RESET}{Color.CYAN}║{Color.RESET}")
        print(f"{Color.CYAN}╠{'═' * 60}╣{Color.RESET}")
        print(f"{Color.CYAN}║{Color.RESET}  {Color.YELLOW}[1]{Color.RESET} {Color.WHITE}📝 Giải bài cụ thể{Color.RESET}{' ' * 38} {Color.CYAN}║{Color.RESET}")
        print(f"{Color.CYAN}║{Color.RESET}  {Color.YELLOW}[2]{Color.RESET} {Color.WHITE}🔗 Giải từ link{Color.RESET}{' ' * 41} {Color.CYAN}║{Color.RESET}")
        print(f"{Color.CYAN}║{Color.RESET}  {Color.YELLOW}[3]{Color.RESET} {Color.WHITE}🔄 Đổi tài khoản{Color.RESET}{' ' * 40} {Color.CYAN}║{Color.RESET}")
        print(f"{Color.CYAN}║{Color.RESET}  {Color.YELLOW}[4]{Color.RESET} {Color.WHITE}🚪 Thoát{Color.RESET}{' ' * 48} {Color.CYAN}║{Color.RESET}")
        print(f"{Color.CYAN}╚{'═' * 60}╝{Color.RESET}")
        print()
        
        choice = input(f"{Color.BRIGHT_YELLOW}➤ Chọn (1-4): {Color.RESET}").strip()
        
        if choice in ['1', '2']:
            lic = load_lic()
            if not lic:
                print()
                error_box("HẾT LƯỢT")
                print()
                print(f"{Color.CYAN}Lựa chọn:{Color.RESET}")
                print(f"  {Color.YELLOW}[1]{Color.RESET} Quay launcher lấy key mới")
                print(f"  {Color.YELLOW}[2]{Color.RESET} Thoát")
                print()
                sub_choice = input(f"{Color.YELLOW}Chọn: {Color.RESET}").strip()
                if sub_choice == '1':
                    info_box("Thoát về launcher...")
                    time.sleep(1)
                    sys.exit(0)
                else:
                    info_box("Tạm biệt!")
                    time.sleep(1)
                    sys.exit(0)
            
            if lic.get('mode') == 'FREE' and lic.get('remain', 0) <= 0:
                print()
                error_box("HẾT LƯỢT")
                print()
                print(f"{Color.CYAN}Lựa chọn:{Color.RESET}")
                print(f"  {Color.YELLOW}[1]{Color.RESET} Quay launcher lấy key mới")
                print(f"  {Color.YELLOW}[2]{Color.RESET} Thoát")
                print()
                sub_choice = input(f"{Color.YELLOW}Chọn: {Color.RESET}").strip()
                if sub_choice == '1':
                    info_box("Thoát về launcher...")
                    time.sleep(1)
                    sys.exit(0)
                else:
                    info_box("Tạm biệt!")
                    time.sleep(1)
                    sys.exit(0)
        
        if choice == '1':
            solve_specific(session, user_id)
        elif choice == '2':
            solve_from_link(session, user_id)
        elif choice == '3':
            print()
            confirm = input(f"{Color.YELLOW}Xác nhận đổi tài khoản? (y/n): {Color.RESET}").strip().lower()
            if confirm == 'y':
                clear_lock()
                success_box("Đã xóa account lock")
                info_box("License vẫn được giữ")
                info_box("Thoát về launcher...")
                time.sleep(1)
                sys.exit(0)
        elif choice == '4':
            info_box("Tạm biệt!")
            time.sleep(1)
            sys.exit(0)
        else:
            error_box("Lựa chọn không hợp lệ")
            time.sleep(1)

# ==================== MAIN ====================
def main():
    session, user_id, user_name = load_session()
    
    if not session or not user_id or not user_name:
        error_box("Không thể tải session")
        info_box("Vui lòng chạy lại launcher")
        input(f"\n{Color.YELLOW}Enter...{Color.RESET}")
        return
    
    lic = load_lic()
    if not lic:
        error_box("Không có license")
        info_box("Vui lòng chạy lại launcher")
        input(f"\n{Color.YELLOW}Enter...{Color.RESET}")
        return
    
    is_vip = check_vip_realtime(user_id)
    if is_vip and lic.get('mode') != 'VIP':
        lic['mode'] = 'VIP'
        lic['remain'] = 999999
        lic['sig'] = sig(lic)
        with open(LIC, 'w') as f:
            f.write(enc(lic))
    
    banner()
    print(f"{Color.BRIGHT_WHITE}👤 {user_name}{Color.RESET}")
    
    mode = lic.get('mode', 'FREE')
    if mode == 'VIP':
        print(f"{Color.BRIGHT_GREEN}⭐ VIP UNLIMITED{Color.RESET}")
    else:
        remain = lic.get('remain', 0)
        print(f"{Color.BRIGHT_YELLOW}💎 {remain} lượt{Color.RESET}")
    
    time.sleep(2)
    
    main_menu(session, user_id, user_name)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Color.YELLOW}👋 Tạm biệt!{Color.RESET}\n")
        sys.exit(0)
    except Exception as e:
        error_box(f"Lỗi: {str(e)}")
        input(f"\n{Color.YELLOW}Enter...{Color.RESET}")
