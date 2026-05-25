from pages.base_page import BasePage
from selenium.webdriver.common.by import By
import time


class CartPage(BasePage):
    # 元素定位器
    CART_ICON = (By.CSS_SELECTOR, ".cart-icon")
    CART_ITEM = (By.CSS_SELECTOR, ".cart-item, .cart-goods-item")
    QUANTITY_PLUS = (By.CSS_SELECTOR, ".quantity-plus")
    QUANTITY_MINUS = (By.CSS_SELECTOR, ".quantity-minus")
    QUANTITY_INPUT = (By.CSS_SELECTOR, ".quantity-input")
    DELETE_BTN = (By.CSS_SELECTOR, ".delete-btn, .remove-btn")
    CHECKBOX = (By.CSS_SELECTOR, ".checkbox, .select-checkbox")
    SELECT_ALL = (By.CSS_SELECTOR, ".select-all")
    TOTAL_PRICE = (By.CSS_SELECTOR, ".total-price, .settlement-amount")
    CHECKOUT_BTN = (By.XPATH, "//button[contains(text(),'结算')]")
    EMPTY_CART = (By.XPATH, "//div[contains(text(),'购物车是空的')]")

    def __init__(self, driver):
        super().__init__(driver)

    def open_cart(self):
        """打开购物车"""
        self.driver.get("https://hmshop-test.itheima.net/Home/cart/index.html")
        time.sleep(2)

    def get_item_count(self):
        """获取购物车商品数量"""
        return len(self.driver.find_elements(*self.CART_ITEM))

    def increase_quantity(self):
        """增加数量"""
        self.click(self.QUANTITY_PLUS)
        time.sleep(0.5)

    def decrease_quantity(self):
        """减少数量"""
        self.click(self.QUANTITY_MINUS)
        time.sleep(0.5)

    def delete_first_item(self):
        """删除第一个商品"""
        self.click(self.DELETE_BTN)
        time.sleep(1)
        # 处理确认弹窗
        try:
            confirm = self.driver.find_element(By.XPATH, "//button[contains(text(),'确认')]")
            confirm.click()
        except Exception as e:
            print(f"处理弹窗时出错:{e}")
    def select_all(self):
        """全选"""
        self.click(self.SELECT_ALL)

    def get_total_price(self):
        """获取总价"""
        text = self.get_text(self.TOTAL_PRICE)
        import re
        numbers = re.findall(r"[\d.]+", text)
        return float(numbers[0]) if numbers else 0

    def checkout(self):
        """去结算"""
        self.click(self.CHECKOUT_BTN)
        time.sleep(2)

    def is_empty(self):
        """购物车是否为空"""
        return len(self.driver.find_elements(*self.EMPTY_CART)) > 0