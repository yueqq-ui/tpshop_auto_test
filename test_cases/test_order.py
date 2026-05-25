import pytest
from utils.driver_manager import DriverManager
from pages.order_page import OrderPage
from pages.cart_page import CartPage
from pages.login_page import LoginPage
import time


class TestOrder:
    def setup_method(self):
        self.driver = DriverManager.get_driver()
        # 先登录
        login_page = LoginPage(self.driver)
        login_page.open_login_page()
        login_page.login("13800138006", "123456")
        time.sleep(2)

    def teardown_method(self):
        DriverManager.quit_driver()

    def test_submit_order(self):
        """TC-ORDER-001: 提交订单"""
        # 先进入购物车结算
        cart_page = CartPage(self.driver)
        cart_page.open_cart()

        if cart_page.get_item_count() == 0:
            print("⚠️ 购物车为空，跳过测试")
            return

        cart_page.checkout()

        # 提交订单
        order_page = OrderPage(self.driver)
        order_page.submit_order()

        assert order_page.is_order_success()
        print("✅ 提交订单测试通过")

    def test_order_total_calculation(self):
        """TC-ORDER-002: 订单金额计算"""
        cart_page = CartPage(self.driver)
        cart_page.open_cart()

        if cart_page.get_item_count() == 0:
            print("⚠️ 购物车为空，跳过测试")
            return

        cart_total = cart_page.get_total_price()
        cart_page.checkout()

        order_page = OrderPage(self.driver)
        order_total = order_page.get_order_total()

        # 订单金额应该等于购物车总价
        assert abs(order_total - cart_total) < 0.01
        print(f"订单金额: {order_total}, 购物车金额: {cart_total}")
        print("✅ 订单金额计算测试通过")