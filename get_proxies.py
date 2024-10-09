import requests
from concurrent.futures import ThreadPoolExecutor
import os

# Hàm kiểm tra proxy với IP và cổng, hỗ trợ cả SOCKS và HTTPS
def check_proxy(ip, port):
    proxy = f'{ip}:{port}'
    proxy_socks = {
        'http': f'socks5://{proxy}',
        'https': f'socks5://{proxy}',
    }
    proxy_https = {
        'http': f'http://{proxy}',
        'https': f'https://{proxy}',
    }

    # Kiểm tra proxy SOCKS5
    try:
        response = requests.get("http://httpbin.org/ip", proxies=proxy_socks, timeout=5)
        if response.status_code == 200:
            print(f"Proxy SOCKS5 {proxy} hoạt động.")
            return ('socks', proxy)  # Trả về loại proxy SOCKS5
    except requests.RequestException:
        pass  # Bỏ qua nếu proxy SOCKS không hoạt động

    # Kiểm tra proxy HTTPS
    try:
        response = requests.get("http://httpbin.org/ip", proxies=proxy_https, timeout=5)
        if response.status_code == 200:
            print(f"Proxy HTTPS {proxy} hoạt động.")
            return ('https', proxy)  # Trả về loại proxy HTTPS
    except requests.RequestException:
        pass  # Bỏ qua nếu proxy HTTPS không hoạt động

    return None  # Nếu không có proxy nào hoạt động

# Hàm kiểm tra tất cả các cổng cho một địa chỉ IP
def check_all_ports(ip):
    socks_proxies = []
    https_proxies = []

    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = {executor.submit(check_proxy, ip, port): port for port in range(1, 65536)}
        for future in futures:
            result = future.result()
            if result:
                proxy_type, proxy = result
                if proxy_type == 'socks':
                    socks_proxies.append(proxy)
                elif proxy_type == 'https':
                    https_proxies.append(proxy)

    return socks_proxies, https_proxies

# Hàm tạo file nếu chưa tồn tại
def create_file_if_not_exists(filename):
    if not os.path.exists(filename):
        open(filename, 'w').close()  # Tạo file rỗng

if __name__ == "__main__":
    # Nhập địa chỉ IP của VPS để kiểm tra
    ip_to_check = input("Nhập địa chỉ IP của VPS cần kiểm tra: ")

    # Kiểm tra tất cả các cổng cho địa chỉ IP
    print(f"Đang kiểm tra tất cả các cổng trên IP {ip_to_check}...")
    socks_proxies, https_proxies = check_all_ports(ip_to_check)

    # Tạo file nếu chưa tồn tại và lưu danh sách proxy SOCKS vào file socks_proxies.txt
    socks_filename = 'socks_proxies.txt'
    create_file_if_not_exists(socks_filename)
    if socks_proxies:
        with open(socks_filename, 'w') as f:
            for proxy in socks_proxies:
                f.write(proxy + '\n')
        print(f"Đã lưu danh sách proxy SOCKS vào {socks_filename}")
    else:
        print("Không tìm thấy proxy SOCKS nào hoạt động.")

    # Tạo file nếu chưa tồn tại và lưu danh sách proxy HTTPS vào file https_proxies.txt
    https_filename = 'https_proxies.txt'
    create_file_if_not_exists(https_filename)
    if https_proxies:
        with open(https_filename, 'w') as f:
            for proxy in https_proxies:
                f.write(proxy + '\n')
        print(f"Đã lưu danh sách proxy HTTPS vào {https_filename}")
    else:
        print("Không tìm thấy proxy HTTPS nào hoạt động.")
