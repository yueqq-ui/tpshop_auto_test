from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
import time
import os


class DriverManager:
    _driver = None

    @classmethod
    def get_driver(cls, browser="edge"):
        if cls._driver is None:
            if browser == "edge":
                options = Options()

                options.add_argument("--disable-blink-features=AutomationControlled")
                options.add_experimental_option("excludeSwitches", ["enable-automation"])
                options.add_experimental_option("useAutomationExtension", False)
                options.add_argument("--disable-gpu")
                options.add_argument("--no-sandbox")
                options.page_load_strategy = 'eager'

                # 禁止自动下载
                os.environ['SE_AVOID_SELENIUM_MANAGER'] = 'true'

                # 使用你的 EdgeDriver 路径
                service = Service(executable_path=r"C:\Users\ASUS\anaconda3\Scripts\msedgedriver.exe")

                cls._driver = webdriver.Edge(options=options, service=service)

                try:
                    cls._driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                except:
                    pass

                print("✅ Edge 浏览器启动成功")

            cls._driver.maximize_window()
            cls._driver.implicitly_wait(15)
        return cls._driver

    @classmethod
    def quit_driver(cls):
        if cls._driver:
            cls._driver.quit()
            cls._driver = None