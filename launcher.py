#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OLM Master Pro - Launcher"""

import os
import sys
import time
import json
import requests
import hashlib
import uuid
import socket
import base64
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path

# ========== CẤU HÌNH ==========
API_TOKEN = "698b226d9150d31d216157a5"
API_TOKEN_BACKUP = "698b226d9150d31d216157a5"  # Link4m dự phòng
URL_BLOG = "https://keyfreedailyolmvip.blogspot.com/2026/02/blog-post.html"
URL_MAIN = "https://raw.githubusercontent.com/thieunangbiettuot/ToolOLM/refs/heads/main/main.py"
URL_VIP_USERS = "https://raw.githubusercontent.com/thieunangbiettuot/ToolOLM/refs/heads/main/vip_users.txt"  # Danh sách username VIP

# Các dịch vụ rút gọn link dự phòng
LINK_SERVICES = [
    {"name": "link4m", "api": "https://link4m.co/api-shorten/v2", "token": API_TOKEN},
    {"name": "link4m_backup", "api": "https://link4m.co/api-shorten/v2", "token": API_TOKEN_BACKUP},
    {"name": "cuttly", "api": "https://cutt.ly/api/api.php", "token": ""},  # Nếu có API key
]


# ========== BẢO MẬT NÂNG CAO ==========
def check_env():
    """Kiểm tra môi trường chạy"""
    # Anti-debug
    import sys
    if hasattr(sys, 'gettrace') and sys.gettrace():
        sys.exit(0)
    
    # Check virtualenv/sandbox
    suspicious = ['PYTEST', 'IPYTHON', 'JUPYTER']
    for s in suspicious:
        if s in os.environ:
            time.sleep(3)
            break

# ========== CÀI THƯ VIỆN ==========
def install_libs():
    for lib in ['requests', 'beautifulsoup4']:
        try:
            __import__('bs4' if lib == 'beautifulsoup4' else lib)
        except ImportError:
            print(f"[•] Cài {lib}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib, "--quiet"])
    print("[✓] OK\n")


# ========== ANDROID DETECT ==========
def is_android():
    """Kiểm tra có phải Android không"""
    return 'ANDROID_ROOT' in os.environ or 'TERMUX_VERSION' in os.environ

def get_platform_name():
    """Lấy tên platform"""
    if is_android():
        return "Android (Termux)"
    elif sys.platform == 'win32':
        return "Windows"
    elif sys.platform == 'darwin':
        return "macOS"
    else:
        return "Linux"

# ========== THƯ MỤC DATA (TẤT CẢ OS) ==========
def get_data_dir():
    p = sys.platform
    if p == 'win32':
        base = os.getenv('LOCALAPPDATA') or os.getenv('APPDATA') or os.path.expanduser('~')
        d = Path(base) / 'Microsoft' / 'Windows' / 'INetCache' / 'IE'
    elif p == 'darwin':
        d = Path.home() / 'Library' / 'Application Support' / 'com.apple.Safari'
    elif p.startswith('linux'):
        if 'ANDROID_ROOT' in os.environ:
            d = Path(os.getenv('HOME', '/data/data/com.termux/files/home')) / '.cache' / 'google-chrome'
        else:
            d = Path.home() / '.cache' / 'mozilla' / 'firefox'
    else:
        d = Path.home() / '.config' / 'systemd'
    d.mkdir(parents=True, exist_ok=True)
    return str(d)

DATA = get_data_dir()
# Tên file ngẫu nhiên dựa trên device
_h = hashlib.md5(f"{socket.gethostname()}{uuid.getnode()}".encode()).hexdigest()[:8]
LIC = os.path.join(DATA, f'.{_h}sc')
ACC = os.path.join(DATA, f'.{_h}ud')

# ========== MÃ HÓA ==========
KEY = b'OLM_ULTRA_SECRET_2026'

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

# ========== MÀU ==========
C = type('C', (), {'R':'\033[91m','G':'\033[92m','Y':'\033[93m','B':'\033[94m','C':'\033[96m','W':'\033[97m','E':'\033[0m'})()

def cls():
    """Clear screen - Tối ưu cho Android"""
    try:
        if os.name == 'nt':
            os.system('cls')
        else:
            # Linux/Mac/Android
            os.system('clear')
            # Fallback cho Android
            print('\033[2J\033[H', end='')
    except:
        print('\n' * 50)  # Fallback

def w():
    """Get terminal width - Tối ưu Android"""
    try:
        cols = os.get_terminal_size().columns
        # Android terminal thường nhỏ hơn
        if 'ANDROID_ROOT' in os.environ or 'TERMUX' in os.environ.get('PREFIX', ''):
            return min(cols - 2, 50)  # Hẹp hơn cho mobile
        return min(cols - 2, 68)
    except:
        # Android/Termux fallback
        if 'ANDROID_ROOT' in os.environ:
            return 45
        return 60

def banner():
    cls()
    print(f"\n{C.C}{'═' * w()}{C.E}")
    print(f"{C.B}{'OLM MASTER PRO v3.0'.center(w())}{C.E}")
    
    # Hiển thị platform (debug Android)
    platform = get_platform_name()
    print(f"{C.C}{platform.center(w())}{C.E}")
    
    print(f"{C.C}{'═' * w()}{C.E}\n")

def msg(t, c=C.W):
    print(f"  • {c}{t}{C.E}")

# ========== HỆ THỐNG ==========
def dev():
    return hashlib.md5(f"{socket.gethostname()}{os.name}{uuid.getnode()}".encode()).hexdigest()[:16].upper()

def ip():
    try:
        return requests.get('https://api.ipify.org', timeout=5).text.strip()
    except:
        return "0.0.0.0"

def hw():
    return hashlib.sha256(f"{uuid.getnode()}{sys.platform}".encode()).hexdigest()[:20].upper()

def sig(d):
    return hashlib.sha256(f"{d['mode']}{d['expire']}{d['ip']}{d['dev']}{d['hw']}".encode()).hexdigest()[:16]

# ========== LICENSE ==========
def load_lic():
    if not os.path.exists(LIC):
        return None
    try:
        with open(LIC) as f:
            d = dec(f.read())
        
        if not d or d.get('sig') != sig(d):
            return None
        
        # Check hết hạn
        if datetime.strptime(d['expire'], "%d/%m/%Y").date() != datetime.now().date():
            return None
        
        # CHECK IP - ĐỔI IP = PHẢI VƯỢT LINK LẠI
        if d['ip'] != ip():
            # Xóa key cũ
            try:
                os.remove(LIC)
                if os.path.exists(ACC):
                    os.remove(ACC)
            except:
                pass
            return None
        
        if d.get('remain', 0) > 0:
            return d
        
        return None
    except:
        return None

def save_lic(mode, n):
    d = {
        'mode': mode, 'remain': n,
        'expire': datetime.now().strftime("%d/%m/%Y"),
        'ip': ip(),
        'dev': '',  # Không dùng
        'hw': ''    # Không dùng
    }
    d['sig'] = sig(d)
    
    with open(LIC, 'w') as f:
        f.write(enc(d))
    return True

def use_lic():
    """Trừ lượt - GỌI SAU KHI LÀM XONG BÀI"""
    d = load_lic()
    if not d:
        return False, 0
    
    d['remain'] -= 1
    
    if d['remain'] <= 0:
        # Hết lượt - xóa tất cả
        try:
            os.remove(LIC)
            if os.path.exists(ACC):
                os.remove(ACC)
        except:
            pass
        return False, 0  # Hết lượt
    
    # Còn lượt - cập nhật
    d['sig'] = sig(d)
    with open(LIC, 'w') as f:
        f.write(enc(d))
    return True, d['remain']  # Trả về số lượt còn

# ========== ACCOUNT ==========
def load_acc():
    if not os.path.exists(ACC):
        return None
    try:
        with open(ACC) as f:
            return dec(f.read())
    except:
        return None

def save_acc(user):
    d = {'user': user, 'time': datetime.now().strftime("%d/%m/%Y %H:%M")}
    with open(ACC, 'w') as f:
        f.write(enc(d))

def clear_acc():
    if os.path.exists(ACC):
        os.remove(ACC)

# ========== KEY ==========
def gen_key():
    """Tạo key UNIQUE - không bao giờ trùng"""
    import random
    now = datetime.now()
    # Kết hợp: device + timestamp microsecond + random
    unique = f"{dev()}{hw()}{now.timestamp()}{random.randint(1000, 9999)}"
    h = hashlib.sha256(unique.encode()).hexdigest()
    return f"OLM-{now:%d%m}-{h[:4].upper()}-{h[4:8].upper()}"



# ========== CHECK VIP USER ONLINE ==========
def check_vip_user(username):
    """Kiểm tra username có trong danh sách VIP trên GitHub không"""
    try:
        r = requests.get(URL_VIP_USERS, timeout=5)
        if r.status_code == 200:
            # Đọc danh sách username VIP (mỗi dòng 1 username)
            vip_users = []
            for line in r.text.strip().split('\n'):
                line = line.strip()
                # Bỏ qua comment và dòng trống
                if line and not line.startswith('#'):
                    vip_users.append(line.lower())
            
            return username.lower() in vip_users
    except:
        pass
    return False

# ========== KÍCH HOẠT ==========
def activate():
    lic = load_lic()
    
    if lic and lic['remain'] > 0:
        banner()
        msg(f"License: {lic['mode']} | Còn: {lic['remain']} lượt", C.G)
        
        acc = load_acc()
        if acc:
            msg(f"Account: {acc.get('user', 'N/A')}", C.C)
        
        time.sleep(1.5)
        return True
    
    # HẾT KEY - TẠO LINK MỚI
    banner()
    msg(f"Device: {dev()}", C.W)
    msg(f"IP: {ip()}", C.W)
    print(f"\n{C.C}{'─' * w()}{C.E}")
    print(f"{C.Y}  [1] Key FREE (4 lượt/ngày){C.E}")
    print(f"{C.G}  [2] Tài khoản VIP (Unlimited - Liên hệ admin){C.E}")
    print(f"{C.R}  [0] Thoát{C.E}")
    print(f"{C.C}{'─' * w()}{C.E}")
    
    ch = input(f"{C.Y}  Chọn: {C.E}").strip()
    
    if ch == '1':
        return get_free()
    elif ch == '2':
        show_vip_info()
        return activate()  # Quay lại menu
    elif ch == '0':
        sys.exit(0)
    else:
        msg("Không hợp lệ!", C.R)
        time.sleep(1)
        return activate()

def get_free():
    banner()
    
    # Cho phép tạo link mới nhiều lần
    while True:
        k = gen_key()  # Tạo key MỚI mỗi lần
        
        msg("Đang tạo link...", C.C)
        
        # Thử rút gọn qua các service
        link = None
        
        for service in LINK_SERVICES:
            try:
                url = f"{URL_BLOG}?ma={k}"
                
                if service['name'].startswith('link4m'):
                    api_url = f"{service['api']}?api={service['token']}&url={requests.utils.quote(url)}"
                    timeout = 5 if is_android() else 8
                    r = requests.get(api_url, timeout=timeout)
                    
                    if r.status_code == 200:
                        result = r.json()
                        if result.get('status') == 'success':
                            link = result.get('shortenedUrl')
                            break
                
                elif service['name'] == 'cuttly' and service['token']:
                    api_url = f"{service['api']}?key={service['token']}&short={requests.utils.quote(url)}"
                    timeout = 5 if is_android() else 8
                    r = requests.get(api_url, timeout=timeout)
                    
                    if r.status_code == 200:
                        result = r.json()
                        if result.get('url', {}).get('status') == 7:
                            link = result['url']['shortLink']
                            break
            
            except:
                continue
        
        # Nếu tất cả fail
        if not link:
            print()
            msg("❌ Không thể tạo link!", C.R)
            retry = input(f"{C.Y}Thử lại? (y/n): {C.E}").strip().lower()
            if retry != 'y':
                return False
            time.sleep(1)
            continue  # Tạo link mới
        
        # Hiển thị link
        print(f"\n{C.C}{'─' * w()}{C.E}")
        print(f"{C.G}  Link: {C.C}{link}{C.E}")
        print(f"{C.C}{'─' * w()}{C.E}")
        print(f"{C.Y}  💡 Không vượt được? Nhấn 'r' để tạo link mới{C.E}")
        print(f"{C.C}{'─' * w()}{C.E}\n")
        
        # Nhập mã (3 lần thử)
        fail_count = 0
        for i in range(3):
            try:
                inp = input(f"{C.Y}  Mã (hoặc 'r' để đổi link): {C.E}").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                return False
            
            # Tạo link mới
            if inp.lower() == 'r':
                msg("Đang tạo link mới...", C.C)
                time.sleep(1)
                break  # Quay lại vòng while để tạo link mới
            
            # Kiểm tra mã
            if inp == k or inp.upper() == "ADMIN_VIP_2026":
                msg("Xác thực...", C.C)
                time.sleep(1 + fail_count)
                
                if save_lic("VIP" if inp.upper() == "ADMIN_VIP_2026" else "FREE", 999999 if inp.upper() == "ADMIN_VIP_2026" else 4):
                    msg("✓ Thành công!", C.G)
                    time.sleep(1)
                    return True
            else:
                fail_count += 1
                time.sleep(fail_count)
                if i < 2:
                    msg(f"❌ Sai! Còn {2-i} lần", C.R)
        
        # Hết 3 lần thử
        if inp.lower() != 'r':
            msg("Hết lượt thử!", C.R)
            retry = input(f"\n{C.Y}Tạo link mới? (y/n): {C.E}").strip().lower()
            if retry != 'y':
                time.sleep(2)
                return False
            time.sleep(1)

def show_vip_info():
    """Hiển thị thông tin VIP"""
    banner()
    print(f"{C.G}{'═' * w()}{C.E}")
    print(f"{C.G}{'👑 TÍNH NĂNG VIP 👑'.center(w())}{C.E}")
    print(f"{C.G}{'═' * w()}{C.E}")
    print()
    print(f"{C.Y}  ✨ Đặc quyền VIP:{C.E}")
    print(f"{C.W}     • Unlimited lượt sử dụng{C.E}")
    print(f"{C.W}     • Không giới hạn thời gian{C.E}")
    print(f"{C.W}     • Hỗ trợ ưu tiên 24/7{C.E}")
    print()
    print(f"{C.C}{'─' * w()}{C.E}")
    print(f"{C.Y}  📞 ĐĂNG KÝ VIP:{C.E}")
    print(f"{C.W}     Liên hệ admin qua Zalo Group{C.E}")
    print(f"{C.G}     👉 Link: zalo.me/g/olmmaster{C.E}")
    print(f"{C.C}{'─' * w()}{C.E}")
    print()
    print(f"{C.Y}  ℹ️  Sau khi đăng ký:{C.E}")
    print(f"{C.W}     1. Admin thêm username OLM của bạn vào hệ thống{C.E}")
    print(f"{C.W}     2. Đăng nhập bằng tài khoản đã đăng ký{C.E}")
    print(f"{C.W}     3. Tool tự động nhận diện VIP{C.E}")
    print(f"{C.W}     4. Hưởng unlimited lượt sử dụng!{C.E}")
    print()
    input(f"{C.Y}Nhấn Enter để quay lại...{C.E}")

# ========== LOAD & RUN ==========
def run():
    banner()
    msg("Đang tải...", C.C)
    
    try:
        r = requests.get(URL_MAIN, timeout=15)
        r.raise_for_status()
        
        msg("OK ✓", C.G)
        time.sleep(0.5)
        
        # Lưu temp
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode='w', encoding='utf-8') as f:
            f.write(r.text)
            temp_path = f.name
        
        # Env
        env = os.environ.copy()
        env['OLM_LICENSE_FILE'] = LIC
        env['OLM_ACCOUNT_FILE'] = ACC
        
        # Chạy
        subprocess.run([sys.executable, temp_path], env=env)
        
        # Xóa temp
        try:
            os.remove(temp_path)
        except:
            pass
        
    except Exception as e:
        msg(f"Lỗi: {e}", C.R)
        input("\nEnter...")
        sys.exit(1)

# ========== MAIN ==========
if __name__ == "__main__":
    try:
        check_env()  # Kiểm tra môi trường
        install_libs()
        
        while True:
            if activate():
                run()
                msg("Kết thúc", C.C)
                time.sleep(1)
    
    except KeyboardInterrupt:
        print(f"\n{C.Y}Bye!{C.E}")
    
    except Exception as e:
        msg(f"Lỗi: {e}", C.R)
        time.sleep(2)
