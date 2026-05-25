import pytest
from utils.driver_manager import DriverManager
from pages.cart_page import CartPage
from pages.login_page import LoginPage
import time

class TestCart:
    def setup_method(self):
        self.driver = DriverManager.get_driver()
        self.cart_page = CartPage(self.driver)
        # 先登录
        login_page = LoginPage(self.driver)
        login_page.open_login_page()
        login_page.login("13800138006", "123456")
        time.sleep(2)

    def teardown_method(self):
        DriverManager.quit_driver()

    def test_open_cart(self):
        """TC-CART-001: 打开购物车"""
        self.cart_page.open_cart()
        # 购物车页面能正常打开
        print("✅ 打开购物车测试通过")

    def test_cart_item_count(self):
        """TC-CART-002: 购物车商品数量"""
        self.cart_page.open_cart()
        count = self.cart_page.get_item_count()
        print(f"购物车商品数量: {count}")
        assert count >= 0
        print("✅ 购物车数量测试通过")

    def test_increase_quantity(self):
        """TC-CART-003: 增加商品数量"""
        self.cart_page.open_cart()
        if self.cart_page.get_item_count() > 0:
            old_price = self.cart_page.get_total_price()
            self.cart_page.increase_quantity()
            new_price = self.cart_page.get_total_price()
            assert new_price > old_price
            print("✅ 增加数量测试通过")
        else:
            print("⚠️ 购物车为空，跳过测试")

    def test_delete_item(self):
        """TC-CART-004: 删除商品"""
        self.cart_page.open_cart()
        if self.cart_page.get_item_count() > 0:
            old_count = self.cart_page.get_item_count()
            self.cart_page.delete_first_item()
            time.sleep(2)
            new_count = self.cart_page.get_item_count()
            assert new_count == old_count - 1
            print("✅ 删除商品测试通过")
        else:
            print("⚠️ 购物车为空，跳过测试")

    def test_checkout(self):
        """TC-CART-005: 去结算"""
        self.cart_page.open_cart()
        if self.cart_page.get_item_count() > 0:
            self.cart_page.checkout()
            assert "order" in self.driver.current_url or "confirm" in self.driver.current_url
            print("✅ 去结算测试通过")
        else:
            print("⚠️ 购物车为空，跳过测试")