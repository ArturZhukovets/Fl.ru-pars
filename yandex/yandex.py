from bs4 import BeautifulSoup
import lxml
import requests
import json
from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service

# url = 'https://eda.yandex.ru/moscow?shippingType=delivery'

def get_data(url):
    service = Service(executable_path=r"C:\py\WEB-SCRAPING\yandex\ChromeDriver\chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    try:
        driver.get(url=url)
        # time.sleep(1)
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)


    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()

    with open('index.html', 'r', encoding='utf-8') as f:
        src = f.read()
    soup = BeautifulSoup(src, 'lxml')
    cont = soup.find('ul', class_='PlaceListInner_placesList PlaceListInner_lg')
    print(cont)
    # headers = {
    #     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
    # }
    # cookies = {'cookies': 'yandexuid=7355491841646500839; yuidss=7355491841646500839; ymex=1961860839.yrts.1646500839#1961860839.yrtsi.1646500839; gdpr=0; _ym_d=1646500895; _ym_uid=1626868350166973221; is_gdpr=0; my=YwA=; is_gdpr_b=CPrlYRCZZigC; amcuid=5058442621647185840; skid=5038780991648484587; Cookie_check=CheckCookieCheckCookie; L=YVpxXQF6Y3kOZEdQB1NuD3FCSmp7WFVFAAERKiosFQsfFA==.1648836189.14934.32456.96b33c941ea7bb1148e92179f6fb40f9; yandex_login=dubinaartu; i=yAAV2nTR7LkVVLFNGuGNxXhgvXTAswmHGc2EjT5fIV9licD9smVd37RbgwIoumz5FmIH9wrCBQqm5GRldXNvpL/JBvc=; ys=udn.cDpkdWJpbmFhcnR1#c_chck.2640661939; Session_id=3:1654899038.5.1.1646500897689:pRjXJQ:2a.1.2:1|554299124.-1.0.1:97866445|901273685.2335292.2.2:2335292|3:253645.841196.YoEaPfciIeMe16aGBCDOQsU7wPM; sessionid2=3:1654899038.5.1.1646500897689:pRjXJQ:2a.1.2:1.499:1|554299124.-1.0.1:97866445|901273685.2335292.2.2:2335292|3:253645.25323.s5tuUm28BNjOlCs3Wf_PuSSkt6U; _ym_isad=2; PHPSESSID=abcdd6cffc6f47b1aacfb495859be3c2; _yasc=F/61op8+ZaR8Nexzay46TazgQyc84ZYnlwHcoHSRNPNrUQIkNgU=; yp=1658399376.csc.1#1656941311.szm.1:1920x1080:1920x937; eda_web={"app":{"lat":null,"lon":null,"ipLat":null,"ipLon":null,"deliveryTime":null,"xDeviceId":"l4wr629d-eluxotqcok-o47k8su87ds-rxhpd3mf99","appBannerShown":false,"isAdult":null,"yandexPlusCashbackOptInChecked":false,"testRunId":null,"initialPromocode":null,"themeVariantKey":"light"}}' }

    # req = requests.get(url, headers=headers, cookies=cookies)
    # soup = BeautifulSoup(req.text, 'lxml')

    # all_cards = []
    # cont = soup.find('div').find('div', class_='UILoader_root').find('div', class_='AppDefaultLayout_container').find('div', class_='DesktopCatalogPage_content').find_all('a')



def main():
    get_data('https://eda.yandex.ru/moscow?shippingType=delivery')


if __name__ == '__main__':
    main()