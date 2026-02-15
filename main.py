#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║                 OLM MASTER PRO - MAIN V1.0                  ║
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
import subprocess
import pickle
import tempfile
from bs4 import BeautifulSoup
from datetime import datetime

# Import colors từ launcher
try:
    # Nếu chạy từ launcher
    from launcher import C, ICONS
except:
    # Nếu chạy độc lập
    class C:
        R = '\033[91m'
        G = '\033[92m'
        Y = '\033[93m'
        B = '\033[94m'
        M = '\033[95m'
        C = '\033[96m'
        W = '\033[97m'
        BOLD = '\033[1m'
        E = '\033[0m'
    
    ICONS = {
        'success': '✓',
        'error': '✗',
        'warning': '⚠',
        'info': 'ℹ',
        'lock': '🔒',
        'user': '👤',
        'key': '🔑',
        'star': '★',
        'rocket': '🚀',
        'diamond': '💎',
        'crown': '👑',
        'check': '✔',
        'exit': '🚪',
        'refresh': '🔄',
        'download': '📥',
        'upload': '📤',
        'link': '🔗',
        'list': '📋',
        'magic': '✨',
        'brain': '🧠',
        'back': '↩️',
        'video': '🎬',
        'theory': '📖',
        'exercise': '📝',
        'search': '🔍',
        'clock': '⏰',
        'fire': '🔥',
        'setting': '⚙️',
        'home': '🏠',
        'book': '📚'
    }

# ========== TIỆN ÍCH HIỂN THỊ ==========
def clear_screen():
    """Xóa màn hình"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_centered(text, color=C.W, width=60):
    """In text căn giữa"""
    padding = (width - len(text.strip())) // 2
    print(f"{color}{' ' * padding}{text}{C.E}")

def print_line(char='═', color=C.C, width=60):
    """In đường kẻ"""
    print(f"{color}{char * width}{C.E}")

def print_header(title=""):
    """In header tool"""
    clear_screen()
    print_line('═', C.B, 60)
    print_centered(f"{ICONS['rocket']} OLM MASTER - AUTO SOLVER {ICONS['fire']}", C.B + C.BOLD, 60)
    print_centered("Created by: Tuấn Anh", C.M, 60)
    if title:
        print_line('─', C.C, 60)
        print_centered(title, C.C, 60)
    print_line('═', C.B, 60)
    print()

def print_menu(title, options):
    """In menu"""
    print(f"\n{C.C}{ICONS['setting']} {title}{C.E}")
    print_line('─', C.C, 40)
    for key, value in options.items():
        print(f"  {C.Y}{key}.{C.E} {value}")
    print_line('─', C.C, 40)

def wait_enter(prompt="Nhấn Enter để tiếp tục..."):
    """Chờ nhấn Enter"""
    input(f"\n{C.Y}{prompt}{C.E}")

def print_status(message, icon='info', color=C.W):
    """In thông báo trạng thái"""
    print(f"{ICONS.get(icon, '')} {color}{message}{C.E}")

def print_box(title, content, color=C.C, width=60):
    """In box với nội dung"""
    print(f"{color}╔{'═' * (width - 2)}╗{C.E}")
    if title:
        title_padding = (width - len(title) - 2) // 2
        print(f"{color}║{' ' * title_padding}{C.BOLD}{title}{C.E}{color}{' ' * (width - title_padding - len(title) - 2)}║{C.E}")
        print(f"{color}╠{'═' * (width - 2)}╣{C.E}")
    for line in content:
        if len(line) > width - 4:
            line = line[:width - 7] + "..."
        line_padding = width - len(line) - 4
        print(f"{color}║ {C.W}{line}{C.E}{color}{' ' * line_padding} ║{C.E}")
    print(f"{color}╚{'═' * (width - 2)}╝{C.E}")

# ========== HEADERS ==========
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'vi-VN,vi;q=0.9,en-US;q=0.8',
    'x-requested-with': 'XMLHttpRequest',
    'origin': 'https://olm.vn',
    'referer': 'https://olm.vn/'
}

# ========== TẢI SESSION ==========
def load_session():
    """Tải session từ launcher"""
    try:
        session_file = os.environ.get('OLM_SESSION_FILE', os.path.join(tempfile.gettempdir(), "session_olm.pkl"))
        if os.path.exists(session_file):
            with open(session_file, 'rb') as f:
                data = pickle.load(f)
                # Tạo session từ cookies
                session = requests.Session()
                session.cookies.update(data['cookies'])
                session.headers.update(HEADERS)
                return session, data.get('user_id'), data.get('user_name')
    except:
        pass
    return None, None, None

# ========== QUẢN LÝ LICENSE ==========
def load_license():
    """Tải license"""
    try:
        lic_file = os.environ.get('OLM_LICENSE_FILE', '.lic')
        if os.path.exists(lic_file):
            with open(lic_file, 'r') as f:
                d = dec(f.read())
            return d
    except:
        pass
    return None

def dec(s):
    """Giải mã đơn giản"""
    try:
        # Giải mã base64
        import base64
        decoded = base64.b64decode(s).decode()
        return json.loads(decoded)
    except:
        return None

def use_credit(assignment=None):
    """Trừ lượt sử dụng"""
    try:
        lic_file = os.environ.get('OLM_LICENSE_FILE', '.lic')
        if not os.path.exists(lic_file):
            return True
        
        with open(lic_file, 'r') as f:
            d = dec(f.read())
        
        if not d:
            return True
        
        # VIP không trừ lượt
        if d.get('mode') == 'VIP':
            return True
        
        # Bài lý thuyết luôn trừ lượt
        if assignment and assignment.get('is_ly_thuyet'):
            remain = d.get('remain', 0)
            if remain > 0:
                d['remain'] = remain - 1
                # Lưu lại
                with open(lic_file, 'w') as f:
                    import base64
                    f.write(base64.b64encode(json.dumps(d).encode()).decode())
                print_status(f"💎 Còn: {d['remain']} lượt", 'info', C.Y)
                return True
            else:
                print_status("Hết lượt!", 'error', C.R)
                return False
        
        # Thông thường - trừ sau khi thành công
        return True
    except:
        return True

def get_remaining_credits():
    """Lấy số lượt còn lại"""
    try:
        lic_file = os.environ.get('OLM_LICENSE_FILE', '.lic')
        if os.path.exists(lic_file):
            with open(lic_file, 'r') as f:
                d = dec(f.read())
            if d:
                if d.get('mode') == 'VIP':
                    return -1  # Unlimited
                return d.get('remain', 0)
    except:
        pass
    return 0

# ========== QUÉT BÀI TẬP (GIỮ NGUYÊN TỪ TOOL GỐC) ==========
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
            
            print_status(f"Đang quét trang {page}/{pages_to_scan}...", 'search', C.Y)
            
            try:
                response = session.get(url, headers=HEADERS, timeout=10)
                
                if response.status_code != 200:
                    print_status(f"Lỗi HTTP {response.status_code}", 'error', C.R)
                    continue
                
                soup = BeautifulSoup(response.text, 'html.parser')
                rows = soup.find_all('tr', class_='my-gived-courseware-item')
                
                if not rows: 
                    print_status(f"Trang {page} không có bài tập", 'warning', C.Y)
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
                    print_status(f"Trang {page}: {page_count} bài cần làm", 'success', C.G)
                else:
                    print_status(f"Trang {page}: không có bài cần làm", 'warning', C.Y)
                    
            except Exception as e:
                print_status(f"Lỗi trang {page}: {str(e)}", 'error', C.R)
                continue
        
        # Tổng kết
        if assignments:
            print_status(f"Tổng cộng: {len(assignments)} bài cần xử lý", 'success', C.G + C.BOLD)
            
            # Thống kê loại bài
            video_count = sum(1 for a in assignments if a['is_video'])
            ly_thuyet_count = sum(1 for a in assignments if a['is_ly_thuyet'])
            bai_tap_count = sum(1 for a in assignments if a['is_bai_tap'])
            kiem_tra_count = sum(1 for a in assignments if a['is_kiem_tra'])
            
            print(f"\n{C.C}📊 THỐNG KÊ LOẠI BÀI:{C.E}")
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
            print_status("Không tìm thấy bài tập nào cần làm", 'warning', C.Y)
            return []
            
    except Exception as e:
        print_status(f"Lỗi khi quét bài tập: {str(e)}", 'error', C.R)
        return []

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

def display_assignments_table(assignments):
    """Hiển thị danh sách bài tập dạng bảng"""
    if not assignments:
        return
    
    print(f"\n{C.M}{'📚 DANH SÁCH BÀI TẬP CẦN LÀM 📚':^90}{C.E}")
    print_line('─', C.M, 90)
    
    for idx, item in enumerate(assignments, 1):
        title = item['title']
        if len(title) > 38:
            title = title[:35] + "..."
        
        # Màu sắc theo loại bài
        if item['is_video']:
            loai_color = C.B
            icon = ICONS['video']
        elif item['is_ly_thuyet']:
            loai_color = C.C
            icon = ICONS['theory']
        elif item['is_kiem_tra']:
            loai_color = C.Y
            icon = ICONS['warning']
        else:
            loai_color = C.G
            icon = ICONS['exercise']
        
        # Màu sắc theo trạng thái
        status = item['status']
        if "Chưa làm" in status or "chưa nộp" in status.lower():
            status_color = C.R
        elif "làm tiếp" in status.lower():
            status_color = C.Y
        else:
            status_color = C.W
        
        print(f"{C.Y}{idx:>2}.{C.E} ", end="")
        print(f"{icon} ", end="")
        print(f"{loai_color}{item['type']:<10}{C.E} ", end="")
        print(f"{C.W}{item['subject']:<15}{C.E} ", end="")
        print(f"{C.W}{title:<40}{C.E} ", end="")
        print(f"{status_color}{status:<15}{C.E}")
    
    print_line('─', C.M, 90)

# ========== XỬ LÝ BÀI TẬP (GIỮ NGUYÊN TỪ TOOL GỐC) ==========
def get_target_score(is_video=False, is_kiem_tra=False):
    """Menu chọn điểm số"""
    if is_video:
        print_status("Video: Tự động chọn 100 điểm", 'video', C.B)
        return 100
    elif is_kiem_tra:
        print_status("Kiểm tra: Tự động chọn điểm cao", 'warning', C.Y)
        return random.randint(85, 100)  # Điểm kiểm tra thường cao
    
    print(f"\n{C.C}{ICONS['star']} CHỌN ĐIỂM SỐ{C.E}")
    print_line('─', C.C, 40)
    print(f"  {C.Y}1.{C.E} {ICONS['star']} 100 điểm (Xuất sắc)")
    print(f"  {C.Y}2.{C.E} {ICONS['info']} Tùy chọn điểm số")
    print_line('─', C.C, 40)
    
    while True:
        choice = input(f"{C.Y}Chọn (1-2): {C.E}").strip()
        
        if choice == '1':
            return 100
        elif choice == '2':
            try:
                score = int(input(f"{C.Y}Nhập điểm số (0-100): {C.E}").strip())
                if 0 <= score <= 100:
                    return score
                else:
                    print_status("Điểm số phải từ 0 đến 100!", 'error', C.R)
            except ValueError:
                print_status("Vui lòng nhập số hợp lệ!", 'error', C.R)
        else:
            print_status("Lựa chọn không hợp lệ!", 'error', C.R)

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
                print_status("Video: Không có quiz_list, sẽ thử phương pháp khác", 'video', C.B)
                return "", 0, id_courseware, id_cate
            else:
                print_status("Không tìm thấy danh sách câu hỏi", 'error', C.R)
                return None, 0, id_courseware, id_cate
        
        # Tách danh sách câu hỏi
        question_ids = [qid.strip() for qid in quiz_list.split(',') if qid.strip()]
        total_questions = len(question_ids)
        
        print_status(f"Tìm thấy {total_questions} câu hỏi", 'info', C.W)
        
        return quiz_list, total_questions, id_courseware, id_cate
        
    except Exception as e:
        print_status(f"Lỗi trích xuất thông tin: {str(e)}", 'error', C.R)
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
    print(f"\n{C.C}{ICONS['upload']} ĐANG XỬ LÝ:{C.E}")
    print(f"{C.W}📖 {assignment['title']}{C.E}")
    
    if assignment['is_video']:
        print(f"{C.B}🎬 Loại: Video{C.E}")
        target_score = 100
    elif assignment['is_ly_thuyet']:
        print(f"{C.C}📚 Loại: Lý thuyết{C.E}")
        target_score = get_target_score(False, False)
    elif assignment['is_kiem_tra']:
        print(f"{C.Y}⚠️ Loại: Kiểm tra{C.E}")
        target_score = get_target_score(False, True)
    else:
        print(f"{C.G}📝 Loại: Bài tập{C.E}")
        target_score = get_target_score(False, False)
    
    try:
        # TRÍCH XUẤT THÔNG TIN
        quiz_list, total_questions, id_courseware, id_cate = extract_quiz_info(
            session, assignment['url'], assignment['is_video']
        )
        
        # XỬ LÝ VIDEO
        if assignment['is_video']:
            print_status("Đang xử lý video...", 'video', C.B)
            success = handle_video_submission(session, assignment, user_id, quiz_list, total_questions, id_courseware, id_cate)
            if success:
                print_status(f"{ICONS['success']} HOÀN THÀNH BÀI ({assignment['title']})", 'success', C.G + C.BOLD)
                wait_enter()
            return success
        
        # BÀI TẬP THƯỜNG & LÝ THUYẾT & KIỂM TRA
        if not quiz_list or total_questions == 0:
            print_status("Không thể lấy thông tin bài", 'error', C.R)
            return False
        
        print_status(f"Đang tạo dữ liệu cho {total_questions} câu...", 'clock', C.Y)
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
        print_status("Đang nộp bài...", 'upload', C.Y)
        
        submit_headers = HEADERS.copy()
        submit_headers['x-csrf-token'] = csrf_token
        
        response = session.post(
            'https://olm.vn/course/teacher-static',
            data=payload,
            headers=submit_headers,
            timeout=15
        )
        
        print_status(f"Phản hồi: HTTP {response.status_code}", 'info', C.W)
        
        # XỬ LÝ KẾT QUẢ
        success = handle_submission_response(response, target_score)
        
        if success:
            print_status(f"{ICONS['success']} HOÀN THÀNH BÀI ({assignment['title']})", 'success', C.G + C.BOLD)
            wait_enter()
        
        return success
            
    except Exception as e:
        print_status(f"Lỗi: {str(e)}", 'error', C.R)
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
        print_status(f"Thử phương pháp {i} cho video...", 'video', C.B)
        success = method(session, assignment, user_id, quiz_list, total_questions, id_courseware, id_cate)
        if success:
            return True
        time.sleep(1)  # Chờ giữa các phương pháp
    
    print_status("Tất cả phương pháp đều thất bại", 'error', C.R)
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
                    print_status(f"Đã nộp trước: {result.get('message', '')}", 'warning', C.Y)
                    return True
                elif result['code'] == 400:
                    print_status(f"Lỗi 400: {result.get('message', '')}", 'error', C.R)
                    return False
                else:
                    actual_score = result.get('score', target_score)
                    print_status(f"Thành công! Điểm: {actual_score}/100", 'success', C.G)
                    return True
            else:
                print_status("Nộp thành công (status 200)", 'success', C.G)
                return True
        except Exception as e:
            if "success" in response.text.lower() or "hoàn thành" in response.text.lower():
                print_status("Có vẻ đã thành công", 'success', C.G)
                return True
            print_status("Nộp thành công (status 200)", 'success', C.G)
            return True
    elif response.status_code == 403:
        print_status("Bài đã được nộp trước đó", 'warning', C.Y)
        return True
    else:
        print_status(f"Lỗi {response.status_code}", 'error', C.R)
        return False

# ========== GIẢI BÀI CỤ THỂ TỪ DANH SÁCH ==========
def solve_from_list(session, user_id):
    """Giải bài cụ thể từ danh sách"""
    print_header("GIẢI BÀI CỦA BẠN")
    
    # Hỏi số trang
    pages_input = input(f"{C.Y}Số trang cần quét (mặc định: 3): {C.E}").strip()
    pages_to_scan = 3
    if pages_input.isdigit() and int(pages_input) > 0:
        pages_to_scan = int(pages_input)
    
    assignments = get_assignments_fixed(session, pages_to_scan)
    if not assignments:
        wait_enter()
        return
    
    display_assignments_table(assignments)
    
    # Chọn bài
    print_status("Chọn bài để giải:", 'info', C.C)
    print_status("  Nhập '0' để giải tất cả", 'info', C.C)
    print_status("  Nhập '1,3,5' để giải nhiều bài", 'info', C.C)
    print_status("  Nhập '1' để giải 1 bài", 'info', C.C)
    
    choice = input(f"\n{C.Y}Chọn: {C.E}").strip()
    
    if choice == '0':
        # Giải tất cả
        selected_assignments = assignments
    elif ',' in choice:
        # Giải nhiều bài
        try:
            indices = [int(x.strip()) for x in choice.split(',')]
            selected_assignments = []
            for idx in indices:
                if 1 <= idx <= len(assignments):
                    selected_assignments.append(assignments[idx - 1])
        except:
            print_status("Lựa chọn không hợp lệ!", 'error', C.R)
            wait_enter()
            return
    else:
        # Giải 1 bài
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(assignments):
                selected_assignments = [assignments[idx]]
            else:
                print_status("Số bài không hợp lệ!", 'error', C.R)
                wait_enter()
                return
        except:
            print_status("Lựa chọn không hợp lệ!", 'error', C.R)
            wait_enter()
            return
    
    if not selected_assignments:
        print_status("Không có bài nào được chọn!", 'error', C.R)
        wait_enter()
        return
    
    # Chọn điểm
    print_status("Chọn điểm số:", 'info', C.C)
    print_menu("ĐIỂM SỐ", [
        f"{C.Y}1{C.E}. {ICONS['star']} 100 điểm (Xuất sắc)",
        f"{C.Y}2{C.E}. {ICONS['info']} Tùy chọn điểm số"
    ])
    
    target_score = 100
    score_choice = input(f"\n{C.Y}Chọn (1-2): {C.E}").strip()
    
    if score_choice == '2':
        try:
            score = int(input(f"{C.Y}Nhập điểm số (0-100): {C.E}").strip())
            if 0 <= score <= 100:
                target_score = score
            else:
                print_status("Điểm số phải từ 0 đến 100!", 'error', C.R)
                wait_enter()
                return
        except ValueError:
            print_status("Vui lòng nhập số hợp lệ!", 'error', C.R)
            wait_enter()
            return
    
    # Xác nhận
    print_status(f"Sẽ giải {len(selected_assignments)} bài với {target_score} điểm", 'warning', C.Y)
    confirm = input(f"{C.Y}Xác nhận? (y/n): {C.E}").strip().lower()
    
    if confirm != 'y':
        print_status("Đã hủy", 'warning', C.Y)
        wait_enter()
        return
    
    # Giải bài
    success_count = 0
    total_count = len(selected_assignments)
    
    for i, assignment in enumerate(selected_assignments, 1):
        print_status(f"Bài {i}/{total_count}: {assignment['title']}", 'info', C.C)
        
        success = submit_assignment(session, assignment, user_id)
        
        if success:
            success_count += 1
            
            # Trừ lượt (chỉ khi thành công)
            if not use_credit(assignment):
                # Hết lượt
                print_status("Hết lượt!", 'error', C.R)
                break
        else:
            print_status("Thất bại!", 'error', C.R)
        
        # Chờ giữa các bài
        if i < total_count:
            wait_time = random.randint(2, 5)
            print_status(f"Chờ {wait_time}s...", 'clock', C.Y)
            time.sleep(wait_time)
    
    # Kết quả
    print_box("KẾT QUẢ", [f"Hoàn thành: {success_count}/{total_count} bài"], C.G)
    
    wait_enter()

# ========== GIẢI BÀI TỪ LINK ==========
def solve_from_link(session, user_id):
    """Giải bài từ link"""
    print_header("GIẢI BÀI TỪ LINK")
    
    print(f"{C.C}{ICONS['link']} NHẬP LINK BÀI TẬP:{C.E}")
    print("Ví dụ: https://olm.vn/chu-de/...")
    print()
    
    url = input(f"{ICONS['link']} {C.Y}Dán link bài tập: {C.E}").strip()
    
    if not url.startswith('https://olm.vn/'):
        print_status("Link không hợp lệ! Phải là link OLM", 'error', C.R)
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
        
        print(f"\n{C.C}📋 THÔNG TIN BÀI TẬP:{C.E}")
        print(f"  {C.W}📖 Link: {url}{C.E}")
        print(f"  {C.C}📝 Loại: {assignment['type']}{C.E}")
        
        confirm = input(f"\n{C.Y}Xác nhận giải bài này? (y/n): {C.E}").strip().lower()
        
        if confirm == 'y':
            success = submit_assignment(session, assignment, user_id)
            
            if success:
                # Trừ lượt
                use_credit(assignment)
            
            wait_enter()
            return success
        else:
            print_status("Đã hủy", 'warning', C.Y)
            wait_enter()
            return False
            
    except Exception as e:
        print_status(f"Lỗi: {str(e)}", 'error', C.R)
        wait_enter()
        return False

# ========== ĐỔI TÀI KHOẢN ==========
def change_account():
    """Đổi tài khoản"""
    try:
        lock_file = os.environ.get('OLM_LOCK_FILE', '.lock')
        if os.path.exists(lock_file):
            os.remove(lock_file)
    except:
        pass
    
    print_box("ĐỔI TÀI KHOẢN", [
        "Vui lòng khởi động lại launcher để đăng nhập tài khoản mới"
    ], C.Y)
    
    wait_enter()
    
    # Thoát
    sys.exit(0)

# ========== XỬ LÝ HẾT LƯỢT ==========
def handle_no_credits():
    """Xử lý khi hết lượt"""
    print_box("HẾT LƯỢT", [
        f"{ICONS['warning']} Bạn đã hết lượt sử dụng",
        f"{ICONS['info']} Vui lòng lấy key mới để tiếp tục"
    ], C.Y)
    
    print_menu("LỰA CHỌN", [
        f"{C.Y}1{C.E}. Quay launcher lấy key mới",
        f"{C.Y}2{C.E}. Thoát"
    ])
    
    choice = input(f"\n{C.Y}Chọn (1-2): {C.E}").strip()
    
    if choice == '1':
        print_status("Khởi động lại launcher...", 'info', C.C)
        time.sleep(1)
        sys.exit(0)
    else:
        print_status("Cảm ơn đã sử dụng!", 'success', C.G)
        time.sleep(1)
        sys.exit(0)

# ========== MENU CHÍNH ==========
def main_menu(session, user_id, user_name):
    """Menu chính"""
    
    while True:
        print_header()
        
        # Hiển thị thông tin user và lượt
        credits = get_remaining_credits()
        if credits == -1:
            credit_info = f"{C.G}{ICONS['crown']} VIP Unlimited{C.E}"
        else:
            credit_info = f"{C.C}{ICONS['diamond']} {credits} lượt{C.E}"
        
        print_box(f"Xin chào: {user_name}", [credit_info], C.B)
        
        # Menu
        print_menu("MENU CHÍNH", [
            f"{C.Y}1{C.E}. {ICONS['brain']} Giải bài cụ thể",
            f"{C.Y}2{C_E}. {ICONS['link']} Giải từ link",
            f"{C.Y}3{C_E}. {ICONS['refresh']} Đổi tài khoản",
            f"{C.Y}4{C_E}. {ICONS['exit']} Thoát"
        ])
        
        choice = input(f"\n{C.Y}Chọn (1-4): {C_E}").strip()
        
        # Kiểm tra lượt trước khi làm bài
        if choice in ['1', '2']:
            credits = get_remaining_credits()
            if credits == 0:
                handle_no_credits()
                continue
        
        if choice == '1':
            solve_from_list(session, user_id)
        
        elif choice == '2':
            solve_from_link(session, user_id)
        
        elif choice == '3':
            change_account()
        
        elif choice == '4':
            print_status("Cảm ơn đã sử dụng!", 'success', C.G)
            time.sleep(1)
            sys.exit(0)
        
        else:
            print_status("Lựa chọn không hợp lệ!", 'error', C.R)
            time.sleep(1)

# ========== MAIN ==========
def main():
    """Hàm chính"""
    # Anti-debug
    if hasattr(sys, 'gettrace') and sys.gettrace():
        sys.exit(0)
    
    # Tải session
    session, user_id, user_name = load_session()
    
    if not session or not user_id:
        print_status("Không tìm thấy session! Vui lòng chạy launcher", 'error', C.R)
        wait_enter()
        return
    
    # Lấy thông tin user
    if not user_name:
        try:
            check_res = session.get("https://olm.vn/thong-tin-tai-khoan/info", timeout=10)
            match = re.search(r'name="name".*?value="(.*?)"', check_res.text)
            if match:
                user_name = match.group(1).strip()
            else:
                user_name = "User"
        except:
            user_name = "User"
    
    # Vào menu chính
    main_menu(session, user_id, user_name)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{C.Y}{ICONS['exit']} Đã dừng chương trình{C.E}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{C.R}{ICONS['error']} Lỗi: {str(e)}{C_E}")
        wait_enter()
