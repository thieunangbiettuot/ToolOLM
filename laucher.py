#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OLM Master Pro - License Activation System
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

LICENSE_FILE = "olm_license.dat"
ACCOUNT_FILE = "olm_account.dat"

# ========== MÀU SẮC ==========
class C:
    R = '\033[91m'; G = '\033[92m'; Y = '\033[93m'
    B = '\033[94m'; C = '\033[96m'; W = '\033[97m'; E = '\033[0m'

# ========== TIỆN ÍCH ==========
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def line(char='─'):
    try:
        w = min(os.get_terminal_size().columns - 4, 65)
    except:
        w = 60
    print(f"{C.C}{char * w}{C.E}")

def banner():
    clear()
    print()
    line('═')
    print(f"{C.B}  OLM MASTER PRO - Education Assistant v3.0{C.E}")
    line('═')
    print()

def msg(text, symbol='•', color=C.W):
    print(f"  {symbol} {color}{text}{C.E}")

# ========== HỆ THỐNG ==========
def get_device_id():
    try:
        data = socket.gethostname() + os.name + str(uuid.getnode())
        return hashlib.md5(data.encode()).hexdigest()[:12].upper()
    except:
        return "UNKNOWN"

def get_ip():
    try:
        return requests.get('https://api.ipify.org', timeout=5).text.strip()
    except:
        return "0.0.0.0"

# ========== LICENSE ==========
def load_license():
    if not os.path.exists(LICENSE_FILE):
        return None
    try:
        with open(LICENSE_FILE, 'r') as f:
            data = json.load(f)
        
        # Check hết hạn
        if data.get('expire') != datetime.now().strftime("%d/%m/%Y"):
            os.remove(LICENSE_FILE)
            if os.path.exists(ACCOUNT_FILE):
                os.remove(ACCOUNT_FILE)
            return None
        
        # Check IP + Device
        if data.get('ip') == get_ip() and data.get('device') == get_device_id():
            # Verify checksum
            check_str = f"{data.get('ip')}{data.get('device')}{data.get('expire')}"
            expected = hashlib.md5(check_str.encode()).hexdigest()[:8]
            if data.get('checksum') != expected:
                os.remove(LICENSE_FILE)
                return None
            
            if data.get('remain', 0) > 0:
                return data
        else:
            msg("Phát hiện thay đổi IP/thiết bị!", '⚠', C.Y)
            os.remove(LICENSE_FILE)
            if os.path.exists(ACCOUNT_FILE):
                os.remove(ACCOUNT_FILE)
        
        return None
    except:
        try:
            os.remove(LICENSE_FILE)
            if os.path.exists(ACCOUNT_FILE):
                os.remove(ACCOUNT_FILE)
        except:
            pass
        return None

def save_license(mode, remain):
    ip = get_ip()
    device = get_device_id()
    expire = datetime.now().strftime("%d/%m/%Y")
    
    # Tạo checksum
    check_str = f"{ip}{device}{expire}"
    checksum = hashlib.md5(check_str.encode()).hexdigest()[:8]
    
    data = {
        'mode': mode,
        'remain': remain,
        'expire': expire,
        'ip': ip,
        'device': device,
        'checksum': checksum
    }
    
    try:
        with open(LICENSE_FILE, 'w') as f:
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
            os.remove(LICENSE_FILE)
            if os.path.exists(ACCOUNT_FILE):
                os.remove(ACCOUNT_FILE)
        except:
            pass
        return True
    
    try:
        with open(LICENSE_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except:
        return False

# ========== KÍCH HOẠT ==========
def activate():
    lic = load_license()
    
    if lic and lic.get('remain', 0) > 0:
        banner()
        msg(f"License: {lic['mode']}", '✓', C.G)
        msg(f"Còn lại: {lic['remain']} lượt", '•', C.C)
        time.sleep(1.5)
        return True
    
    banner()
    
    device = get_device_id()
    ip = get_ip()
    
    msg(f"Device: {device}", '•', C.W)
    msg(f"IP: {ip}", '•', C.W)
    print()
    line()
    print(f"{C.Y}  [1] Key FREE (4 lượt/ngày){C.E}")
    print(f"{C.G}  [2] Key VIP (Unlimited){C.E}")
    print(f"{C.C}  [3] Thông tin VIP{C.E}")
    print(f"{C.R}  [0] Thoát{C.E}")
    line()
    
    choice = input(f"{C.Y}  Chọn: {C.E}").strip()
    
    if choice == '1':
        return activate_free()
    elif choice == '2':
        return activate_vip()
    elif choice == '3':
        show_vip_info()
        return activate()
    elif choice == '0':
        msg("Tạm biệt!", '•', C.C)
        sys.exit(0)
    else:
        msg("Lựa chọn không hợp lệ!", '✗', C.R)
        time.sleep(1)
        return activate()

def activate_free():
    banner()
    
    device = get_device_id()
    daily_key = f"OLM{datetime.now().strftime('%d%m')}{device[-3:]}"
    
    msg("Đang tạo link kích hoạt...", '•', C.C)
    time.sleep(1)
    
    # Tạo link với ?ma= (ĐÚNG!)
    full_url = f"{URL_BLOG}?ma={daily_key}"
    
    try:
        # API v2 đúng cách
        api_url = f"https://link4m.co/api-shorten/v2?api={API_TOKEN}&url={requests.utils.quote(full_url)}"
        resp = requests.get(api_url, timeout=10)
        result = resp.json()
        
        if result.get('status') == 'success':
            short_link = result.get('shortenedUrl')
        else:
            short_link = full_url
    except:
        short_link = full_url
    
    print()
    line()
    print(f"{C.G}  BƯỚC 1: Truy cập link{C.E}")
    print(f"{C.C}  {short_link}{C.E}")
    print()
    print(f"{C.G}  BƯỚC 2: Nhập mã kích hoạt{C.E}")
    line()
    print()
    
    for attempt in range(3):
        key_input = input(f"{C.Y}  Mã: {C.E}").strip()
        
        if key_input == daily_key or key_input.upper() == "ADMIN_PREMIUM_2026":
            is_vip = key_input.upper() == "ADMIN_PREMIUM_2026"
            
            print()
            msg("Đang xác thực...", '•', C.C)
            time.sleep(1)
            
            if save_license("VIP" if is_vip else "FREE", 999999 if is_vip else 4):
                msg("Kích hoạt thành công!", '✓', C.G)
                time.sleep(1.5)
                return True
        else:
            remaining = 2 - attempt
            if remaining > 0:
                msg(f"Sai mã! Còn {remaining} lần", '✗', C.R)
            else:
                msg("Hết lượt thử!", '✗', C.R)
                time.sleep(1.5)
                return False
    
    return False

def activate_vip():
    banner()
    
    line()
    print(f"{C.G}  VIP PREMIUM ACTIVATION{C.E}")
    line()
    print()
    
    vip_key = input(f"{C.Y}  Mã VIP: {C.E}").strip()
    
    valid = ["OLM_VIP_2026", "PREMIUM_UNLIMITED"]
    
    if vip_key.upper() in valid:
        print()
        msg("Đang xác thực...", '•', C.C)
        time.sleep(1)
        
        if save_license("VIP", 999999):
            msg("Kích hoạt VIP thành công!", '✓', C.G)
            time.sleep(1.5)
            return True
    
    msg("Mã VIP không hợp lệ!", '✗', C.R)
    time.sleep(1.5)
    return False

def show_vip_info():
    banner()
    
    line()
    print(f"{C.G}  VIP PREMIUM - 50K/tháng{C.E}")
    line()
    print()
    print(f"{C.G}  ✓ Unlimited lượt giải{C.E}")
    print(f"{C.G}  ✓ Xử lý ưu tiên{C.E}")
    print(f"{C.G}  ✓ Hỗ trợ 24/7{C.E}")
    print(f"{C.G}  ✓ Cập nhật mới{C.E}")
    print()
    print(f"{C.C}  Zalo: 0123456789{C.E}")
    print(f"{C.C}  Email: vip@olmmaster.pro{C.E}")
    print()
    
    input(f"{C.Y}Nhấn Enter...{C.E}")

# ========== LOAD TOOL ==========
def load_tool():
    banner()
    
    msg("Đang kết nối máy chủ...", '•', C.C)
    
    try:
        resp = requests.get(URL_MAIN_TOOL, timeout=15)
        resp.raise_for_status()
        
        msg("Đã tải module chính", '✓', C.G)
        time.sleep(1)
        
        msg("Đang khởi động...", '•', C.C)
        time.sleep(1)
        
        # Truyền hàm
        exec_globals = {
            '__name__': '__main__',
            'consume_one_attempt': consume_attempt,
            'check_local_status': load_license,
        }
        
        exec(resp.text, exec_globals)
        
    except Exception as e:
        msg(f"Lỗi: {e}", '✗', C.R)
        input("\nNhấn Enter...")
        sys.exit(1)

# ========== MAIN ==========
if __name__ == "__main__":
    try:
        while True:
            if activate():
                load_tool()
                msg("Phiên kết thúc", '•', C.C)
                time.sleep(2)
            
    except KeyboardInterrupt:
        print(f"\n{C.Y}Đã dừng{C.E}")
    except Exception as e:
        msg(f"Lỗi: {e}", '✗', C.R)
        time.sleep(3)
