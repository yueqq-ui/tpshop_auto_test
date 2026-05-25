from pages.base_page import BasePage
from selenium.webdriver.common.by import By
import time


class OrderPage(BasePage):
    # 元素定位器
    ADDRESS_SELECT = (By.CSS_SELECTOR, ".address-item")
    ADD_ADDRESS_BTN = (By.XPATH, "//button[contains(text(),'新增地址')]")
    RECEIVER_NAME = (By.NAME, "consignee")
    RECEIVER_PHONE = (By.NAME, "mobile")
    RECEIVER_ADDRESS = (By.NAME, "address")
    SAVE_ADDRESS_BTN = (By.XPATH, "//button[contains(text(),'保存')]")

    ORDER_TOTAL = (By.CSS_SELECTOR, ".order-total, .total-amount")
    SUBMIT_ORDER_BTN = (By.XPATH, "//button[contains(text(),'提交订单')]")
    PAYMENT_METHOD = (By.CSS_SELECTOR, ".payment-method")

    ORDER_SUCCESS = (By.CSS_SELECTOR, ".order-success")
    ORDER_NUMBER = (By.CSS_SELECTOR, ".order-number")

    def __init__(self, driver):
        super().__init__(driver)

    def select_address(self, index=0):
        """选择地址"""
        addresses = self.driver.find_elements(*self.ADDRESS_SELECT)
        if addresses:
            addresses[index].click()

    def add_new_address(self, name, phone, address):
        """新增地址"""
        self.click(self.ADD_ADDRESS_BTN)
        time.sleep(1)
        self.input_text(self.RECEIVER_NAME, name)
        self.input_text(self.RECEIVER_PHONE, phone)
        self.input_text(self.RECEIVER_ADDRESS, address)
        self.click(self.SAVE_ADDRESS_BTN)
        time.sleep(1)

    def get_order_total(self):
        """获取订单总金额"""
        text = self.get_text(self.ORDER_TOTAL)
        import re
        numbers = re.findall(r"[\d.]+", text)
        return float(numbers[0]) if numbers else 0

    def submit_order(self):
        """提交订单"""
        self.click(self.SUBMIT_ORDER_BTN)
        time.sleep(3)

    def is_order_success(self):
        """判断订单是否提交成功"""
        return self.is_element_visible(self.ORDER_SUCCESS, timeout=5)

    def get_order_number(self):
        """获取订单号"""
        return self.get_text(self.ORDER_NUMBER)