import os
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# ================= AYARLAR =================
# Chromedriver yolun (önceki adımlarda /usr/bin/chromedriver yapmıştık)
CHROMEDRIVER_PATH = "/usr/bin/chromedriver" 
OUTPUT_DIR = "/storage/workspace/m00836648/youtube_login_tool/extracted_cookies"

# Hangi profili elle açtıysan dosya ismine onu yazalım
CURRENT_PROFILE_NAME = "Default" 

def main():
    print(f"--- '{CURRENT_PROFILE_NAME}' Profiline Bağlanılıyor ---")
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Selenium Ayarları
    chrome_options = Options()
    # EN ÖNEMLİ KISIM: Var olan 9222 portuna bağlan diyoruz
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    service = Service(executable_path=CHROMEDRIVER_PATH)
    
    driver = None
    try:
        print("Açık olan Chrome'a bağlanılıyor...")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print(f"✅ Bağlantı Başarılı!")
        print(f"Sayfa Başlığı: {driver.title}")
        
        if "Portal" in driver.title:
            print("⚠️ UYARI: Sayfa hala Portal'da görünüyor. Lütfen ekrandan girişi tamamlayın.")
        
        # O an açık olan sayfanın cookie'lerini al
        cookies = driver.get_cookies()
        
        if cookies:
            print(f"✅ {len(cookies)} adet cookie çekildi.")
            
            # Kaydet
            safe_name = CURRENT_PROFILE_NAME.replace(" ", "_")
            file_path = os.path.join(OUTPUT_DIR, f"cookies_{safe_name}.txt")
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("# Netscape HTTP Cookie File\n\n")
                for c in cookies:
                    # Domain kontrolü
                    if "youtube" in c.get("domain", "") or "google" in c.get("domain", ""):
                        domain = c.get("domain", "")
                        flag = "TRUE" if domain.startswith(".") else "FALSE"
                        path = c.get("path", "/")
                        secure = "TRUE" if c.get("secure") else "FALSE"
                        expiry = int(c.get('expiry', time.time() + 31536000))
                        name = c.get("name", "")
                        value = c.get("value", "")
                        
                        f.write(f"{domain}\t{flag}\t{path}\t{secure}\t{expiry}\t{name}\t{value}\n")
            
            print(f"💾 Dosya kaydedildi: {file_path}")
        else:
            print("⚠️ Cookie bulunamadı. YouTube sayfası tam yüklenmedi mi?")

    except Exception as e:
        print("\n❌ HATA OLUŞTU:")
        print(str(e))
        print("Lütfen Chrome'un '--remote-debugging-port=9222' ile başlatıldığından emin olun.")

    finally:
        # Chrome'u kapatmamak için quit() çağırmıyoruz, sadece memory'den siliyoruz
        print("İşlem tamamlandı.")

if __name__ == "__main__":
    main()
