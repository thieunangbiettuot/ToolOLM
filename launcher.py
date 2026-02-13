#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OLM MASTER PRO - License Activation System v3.0
Advanced Educational Assistant with Smart Security
"""

import os, sys, time, json, requests, hashlib, uuid, socket, base64
from datetime import datetime, timedelta
from pathlib import Path

# ========== CẤU HÌNH ==========
API_TOKEN = "698b226d9150d31d216157a5"
URL_BLOG = "https://keyfreedailyolmvip.blogspot.com/2026/02/blog-post.html"
URL_MAIN_TOOL = "https://raw.githubusercontent.com/thieunangbiettuot/ToolOLM/refs/heads/main/main.py"

# Lưu file ở chỗ KHÓ TÌM
def get_data_dir():
    """Lấy thư mục lưu data (ẩn)"""
    if os.name == 'nt':  # Windows
        base = os.environ.get('APPDATA') or os.path.expanduser('~')
        data_dir = os.path.join(base, '.cache', 'Microsoft', 'EdgeUpdate')
    else:  # Linux/Mac
        base = os.path.expanduser('~')
        data_dir = os.path.join(base, '.cache', 'fontconfig')
    
    os.makedirs(data_dir, exist_ok=True)
    return data_dir

DATA_DIR = get_data_dir()
LICENSE_FILE = os.path.join(DATA_DIR, '.sysconf.dat')
ACCOUNT_FILE = os.path.join(DATA_DIR, '.userdata.dat')

# Mã hóa key (XOR + Base64)
ENCRYPT_KEY = b'OLM_MASTER_PRO_2026_SECRET_KEY_ULTRA_SECURE'

def encrypt(data):
    """Mã hóa dữ liệu"""
    text = json.dumps(data).encode()
    encrypted = bytearray()
    for i, byte in enumerate(text):
        encrypted.append(byte ^ ENCRYPT_KEY[i % len(ENCRYPT_KEY)])
    return base64.b85encode(bytes(encrypted)).decode()

def decrypt(encrypted_text):
    """Giải mã dữ liệu"""
    try:
        encrypted = base64.b85decode(encrypted_text.encode())
        decrypted = bytearray()
        for i, byte in enumerate(encrypted):
            decrypted.append(byte ^ ENCRYPT_KEY[i % len(ENCRYPT_KEY)])
        return json.loads(bytes(decrypted).decode())
    except:
        return None

# ========== MÀU SẮC ==========
class C:
    R='\033[91m';G='\033[92m';Y='\033[93m';B='\033[94m';C='\033[96m';W='\033[97m';P='\033[95m';E='\033[0m'

# ========== TIỆN ÍCH ==========
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def w():
    """Get terminal width"""
    try:
        return min(os.get_terminal_size().columns - 4, 68)
    except:
        return 60

def line(char='─'):
    print(f"{C.C}{char * w()}{C.E}")

def banner():
    clear()
    print()
    line('═')
    print(f"{C.B}{'OLM MASTER PRO - Education Assistant v3.0'.center(w())}{C.E}")
    print(f"{C.P}{'Powered by Advanced AI Technology'.center(w())}{C.E}")
    line('═')
    print()

def msg(text, icon='•', color=C.W):
    print(f"  {icon} {color}{text}{C.E}")

# ========== HỆ THỐNG ==========
def get_device_id():
    try:
        data = f"{socket.gethostname()}{os.name}{uuid.getnode()}"
        return hashlib.md5(data.encode()).hexdigest()[:16].upper()
    except:
        return "DEVICE_UNKNOWN"

def get_ip():
    try:
        return requests.get('https://api.ipify.org', timeout=5).text.strip()
    except:
        return "0.0.0.0"

def get_hwid():
    """Hardware ID - Kết hợp nhiều yếu tố"""
    try:
        hw = f"{uuid.getnode()}{os.name}{sys.platform}"
        return hashlib.sha256(hw.encode()).hexdigest()[:24]
    except:
        return "HWID_UNKNOWN"

# ========== BẢO MẬT NÂNG CAO ==========
def generate_key_signature(key_data):
    """Tạo chữ ký cho key để chống giả mạo"""
    sig_str = f"{key_data['mode']}{key_data['expire']}{key_data['ip']}{key_data['device']}"
    return hashlib.sha256(sig_str.encode()).hexdigest()[:16]

def verify_license_integrity(data):
    """Kiểm tra tính toàn vẹn của license"""
    expected_sig = generate_key_signature(data)
    return data.get('signature') == expected_sig

# ========== LICENSE ==========
def load_license():
    if not os.path.exists(LICENSE_FILE):
        return None
    try:
        with open(LICENSE_FILE, 'r') as f:
            encrypted = f.read()
        
        data = decrypt(encrypted)
        if not data:
            cleanup_license()
            return None
        
        # Check hết hạn
        expire = datetime.strptime(data.get('expire'), "%d/%m/%Y")
        if expire.date() != datetime.now().date():
            cleanup_license()
            return None
        
        # Verify signature
        if not verify_license_integrity(data):
            msg("Phát hiện license bị chỉnh sửa!", '⚠', C.R)
            cleanup_license()
            return None
        
        # Check IP + Device + HWID
        if (data.get('ip') == get_ip() and 
            data.get('device') == get_device_id() and
            data.get('hwid') == get_hwid()):
            
            if data.get('remain', 0) > 0:
                return data
        else:
            msg("Phát hiện thay đổi thiết bị hoặc IP!", '⚠', C.Y)
            cleanup_license()
        
        return None
    except:
        cleanup_license()
        return None

def cleanup_license():
    """Xóa license và account khi hết hạn"""
    try:
        if os.path.exists(LICENSE_FILE):
            os.remove(LICENSE_FILE)
        if os.path.exists(ACCOUNT_FILE):
            os.remove(ACCOUNT_FILE)
    except:
        pass

def save_license(mode, remain):
    data = {
        'mode': mode,
        'remain': remain,
        'expire': datetime.now().strftime("%d/%m/%Y"),
        'ip': get_ip(),
        'device': get_device_id(),
        'hwid': get_hwid(),
        'created': datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }
    
    # Tạo signature
    data['signature'] = generate_key_signature(data)
    
    try:
        encrypted = encrypt(data)
        with open(LICENSE_FILE, 'w') as f:
            f.write(encrypted)
        return True
    except:
        return False

def consume_attempt():
    data = load_license()
    if not data:
        return False
    
    data['remain'] -= 1
    data['last_used'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    if data['remain'] <= 0:
        cleanup_license()
        return True
    
    # Update signature
    data['signature'] = generate_key_signature(data)
    
    try:
        encrypted = encrypt(data)
        with open(LICENSE_FILE, 'w') as f:
            f.write(encrypted)
        return True
    except:
        return False

# ========== TẠO KEY PHỨC TẠP HƠN ==========
def generate_daily_key():
    """Tạo key phức tạp, khó đoán"""
    device = get_device_id()
    hwid = get_hwid()
    date = datetime.now().strftime("%d%m%Y")
    
    # Kết hợp nhiều yếu tố
    key_base = f"{device}{hwid}{date}"
    key_hash = hashlib.sha256(key_base.encode()).hexdigest()
    
    # Format: OLM-DDMM-XXXX-YYYY
    part1 = datetime.now().strftime("%d%m")
    part2 = key_hash[:4].upper()
    part3 = key_hash[4:8].upper()
    
    return f"OLM-{part1}-{part2}-{part3}"

# ========== KÍCH HOẠT ==========
def activate():
    lic = load_license()
    
    if lic and lic.get('remain', 0) > 0:
        banner()
        msg(f"License: {lic['mode']}", '✓', C.G)
        msg(f"Còn lại: {lic['remain']} lượt", '💎', C.C)
        msg(f"Hết hạn: {lic['expire']}", '⏰', C.Y)
        time.sleep(2)
        return True
    
    banner()
    
    device = get_device_id()
    ip = get_ip()
    
    msg(f"Device ID: {device}", '🔑', C.W)
    msg(f"IP Address: {ip}", '🌐', C.W)
    print()
    line()
    print(f"{C.Y}  [1] 🎁 Key FREE (4 lượt/ngày){C.E}")
    print(f"{C.G}  [2] 👑 Key VIP Premium (Unlimited){C.E}")
    print(f"{C.C}  [3] ℹ️  Thông tin gói VIP{C.E}")
    print(f"{C.P}  [4] 📊 Thống kê hệ thống{C.E}")
    print(f"{C.R}  [0] 🚪 Thoát{C.E}")
    line()
    
    choice = input(f"{C.Y}  ➤ Chọn: {C.E}").strip()
    
    if choice == '1':
        return activate_free()
    elif choice == '2':
        return activate_vip()
    elif choice == '3':
        show_vip_info()
        return activate()
    elif choice == '4':
        show_stats()
        return activate()
    elif choice == '0':
        msg("Tạm biệt! Hẹn gặp lại 👋", '✨', C.C)
        sys.exit(0)
    else:
        msg("Lựa chọn không hợp lệ!", '❌', C.R)
        time.sleep(1)
        return activate()

def activate_free():
    banner()
    
    daily_key = generate_daily_key()
    
    msg("Đang tạo link kích hoạt...", '⏳', C.C)
    time.sleep(1)
    
    # URL với ?ma=
    full_url = f"{URL_BLOG}?ma={daily_key}"
    
    try:
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
    line('─')
    print(f"{C.G}  📋 BƯỚC 1: Truy cập link để lấy mã{C.E}")
    line('─')
    print(f"{C.C}  {short_link}{C.E}")
    print()
    line('─')
    print(f"{C.G}  🔐 BƯỚC 2: Nhập mã kích hoạt{C.E}")
    line('─')
    print(f"{C.Y}  Format mã: OLM-DDMM-XXXX-YYYY{C.E}")
    print()
    
    for attempt in range(3):
        key_input = input(f"{C.Y}  🔑 Nhập mã: {C.E}").strip()
        
        # Check key
        if key_input == daily_key:
            print()
            msg("Đang xác thực...", '⏳', C.C)
            time.sleep(1.5)
            
            if save_license("FREE", 4):
                msg("🎉 Kích hoạt FREE thành công!", '✓', C.G)
                msg("Bạn có 4 lượt sử dụng hôm nay", '💎', C.C)
                time.sleep(2)
                return True
        elif key_input.upper() in ["ADMIN_PREMIUM_2026", "VIP_UNLIMITED_2026"]:
            # Admin key
            print()
            msg("Đang xác thực VIP...", '⏳', C.C)
            time.sleep(1.5)
            
            if save_license("VIP", 999999):
                msg("👑 Kích hoạt VIP thành công!", '✓', C.G)
                msg("Bạn có UNLIMITED lượt sử dụng!", '🌟', C.C)
                time.sleep(2)
                return True
        else:
            remaining = 2 - attempt
            if remaining > 0:
                msg(f"❌ Sai mã! Còn {remaining} lần thử", '⚠', C.R)
                print()
            else:
                msg("⛔ Hết lượt thử! Vui lòng lấy link mới.", '✗', C.R)
                time.sleep(2)
                return False
    
    return False

def activate_vip():
    banner()
    
    line('─')
    print(f"{C.G}{'👑 VIP PREMIUM ACTIVATION 👑'.center(w())}{C.E}")
    line('─')
    print()
    
    vip_key = input(f"{C.Y}  🔐 Nhập mã VIP: {C.E}").strip()
    
    valid_keys = [
        "OLM_VIP_2026_PREMIUM",
        "PREMIUM_UNLIMITED_2026",
        "VIP_MASTER_PRO_2026"
    ]
    
    if vip_key.upper() in valid_keys:
        print()
        msg("Đang xác thực VIP Premium...", '⏳', C.C)
        time.sleep(2)
        
        if save_license("VIP", 999999):
            msg("🎊 Kích hoạt VIP Premium thành công!", '✓', C.G)
            msg("Chào mừng bạn đến với VIP Club! 🌟", '👑', C.P)
            time.sleep(2)
            return True
    
    msg("❌ Mã VIP không hợp lệ!", '✗', C.R)
    time.sleep(2)
    return False

def show_vip_info():
    banner()
    
    line('═')
    print(f"{C.P}{'👑 VIP PREMIUM PACKAGE 👑'.center(w())}{C.E}")
    line('═')
    print()
    
    features = [
        ("🚀 Unlimited lượt giải bài", C.G),
        ("⚡ Tốc độ xử lý nhanh x2", C.C),
        ("🛡️  Hỗ trợ kỹ thuật 24/7", C.Y),
        ("🎁 Tính năng độc quyền", C.P),
        ("📱 Hỗ trợ đa thiết bị", C.B),
        ("🔄 Cập nhật tự động", C.G)
    ]
    
    for feat, color in features:
        msg(feat, '✓', color)
    
    print()
    line('─')
    print(f"{C.Y}  💰 GIÁ: {C.G}{C.B}50.000 VNĐ/tháng{C.E}")
    print(f"{C.Y}  💎 Ưu đãi: {C.G}140K/3 tháng (Tiết kiệm 10K){C.E}")
    line('─')
    print()
    print(f"{C.C}  📞 LIÊN HỆ MUA VIP:{C.E}")
    print(f"{C.W}  • Zalo: 0123456789{C.E}")
    print(f"{C.W}  • Email: vip@olmmaster.pro{C.E}")
    print(f"{C.W}  • Facebook: fb.com/olmmaster{C.E}")
    print()
    
    input(f"{C.Y}Nhấn Enter để quay lại...{C.E}")

def show_stats():
    """Hiển thị thống kê hệ thống"""
    banner()
    
    line('═')
    print(f"{C.C}{'📊 THỐNG KÊ HỆ THỐNG 📊'.center(w())}{C.E}")
    line('═')
    print()
    
    # Thông tin thiết bị
    msg(f"Device ID: {get_device_id()}", '🔑', C.W)
    msg(f"Hardware ID: {get_hwid()}", '🔧', C.W)
    msg(f"IP Address: {get_ip()}", '🌐', C.W)
    msg(f"Platform: {sys.platform}", '💻', C.W)
    msg(f"Python: {sys.version.split()[0]}", '🐍', C.W)
    
    print()
    
    # License info
    lic = load_license()
    if lic:
        line('─')
        print(f"{C.G}  LICENSE HIỆN TẠI:{C.E}")
        line('─')
        msg(f"Loại: {lic['mode']}", '👑' if lic['mode'] == 'VIP' else '🎁', C.G)
        msg(f"Còn lại: {lic['remain']} lượt", '💎', C.C)
        msg(f"Hết hạn: {lic['expire']}", '⏰', C.Y)
        msg(f"Kích hoạt: {lic.get('created', 'N/A')}", '📅', C.W)
        if lic.get('last_used'):
            msg(f"Dùng lần cuối: {lic['last_used']}", '🕐', C.W)
    else:
        line('─')
        msg("Chưa kích hoạt license", '⚠', C.Y)
        line('─')
    
    print()
    input(f"{C.Y}Nhấn Enter để quay lại...{C.E}")

# ========== LOAD TOOL ==========
def load_tool():
    banner()
    
    msg("Đang kết nối GitHub...", '🌐', C.C)
    
    try:
        resp = requests.get(URL_MAIN_TOOL, timeout=15)
        resp.raise_for_status()
        
        msg("Đã tải module chính ✓", '📥', C.G)
        time.sleep(1)
        
        msg("Đang khởi động OLM Master Pro...", '🚀', C.B)
        time.sleep(1)
        
        # Truyền hàm vào global scope của main.py
        exec_globals = globals().copy()
        exec_globals.update({
            '__name__': '__main__',
            'consume_one_attempt': consume_attempt,
            'check_local_status': load_license,
            'LICENSE_FILE': LICENSE_FILE,
            'ACCOUNT_FILE': ACCOUNT_FILE,
        })
        
        # Chạy main.py
        exec(resp.text, exec_globals)
        
    except requests.exceptions.RequestException as e:
        msg("❌ Không thể kết nối GitHub!", '✗', C.R)
        msg(f"Chi tiết: {e}", 'ℹ', C.Y)
        msg("Kiểm tra kết nối Internet", 'ℹ', C.Y)
        input("\nNhấn Enter...")
        sys.exit(1)
    except Exception as e:
        msg(f"❌ Lỗi: {e}", '✗', C.R)
        import traceback
        traceback.print_exc()
        input("\nNhấn Enter...")
        sys.exit(1)

# ========== MAIN ==========
if __name__ == "__main__":
    try:
        while True:
            if activate():
                load_tool()
                msg("Phiên làm việc đã kết thúc", '✓', C.C)
                time.sleep(2)
            
    except KeyboardInterrupt:
        print(f"\n\n{C.Y}  👋 Tạm biệt!{C.E}\n")
    except Exception as e:
        msg(f"Lỗi: {e}", '❌', C.R)
        time.sleep(3)
