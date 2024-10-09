from cryptography.fernet import Fernet

def generate_key():
    """Tạo một khóa mã hóa mới và lưu vào file."""
    key = Fernet.generate_key()
    with open('secret.key', 'wb') as key_file:
        key_file.write(key)
    print("Khóa mã hóa đã được tạo và lưu vào 'secret.key'.")

def load_key():
    """Tải khóa mã hóa từ file."""
    return open('secret.key', 'rb').read()

def encrypt_message(message):
    """Mã hóa thông điệp."""
    key = load_key()
    fernet = Fernet(key)
    encrypted_message = fernet.encrypt(message.encode())
    return encrypted_message

def decrypt_message(encrypted_message):
    """Giải mã thông điệp."""
    key = load_key()
    fernet = Fernet(key)
    decrypted_message = fernet.decrypt(encrypted_message).decode()
    return decrypted_message

if __name__ == "__main__":
    # Tạo khóa mã hóa (chỉ chạy lần đầu tiên)
    generate_key()

    # Nhập thông điệp để mã hóa
    message = input("Nhập thông điệp để mã hóa: ")
    encrypted = encrypt_message(message)
    print(f"Thông điệp đã mã hóa: {encrypted}")

    # Giải mã thông điệp
    decrypted = decrypt_message(encrypted)
    print(f"Thông điệp đã giải mã: {decrypted}")
