import requests
from concurrent.futures import ThreadPoolExecutor

# Hàm kiểm tra proxy từ IP và cổng
def check_proxy(ip, port):
    proxy = f'{ip}:{port}'
    proxy_dict = {
        'http': f'http://{proxy}',
        'https': f'https://{proxy}',
    }

    try:
        response = requests.get("http://httpbin.org/ip", proxies=proxy_dict, timeout=5)
        if response.status_code == 200:
            print(f"Proxy {proxy} hoạt động.")
            return proxy  # Trả về proxy nếu nó hoạt động
    except requests.RequestException:
        pass  # Bỏ qua nếu proxy không hoạt động hoặc có lỗi

    return None

# Hàm kiểm tra tất cả các cổng cho một địa chỉ IP
def check_all_ports(ip):
    working_proxies = []
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = {executor.submit(check_proxy, ip, port): port for port in range(1, 65536)}
        for future in futures:
            result = future.result()
            if result:
                working_proxies.append(result)

    return working_proxies

if __name__ == "__main__":
    # Nhập địa chỉ IP của VPS để kiểm tra
    ip_to_check = input("Nhập địa chỉ IP của VPS cần kiểm tra: ")

    # Kiểm tra tất cả các cổng cho địa chỉ IP
    print(f"Đang kiểm tra tất cả các cổng trên IP {ip_to_check}...")
    working_proxies = check_all_ports(ip_to_check)

    # In danh sách các proxy hoạt động
    if working_proxies:
        print("Các proxy hoạt động tìm thấy:", working_proxies)
        # Lưu danh sách proxy vào tệp
        with open('vps_proxies.txt', 'w') as f:
            for proxy in working_proxies:
                f.write(proxy + '\n')
        print("Đã lưu danh sách proxy vào vps_proxies.txt")
    else:
        print("Không tìm thấy proxy nào hoạt động cho địa chỉ IP này.")
