import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

def encrypt_python_file(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()
    key = get_random_bytes(32)
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv
    encrypted_data = cipher.encrypt(pad(data, AES.block_size))

    with open("encrypted_payload.dat", "wb") as f:
        f.write(iv + encrypted_data)

    with open("secret.key", "wb") as f:
        f.write(key)

    print(f"[+] '{file_path}' 암호화 완료.")
    print("[+] 생성됨: encrypted_payload.dat, secret.key")

if __name__ == "__main__":
    target_file = "test.py"#edit
    encrypt_python_file(target_file)
