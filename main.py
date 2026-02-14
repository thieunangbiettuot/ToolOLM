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
import pickle
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

def print_centered(text, color=Colors.WHITE, width=60):
    padding = (width - len(text.strip())) // 2
    print(f"{color}{' ' * padding}{text}{Colors.END}")

def print_line(char='═', color=Colors.CYAN, width=60):
    print(f"{color}{char * width}{Colors.END}")

def print_header(title=""):
    clear_screen()
    print_line('═', Colors.BLUE, 60)
    print_centered("🎯 OLM MASTER PRO - MAIN 🎯", Colors.BLUE + Colors.BOLD, 60)
    print_centered("Premium Auto Solver Tool", Colors.PURPLE, 60)
    if title:
        print_line('─', Colors.CYAN, 60)
        print_centered(title, Colors.CYAN, 60)
    print_line('═', Colors.BLUE, 60)
    print()

def print_menu(title, options):
    print(f"\n{Colors.CYAN}{ICONS['setting']} {title}{Colors.END}")
    print_line('─', Colors.CYAN, 45)
    for key, value in options.items():
        print(f"  {Colors.YELLOW}{key}.{Colors.END} {value}")
    print_line('─', Colors.CYAN, 45)

def wait_enter(prompt="Press Enter to continue..."):
    input(f"\n{Colors.YELLOW}{prompt}{Colors.END}")

def print_status(message, icon='info', color=Colors.WHITE):
    print(f"{ICONS.get(icon, '')} {color}{message}{Colors.END}")

# ========== PHẦN QUÉT BÀI TẬP ==========
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'vi-VN,vi;q=0.9,en-US;q=0.8',
    'x-requested-with': 'XMLHttpRequest',
    'origin': 'https://olm.vn',
    'referer': 'https://olm.vn/'
}

def get_assignments_fixed(session, pages_to_scan=3):
    print_header(f"SCANNING ASSIGNMENTS ({pages_to_scan} pages)")
    
    assignments = []
    seen_links = set()
    
    try:
        for page in range(1, pages_to_scan + 1):
            if page == 1:
                url = "https://olm.vn/lop-hoc-cua-toi?action=login"
            else:
                url = f"https://olm.vn/lop-hoc-cua-toi/page-{page}?action=login"
            
            print_status(f"Scanning page {page}/{pages_to_scan}...", 'search', Colors.YELLOW)
            
            try:
                response = session.get(url, headers=HEADERS, timeout=10)
                
                if response.status_code != 200:
                    print_status(f"HTTP Error {response.status_code}", 'error', Colors.RED)
                    continue
                
                soup = BeautifulSoup(response.text, 'html.parser')
                rows = soup.find_all('tr', class_='my-gived-courseware-item')
                
                if not rows: 
                    print_status(f"Page {page} has no assignments", 'warning', Colors.YELLOW)
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
                        mon_text = mon.get_text(strip=True) if mon else "Other"
                        
                        ten_bai = link_text
                        ten_bai = re.sub(r'\([^)]*\)', '', ten_bai).strip()
                        
                        status = "Not started"
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
                    print_status(f"Page {page}: {page_count} assignments found", 'success', Colors.GREEN)
                else:
                    print_status(f"Page {page}: no assignments found", 'warning', Colors.YELLOW)
                    
            except Exception as e:
                print_status(f"Page {page} error: {str(e)}", 'error', Colors.RED)
                continue
        
        if assignments:
            print_status(f"Total: {len(assignments)} assignments ready", 'success', Colors.GREEN + Colors.BOLD)
            
            video_count = sum(1 for a in assignments if a['is_video'])
            ly_thuyet_count = sum(1 for a in assignments if a['is_ly_thuyet'])
            bai_tap_count = sum(1 for a in assignments if a['is_bai_tap'])
            kiem_tra_count = sum(1 for a in assignments if a['is_kiem_tra'])
            
            print(f"\n{Colors.CYAN}📊 STATISTICS:{Colors.END}")
            if video_count > 0:
                print(f"  {ICONS['video']} Videos: {video_count}")
            if ly_thuyet_count > 0:
                print(f"  {ICONS['theory']} Theory: {ly_thuyet_count}")
            if bai_tap_count > 0:
                print(f"  {ICONS['exercise']} Exercises: {bai_tap_count}")
            if kiem_tra_count > 0:
                print(f"  {ICONS['warning']} Tests: {kiem_tra_count}")
            
            return assignments
        else:
            print_status("No assignments found", 'warning', Colors.YELLOW)
            return []
            
    except Exception as e:
        print_status(f"Scan error: {str(e)}", 'error', Colors.RED)
        return []

def display_assignments_table(assignments):
    if not assignments:
        return
    
    print(f"\n{Colors.PURPLE}{'📚 ASSIGNMENTS READY FOR PROCESSING 📚':^90}{Colors.END}")
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

# ========== PHẦN XỬ LÝ BÀI TẬP (giữ nguyên logic gốc) ==========
def get_target_score(is_video=False, is_kiem_tra=False):
    if is_video:
        print_status("Video: Auto-selecting 100 points", 'video', Colors.BLUE)
        return 100
    elif is_kiem_tra:
        print_status("Test: Auto-selecting high score", 'warning', Colors.YELLOW)
        return random.randint(85, 100)
    
    print(f"\n{Colors.CYAN}{ICONS['star']} SELECT SCORE{Colors.END}")
    print_line('─', Colors.CYAN, 40)
    print(f"  {Colors.YELLOW}1.{Colors.END} {ICONS['star']} 100 points (Perfect)")
    print(f"  {Colors.YELLOW}2.{Colors.END} {ICONS['question']} Custom score")
    print_line('─', Colors.CYAN, 40)
    
    while True:
        choice = input(f"{Colors.YELLOW}Choose (1-2): {Colors.END}").strip()
        
        if choice == '1':
            return 100
        elif choice == '2':
            try:
                score = int(input(f"{Colors.YELLOW}Enter score (0-100): {Colors.END}").strip())
                if 0 <= score <= 100:
                    return score
                else:
                    print_status("Score must be 0-100!", 'error', Colors.RED)
            except ValueError:
                print_status("Please enter a valid number!", 'error', Colors.RED)
        else:
            print_status("Invalid choice!", 'error', Colors.RED)

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
                print_status("Video: No quiz_list, trying alternative method", 'video', Colors.BLUE)
                return "", 0, id_courseware, id_cate
            else:
                print_status("No question list found", 'error', Colors.RED)
                return None, 0, id_courseware, id_cate
        
        question_ids = [qid.strip() for qid in quiz_list.split(',') if qid.strip()]
        total_questions = len(question_ids)
        
        print_status(f"Found {total_questions} questions", 'info', Colors.WHITE)
        
        return quiz_list, total_questions, id_courseware, id_cate
        
    except Exception as e:
        print_status(f"Info extraction error: {str(e)}", 'error', Colors.RED)
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

def submit_assignment(session, assignment, user_id):
    print(f"\n{Colors.CYAN}{ICONS['upload']} PROCESSING:{Colors.END}")
    print(f"{Colors.WHITE}📖 {assignment['title']}{Colors.END}")
    
    if assignment['is_video']:
        print(f"{Colors.BLUE}🎬 Type: Video{Colors.END}")
        target_score = 100
    elif assignment['is_ly_thuyet']:
        print(f"{Colors.CYAN}📚 Type: Theory{Colors.END}")
        target_score = get_target_score(False, False)
    elif assignment['is_kiem_tra']:
        print(f"{Colors.YELLOW}⚠️ Type: Test{Colors.END}")
        target_score = get_target_score(False, True)
    else:
        print(f"{Colors.GREEN}📝 Type: Exercise{Colors.END}")
        target_score = get_target_score(False, False)
    
    try:
        quiz_list, total_questions, id_courseware, id_cate = extract_quiz_info(
            session, assignment['url'], assignment['is_video']
        )
        
        if assignment['is_video']:
            print_status("Processing video...", 'video', Colors.BLUE)
            success = handle_video_submission(session, assignment, user_id, quiz_list, total_questions, id_courseware, id_cate)
            if success:
                print_status(f"{ICONS['success']} COMPLETED ({assignment['title']})", 'success', Colors.GREEN + Colors.BOLD)
                wait_enter()
            return success
        
        if not quiz_list or total_questions == 0:
            print_status("Cannot get assignment info", 'error', Colors.RED)
            return False
        
        print_status(f"Creating data for {total_questions} questions...", 'clock', Colors.YELLOW)
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
        
        print_status("Submitting assignment...", 'upload', Colors.YELLOW)
        
        submit_headers = HEADERS.copy()
        submit_headers['x-csrf-token'] = csrf_token
        
        response = session.post(
            'https://olm.vn/course/teacher-static',
            data=payload,
            headers=submit_headers,
            timeout=15
        )
        
        print_status(f"Response: HTTP {response.status_code}", 'info', Colors.WHITE)
        
        success = handle_submission_response(response, target_score)
        
        if success:
            print_status(f"{ICONS['success']} COMPLETED ({assignment['title']})", 'success', Colors.GREEN + Colors.BOLD)
            wait_enter()
        
        return success
            
    except Exception as e:
        print_status(f"Error: {str(e)}", 'error', Colors.RED)
        return False

def handle_video_submission(session, assignment, user_id, quiz_list, total_questions, id_courseware, id_cate):
    methods = [
        try_video_simple_method,
        try_video_with_quiz,
        try_video_complex_method,
    ]
    
    for i, method in enumerate(methods, 1):
        print_status(f"Trying method {i} for video...", 'video', Colors.BLUE)
        success = method(session, assignment, user_id, quiz_list, total_questions, id_courseware, id_cate)
        if success:
            return True
        time.sleep(1)
    
    print_status("All methods failed", 'error', Colors.RED)
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
        
    except Exception as e:
        return False

def handle_submission_response(response, target_score):
    if response.status_code == 200:
        try:
            result = response.json()
            
            if 'code' in result:
                if result['code'] == 403:
                    print_status(f"Already submitted: {result.get('message', '')}", 'warning', Colors.YELLOW)
                    return True
                elif result['code'] == 400:
                    print_status(f"Error 400: {result.get('message', '')}", 'error', Colors.RED)
                    return False
                else:
                    actual_score = result.get('score', target_score)
                    print_status(f"Success! Score: {actual_score}/100", 'success', Colors.GREEN)
                    return True
            else:
                print_status("Submission successful (status 200)", 'success', Colors.GREEN)
                return True
        except Exception as e:
            if "success" in response.text.lower() or "hoàn thành" in response.text.lower():
                print_status("Seems successful", 'success', Colors.GREEN)
                return True
            print_status("Submission successful (status 200)", 'success', Colors.GREEN)
            return True
    elif response.status_code == 403:
        print_status("Assignment already submitted", 'warning', Colors.YELLOW)
        return True
    else:
        print_status(f"Error {response.status_code}", 'error', Colors.RED)
        return False

# ========== GIẢI BÀI TỪ LINK ==========
def solve_from_link(session, user_id):
    print_header("SOLVE FROM LINK")
    
    print(f"{Colors.CYAN}{ICONS['link']} ENTER ASSIGNMENT LINK:{Colors.END}")
    print("Example: https://olm.vn/chu-de/...")
    print()
    
    url = input(f"{ICONS['link']} {Colors.YELLOW}Paste assignment link: {Colors.END}").strip()
    
    if not url.startswith('https://olm.vn/'):
        print_status("Invalid link! Must be OLM link", 'error', Colors.RED)
        wait_enter()
        return False
    
    try:
        resp = session.get(url, timeout=10)
        is_video = 'video' in url.lower() or '[Video]' in resp.text
        is_ly_thuyet = 'ly-thuyet' in url.lower() or 'lý-thuyết' in url.lower() or '[Lý thuyết]' in resp.text
        
        assignment = {
            'title': "Assignment from link",
            'subject': "Custom",
            'type': "Exercise",
            'status': "Not started",
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
            assignment['type'] = "Theory"
        
        print(f"\n{Colors.CYAN}📋 ASSIGNMENT INFO:{Colors.END}")
        print(f"  {Colors.WHITE}📖 Link: {url}{Colors.END}")
        print(f"  {Colors.CYAN}📝 Type: {assignment['type']}{Colors.END}")
        
        confirm = input(f"\n{Colors.YELLOW}Confirm processing? (y/n): {Colors.END}").strip().lower()
        
        if confirm == 'y':
            success = submit_assignment(session, assignment, user_id)
            return success
        else:
            print_status("Cancelled", 'warning', Colors.YELLOW)
            return False
            
    except Exception as e:
        print_status(f"Error: {str(e)}", 'error', Colors.RED)
        return False

# ========== GIẢI BÀI CỤ THỂ MỚI ==========
def solve_specific_assignments(session, user_id, license_data):
    print_header("SOLVE SPECIFIC ASSIGNMENTS")
    
    pages_input = input(f"{Colors.YELLOW}Number of pages to scan (default: 3): {Colors.END}").strip()
    pages_to_scan = 3
    if pages_input.isdigit() and int(pages_input) > 0:
        pages_to_scan = int(pages_input)
    
    assignments = get_assignments_fixed(session, pages_to_scan)
    if not assignments:
        wait_enter()
        return license_data
    
    display_assignments_table(assignments)
    
    try:
        selection = input(f"\n{Colors.YELLOW}Select assignments (0=all, 1,3,5=specific): {Colors.END}").strip()
        
        selected_assignments = []
        if selection == "0":
            selected_assignments = assignments
        elif "," in selection:
            indices = [int(x.strip()) - 1 for x in selection.split(",") if x.strip().isdigit()]
            selected_assignments = [assignments[i] for i in indices if 0 <= i < len(assignments)]
        elif selection.isdigit():
            idx = int(selection) - 1
            if 0 <= idx < len(assignments):
                selected_assignments = [assignments[idx]]
        
        if not selected_assignments:
            print_status("No assignments selected!", 'error', Colors.RED)
            wait_enter()
            return license_data
        
        first_assignment = selected_assignments[0]
        is_video = any(a['is_video'] for a in selected_assignments)
        is_kiem_tra = any(a['is_kiem_tra'] for a in selected_assignments)
        target_score = get_target_score(is_video, is_kiem_tra)
        
        print(f"\n{Colors.CYAN}Confirm processing {len(selected_assignments)} assignments with score {target_score}?{Colors.END}")
        confirm = input(f"{Colors.YELLOW}Continue? (y/n): {Colors.END}").strip().lower()
        if confirm != 'y':
            print_status("Cancelled", 'warning', Colors.YELLOW)
            wait_enter()
            return license_data
        
        success_count = 0
        total_count = len(selected_assignments)
        
        for idx, assignment in enumerate(selected_assignments, 1):
            print(f"\n{Colors.YELLOW}📊 Assignment {idx}/{total_count}: {assignment['title']}{Colors.END}")
            
            success = submit_assignment(session, assignment, user_id)
            
            if success:
                success_count += 1
                if license_data['mode'] == 'FREE':
                    if license_data['remain'] > 0:
                        if assignment['is_ly_thuyet'] or success:
                            license_data['remain'] -= 1
                            print_status(f"{ICONS['diamond']} Remaining: {license_data['remain']} uses", 'info', Colors.CYAN)
            else:
                if assignment['is_ly_thuyet'] and license_data['mode'] == 'FREE' and license_data['remain'] > 0:
                    license_data['remain'] -= 1
                    print_status(f"{ICONS['diamond']} Remaining: {license_data['remain']} uses", 'info', Colors.CYAN)
        
        print(f"\n{Colors.CYAN}{ICONS['star']} RESULTS:{Colors.END}")
        print(f"{Colors.GREEN}Success: {success_count}/{total_count}{Colors.END}")
        
        wait_enter()
        return license_data
        
    except Exception as e:
        print_status(f"Selection error: {str(e)}", 'error', Colors.RED)
        wait_enter()
        return license_data

# ========== MENU CHÍNH ==========
def main_menu(session_data):
    session = session_data['session']
    user_id = session_data['user_id']
    user_name = session_data['user_name']
    license_data = session_data['license']
    
    while True:
        print_header("MAIN MENU")
        print(f"{ICONS['user']} {Colors.GREEN}Welcome: {user_name}{Colors.END}")
        print(f"{ICONS['diamond']} {Colors.CYAN}Remaining uses: {license_data['remain'] if license_data['mode'] == 'FREE' else 'Unlimited'}{Colors.END}")
        print()
        
        menu_options = {
            '1': f"{ICONS['brain']} Solve specific assignments",
            '2': f"{ICONS['link']} Solve from link",
            '3': f"{ICONS['refresh']} Change account",
            '4': f"{ICONS['exit']} Exit"
        }
        
        print_menu("OPTIONS", menu_options)
        
        choice = input(f"\n{Colors.YELLOW}Choose option (1-4): {Colors.END}").strip()
        
        if choice == '1':
            license_data = solve_specific_assignments(session, user_id, license_data)
            
        elif choice == '2':
            solve_from_link(session, user_id)
            
        elif choice == '3':
            print_status("Returning to launcher to change account...", 'refresh', Colors.YELLOW)
            time.sleep(1)
            return 'change_account'
            
        elif choice == '4':
            print_status("Thank you for using!", 'exit', Colors.GREEN)
            time.sleep(1)
            return 'exit'
            
        else:
            print_status("Invalid option!", 'error', Colors.RED)
            time.sleep(1)
        
        if license_data['mode'] == 'FREE' and license_data['remain'] <= 0:
            print(f"\n{Colors.RED}⛔ OUT OF USES{Colors.END}")
            print(f"{Colors.YELLOW}[1] Return to launcher for new key{Colors.END}")
            print(f"{Colors.YELLOW}[2] Exit{Colors.END}")
            sub_choice = input(f"\n{Colors.YELLOW}Choose: {Colors.END}").strip()
            
            if sub_choice == '1':
                return 'get_new_key'
            else:
                return 'exit'

# ========== CHƯƠNG TRÌNH CHÍNH ==========
def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <session_file>")
        sys.exit(1)
    
    session_file = sys.argv[1]
    
    try:
        with open(session_file, 'rb') as f:
            session_data = pickle.load(f)
        
        result = main_menu(session_data)
        
        if result == 'change_account':
            pass
        elif result == 'get_new_key':
            import platform
            import hashlib
            import uuid
            
            def get_appdata_path():
                system = platform.system()
                if system == "Windows":
                    return os.path.join(os.getenv('LOCALAPPDATA', ''), 'Microsoft', 'Windows', 'INetCache', 'IE')
                elif system == "Darwin":
                    return os.path.expanduser('~/Library/Application Support/com.apple.Safari')
                else:
                    if 'ANDROID_ROOT' in os.environ or 'TERMUX_VERSION' in os.environ:
                        return os.path.expanduser('~/.cache/google-chrome')
                    else:
                        return os.path.expanduser('~/.cache/mozilla/firefox')
            
            def get_device_hash():
                mac = uuid.getnode()
                hostname = platform.node()
                return hashlib.md5(f"{mac}{hostname}".encode()).hexdigest()[:16]
            
            appdata = get_appdata_path()
            device_hash = get_device_hash()
            license_file = os.path.join(appdata, f'.{device_hash}sc')
            
            if os.path.exists(license_file):
                os.remove(license_file)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
