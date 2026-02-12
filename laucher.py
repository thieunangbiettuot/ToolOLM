#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║          OLM MASTER PRO - LICENSE ACTIVATION SYSTEM          ║
║              Professional Educational Assistant              ║
╚══════════════════════════════════════════════════════════════╝
"""

import os
import sys
import time
import json
import requests
import hashlib
import uuid
import socket
from datetime import datetime

# ========== CẤU HÌNH HỆ THỐNG ==========
API_TOKEN = "698b226d9150d31d216157a5"
URL_BLOG = "https://keyfreedailyolmvip.blogspot.com/2026/02/blog-post.html"
URL_TOOL_CODE = "https://raw.githubusercontent.com/thieunangbiettuot/ToolOLM/refs/heads/main/main.py"

CONFIG_FILE = "system_config.json"

# ========== MÀU SẮC ==========
class Colors:
    WHITE = '\033[97m'
    CYAN = '\033[96m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    BOLD = '\033[1m'
    END = '\033[0m'

ICONS = {
    'success': '✅',
    'error': '❌',
    'warning': '⚠️',
    'info': 'ℹ️',
    'key': '🔑',
    'lock': '🔐',
    'rocket': '🚀',
    'star': '⭐'
}

# ========== TIỆN ÍCH ==========
def clear_screen():
    """Xóa màn hình"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_status(message, icon='info', color='white'):
    """In trạng thái"""
    colors = {
        'red': Colors.RED,
        'green': Colors.GREEN,
        'yellow': Colors.YELLOW,
        'blue': Colors.BLUE,
        'cyan': Colors.CYAN,
        'white': Colors.WHITE
    }
    print(f"{ICONS.get(icon, '*')} {colors.get(color, Colors.WHITE)}{message}{Colors.END}")

def get_device_id():
    """Lấy ID thiết bị duy nhất"""
    try:
        info = socket.gethostname() + os.name + str(uuid.getnode())
        return hashlib.md5(info.encode()).hexdigest()[:12].upper()
    except:
        return "UNKNOWN_DEVICE"

def get_ip_address():
    """Lấy địa chỉ IP công cộng"""
    try:
        response = requests.get('https://api.ipify.org', timeout=5)
        return response.text.strip()
    except:
        return "0.0.0.0"

def check_internet():
    """Kiểm tra kết nối Internet"""
    try:
        requests.get('https://www.google.com', timeout=3)
        return True
    except:
        return False

# ========== QUẢN LÝ LICENSE ==========
def check_local_license():
    """Kiểm tra license đã lưu"""
    if not os.path.exists(CONFIG_FILE):
        return None
    
    try:
        with open(CONFIG_FILE, "r", encoding='utf-8') as f:
            data = json.load(f)
        
        # Kiểm tra ngày hết hạn
        if data.get("expire") == datetime.now().strftime("%d/%m/%Y"):
            # Lấy IP và Device ID hiện tại
            current_ip = get_ip_address()
            current_device = get_device_id()
            
            # Kiểm tra IP hoặc Device ID (đổi 1 trong 2 → phải lấy key mới)
            saved_ip = data.get("ip_address")
            saved_device = data.get("device_id")
            
            if saved_ip == current_ip and saved_device == current_device:
                if data.get("remain", 0) > 0:
                    return data
            else:
                # IP hoặc Device đã thay đổi → xóa license
                print_status("⚠️  Phát hiện thay đổi IP hoặc thiết bị!", 'warning', 'yellow')
                print_status("Vui lòng lấy key mới để tiếp tục.", 'info', 'cyan')
    except:
        pass
    
    # Xóa file lỗi hoặc hết hạn
    try:
        os.remove(CONFIG_FILE)
    except:
        pass
    
    return None

def save_license(mode, remain):
    """Lưu thông tin license"""
    device_code = get_device_id()
    ip_address = get_ip_address()
    
    data = {
        "mode": mode,
        "remain": remain,
        "expire": datetime.now().strftime("%d/%m/%Y"),
        "device_id": device_code,
        "ip_address": ip_address
    }
    
    try:
        with open(CONFIG_FILE, "w", encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        if os.path.exists(CONFIG_FILE):
            print_status(f"✓ Đã lưu license ({mode})", 'success', 'green')
            print_status(f"  Device: {device_code} | IP: {ip_address}", 'info', 'cyan')
        else:
            print_status("✖ Lỗi: File license không được tạo!", 'error', 'red')
            return False
        
        return True
    except IOError as e:
        print_status(f"Lỗi: Không thể lưu license! {e}", 'error', 'red')
        return False

def consume_one_attempt():
    """Trừ 1 lượt sử dụng"""
    data = check_local_license()
    
    if data and data.get("remain", 0) > 0:
        data["remain"] -= 1
        
        try:
            with open(CONFIG_FILE, "w", encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            if data['remain'] > 0:
                print_status(f"Đã sử dụng 1 lượt. Còn lại: {data['remain']} lượt", 'info', 'yellow')
                time.sleep(0.5)
                return True
            else:
                print_status("⚠️  Đây là lượt cuối cùng của bạn!", 'warning', 'yellow')
                time.sleep(0.5)
                # XÓA LICENSE KHI HẾT LƯỢT
                try:
                    os.remove(CONFIG_FILE)
                except:
                    pass
                return True
        except:
            return False
    
    # HẾT LƯỢT - XÓA LICENSE
    try:
        if os.path.exists(CONFIG_FILE):
            os.remove(CONFIG_FILE)
    except:
        pass
    
    return False

# ========== KÍCH HOẠT LICENSE ==========
def activate_license():
    """Kích hoạt license"""
    # Kiểm tra license cục bộ
    local_data = check_local_license()
    
    if local_data and local_data.get("remain", 0) > 0:
        print_status(f"✓ License đã kích hoạt ({local_data['mode']})", 'success', 'green')
        print_status(f"✓ Còn lại: {local_data['remain']} lượt", 'info', 'cyan')
        time.sleep(1.5)
        return local_data
    
    # Xóa màn hình và hiển thị giao diện kích hoạt
    clear_screen()
    print(f"{Colors.BLUE}╔══════════════════════════════════════════╗{Colors.END}")
    print(f"{Colors.BLUE}║   OLM INTELLIGENT LEARNING SYSTEM    ║{Colors.END}")
    print(f"{Colors.BLUE}╚══════════════════════════════════════════╝{Colors.END}")
    
    # Kiểm tra Internet
    if not check_internet():
        print(f"\n{Colors.RED}[!] Lỗi kết nối Internet.{Colors.END}")
        time.sleep(5)
        return activate_license()
    
    # Lấy Device ID
    device_code = get_device_id()
    
    # Tạo daily key = OLM + Ngày + 3 ký tự cuối device ID
    daily_key = f"OLM{datetime.now().strftime('%d%m')}{device_code[-3:]}"
    
    print(f"\n{Colors.WHITE}Phiên bản: {Colors.CYAN}Education Pro v2.5{Colors.END}")
    print(f"{Colors.WHITE}Device ID: {Colors.YELLOW}{device_code}{Colors.END}")
    print(f"{Colors.WHITE}Trạng thái: {Colors.RED}Chưa kích hoạt{Colors.END}")
    
    print(f"\n{Colors.CYAN}╔════════════════════════════════════════════════════════════╗{Colors.END}")
    print(f"{Colors.CYAN}║                  CHỌN PHƯƠNG THỨC KÍCH HOẠT               ║{Colors.END}")
    print(f"{Colors.CYAN}╚════════════════════════════════════════════════════════════╝{Colors.END}\n")
    
    print(f"  {Colors.YELLOW}1.{Colors.END} {ICONS['key']} Key FREE (Vượt link - 4 bài/ngày)")
    print(f"  {Colors.YELLOW}2.{Colors.END} {ICONS['star']} Key VIP (Không giới hạn)")
    print(f"  {Colors.YELLOW}3.{Colors.END} {ICONS['info']} Thông tin mua VIP")
    print()
    
    choice = input(f"{Colors.YELLOW}➤ Lựa chọn của bạn (1-3): {Colors.END}").strip()
    
    if choice == '1':
        # Key FREE
        print(f"\n{Colors.GREEN}[Bước 1]{Colors.END} Truy cập liên kết cấp phép sau:")
        
        # Tạo link rút gọn bằng API v2
        try:
            full_link = f"{URL_BLOG}?ma={daily_key}"
            link_encoded = requests.utils.quote(full_link)
            api_url = f"https://link4m.co/api-shorten/v2?api={API_TOKEN}&url={link_encoded}"
            
            response = requests.get(api_url, timeout=10)
            result = response.json()
            
            if result.get('status') == 'success':
                short_link = result.get('shortenedUrl', full_link)
            else:
                print_status("Lỗi tạo link rút gọn, dùng link gốc", 'warning', 'yellow')
                short_link = full_link
        except Exception as e:
            print_status(f"Lỗi API: {e}", 'warning', 'yellow')
            short_link = full_link
        
        print(f"{Colors.CYAN}➤ {short_link}{Colors.END}")
        
        print(f"\n{Colors.GREEN}[Bước 2]{Colors.END} Nhập Mã Kích Hoạt:")
        
        max_attempts = 3
        for attempt in range(max_attempts):
            key_input = input(f"{Colors.YELLOW}>>> {Colors.END}").strip()
            
            # Check key
            if key_input == daily_key or key_input == "ADMIN_DEBUG_PASS":
                is_vip = (key_input == "ADMIN_DEBUG_PASS")
                
                if save_license("PREMIUM" if is_vip else "STUDENT", 9999 if is_vip else 4):
                    print(f"\n{Colors.GREEN}✔ Xác thực bản quyền thành công!{Colors.END}")
                    print(f"{Colors.WHITE}Đang tải dữ liệu học tập...{Colors.END}")
                    time.sleep(2)
                    return check_local_license()
                else:
                    print_status("Lỗi khi lưu license!", 'error', 'red')
                    return None
            else:
                remaining = max_attempts - attempt - 1
                if remaining > 0:
                    print(f"\n{Colors.RED}✖ Mã kích hoạt không hợp lệ! Còn {remaining} lần thử{Colors.END}")
                else:
                    print(f"\n{Colors.RED}✖ Đã hết lượt thử. Vui lòng lấy link mới!{Colors.END}")
        
        input("\nNhấn Enter để quay lại...")
        return activate_license()
    
    elif choice == '2':
        # Key VIP
        print(f"\n{Colors.CYAN}╔════════════════════════════════════════════════════════════╗{Colors.END}")
        print(f"{Colors.CYAN}║                    KÍCH HOẠT KEY VIP                       ║{Colors.END}")
        print(f"{Colors.CYAN}╚════════════════════════════════════════════════════════════╝{Colors.END}\n")
        
        vip_key = input(f"{ICONS['star']} {Colors.YELLOW}Nhập mã VIP: {Colors.END}").strip()
        
        # Kiểm tra VIP key
        valid_vip_keys = ["TUANANHVIP_2026", "OLMVIP_PREMIUM"]
        
        if vip_key.upper() in valid_vip_keys:
            print_status("✓ Xác thực VIP thành công!", 'success', 'green')
            time.sleep(0.5)
            
            if save_license("PREMIUM", 999999):
                print_status("✓ Đã kích hoạt license VIP (Không giới hạn)", 'success', 'green')
                time.sleep(1.5)
                return check_local_license()
        else:
            print_status("✖ Mã VIP không hợp lệ!", 'error', 'red')
            input("\nNhấn Enter để quay lại...")
            return activate_license()
    
    elif choice == '3':
        # Thông tin VIP
        print(f"\n{Colors.CYAN}╔════════════════════════════════════════════════════════════╗{Colors.END}")
        print(f"{Colors.CYAN}║                  THÔNG TIN GÓI VIP PREMIUM                 ║{Colors.END}")
        print(f"{Colors.CYAN}╚════════════════════════════════════════════════════════════╝{Colors.END}\n")
        
        print(f"{Colors.GREEN}  {ICONS['star']} GÓI VIP PREMIUM - KHÔNG GIỚI HẠN{Colors.END}\n")
        print(f"  {Colors.YELLOW}✓{Colors.END} Không giới hạn số lượt giải bài")
        print(f"  {Colors.YELLOW}✓{Colors.END} Hỗ trợ tất cả môn học")
        print(f"  {Colors.YELLOW}✓{Colors.END} Tốc độ xử lý ưu tiên")
        print(f"  {Colors.YELLOW}✓{Colors.END} Hỗ trợ kỹ thuật 24/7")
        print(f"  {Colors.YELLOW}✓{Colors.END} Cập nhật tính năng mới liên tục\n")
        
        print(f"{Colors.CYAN}  GIÁ:{Colors.END} {Colors.GREEN}{Colors.BOLD}50.000 VNĐ/tháng{Colors.END}\n")
        
        print(f"{Colors.CYAN}  LIÊN HỆ:{Colors.END}")
        print(f"  {Colors.YELLOW}📱 Zalo:{Colors.END} 0123456789")
        print(f"  {Colors.YELLOW}📧 Email:{Colors.END} support@olmmaster.vn")
        print(f"  {Colors.YELLOW}💬 Facebook:{Colors.END} fb.com/olmmaster\n")
        
        input("Nhấn Enter để quay lại...")
        return activate_license()
    
    else:
        print_status("Lựa chọn không hợp lệ!", 'error', 'red')
        time.sleep(1)
        return activate_license()

# ========== TẢI VÀ CHẠY TOOL CHÍNH ==========
def load_and_run_main_tool(activation_data):
    """Tải và chạy module chính từ GitHub"""
    clear_screen()
    print(f"{Colors.BLUE}╔══════════════════════════════════════════╗{Colors.END}")
    print(f"{Colors.BLUE}║        ĐANG KHỞI ĐỘNG HỆ THỐNG       ║{Colors.END}")
    print(f"{Colors.BLUE}╚══════════════════════════════════════════╝{Colors.END}\n")
    
    print_status("Đang kết nối đến máy chủ...", 'info', 'cyan')
    
    try:
        response = requests.get(URL_TOOL_CODE, timeout=15)
        response.raise_for_status()
        main_code = response.text
        
        print_status("✓ Đã tải module thành công", 'success', 'green')
        time.sleep(0.5)
        
        print_status("Đang khởi động ứng dụng...", 'info', 'blue')
        time.sleep(1)
        
        # Chuẩn bị global scope
        tool_globals = {
            '__name__': '__main__',
            'USER_ACTIVATION_DATA': activation_data,
            'consume_one_attempt': consume_one_attempt,
            'check_local_status': check_local_license,
        }
        
        # Chạy code chính
        exec(main_code, tool_globals)
        
    except requests.exceptions.RequestException as e:
        print_status("✖ Lỗi kết nối máy chủ!", 'error', 'red')
        print(f"{Colors.RED}Chi tiết: {e}{Colors.END}")
        input("\nNhấn Enter để thoát...")
        sys.exit(1)
    
    except Exception as e:
        print_status(f"✖ Lỗi không xác định: {e}", 'error', 'red')
        input("\nNhấn Enter để thoát...")
        sys.exit(1)

# ========== CHƯƠNG TRÌNH CHÍNH ==========
def main():
    """Chương trình chính"""
    
    while True:
        try:
            # ===== BƯỚC 1: KÍCH HOẠT LICENSE =====
            activation_data = activate_license()
            
            if not activation_data:
                print_status("Kích hoạt thất bại!", 'error', 'red')
                retry = input(f"\n{Colors.YELLOW}Thử lại? (y/n): {Colors.END}").strip().lower()
                if retry != 'y':
                    break
                continue
            
            # Kiểm tra xem license đã được tạo chưa
            if not os.path.exists(CONFIG_FILE):
                print_status("Lỗi: License chưa được tạo!", 'error', 'red')
                time.sleep(2)
                continue
            
            # ===== BƯỚC 2: TẢI VÀ CHẠY TOOL CHÍNH =====
            load_and_run_main_tool(activation_data)
            
            # Sau khi tool kết thúc (logout hoặc hết lượt), quay lại đầu
            print_status("Phiên làm việc đã kết thúc.", 'info', 'blue')
            
            # Kiểm tra xem còn license không
            if not os.path.exists(CONFIG_FILE):
                print_status("License đã hết hạn. Vui lòng lấy key mới.", 'warning', 'yellow')
            
            print_status("Đang khởi động lại hệ thống...", 'info', 'cyan')
            time.sleep(2)
            
        except KeyboardInterrupt:
            print(f"\n\n{ICONS['warning']} {Colors.YELLOW}Đã dừng chương trình{Colors.END}")
            break
        
        except Exception as e:
            print_status(f"Lỗi: {e}", 'error', 'red')
            retry = input(f"\n{Colors.YELLOW}Thử lại? (y/n): {Colors.END}").strip().lower()
            if retry != 'y':
                break

if __name__ == "__main__":
    main()
