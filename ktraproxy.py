import requests
from concurrent.futures import ThreadPoolExecutor

# Hàm kiểm tra proxy
def check_proxy(ip, port):
    proxy = f'{ip}:{port}'
    proxy_dict = {
        'http': proxy,
        'https': proxy,
    }
    try:
        response = requests.get("http://httpbin.org/ip", proxies=proxy_dict, timeout=5)
        if response.status_code == 200:
            print(f"Proxy {proxy} hoạt động.")
            return proxy
    except requests.exceptions.RequestException:
        pass
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
    # Nhập địa chỉ IP để kiểm tra
    ip_to_check = input("Nhập địa chỉ IP cần kiểm tra: ")

    # Kiểm tra tất cả các cổng cho địa chỉ IP
    working_proxies = check_all_ports(ip_to_check)

    # In danh sách các proxy hoạt động
    if working_proxies:
        print("Các proxy hoạt động:", working_proxies)
    else:
        print("Không tìm thấy proxy nào hoạt động cho địa chỉ IP này.")
