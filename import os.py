import os
import speedtest
from ping3 import ping
import platform

def check_network_status():
    # İşletim sistemine göre ping komutunu ayarlama
    param = "-n 1" if platform.system().lower() == "windows" else "-c 1"
    
    # Internet bağlantısı kontrolü
    response = os.system(f"ping {param} google.com > nul 2>&1" if platform.system().lower() == "windows" else f"ping {param} google.com > /dev/null 2>&1")
    
    if response == 0:
        return True
    else:
        return False

def run_speedtest():
    st = speedtest.Speedtest()
    print("Bağlanılabilir sunucular aranıyor...")
    
    # Tüm sunucuları getir
    servers = st.get_servers()
    
    # Tüm sunucuları listele
    print("Bulunan sunucular:")
    for server_group in servers.values():
        for server in server_group:
            print(f"{server['sponsor']} - {server['name']}, {server['country']} ({server['id']})")
    
    # En iyi sunucuyu seç ve göster
    best_server = st.get_best_server()
    print(f"\nBağlanılan sunucu: {best_server['sponsor']} - {best_server['name']}, {best_server['country']} ({best_server['id']})")
    
    # Hız testi yapılıyor
    print("İndirme hızı testi yapılıyor...")
    download_speed = st.download() / 10**6  # Mbps olarak
    print("Yükleme hızı testi yapılıyor...")
    upload_speed = st.upload() / 10**6  # Mbps olarak
    return download_speed, upload_speed

def run_ping_test(host="google.com"):
    print(f"{host} adresine ping testi yapılıyor...")
    try:
        latency = ping(host, timeout=2)  # Ping testini 2 saniye zaman aşımı ile yapar
        return latency
    except Exception as e:
        print(f"Ping testi başarısız: {e}")
        return None

def calculate_packet_loss(host="google.com", count=100):
    """Paket kaybı oranını hesaplayan fonksiyon"""
    print(f"{host} adresine {count} paket gönderiliyor...")
    successful_pings = 0
    
    for i in range(count):
        try:
            response = ping(host, timeout=2)  # Zaman aşımı 2 saniye
            if response:  # Eğer yanıt varsa başarılı
                successful_pings += 1
        except Exception as e:
            print(f"Ping hatası: {e}")
    
    # Başarısız ping sayısı (toplam deneme - başarılı pingler)
    failed_pings = count - successful_pings
    
    # Paket kaybı oranını hesapla
    packet_loss_percentage = (failed_pings / count) * 100
    return packet_loss_percentage

def main():
    if check_network_status():
        print("İnternet bağlantısı mevcut.")
        
        # Hız testi
        download_speed, upload_speed = run_speedtest()
        if download_speed and upload_speed:
            print(f"İndirme Hızı: {download_speed:.2f} Mbps")
            print(f"Yükleme Hızı: {upload_speed:.2f} Mbps")
        
        # Ping testi
        latency = run_ping_test()
        if latency:
            print(f"Ping Gecikmesi: {latency:.2f} ms")
        else:
            print("Ping başarısız.")
        
        # Paket kaybı oranı testi
        packet_loss = calculate_packet_loss(count=100)
        print(f"Paket Kaybı Oranı: %{packet_loss:.2f}")
    else:
        print("İnternet bağlantısı yok!")

if __name__ == "__main__":
    main()
