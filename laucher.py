#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║                    OLM MASTER PRO v3.0                       ║
║              Professional License Activation                 ║
║                    Powered by AI Technology                  ║
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

# ========== CẤU HÌNH ==========
API_TOKEN = "698b226d9150d31d216157a5"
URL_BLOG = "https://keyfreedailyolmvip.blogspot.com/2026/02/blog-post.html"
URL_MAIN_TOOL = "https://raw.githubusercontent.com/thieunangbiettuot/ToolOLM/refs/heads/main/main.py"

CONFIG_FILE = "olm_license.dat"
ACCOUNT_LOCK_FILE = "olm_account.dat"

# ========== MÀU SẮC & BIỂU TƯỢNG ==========
class Color:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    
    # Gradient colors
    PINK = '\033[38;5;213m'
    ORANGE = '\033[38;5;214m'
    PURPLE = '\033[38;5;141m'

class Icon:
    ROCKET = '🚀'
    STAR = '⭐'
    LOCK = '🔐'
    KEY = '🔑'
    CHECK = '✓'
    CROSS = '✗'
    WARNING = '⚠'
    INFO = 'ℹ'
    ARROW = '➤'
    SPARKLE = '✨'
    SHIELD = '🛡'
    FIRE = '🔥'
    CROWN = '👑'

# ========== TIỆN ÍCH ==========
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_gradient_line(char='═', width=70):
    """In đường kẻ với gradient"""
    colors = [Color.CYAN, Color.BLUE, Color.PURPLE]
    line = ''
    for i in range(width):
        color = colors[i % len(colors)]
        line += f"{color}{char}"
    print(line + Color.END)

def print_box(text, color=Color.CYAN, width=70):
    """In text trong box"""
    padding = (width - len(text) - 4) // 2
    print(f"{color}║{' ' * padding} {text} {' ' * padding}║{Color.END}")

def print_banner():
    """Banner chuyên nghiệp"""
    clear()
    print()
    print(f"{Color.CYAN}{Color.BOLD}")
    print("    ╔═══════════════════════════════════════════════════════════════╗")
    print("    ║                                                               ║")
    print(f"    ║       {Icon.ROCKET}  {Color.PURPLE}OLM MASTER PRO{Color.CYAN} - {Color.PINK}Education Assistant{Color.CYAN}  {Icon.FIRE}      ║")
    print("    ║                                                               ║")
    print(f"    ║              {Color.YELLOW}Professional License Manager v3.0{Color.CYAN}              ║")
    print("    ║                                                               ║")
    print("    ╚═══════════════════════════════════════════════════════════════╝")
    print(Color.END)
    print()

def status(msg, icon=Icon.INFO, color=Color.WHITE):
    print(f"  {icon} {color}{msg}{Color.END}")

def success(msg):
    status(msg, Icon.CHECK, Color.GREEN)

def error(msg):
    status(msg, Icon.CROSS, Color.RED)

def warning(msg):
    status(msg, Icon.WARNING, Color.YELLOW)

def info(msg):
    status(msg, Icon.INFO, Color.CYAN)

# ========== HỆ THỐNG ==========
def get_device_id():
    try:
        data = socket.gethostname() + os.name + str(uuid.getnode())
        return hashlib.md5(data.encode()).hexdigest()[:16].upper()
    except:
        return "DEVICE_UNKNOWN"

def get_ip():
    try:
        return requests.get('https://api.ipify.org?format=json', timeout=5).json()['ip']
    except:
        return "0.0.0.0"

def check_internet():
    try:
        requests.get('https://www.google.com', timeout=3)
        return True
    except:
        return False

# ========== QUẢN LÝ LICENSE ==========
def load_license():
    if not os.path.exists(CONFIG_FILE):
        return None
    try:
        with open(CONFIG_FILE, 'r') as f:
            data = json.load(f)
        
        # Check ngày hết hạn
        if data.get('expire') != datetime.now().strftime("%d/%m/%Y"):
            os.remove(CONFIG_FILE)
            return None
        
        # Check IP + Device
        if data.get('ip') == get_ip() and data.get('device') == get_device_id():
            if data.get('remain', 0) > 0:
                return data
        else:
            warning("Phát hiện thay đổi IP hoặc thiết bị!")
            os.remove(CONFIG_FILE)
        
        return None
    except:
        try:
            os.remove(CONFIG_FILE)
        except:
            pass
        return None

def save_license(mode, remain):
    data = {
        'mode': mode,
        'remain': remain,
        'expire': datetime.now().strftime("%d/%m/%Y"),
        'ip': get_ip(),
        'device': get_device_id(),
        'created': datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }
    
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except:
        return False

def consume_attempt():
    data = load_license()
    if not data:
        return False
    
    data['remain'] -= 1
    
    if data['remain'] <= 0:
        try:
            os.remove(CONFIG_FILE)
            if os.path.exists(ACCOUNT_LOCK_FILE):
                os.remove(ACCOUNT_LOCK_FILE)
        except:
            pass
        return True  # Lượt cuối
    
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except:
        return False

# ========== KÍCH HOẠT ==========
def show_activation_ui():
    print_banner()
    
    device = get_device_id()
    ip = get_ip()
    
    print(f"{Color.CYAN}  ┌─────────────────────────────────────────────────────────────┐{Color.END}")
    print(f"{Color.CYAN}  │{Color.END}  {Color.BOLD}System Information{Color.END}                                          {Color.CYAN}│{Color.END}")
    print(f"{Color.CYAN}  ├─────────────────────────────────────────────────────────────┤{Color.END}")
    print(f"{Color.CYAN}  │{Color.END}  {Icon.SHIELD} Device ID : {Color.YELLOW}{device:<42}{Color.END} {Color.CYAN}│{Color.END}")
    print(f"{Color.CYAN}  │{Color.END}  {Icon.SPARKLE} IP Address: {Color.YELLOW}{ip:<42}{Color.END} {Color.CYAN}│{Color.END}")
    print(f"{Color.CYAN}  │{Color.END}  {Icon.FIRE} Status    : {Color.RED}Chưa kích hoạt{' ' * 34}{Color.END} {Color.CYAN}│{Color.END}")
    print(f"{Color.CYAN}  └─────────────────────────────────────────────────────────────┘{Color.END}")
    print()

def activate_free_key():
    show_activation_ui()
    
    device = get_device_id()
    daily_key = f"OLM{datetime.now().strftime('%d%m')}{device[-3:]}"
    
    print(f"{Color.GREEN}  ╔═════════════════════════════════════════════════════════════╗{Color.END}")
    print(f"{Color.GREEN}  ║{Color.END}              {Icon.KEY} {Color.BOLD}FREE LICENSE ACTIVATION{Color.END}                    {Color.GREEN}║{Color.END}")
    print(f"{Color.GREEN}  ╚═════════════════════════════════════════════════════════════╝{Color.END}")
    print()
    
    info("Đang tạo link kích hoạt...")
    time.sleep(1)
    
    # Tạo link
    try:
        full_url = f"{URL_BLOG}?key={daily_key}"
        encoded = requests.utils.quote(full_url)
        
        # Dùng API shortener đơn giản hơn
        api = f"https://link4m.co/api-shorten/v2"
        payload = {'api': API_TOKEN, 'url': full_url}
        
        resp = requests.post(api, data=payload, timeout=10)
        result = resp.json()
        
        if result.get('status') == 'success':
            short_link = result.get('shortenedUrl')
        else:
            # Fallback
            short_link = full_url
    except:
        short_link = full_url
    
    print()
    print(f"{Color.YELLOW}  ┌───────────────────────────────────────────────────────────┐{Color.END}")
    print(f"{Color.YELLOW}  │{Color.END} {Color.BOLD}BƯỚC 1:{Color.END} Truy cập link để lấy mã kích hoạt               {Color.YELLOW}│{Color.END}")
    print(f"{Color.YELLOW}  ├───────────────────────────────────────────────────────────┤{Color.END}")
    print(f"{Color.YELLOW}  │{Color.END} {Icon.ARROW} {Color.CYAN}{short_link:<54}{Color.END}{Color.YELLOW}│{Color.END}")
    print(f"{Color.YELLOW}  └───────────────────────────────────────────────────────────┘{Color.END}")
    print()
    
    print(f"{Color.YELLOW}  ┌───────────────────────────────────────────────────────────┐{Color.END}")
    print(f"{Color.YELLOW}  │{Color.END} {Color.BOLD}BƯỚC 2:{Color.END} Nhập mã kích hoạt vào đây                       {Color.YELLOW}│{Color.END}")
    print(f"{Color.YELLOW}  └───────────────────────────────────────────────────────────┘{Color.END}")
    print()
    
    for attempt in range(3):
        key_input = input(f"  {Icon.KEY} {Color.BOLD}Nhập mã: {Color.END}").strip()
        
        if key_input == daily_key or key_input.upper() == "ADMIN_PREMIUM_2026":
            is_vip = key_input.upper() == "ADMIN_PREMIUM_2026"
            
            print()
            info("Đang xác thực...")
            time.sleep(1)
            
            if save_license("VIP" if is_vip else "FREE", 999999 if is_vip else 4):
                print()
                success("Kích hoạt thành công!")
                success(f"Loại: {'VIP Premium' if is_vip else 'FREE (4 lượt)'}")
                time.sleep(2)
                return True
        else:
            remaining = 2 - attempt
            if remaining > 0:
                error(f"Mã không hợp lệ! Còn {remaining} lần thử")
                print()
            else:
                error("Hết lượt thử. Vui lòng lấy link mới!")
                time.sleep(2)
                return False
    
    return False

def activate_vip_key():
    show_activation_ui()
    
    print(f"{Color.PURPLE}  ╔═════════════════════════════════════════════════════════════╗{Color.END}")
    print(f"{Color.PURPLE}  ║{Color.END}              {Icon.CROWN} {Color.BOLD}VIP PREMIUM ACTIVATION{Color.END}                   {Color.PURPLE}║{Color.END}")
    print(f"{Color.PURPLE}  ╚═════════════════════════════════════════════════════════════╝{Color.END}")
    print()
    
    vip_key = input(f"  {Icon.CROWN} {Color.BOLD}Nhập mã VIP: {Color.END}").strip()
    
    valid_keys = ["OLM_VIP_2026", "PREMIUM_UNLIMITED", "ADMIN_PREMIUM_2026"]
    
    if vip_key.upper() in valid_keys:
        print()
        info("Đang xác thực VIP...")
        time.sleep(1)
        
        if save_license("VIP", 999999):
            print()
            success("Kích hoạt VIP thành công!")
            success("Loại: Premium Unlimited")
            time.sleep(2)
            return True
    
    error("Mã VIP không hợp lệ!")
    time.sleep(2)
    return False

def show_vip_info():
    print_banner()
    
    print(f"{Color.PINK}  ╔═════════════════════════════════════════════════════════════╗{Color.END}")
    print(f"{Color.PINK}  ║{Color.END}              {Icon.CROWN} {Color.BOLD}VIP PREMIUM PACKAGE{Color.END}                      {Color.PINK}║{Color.END}")
    print(f"{Color.PINK}  ╚═════════════════════════════════════════════════════════════╝{Color.END}")
    print()
    
    features = [
        ("Không giới hạn lượt giải bài", Icon.CHECK),
        ("Hỗ trợ tất cả môn học", Icon.CHECK),
        ("Tốc độ xử lý ưu tiên", Icon.ROCKET),
        ("Hỗ trợ kỹ thuật 24/7", Icon.SHIELD),
        ("Cập nhật tính năng mới", Icon.SPARKLE),
    ]
    
    for feature, icon in features:
        print(f"  {icon} {Color.GREEN}{feature}{Color.END}")
    
    print()
    print(f"{Color.YELLOW}  {Icon.FIRE} GIÁ: {Color.BOLD}50.000 VNĐ/tháng{Color.END}")
    print()
    print(f"{Color.CYAN}  LIÊN HỆ:{Color.END}")
    print(f"  {Icon.SPARKLE} Zalo    : 0123456789")
    print(f"  {Icon.SPARKLE} Email   : vip@olmmaster.pro")
    print(f"  {Icon.SPARKLE} Facebook: fb.com/olmmaster")
    print()
    
    input(f"{Color.YELLOW}Nhấn Enter để quay lại...{Color.END}")

# ========== MENU CHÍNH ==========
def main_menu():
    while True:
        license_data = load_license()
        
        if license_data and license_data.get('remain', 0) > 0:
            print_banner()
            
            mode = license_data.get('mode', 'FREE')
            remain = license_data.get('remain', 0)
            
            print(f"{Color.GREEN}  ┌─────────────────────────────────────────────────────────────┐{Color.END}")
            print(f"{Color.GREEN}  │{Color.END}  {Icon.CHECK} {Color.BOLD}License Status{Color.END}                                         {Color.GREEN}│{Color.END}")
            print(f"{Color.GREEN}  ├─────────────────────────────────────────────────────────────┤{Color.END}")
            print(f"{Color.GREEN}  │{Color.END}  {Icon.KEY} Loại      : {Color.YELLOW}{mode:<45}{Color.END} {Color.GREEN}│{Color.END}")
            print(f"{Color.GREEN}  │{Color.END}  {Icon.FIRE} Còn lại   : {Color.CYAN}{remain if remain < 999 else 'Unlimited':<45}{Color.END} {Color.GREEN}│{Color.END}")
            print(f"{Color.GREEN}  │{Color.END}  {Icon.SPARKLE} Hết hạn   : {Color.WHITE}{license_data.get('expire', 'N/A'):<45}{Color.END} {Color.GREEN}│{Color.END}")
            print(f"{Color.GREEN}  └─────────────────────────────────────────────────────────────┘{Color.END}")
            print()
            
            success("License hợp lệ! Đang khởi động tool...")
            time.sleep(2)
            return True
        
        # Chưa có license
        print_banner()
        
        print(f"{Color.CYAN}  ╔═════════════════════════════════════════════════════════════╗{Color.END}")
        print(f"{Color.CYAN}  ║{Color.END}                   {Color.BOLD}PHƯƠNG THỨC KÍCH HOẠT{Color.END}                      {Color.CYAN}║{Color.END}")
        print(f"{Color.CYAN}  ╚═════════════════════════════════════════════════════════════╝{Color.END}")
        print()
        
        options = [
            (f"{Icon.KEY}  Free License (4 lượt/ngày)", "1"),
            (f"{Icon.CROWN}  VIP Premium (Không giới hạn)", "2"),
            (f"{Icon.INFO}  Thông tin gói VIP", "3"),
            (f"{Icon.CROSS}  Thoát", "0"),
        ]
        
        for opt, num in options:
            color = Color.YELLOW if num in ['1', '2'] else Color.PURPLE if num == '3' else Color.RED
            print(f"  {color}[{num}]{Color.END} {opt}")
        
        print()
        choice = input(f"  {Icon.ARROW} {Color.BOLD}Lựa chọn: {Color.END}").strip()
        
        if choice == '1':
            if activate_free_key():
                continue
        elif choice == '2':
            if activate_vip_key():
                continue
        elif choice == '3':
            show_vip_info()
        elif choice == '0':
            print()
            info("Tạm biệt!")
            time.sleep(1)
            sys.exit(0)
        else:
            error("Lựa chọn không hợp lệ!")
            time.sleep(1)

# ========== TẢI TOOL CHÍNH ==========
def load_main_tool():
    clear()
    print_banner()
    
    info("Đang kết nối máy chủ...")
    
    try:
        resp = requests.get(URL_MAIN_TOOL, timeout=15)
        resp.raise_for_status()
        
        success("Đã tải module chính")
        time.sleep(1)
        
        info("Đang khởi động OLM Master Pro...")
        time.sleep(1)
        
        # Truyền hàm vào tool chính
        exec_globals = {
            '__name__': '__main__',
            'consume_one_attempt': consume_attempt,
            'check_local_status': load_license,
        }
        
        exec(resp.text, exec_globals)
        
    except Exception as e:
        error(f"Lỗi tải tool: {e}")
        input("\nNhấn Enter...")
        sys.exit(1)

# ========== MAIN ==========
if __name__ == "__main__":
    try:
        while True:
            if not check_internet():
                print_banner()
                error("Không có kết nối Internet!")
                time.sleep(3)
                continue
            
            # Menu kích hoạt
            if main_menu():
                # Đã kích hoạt → Load tool chính
                load_main_tool()
                
                # Tool kết thúc → Quay lại menu
                info("Phiên làm việc kết thúc")
                time.sleep(2)
            
    except KeyboardInterrupt:
        print(f"\n\n  {Icon.WARNING} {Color.YELLOW}Đã dừng{Color.END}")
    except Exception as e:
        error(f"Lỗi: {e}")
        time.sleep(3)
