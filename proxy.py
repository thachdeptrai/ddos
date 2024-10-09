import requests
from bs4 import BeautifulSoup

# URL của trang chứa danh sách proxy
url = 'http://nrokimdung.xyz/'

# Gửi yêu cầu GET đến trang mà không xác thực chứng chỉ SSL
response = requests.get(url, verify=False)

# Kiểm tra trạng thái phản hồi
if response.status_code == 200:
    # Phân tích HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Tìm bảng chứa danh sách proxy
    proxy_table = soup.find('table')  # Tìm bảng đầu tiên
    proxies = []

    # Lặp qua các hàng trong bảng
    if proxy_table:
        for row in proxy_table.find_all('tr')[1:]:  # Bỏ qua hàng tiêu đề
            cols = row.find_all('td')
            if len(cols) >= 2:  # Kiểm tra có đủ cột
                ip = cols[0].text.strip()  # Địa chỉ IP
                port = cols[1].text.strip()  # Cổng
                proxies.append(f'{ip}:{port}')

    # In danh sách proxy
    if proxies:
        print("Danh sách proxy:")
        for proxy in proxies:
            print(proxy)
    else:
        print("Không tìm thấy proxy.")
else:
    print("Không thể lấy danh sách proxy. Mã lỗi:", response.status_code)
