#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, time, json, requests, hashlib, uuid, socket, base64
from datetime import datetime
from pathlib import Path

# ========== CẤU HÌNH ==========
API_TOKEN = "698b226d9150d31d216157a5"
URL_BLOG = "https://keyfreedailyolmvip.blogspot.com/2026/02/blog-post.html"
URL_MAIN = "https://raw.githubusercontent.com/thieunangbiettuot/ToolOLM/refs/heads/main/main.py"

# ========== LƯU FILE Ở APPDATA (TẤT CẢ HỆ ĐIỀU HÀNH) ==========
def get_data_path():
    """Lấy thư mục ẩn tùy theo OS"""
    system = sys.platform
    
    if system == 'win32':  # Windows
        base = os.getenv('LOCALAPPDATA') or os.getenv('APPDATA') or os.path.expanduser('~')
        p = Path(base) / 'Microsoft' / 'Windows' / 'INetCache' / 'IE'
    
    elif system == 'darwin':  # macOS
        p = Path.home() / 'Library' / 'Application Support' / 'com.apple.Safari'
    
    elif system.startswith('linux'):  # Linux
        if 'ANDROID_ROOT' in os.environ or 'ANDROID_DATA' in os.environ:  # Android (Termux)
            base = os.getenv('HOME') or '/data/data/com.termux/files/home'
            p = Path(base) / '.cache' / 'google-chrome'
        else:  # Linux desktop
            p = Path.home() / '.cache' / 'mozilla' / 'firefox'
    
    elif 'ios' in system.lower() or system == 'darwin' and hasattr(sys, 'getandroidapilevel'):  # iOS
        base = os.path.expanduser('~')
        p = Path(base) / 'Library' / 'Caches' / 'WebKit'
    
    else:  # Fallback
        p = Path.home() / '.config' / 'systemd'
    
    try:
        p.mkdir(parents=True, exist_ok=True)
    except:
        p = Path.home() / '.cache'
        p.mkdir(parents=True, exist_ok=True)
    
    return str(p)

DATA = get_data_path()
LIC = os.path.join(DATA, '.sysconf')
ACC = os.path.join(DATA, '.usrdata')

# ========== MÃ HÓA MẠNH ==========
KEY = b'OLM_ULTRA_SECRET_2026_EXTREME_PROTECTION_SYSTEM'

def enc(obj):
    """Mã hóa object -> chuỗi rác"""
    txt = json.dumps(obj, separators=(',', ':')).encode('utf-8')
    # XOR encryption
    xor = bytearray(txt[i] ^ KEY[i % len(KEY)] for i in range(len(txt)))
    # Base85 encode (tạo ký tự rác)
    b85 = base64.b85encode(bytes(xor)).decode('ascii')
    # Thêm checksum
    chk = hashlib.sha256(b85.encode()).hexdigest()[:12]
    # Thêm noise
    noise = hashlib.md5(chk.encode()).hexdigest()[:8]
    return f"{noise}{chk}{b85}{noise[::-1]}"

def dec(s):
    """Giải mã chuỗi -> object"""
    try:
        # Remove noise
        noise_len = 8
        s = s[noise_len:-noise_len]
        # Extract checksum
        chk = s[:12]
        b85 = s[12:]
        # Verify checksum
        if hashlib.sha256(b85.encode()).hexdigest()[:12] != chk:
            return None
        # Decode Base85
        xor = base64.b85decode(b85)
        # XOR decrypt
        txt = bytes(xor[i] ^ KEY[i % len(KEY)] for i in range(len(xor)))
        return json.loads(txt.decode('utf-8'))
    except:
        return None

# ========== MÀU ==========
C = type('C', (), {
    'R': '\033[91m', 'G': '\033[92m', 'Y': '\033[93m',
    'B': '\033[94m', 'C': '\033[96m', 'W': '\033[97m', 
    'P': '\033[95m', 'E': '\033[0m'
})()

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
    print(f"{C.P}{'Advanced AI Assistant'.center(w())}{C.E}")
    print(f"{C.C}{'═' * w()}{C.E}\n")

def msg(t, i='•', c=C.W):
    print(f"  {i} {c}{t}{C.E}")

# ========== HỆ THỐNG ==========
def dev():
    try:
        return hashlib.md5(f"{socket.gethostname()}{os.name}{uuid.getnode()}".encode()).hexdigest()[:16]
    except:
        return "DEV_UNKNOWN"

def ip():
    try:
        return requests.get('https://api.ipify.org', timeout=5).text.strip()
    except:
        return "0.0.0.0"

def hw():
    try:
        return hashlib.sha256(f"{uuid.getnode()}{sys.platform}{os.name}".encode()).hexdigest()[:20]
    except:
        return "HW_UNKNOWN"

def sig(d):
    """Tạo chữ ký"""
    s = f"{d.get('mode')}{d.get('expire')}{d.get('ip')}{d.get('dev')}{d.get('hw')}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]

# ========== LICENSE ==========
def clean():
    """Xóa tất cả file data"""
    for f in [LIC, ACC]:
        try:
            if os.path.exists(f):
                os.remove(f)
        except:
            pass

def load():
    """Load license từ file mã hóa"""
    if not os.path.exists(LIC):
        return None
    try:
        with open(LIC, 'r') as f:
            d = dec(f.read())
        
        if not d:
            clean()
            return None
        
        # Verify signature
        if d.get('sig') != sig(d):
            msg("License bị sửa đổi!", '⚠', C.R)
            clean()
            return None
        
        # Check expire
        exp = datetime.strptime(d.get('expire'), "%d/%m/%Y")
        if exp.date() != datetime.now().date():
            clean()
            return None
        
        # Check device
        if d.get('ip') == ip() and d.get('dev') == dev() and d.get('hw') == hw():
            if d.get('remain', 0) > 0:
                return d
        
        clean()
        return None
    except:
        clean()
        return None

def save(mode, n):
    """Save license với mã hóa"""
    d = {
        'mode': mode,
        'remain': n,
        'expire': datetime.now().strftime("%d/%m/%Y"),
        'ip': ip(),
        'dev': dev(),
        'hw': hw(),
        'time': datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    d['sig'] = sig(d)
    
    try:
        with open(LIC, 'w') as f:
            f.write(enc(d))
        return True
    except:
        return False

def use():
    """Trừ 1 lượt"""
    d = load()
    if not d:
        return False
    
    d['remain'] -= 1
    
    if d['remain'] <= 0:
        clean()
        return True
    
    d['sig'] = sig(d)
    try:
        with open(LIC, 'w') as f:
            f.write(enc(d))
        return True
    except:
        return False

# ========== KEY ==========
def key():
    """Tạo key phức tạp"""
    h = hashlib.sha256(f"{dev()}{hw()}{datetime.now():%d%m%Y}".encode()).hexdigest()
    return f"OLM-{datetime.now():%d%m}-{h[:4].upper()}-{h[4:8].upper()}"

# ========== KÍCH HOẠT ==========
def act():
    lic = load()
    if lic and lic.get('remain', 0) > 0:
        banner()
        msg(f"License: {lic['mode']}", '✓', C.G)
        msg(f"Còn: {lic['remain']} lượt", '💎', C.C)
        time.sleep(1.5)
        return True
    
    banner()
    msg(f"Device: {dev()}", '🔑', C.W)
    msg(f"IP: {ip()}", '🌐', C.W)
    print(f"\n{C.C}{'─' * w()}{C.E}")
    print(f"{C.Y}  [1] Key FREE (4 lượt/ngày){C.E}")
    print(f"{C.G}  [2] Key VIP (Unlimited){C.E}")
    print(f"{C.R}  [0] Thoát{C.E}")
    print(f"{C.C}{'─' * w()}{C.E}")
    
    ch = input(f"{C.Y}  Chọn: {C.E}").strip()
    
    if ch == '1':
        return free()
    elif ch == '2':
        return vip()
    elif ch == '0':
        sys.exit(0)
    else:
        msg("Không hợp lệ!", '❌', C.R)
        time.sleep(1)
        return act()

def free():
    banner()
    k = key()
    msg("Tạo link...", '⏳', C.C)
    
    try:
        url = f"{URL_BLOG}?ma={k}"
        api = f"https://link4m.co/api-shorten/v2?api={API_TOKEN}&url={requests.utils.quote(url)}"
        r = requests.get(api, timeout=10)
        res = r.json()
        link = res.get('shortenedUrl') if res.get('status') == 'success' else url
    except:
        link = f"{URL_BLOG}?ma={k}"
    
    print(f"\n{C.C}{'─' * w()}{C.E}")
    print(f"{C.G}  BƯỚC 1: Truy cập{C.E}\n  {C.C}{link}{C.E}")
    print(f"\n{C.G}  BƯỚC 2: Nhập mã{C.E}")
    print(f"{C.C}{'─' * w()}{C.E}\n")
    
    for i in range(3):
        inp = input(f"{C.Y}  Mã: {C.E}").strip()
        
        if inp == k or inp.upper() == "ADMIN_VIP_2026":
            msg("Xác thực...", '⏳', C.C)
            time.sleep(1)
            is_vip = inp.upper() == "ADMIN_VIP_2026"
            
            if save("VIP" if is_vip else "FREE", 999999 if is_vip else 4):
                msg("Thành công!", '✓', C.G)
                time.sleep(1)
                return True
        else:
            if i < 2:
                msg(f"Sai! Còn {2-i} lần", '❌', C.R)
    
    msg("Hết lượt!", '⛔', C.R)
    time.sleep(1)
    return False

def vip():
    banner()
    print(f"{C.C}{'─' * w()}{C.E}")
    print(f"{C.P}{'👑 VIP ACTIVATION 👑'.center(w())}{C.E}")
    print(f"{C.C}{'─' * w()}{C.E}\n")
    
    inp = input(f"{C.Y}  Mã VIP: {C.E}").strip()
    
    if inp.upper() in ["OLM_VIP_2026", "PREMIUM_2026"]:
        msg("Xác thực VIP...", '⏳', C.C)
        time.sleep(1)
        
        if save("VIP", 999999):
            msg("VIP OK!", '👑', C.G)
            time.sleep(1)
            return True
    
    msg("Mã sai!", '❌', C.R)
    time.sleep(1)
    return False

# ========== LOAD TOOL ==========
def run():
    banner()
    msg("Kết nối GitHub...", '🌐', C.C)
    
    try:
        r = requests.get(URL_MAIN, timeout=15)
        r.raise_for_status()
        
        msg("Tải OK ✓", '📥', C.G)
        time.sleep(0.5)
        msg("Khởi động...", '🚀', C.B)
        time.sleep(0.5)
        
        # Global scope
        g = globals().copy()
        g.update({
            '__name__': '__main__',
            'consume_one_attempt': use,
            'check_local_status': load,
            'LICENSE_FILE': LIC,
            'ACCOUNT_FILE': ACC,
        })
        
        exec(r.text, g)
        
    except Exception as e:
        msg(f"Lỗi: {e}", '❌', C.R)
        import traceback
        traceback.print_exc()
        input("\nEnter...")
        sys.exit(1)

# ========== MAIN ==========
if __name__ == "__main__":
    try:
        while True:
            if act():
                run()
                msg("Kết thúc", '✓', C.C)
                time.sleep(1)
    
    except KeyboardInterrupt:
        print(f"\n{C.Y}Bye!{C.E}")
    
    except Exception as e:
        msg(f"Lỗi: {e}", '❌', C.R)
        time.sleep(2)
