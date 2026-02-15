#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║              OLM MASTER PRO V1.0 - MAIN                      ║
║                  Created by: Tuấn Anh                        ║
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
import platform
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# ========== CẤU HÌNH ==========
GITHUB_VIP = "https://raw.githubusercontent.com/thieunangbiettuot/ToolOLM/refs/heads/main/vip_users.txt"

# ========== MÀU SẮC ==========
class C:
    R = '\033[91m'  # Red
    G = '\033[92m'  # Green
    Y = '\033[93m'  # Yellow
    B = '\033[94m'  # Blue
    M = '\033[95m'  # Magenta
    C = '\033[96m'  # Cyan
    W = '\033[97m'  # White
    BD = '\033[1m'  # Bold
    E = '\033[0m'   # End

# ========== PHÁT HIỆN HỆ ĐIỀU HÀNH ==========
def get_os_type():
    """Phát hiện hệ điều hành"""
    system = platform.system().lower()
    if 'android' in platform.platform().lower() or 'ANDROID_ROOT' in os.environ or 'TERMUX_VERSION' in os.environ:
        return 'android'
    return system

def is_android():
    """Kiểm tra có phải Android/Termux không"""
    return get_os_type() == 'android'

def get_terminal_width():
    """Lấy độ rộng terminal"""
    try:
        cols = os.get_terminal_size().columns
        if is_android():
            return min(cols - 2, 45)
        return min(cols - 2, 68)
    except:
        return 45 if is_android() else 60

# ========== ĐƯỜNG DẪN FILE ==========
def get_base_path():
    """Lấy đường dẫn cơ sở để lưu file"""
    os_type = get_os_type()
    
    if os_type == 'windows':
        base = os.path.join(os.environ.get('LOCALAPPDATA', os.path.expanduser('~')), 
                           'Microsoft', 'Windows', 'INetCache', 'IE')
    elif os_type == 'darwin':  # macOS
        base = os.path.join(os.path.expanduser('~'), 'Library', 'Application Support', 
                           'com.apple.Safari')
    elif os_type == 'android':
        base = os.path.join(os.path.expanduser('~'), '.cache', 'google-chrome')
    else:  # Linux
        base = os.path.join(os.path.expanduser('~'), '.cache', 'mozilla', 'firefox')
    
    os.makedirs(base, exist_ok=True)
    return base

def get_device_hash():
    """Tạo hash thiết bị duy nhất"""
    import uuid
    hostname = platform.node()
    mac = uuid.getnode()
    device_str = f"{hostname}{mac}{platform.system()}"
    return hashlib.md5(device_str.encode()).hexdigest()[:12]

DEVICE_HASH = get_device_hash()
BASE_PATH = get_base_path()

# File paths
LICENSE_FILE = os.path.join(BASE_PATH, f'.{DEVICE_HASH}sc')
SESSION_FILE = os.path.join(BASE_PATH, f'.{DEVICE_HASH}ss')
LOCK_FILE = os.path.join(BASE_PATH, f'.{DEVICE_HASH}lk')

# ========== MÃ HÓA/GIẢI MÃ (GIỐNG LAUNCHER) ==========
SECRET_KEY = f"{DEVICE_HASH}:olmv1:secret".encode()

def xor_cipher(data, key):
    """XOR encryption/decryption"""
    key_len = len(key)
    return bytes([data[i] ^ key[i % key_len] for i in range(len(data))])

def decode_data(encoded):
    """Giải mã dữ liệu"""
    try:
        # Remove noise
        data = encoded[8:-8]
        
        # Extract checksum and b85
        checksum = data[:12]
        b85 = data[12:]
        
        # Verify checksum
        expected_checksum = hashlib.sha256(b85.encode()).hexdigest()[:12]
        if checksum != expected_checksum:
            return None
        
        # Decode
        encrypted = base64.b85decode(b85)
        decrypted = xor_cipher(encrypted, SECRET_KEY)
        json_str = decrypted.decode('utf-8')
        
        return json.loads(json_str)
    except:
        return None

def encode_data(data):
    """Mã hóa dữ liệu"""
    try:
        # Convert to JSON
        json_str = json.dumps(data)
        json_bytes = json_str.encode('utf-8')
        
        # XOR encrypt
        encrypted = xor_cipher(json_bytes, SECRET_KEY)
        
        # Base85 encode
        b85 = base64.b85encode(encrypted).decode('ascii')
        
        # Add checksum
        checksum = hashlib.sha256(b85.encode()).hexdigest()[:12]
        
        # Add noise
        noise_prefix = hashlib.md5(f"{time.time()}{random.random()}".encode()).hexdigest()[:8]
        noise_suffix = noise_prefix[::-1]
        
        # Combine
        result = f"{noise_prefix}{checksum}{b85}{noise_suffix}"
        return result
    except:
        return None

def save_file(filepath, data):
    """Lưu file"""
    try:
        encoded = encode_data(data)
        if encoded:
            with open(filepath, 'w') as f:
                f.write(encoded)
            return True
    except:
        pass
    return False

def load_file(filepath):
    """Đọc file"""
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                encoded = f.read()
            return decode_data(encoded)
    except:
        pass
    return None
# ========== UI ==========
def clear():
    """Xóa màn hình"""
    os.system('cls' if os.name == 'nt' else 'clear')
    if is_android():
        print('\033[2J\033[H', end='')

def print_line(char='═', width=None):
    """In đường kẻ"""
    if width is None:
        width = get_terminal_width()
    print(f"{C.C}{char * width}{C.E}")

def print_header(title="OLM MASTER PRO"):
    """In header"""
    clear()
    width = get_terminal_width()
    print_line('═', width)
    padding = (width - len(title)) // 2
    print(f"{C.B}{C.BD}{' ' * padding}{title}{C.E}")
    print_line('═', width)
    print()

def print_msg(msg, icon='•', color=C.W):
    """In thông báo"""
    print(f"{icon} {color}{msg}{C.E}")

def wait_enter(msg="Nhấn Enter để tiếp tục..."):
    """Chờ nhấn Enter"""
    input(f"\n{C.Y}{msg}{C.E}")

# ========== LICENSE MANAGEMENT ==========
def compute_signature(license_data):
    """Tính signature cho license"""
    sig_str = f"{license_data['mode']}{license_data['expire']}{license_data.get('ip', '')}{license_data.get('remain', 0)}"
    return hashlib.sha256(sig_str.encode()).hexdigest()[:16]

def load_license():
    """Đọc license"""
    data = load_file(LICENSE_FILE)
    
    if not data:
        return None
    
    # Verify signature
    expected_sig = compute_signature(data)
    if data.get('sig') != expected_sig:
        # File bị sửa
        try:
            os.remove(LICENSE_FILE)
        except:
            pass
        return None
    
    # Check expire
    try:
        expire_date = datetime.strptime(data['expire'], "%d/%m/%Y").date()
        if expire_date < datetime.now().date():
            return None
    except:
        return None
    
    # Check remain
    remain = data.get('remain', 0)
    if data.get('mode') == 'FREE' and remain <= 0:
        return None
    
    return data

def update_license_remain(new_remain):
    """Cập nhật số lượt còn lại"""
    data = load_license()
    if data and data.get('mode') == 'FREE':
        data['remain'] = new_remain
        data['sig'] = compute_signature(data)
        save_file(LICENSE_FILE, data)

def deduct_license():
    """Trừ lượt (chỉ gọi SAU KHI hoàn thành bài)"""
    license_data = load_license()
    
    if not license_data:
        return False
    
    # VIP không trừ
    if license_data.get('mode') == 'VIP':
        return True
    
    # FREE trừ lượt
    remain = license_data.get('remain', 0)
    if remain > 0:
        new_remain = remain - 1
        update_license_remain(new_remain)
        
        # Hiển thị
        if new_remain > 0:
            print_msg(f"💎 Còn: {new_remain} lượt", '💎', C.G)
        else:
            print_msg("⛔ HẾT LƯỢT", '⛔', C.R)
        
        return True
    
    return False

def check_vip_realtime(username):
    """Kiểm tra VIP realtime"""
    try:
        response = requests.get(GITHUB_VIP, timeout=5)
        if response.status_code == 200:
            vip_list = response.text.strip().split('\n')
            vip_users = [line.strip().lower() for line in vip_list 
                        if line.strip() and not line.strip().startswith('#')]
            return username.lower() in vip_users
    except:
        pass
    return False

# ========== SESSION MANAGEMENT ==========
def load_session():
    """Đọc session từ launcher"""
    session_data = load_file(SESSION_FILE)
    
    if not session_data:
        return None, None, None
    
    # Tạo lại session
    session = requests.Session()
    
    # Set cookies
    cookies_dict = session_data.get('cookies', {})
    for name, value in cookies_dict.items():
        session.cookies.set(name, value)
    
    # Set headers
    session.headers.update({
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'vi-VN,vi;q=0.9',
        'x-requested-with': 'XMLHttpRequest',
        'origin': 'https://olm.vn',
        'referer': 'https://olm.vn/'
    })
    
    user_id = session_data.get('user_id')
    user_name = session_data.get('user_name')
    
    return session, user_id, user_name

def clear_account_lock():
    """Xóa account lock"""
    try:
        if os.path.exists(LOCK_FILE):
            os.remove(LOCK_FILE)
        return True
    except:
        return False
# ========== HEADERS ==========
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'vi-VN,vi;q=0.9',
    'x-requested-with': 'XMLHttpRequest',
    'origin': 'https://olm.vn',
    'referer': 'https://olm.vn/'
}

# ========== QUÉT BÀI TẬP ==========
def get_assignments_fixed(session, pages_to_scan=3):
    """Lấy danh sách bài tập - BẢN ĐÃ SỬA"""
    print_header(f"QUÉT BÀI TẬP ({pages_to_scan} trang)")
    
    assignments = []
    seen_links = set()
    
    try:
        for page in range(1, pages_to_scan + 1):
            if page == 1:
                url = "https://olm.vn/lop-hoc-cua-toi?action=login"
            else:
                url = f"https://olm.vn/lop-hoc-cua-toi/page-{page}?action=login"
            
            print_msg(f"Đang quét trang {page}/{pages_to_scan}...", '🔍', C.Y)
            
            try:
                timeout = 5 if is_android() else 10
                response = session.get(url, headers=HEADERS, timeout=timeout)
                
                if response.status_code != 200:
                    print_msg(f"Lỗi HTTP {response.status_code}", '❌', C.R)
                    continue
                
                soup = BeautifulSoup(response.text, 'html.parser')
                rows = soup.find_all('tr', class_='my-gived-courseware-item')
                
                if not rows:
                    print_msg(f"Trang {page} không có bài", '⚠️', C.Y)
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
                    is_tu_luan = "[Tự luận]" in loai_raw or "[Tu luan]" in loai_raw
                    is_bai_tap = not (is_video or is_ly_thuyet or is_kiem_tra)
                    
                    # BỎ QUA BÀI TỰ LUẬN và BÀI KIỂM TRA
                    if is_tu_luan or is_kiem_tra:
                        continue
                    
                    # Kiểm tra trạng thái
                    should_process = False
                    status_spans = []
                    
                    # Tìm span trạng thái
                    status_spans.extend(main_link.find_all('span', class_='message-static-item'))
                    
                    if not status_spans:
                        status_spans.extend(row.find_all('span', class_='message-static-item'))
                    
                    if not status_spans:
                        warning_spans = row.find_all('span', class_='alert-warning')
                        for span in warning_spans:
                            span_text = span.get_text(strip=True)
                            if span_text not in ['Hóa học', 'Toán', 'Ngữ văn', 'Tiếng Anh', 'Tin học']:
                                status_spans.append(span)
                    
                    # Kiểm tra span
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
                        
                        # Lấy thông tin
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
                        
                        # URL đầy đủ
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
                    print_msg(f"Trang {page}: {page_count} bài", '✓', C.G)
                else:
                    print_msg(f"Trang {page}: 0 bài", '⚠️', C.Y)
                    
            except Exception as e:
                print_msg(f"Lỗi trang {page}", '❌', C.R)
                continue
        
        # Tổng kết
        if assignments:
            print_msg(f"Tổng: {len(assignments)} bài cần làm", '📚', C.G + C.BD)
            
            # Thống kê
            video_count = sum(1 for a in assignments if a['is_video'])
            ly_thuyet_count = sum(1 for a in assignments if a['is_ly_thuyet'])
            bai_tap_count = sum(1 for a in assignments if a['is_bai_tap'])
            
            print()
            print(f"{C.C}📊 THỐNG KÊ:{C.E}")
            if video_count > 0:
                print(f"  🎬 Video: {video_count}")
            if ly_thuyet_count > 0:
                print(f"  📖 Lý thuyết: {ly_thuyet_count}")
            if bai_tap_count > 0:
                print(f"  📝 Bài tập: {bai_tap_count}")
            
            return assignments
        else:
            print_msg("Không tìm thấy bài", '⚠️', C.Y)
            return []
            
    except Exception as e:
        print_msg(f"Lỗi: {str(e)}", '❌', C.R)
        return []

def display_assignments_table(assignments):
    """Hiển thị danh sách bài"""
    if not assignments:
        return
    
    print(f"\n{C.M}{'📚 DANH SÁCH BÀI TẬP':^60}{C.E}")
    print_line('─')
    
    for idx, item in enumerate(assignments, 1):
        title = item['title']
        if len(title) > 35:
            title = title[:32] + "..."
        
        # Icon theo loại
        if item['is_video']:
            icon = '🎬'
            color = C.B
        elif item['is_ly_thuyet']:
            icon = '📖'
            color = C.C
        else:
            icon = '📝'
            color = C.G
        
        print(f"{C.Y}{idx:>2}.{C.E} {icon} {color}{item['type']:<12}{C.E} {C.W}{title}{C.E}")
    
    print_line('─')
# ========== LOGIC GIẢI BÀI ==========
def extract_quiz_info(session, url, is_video=False):
    """Trích xuất thông tin quiz"""
    try:
        timeout = 5 if is_android() else 10
        resp = session.get(url, timeout=timeout)
        html = resp.text
        
        # Tìm quiz_list
        quiz_list = None
        
        # Pattern 1
        pattern1 = r'quiz_list\s*[:=]\s*["\'](\d{6,}(?:,\d{6,})*)["\']'
        match1 = re.search(pattern1, html)
        if match1:
            quiz_list = match1.group(1)
        
        # Pattern 2
        if not quiz_list:
            pattern2 = r'\b\d{9,}(?:,\d{9,})+\b'
            matches = re.findall(pattern2, html)
            if matches:
                quiz_list = max(matches, key=len)
        
        # Pattern 3
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
            cw_match = re.search(r'data-courseware\s*=\s*["\'](\d+)["\']', html)
            if cw_match:
                id_courseware = cw_match.group(1)
        
        # Tìm id_cate
        id_cate = None
        cate_match = re.search(r'-(\d+)(?:\?|$)', url)
        if cate_match:
            id_cate = cate_match.group(1)
        
        if not quiz_list:
            if is_video:
                return "", 0, id_courseware, id_cate
            else:
                return None, 0, id_courseware, id_cate
        
        # Tách danh sách
        question_ids = [qid.strip() for qid in quiz_list.split(',') if qid.strip()]
        total_questions = len(question_ids)
        
        return quiz_list, total_questions, id_courseware, id_cate
        
    except:
        return None, 0, None, None

def create_data_log(total_questions, target_score):
    """Tạo data_log"""
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

def submit_assignment(session, assignment, user_id, target_score):
    """Nộp bài tập"""
    print(f"\n{C.C}📤 ĐANG XỬ LÝ:{C.E}")
    print(f"{C.W}  📖 {assignment['title']}{C.E}")
    
    # Hiển thị loại
    if assignment['is_video']:
        print(f"{C.B}  🎬 Video{C.E}")
    elif assignment['is_ly_thuyet']:
        print(f"{C.C}  📚 Lý thuyết{C.E}")
    else:
        print(f"{C.G}  📝 Bài tập{C.E}")
    
    try:
        # Trích xuất
        quiz_list, total_questions, id_courseware, id_cate = extract_quiz_info(
            session, assignment['url'], assignment['is_video']
        )
        
        # Video
        if assignment['is_video']:
            success = handle_video_submission(session, assignment, user_id, 
                                             quiz_list, total_questions, 
                                             id_courseware, id_cate)
            return success
        
        # Bài tập thường
        if not quiz_list or total_questions == 0:
            print_msg("Không lấy được thông tin", '❌', C.R)
            return False
        
        # Tạo data
        data_log, total_time, correct_needed = create_data_log(total_questions, target_score)
        
        # CSRF token
        csrf_token = session.cookies.get('XSRF-TOKEN')
        
        if not csrf_token:
            timeout = 5 if is_android() else 10
            resp = session.get(assignment['url'], timeout=timeout)
            csrf_match = re.search(r'<meta name="csrf-token" content="([^"]+)"', resp.text)
            csrf_token = csrf_match.group(1) if csrf_match else ""
        
        # Payload
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
        
        # Gửi
        print_msg("Đang nộp bài...", '⏳', C.Y)
        
        submit_headers = HEADERS.copy()
        submit_headers['x-csrf-token'] = csrf_token
        
        timeout = 10 if is_android() else 15
        response = session.post(
            'https://olm.vn/course/teacher-static',
            data=payload,
            headers=submit_headers,
            timeout=timeout
        )
        
        # Xử lý kết quả
        success = handle_submission_response(response, target_score)
        
        return success
            
    except Exception as e:
        print_msg(f"Lỗi: {str(e)}", '❌', C.R)
        return False

def handle_submission_response(response, target_score):
    """Xử lý phản hồi"""
    if response.status_code == 200:
        try:
            result = response.json()
            
            if 'code' in result:
                if result['code'] == 403:
                    print_msg("Đã nộp trước đó", '⚠️', C.Y)
                    return True
                elif result['code'] == 400:
                    print_msg(f"Lỗi 400", '❌', C.R)
                    return False
                else:
                    print_msg("✓ Thành công!", '✓', C.G)
                    return True
            else:
                print_msg("✓ Thành công!", '✓', C.G)
                return True
        except:
            print_msg("✓ Thành công!", '✓', C.G)
            return True
    elif response.status_code == 403:
        print_msg("Đã nộp trước", '⚠️', C.Y)
        return True
    else:
        print_msg(f"Lỗi {response.status_code}", '❌', C.R)
        return False
# ========== XỬ LÝ VIDEO ==========
def handle_video_submission(session, assignment, user_id, quiz_list, total_questions, id_courseware, id_cate):
    """Xử lý video"""
    methods = [
        try_video_simple_method,
        try_video_with_quiz,
        try_video_complex_method,
    ]
    
    for method in methods:
        success = method(session, assignment, user_id, quiz_list, total_questions, id_courseware, id_cate)
        if success:
            return True
        time.sleep(0.5)
    
    return False

def try_video_simple_method(session, assignment, user_id, quiz_list, total_questions, id_courseware, id_cate):
    """Video method 1"""
    try:
        csrf_token = session.cookies.get('XSRF-TOKEN')
        if not csrf_token:
            timeout = 5 if is_android() else 10
            resp = session.get(assignment['url'], timeout=timeout)
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
        
        timeout = 8 if is_android() else 10
        response = session.post(
            'https://olm.vn/course/teacher-static',
            data=payload,
            headers=submit_headers,
            timeout=timeout
        )
        
        return handle_submission_response(response, 100)
    except:
        return False

def try_video_with_quiz(session, assignment, user_id, quiz_list, total_questions, id_courseware, id_cate):
    """Video method 2"""
    try:
        if not quiz_list or total_questions == 0:
            return False
        
        csrf_token = session.cookies.get('XSRF-TOKEN')
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
        
        timeout = 8 if is_android() else 10
        response = session.post(
            'https://olm.vn/course/teacher-static',
            data=payload,
            headers=submit_headers,
            timeout=timeout
        )
        
        return handle_submission_response(response, 100)
    except:
        return False

def try_video_complex_method(session, assignment, user_id, quiz_list, total_questions, id_courseware, id_cate):
    """Video method 3"""
    try:
        csrf_token = session.cookies.get('XSRF-TOKEN')
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
            'id_courseware': id_courseware or '0',
            'time_spent': str(time_spent),
            'score': '100',
            'data_log': json.dumps(data_log, separators=(',', ':')),
            'date_end': str(current_time),
            'ended': '1',
            'cv_q': '1',
            'correct': str(len(data_log)),
            'count_problems': str(len(data_log))
        }
        
        if quiz_list:
            payload['quiz_list'] = quiz_list
        
        submit_headers = HEADERS.copy()
        submit_headers['x-csrf-token'] = csrf_token
        
        timeout = 8 if is_android() else 10
        response = session.post(
            'https://olm.vn/course/teacher-static',
            data=payload,
            headers=submit_headers,
            timeout=timeout
        )
        
        return handle_submission_response(response, 100)
    except:
        return False

# ========== GIẢI BÀI CỤ THỂ ==========
def solve_specific_from_list(session, user_id):
    """Giải bài cụ thể từ danh sách"""
    print_header("GIẢI BÀI CỤ THỂ")
    
    # Hỏi số trang
    pages_input = input(f"{C.Y}Số trang quét (mặc định 3): {C.E}").strip()
    pages_to_scan = 3
    if pages_input.isdigit() and int(pages_input) > 0:
        pages_to_scan = min(int(pages_input), 10)
    
    # Quét bài
    assignments = get_assignments_fixed(session, pages_to_scan)
    if not assignments:
        wait_enter()
        return 0, 0
    
    display_assignments_table(assignments)
    
    # Chọn bài
    print()
    print(f"{C.C}Chọn bài để giải:{C.E}")
    print(f"  • Nhập {C.Y}0{C.E} để giải tất cả")
    print(f"  • Nhập {C.Y}1,3,5{C.E} để giải nhiều bài")
    print(f"  • Nhập {C.Y}1{C.E} để giải 1 bài")
    print()
    
    selection = input(f"{C.Y}Chọn: {C.E}").strip()
    
    # Parse selection
    selected_assignments = []
    
    if selection == '0':
        # Tất cả
        selected_assignments = assignments
    elif ',' in selection:
        # Nhiều bài
        try:
            indices = [int(x.strip()) - 1 for x in selection.split(',')]
            selected_assignments = [assignments[i] for i in indices if 0 <= i < len(assignments)]
        except:
            print_msg("Định dạng không hợp lệ!", '❌', C.R)
            wait_enter()
            return 0, 0
    else:
        # 1 bài
        try:
            idx = int(selection) - 1
            if 0 <= idx < len(assignments):
                selected_assignments = [assignments[idx]]
        except:
            print_msg("Số không hợp lệ!", '❌', C.R)
            wait_enter()
            return 0, 0
    
    if not selected_assignments:
        print_msg("Không có bài nào được chọn!", '⚠️', C.Y)
        wait_enter()
        return 0, 0
    
    # Chọn điểm 1 lần cho tất cả
    print()
    print(f"{C.C}⭐ CHỌN ĐIỂM CHO TẤT CẢ BÀI:{C.E}")
    print(f"  {C.Y}1.{C.E} 100 điểm")
    print(f"  {C.Y}2.{C.E} Tùy chọn")
    print()
    
    target_score = 100
    score_choice = input(f"{C.Y}Chọn (1-2): {C.E}").strip()
    
    if score_choice == '2':
        try:
            score = int(input(f"{C.Y}Nhập điểm (0-100): {C.E}").strip())
            target_score = max(0, min(100, score))
        except:
            target_score = 100
    
    # Confirm
    print()
    print(f"{C.C}📋 XÁC NHẬN:{C.E}")
    print(f"  • Số bài: {len(selected_assignments)}")
    print(f"  • Điểm: {target_score}")
    print()
    
    confirm = input(f"{C.Y}Xác nhận? (y/n): {C.E}").strip().lower()
    
    if confirm != 'y':
        print_msg("Đã hủy", '⚠️', C.Y)
        wait_enter()
        return 0, 0
    
    # Làm bài
    return process_assignments(session, selected_assignments, user_id, target_score)

def process_assignments(session, assignments, user_id, target_score):
    """Xử lý danh sách bài"""
    print_header("BẮT ĐẦU XỬ LÝ")
    
    success_count = 0
    total_count = len(assignments)
    
    for idx, assignment in enumerate(assignments, 1):
        print(f"\n{C.Y}📊 Bài {idx}/{total_count}{C.E}")
        
        # Check license trước khi làm
        license_data = load_license()
        if not license_data:
            print_msg("⛔ HẾT LƯỢT", '⛔', C.R)
            break
        
        if license_data.get('mode') == 'FREE' and license_data.get('remain', 0) <= 0:
            print_msg("⛔ HẾT LƯỢT", '⛔', C.R)
            break
        
        # Làm bài
        success = submit_assignment(session, assignment, user_id, target_score)
        
        if success:
            success_count += 1
            
            # Trừ lượt SAU KHI thành công
            # ĐẶC BIỆT: Lý thuyết luôn trừ lượt dù thành công hay thất bại
            if assignment['is_ly_thuyet']:
                deduct_license()
            else:
                deduct_license()
        else:
            # Thất bại - chỉ trừ nếu là lý thuyết
            if assignment['is_ly_thuyet']:
                print_msg("⚠️ Lý thuyết vẫn trừ lượt", '⚠️', C.Y)
                deduct_license()
        
        # Chờ giữa các bài
        if idx < total_count:
            wait_time = random.randint(2, 4)
            time.sleep(wait_time)
    
    # Kết quả
    print()
    print_line('═')
    print(f"{C.G}✓ Hoàn thành: {success_count}/{total_count}{C.E}")
    print_line('═')
    
    wait_enter()
    return success_count, total_count

# ========== GIẢI BÀI TỪ LINK ==========
def solve_from_link(session, user_id):
    """Giải bài từ link"""
    print_header("GIẢI BÀI TỪ LINK")
    
    print(f"{C.C}🔗 NHẬP LINK:{C.E}")
    print("Ví dụ: https://olm.vn/chu-de/...")
    print()
    
    url = input(f"🔗 {C.Y}Dán link: {C.E}").strip()
    
    if not url.startswith('https://olm.vn/'):
        print_msg("Link không hợp lệ!", '❌', C.R)
        wait_enter()
        return 0, 0
    
    try:
        # Kiểm tra loại
        timeout = 5 if is_android() else 10
        resp = session.get(url, timeout=timeout)
        is_video = 'video' in url.lower() or '[Video]' in resp.text
        is_ly_thuyet = 'ly-thuyet' in url.lower() or '[Lý thuyết]' in resp.text
        
        # Tạo assignment
        assignment = {
            'title': "Bài từ link",
            'subject': "Tự chọn",
            'type': "Video" if is_video else ("Lý thuyết" if is_ly_thuyet else "Bài tập"),
            'status': "Chưa làm",
            'url': url,
            'page': 1,
            'is_video': is_video,
            'is_ly_thuyet': is_ly_thuyet,
            'is_bai_tap': not (is_video or is_ly_thuyet),
            'is_kiem_tra': False,
            'is_tu_luan': False
        }
        
        # Chọn điểm
        target_score = 100
        if not is_video:
            print()
            print(f"{C.C}⭐ CHỌN ĐIỂM:{C.E}")
            print(f"  {C.Y}1.{C.E} 100 điểm")
            print(f"  {C.Y}2.{C.E} Tùy chọn")
            print()
            
            score_choice = input(f"{C.Y}Chọn: {C.E}").strip()
            
            if score_choice == '2':
                try:
                    score = int(input(f"{C.Y}Nhập điểm (0-100): {C.E}").strip())
                    target_score = max(0, min(100, score))
                except:
                    target_score = 100
        
        # Confirm
        print()
        print(f"{C.C}📋 THÔNG TIN:{C.E}")
        print(f"  • Link: {url}")
        print(f"  • Loại: {assignment['type']}")
        print(f"  • Điểm: {target_score}")
        print()
        
        confirm = input(f"{C.Y}Xác nhận? (y/n): {C.E}").strip().lower()
        
        if confirm == 'y':
            # Check license
            license_data = load_license()
            if not license_data:
                print_msg("⛔ HẾT LƯỢT", '⛔', C.R)
                wait_enter()
                return 0, 0
            
            if license_data.get('mode') == 'FREE' and license_data.get('remain', 0) <= 0:
                print_msg("⛔ HẾT LƯỢT", '⛔', C.R)
                wait_enter()
                return 0, 0
            
            # Làm bài
            success = submit_assignment(session, assignment, user_id, target_score)
            
            if success:
                # Trừ lượt
                if assignment['is_ly_thuyet']:
                    deduct_license()
                else:
                    deduct_license()
                
                wait_enter()
                return 1, 1
            else:
                if assignment['is_ly_thuyet']:
                    print_msg("⚠️ Lý thuyết vẫn trừ lượt", '⚠️', C.Y)
                    deduct_license()
                
                wait_enter()
                return 0, 1
        else:
            print_msg("Đã hủy", '⚠️', C.Y)
            wait_enter()
            return 0, 0
            
    except Exception as e:
        print_msg(f"Lỗi: {str(e)}", '❌', C.R)
        wait_enter()
        return 0, 0
# ========== MENU CHÍNH ==========
def main_menu(session, user_id, user_name):
    """Menu chính - 4 options"""
    
    while True:
        print_header("MENU CHÍNH")
        
        # Hiển thị user
        print(f"👤 {C.G}{user_name}{C.E}")
        
        # Hiển thị license
        license_data = load_license()
        if license_data:
            mode = license_data.get('mode', 'FREE')
            if mode == 'VIP':
                print(f"⭐ {C.G}VIP - Không giới hạn{C.E}")
            else:
                remain = license_data.get('remain', 0)
                if remain > 0:
                    print(f"💎 {C.Y}FREE - Còn {remain} lượt{C.E}")
                else:
                    print(f"⛔ {C.R}HẾT LƯỢT{C.E}")
        else:
            print(f"⛔ {C.R}Không có license{C.E}")
        
        print()
        print_line('─')
        
        # Menu options
        print(f"  {C.Y}1.{C.E} 📝 Giải bài cụ thể")
        print(f"  {C.Y}2.{C.E} 🔗 Giải từ link")
        print(f"  {C.Y}3.{C.E} 🔄 Đổi tài khoản")
        print(f"  {C.Y}4.{C.E} 🚪 Thoát")
        
        print_line('─')
        
        choice = input(f"\n{C.Y}Chọn (1-4): {C.E}").strip()
        
        # Check license trước khi làm bài
        if choice in ['1', '2']:
            license_data = load_license()
            
            if not license_data:
                print()
                print_msg("⛔ HẾT LƯỢT", '⛔', C.R)
                print()
                print(f"{C.C}LỰA CHỌN:{C.E}")
                print(f"  {C.Y}1.{C.E} Quay launcher lấy key mới")
                print(f"  {C.Y}2.{C.E} Thoát")
                print()
                
                sub_choice = input(f"{C.Y}Chọn: {C.E}").strip()
                
                if sub_choice == '1':
                    print_msg("Thoát về launcher...", '🔄', C.Y)
                    time.sleep(1)
                    sys.exit(0)
                else:
                    print_msg("Tạm biệt!", '👋', C.C)
                    time.sleep(1)
                    sys.exit(0)
            
            if license_data.get('mode') == 'FREE' and license_data.get('remain', 0) <= 0:
                print()
                print_msg("⛔ HẾT LƯỢT", '⛔', C.R)
                print()
                print(f"{C.C}LỰA CHỌN:{C.E}")
                print(f"  {C.Y}1.{C.E} Quay launcher lấy key mới")
                print(f"  {C.Y}2.{C.E} Thoát")
                print()
                
                sub_choice = input(f"{C.Y}Chọn: {C.E}").strip()
                
                if sub_choice == '1':
                    print_msg("Thoát về launcher...", '🔄', C.Y)
                    time.sleep(1)
                    sys.exit(0)
                else:
                    print_msg("Tạm biệt!", '👋', C.C)
                    time.sleep(1)
                    sys.exit(0)
        
        # Xử lý choice
        if choice == '1':
            # Giải bài cụ thể
            solve_specific_from_list(session, user_id)
            
        elif choice == '2':
            # Giải từ link
            solve_from_link(session, user_id)
            
        elif choice == '3':
            # Đổi tài khoản
            print()
            confirm = input(f"{C.Y}Xác nhận đổi tài khoản? (y/n): {C.E}").strip().lower()
            
            if confirm == 'y':
                # Xóa account lock
                clear_account_lock()
                
                print_msg("Đã xóa account lock", '✓', C.G)
                print_msg("License vẫn được giữ", 'ℹ️', C.C)
                print_msg("Thoát về launcher...", '🔄', C.Y)
                time.sleep(1)
                sys.exit(0)
            
        elif choice == '4':
            # Thoát
            print_msg("Tạm biệt!", '👋', C.C)
            time.sleep(1)
            sys.exit(0)
            
        else:
            print_msg("Lựa chọn không hợp lệ!", '❌', C.R)
            time.sleep(1)

# ========== MAIN ==========
def main():
    """Main function"""
    
    # Load session từ launcher
    session, user_id, user_name = load_session()
    
    if not session or not user_id or not user_name:
        print_header("LỖI")
        print_msg("Không thể tải session!", '❌', C.R)
        print_msg("Vui lòng chạy lại launcher", 'ℹ️', C.W)
        wait_enter()
        return
    
    # Load license
    license_data = load_license()
    
    if not license_data:
        print_header("LỖI")
        print_msg("Không có license!", '❌', C.R)
        print_msg("Vui lòng chạy lại launcher", 'ℹ️', C.W)
        wait_enter()
        return
    
    # Check VIP realtime (ngầm)
    is_vip = check_vip_realtime(user_id)
    if is_vip and license_data.get('mode') != 'VIP':
        # Upgrade to VIP
        license_data['mode'] = 'VIP'
        license_data['remain'] = -1
        license_data['sig'] = compute_signature(license_data)
        save_file(LICENSE_FILE, license_data)
    
    # Vào menu
    print_header("KHỞI ĐỘNG")
    print_msg(f"Xin chào: {user_name}", '👤', C.G)
    
    mode = license_data.get('mode', 'FREE')
    if mode == 'VIP':
        print_msg("⭐ Tài khoản VIP", '⭐', C.G)
    else:
        remain = license_data.get('remain', 0)
        print_msg(f"💎 Còn {remain} lượt làm bài", '💎', C.G)
    
    time.sleep(2)
    
    # Menu chính
    main_menu(session, user_id, user_name)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{C.Y}Đã dừng chương trình{C.E}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{C.R}Lỗi: {str(e)}{C.E}")
        wait_enter()
