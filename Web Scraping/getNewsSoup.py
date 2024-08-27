from selenium import webdriver 
from bs4 import BeautifulSoup

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service as ChromeService
from urllib.error import URLError

import time

# Belirli bir URL'den haber sayfasını çeken fonksiyon.
def get_news(url="", day_news=False):
    global timeoutException_count
    global webDriverException_count 
    global urlError_count 
    
    driver_path = "../chromedriver-win32/chromedriver.exe"
    
    try:
        main_url = "https://www.sabah.com.tr"

        full_url = main_url + url

        service = ChromeService(executable_path=driver_path)

        driver = webdriver.Chrome(service=service)

        # Sayfa boyutunu ayarlama
        driver.set_window_size(5, 5)
        
        # Belirtilen URL'yi açma
        driver.get(full_url)
                
        if day_news:
            last_height = -10
            while True:  
                driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                new_height =  driver.execute_script("return document.body.scrollHeight")
            
                if new_height == last_height:
                    break
                last_height = new_height
                time.sleep(1.5)
        
        # Sayfa kaynağını alıp BeautifulSoup kullanarak parse etme
        source = driver.page_source
        soup = BeautifulSoup(source, features="html.parser")

    except TimeoutException:
        return None

    except WebDriverException:
        return None

    except URLError:
        return None

    finally:
        # WebDriver'ı kapatma
        driver.quit()

    # Parse edilmiş HTML içeriğini geri döndürme
    return soup

# Haber içeriğini alan fonksiyon.
def get_content(content_soup, url=""):
    # Haber içeriğini tutacak boş bir string
    news_content = ""   
    # Belirli bir URL'ye özgü div yapısını içeren ana div'i bulma
    top_div = content_soup.find_all("div", attrs={"class": "col-sm-12 view20" + url})
    # Eğer belirli bir div yapısı bulunursa devam et
    if top_div is not None:
        # Her bir ana div içinde dolaş
        for div in top_div:
            # İç içe geçmiş div'ler arasında, içerik div'ini bulma
            inner_div = div.find("div", attrs={"class": "newsDetailText"})
            # Eğer içerik div'i bulunursa devam et
            if inner_div is not None:
                # İçerik div'inin içindeki detay div'ini bulma
                detail_div = inner_div.find("div", attrs={"class": "newsBox selectionShareable"})
                # Eğer detay div'i bulunursa devam et
                if detail_div is not None:
                    # Detay div'i içindeki paragrafları bulma
                    paragraphs = detail_div.find_all('p')
                    # Eğer paragraflar bulunursa devam et
                    if paragraphs is not None:
                        # Her bir paragrafı dolaşarak haber içeriğini birleştirme
                        for paragraph in paragraphs:
                            if paragraph is not None:
                                news_content += paragraph.text
    # Oluşturulan haber içeriğini geri döndürme
    return news_content

# 'roza' URL'sinden haber içeriğini alan fonksiyon.
def get_news_from_roza(content_url):
    # Haber içeriğini tutacak boş bir string
    news_content = ""

    try:
        # Belirli bir 'roza' URL'sine ait haber sayfasını çekme
        soup = get_news(url=content_url)

        # Haber içeriğini içeren div yapısını bulma
        paragraphs = soup.find("div", class_="detail-text-area")

        # Eğer belirli bir div yapısı bulunursa devam et
        if paragraphs is not None:
            # Her bir paragrafı dolaş
            for p in paragraphs.find_all("p"):
                # Eğer paragraf içinde "strong" etiketi yoksa, içeriği birleştir
                if not p.find("strong"):
                    news_content += p.get_text(strip=True) + " "

    except Exception as e:
        print(f"Error : {e}")

    # Oluşturulan haber içeriğini geri döndürme
    return news_content.strip()

def get_news_from_finans(content_url):
    news_content = ""
    
    soup = get_news(url=content_url)
    
    # Haber içeriğini içeren div yapısını bulma
    paragraphs = soup.find("div", attrs={"class" : "detail-text-area"})

    # Eğer belirli bir div yapısı bulunursa devam et
    if paragraphs is not None:
        # Her bir paragrafı dolaş
        for p in paragraphs.find_all("p"):
            # Eğer paragraf içinde "strong" etiketi yoksa, içeriği birleştir
            if p.find("strong") is None:
                news_content += p.text

    # Oluşturulan haber içeriğini geri döndürme
    return news_content