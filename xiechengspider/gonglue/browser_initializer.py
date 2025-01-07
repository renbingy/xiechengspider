from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from pathlib import Path


class BrowserInitializer:
    def __init__(self, chromedriver: Path = Path('E:/test/chromedriver-win64/chromedriver.exe')) -> None:
        self.chromedriver = chromedriver
    def init_chrome_driver(self) -> webdriver.Chrome:

        chrome_options = Options()
        # /chrome_options.headless = True
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                                    "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920x1080")
        service = Service(self.chromedriver)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver

    def create_wait_object(self, driver: webdriver.Chrome) -> WebDriverWait:
        return WebDriverWait(driver, 10)


if __name__ == '__main__':
    # webdriver_path = Path('E:/test/chromedriver-win64/chromedriver.exe')
    w = BrowserInitializer()
    drive = w.init_chrome_driver()
    drive.get('https://www.baidu.com/')
