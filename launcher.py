#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OLM Master Pro - Launcher & License Manager
"""

import os, sys, time, json, requests, hashlib, uuid, socket, base64, subprocess, tempfile
from datetime import datetime
from pathlib import Path

# ========== CẤU HÌNH ==========
API_TOKEN = "698b226d9150d31d216157a5"
URL_BLOG = "https://keyfreedailyolmvip.blogspot.com/2026/02/blog-post.html"
URL_MAIN = "https://raw.githubusercontent.com/thieunangbiettuot/ToolOLM/refs/heads/main/main.py"

# ========== CÀI ĐẶT THƯ VIỆN ==========
def install_libs():
    libs = ['requests', 'beautifulsoup4']
    for lib in libs:
        try:
            if lib == 'beautifulsoup4':
                __import__('bs4')
            else:
                __import__(lib)
        except ImportError:
            print(f"[•] Đang cài {lib}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib, "--quiet"])
    print("[✓] Thư viện OK\n")

# ========== LƯU FILE (TẤT CẢ HỆ ĐIỀU HÀNH) ==========
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
LIC_FILE = os.path.join(DATA, '.sysconf')
ACC_FILE = os.path.join(DATA, '.usrdata')

# ========== MÃ HÓA ==========
KEY = b'OLM_ULTRA_SECRET_2026_PROTECTION'

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
    os.system('cls' if os.name == 'nt' else 'clear')

def w():
    try:
        return min(os.get_terminal_size().columns - 2, 68)
    except:
        return 60

def banner():
    cls()
    print(f"\n{C.C}{'═' * w()}{C.E}")
    print(f"{C.B}{'OLM MASTER PRO v3.0'.center(w())}{C.E}")
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
    if not os.path.exists(LIC_FILE):
        return None
    try:
        with open(LIC_FILE) as f:
            d = dec(f.read())
        
        if not d or d.get('sig') != sig(d):
            return None
        
        # Check hết hạn
        if datetime.strptime(d['expire'], "%d/%m/%Y").date() != datetime.now().date():
            return None
        
        # Check device
        if d['ip'] != ip() or d['dev'] != dev() or d['hw'] != hw():
            msg("Thay đổi thiết bị! Lấy key mới.", C.Y)
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
        'ip': ip(), 'dev': dev(), 'hw': hw()
    }
    d['sig'] = sig(d)
    
    with open(LIC_FILE, 'w') as f:
        f.write(enc(d))
    return True

def use_lic():
    """Trừ 1 lượt - được gọi từ main.py"""
    d = load_lic()
    if not d:
        return False
    
    d['remain'] -= 1
    
    if d['remain'] <= 0:
        # Hết lượt → xóa license và account
        os.remove(LIC_FILE)
        if os.path.exists(ACC_FILE):
            os.remove(ACC_FILE)
        return True  # Trả về True để báo đã trừ xong (nhưng hết lượt)
    
    # Còn lượt → lưu lại
    d['sig'] = sig(d)
    with open(LIC_FILE, 'w') as f:
        f.write(enc(d))
    return True

# ========== ACCOUNT LOCK ==========
def load_acc():
    if not os.path.exists(ACC_FILE):
        return None
    try:
        with open(ACC_FILE) as f:
            return dec(f.read())
    except:
        return None

def save_acc(user):
    d = {'user': user, 'time': datetime.now().strftime("%d/%m/%Y %H:%M")}
    with open(ACC_FILE, 'w') as f:
        f.write(enc(d))

def clear_acc():
    if os.path.exists(ACC_FILE):
        os.remove(ACC_FILE)

# ========== KEY ==========
def gen_key():
    h = hashlib.sha256(f"{dev()}{hw()}{datetime.now():%d%m%Y}".encode()).hexdigest()
    return f"OLM-{datetime.now():%d%m}-{h[:4].upper()}-{h[4:8].upper()}"

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
    
    banner()
    msg(f"Device: {dev()}", C.W)
    msg(f"IP: {ip()}", C.W)
    print(f"\n{C.C}{'─' * w()}{C.E}")
    print(f"{C.Y}  [1] Key FREE (4 lượt/ngày){C.E}")
    print(f"{C.G}  [2] Key VIP (Unlimited){C.E}")
    print(f"{C.R}  [0] Thoát{C.E}")
    print(f"{C.C}{'─' * w()}{C.E}")
    
    ch = input(f"{C.Y}  Chọn: {C.E}").strip()
    
    if ch == '1':
        return get_free()
    elif ch == '2':
        return get_vip()
    elif ch == '0':
        sys.exit(0)
    else:
        msg("Không hợp lệ!", C.R)
        time.sleep(1)
        return activate()

def get_free():
    banner()
    k = gen_key()
    msg("Tạo link...", C.C)
    
    try:
        url = f"{URL_BLOG}?ma={k}"
        api = f"https://link4m.co/api-shorten/v2?api={API_TOKEN}&url={requests.utils.quote(url)}"
        r = requests.get(api, timeout=10)
        link = r.json().get('shortenedUrl', url) if r.json().get('status') == 'success' else url
    except:
        link = f"{URL_BLOG}?ma={k}"
    
    print(f"\n{C.C}{'─' * w()}{C.E}")
    print(f"{C.G}  BƯỚC 1: {C.C}{link}{C.E}")
    print(f"{C.G}  BƯỚC 2: Nhập mã{C.E}")
    print(f"{C.C}{'─' * w()}{C.E}\n")
    
    for i in range(3):
        inp = input(f"{C.Y}  Mã: {C.E}").strip()
        
        if inp == k or inp.upper() == "ADMIN_VIP_2026":
            msg("Xác thực...", C.C)
            time.sleep(1)
            
            if save_lic("VIP" if inp.upper() == "ADMIN_VIP_2026" else "FREE", 999999 if inp.upper() == "ADMIN_VIP_2026" else 4):
                msg("OK!", C.G)
                time.sleep(1)
                return True
        else:
            if i < 2:
                msg(f"Sai! Còn {2-i} lần", C.R)
    
    msg("Hết lượt!", C.R)
    time.sleep(1)
    return False

def get_vip():
    banner()
    inp = input(f"{C.Y}  Mã VIP: {C.E}").strip()
    
    if inp.upper() in ["OLM_VIP_2026", "PREMIUM_2026"]:
        msg("Xác thực...", C.C)
        time.sleep(1)
        
        if save_lic("VIP", 999999):
            msg("VIP OK!", C.G)
            time.sleep(1)
            return True
    
    msg("Sai!", C.R)
    time.sleep(1)
    return False

# ========== LOAD & RUN ==========
def run():
    banner()
    msg("Tải tool từ GitHub...", C.C)
    
    try:
        r = requests.get(URL_MAIN, timeout=15)
        r.raise_for_status()
        
        msg("OK ✓", C.G)
        time.sleep(0.5)
        
        # Lưu vào temp
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode='w', encoding='utf-8') as f:
            f.write(r.text)
            temp_path = f.name
        
        # Truyền biến môi trường
        env = os.environ.copy()
        env['OLM_LICENSE_FILE'] = LIC_FILE
        env['OLM_ACCOUNT_FILE'] = ACC_FILE
        
        # Chạy
        result = subprocess.run(
            [sys.executable, temp_path],
            env=env,
            capture_output=False
        )
        
        # Xóa temp
        try:
            os.remove(temp_path)
        except:
            pass
        
        # Kiểm tra còn lượt không
        lic = load_lic()
        if not lic or lic.get('remain', 0) <= 0:
            banner()
            msg("⛔ HẾT LƯỢT!", C.R)
            msg("Vui lòng lấy key mới để tiếp tục", C.Y)
            time.sleep(2)
            return False  # Quay lại màn hình activate
        
        return True
        
    except Exception as e:
        msg(f"Lỗi: {e}", C.R)
        input("\nEnter...")
        sys.exit(1)

# ========== MAIN ==========
if __name__ == "__main__":
    try:
        install_libs()
        
        while True:
            if activate():
                if not run():
                    # Hết lượt → quay lại activate để lấy key mới
                    continue
                else:
                    # User thoát bình thường → hỏi tiếp tục
                    msg("Kết thúc phiên", C.C)
                    time.sleep(1)
            else:
                # Activate thất bại → thoát
                break
    
    except KeyboardInterrupt:
        print(f"\n{C.Y}Bye!{C.E}")
    
    except Exception as e:
        msg(f"Lỗi: {e}", C.R)
        time.sleep(2)
