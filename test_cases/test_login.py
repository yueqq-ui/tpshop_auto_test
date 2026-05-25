import pytest
from utils.driver_manager import DriverManager
from pages.login_page import LoginPage
import time


class TestLogin:
    def setup_method(self):
        self.driver = DriverManager.get_driver()
        self.login_page = LoginPage(self.driver)
        self.login_page.open_login_page()

    def teardown_method(self):
        DriverManager.quit_driver()

    def test_login_success(self):
        """TC-LOGIN-001: 正常登录"""
        self.login_page.login("13800138006", "123456", "8888")
        time.sleep(3)

        current_url = self.driver.current_url
        print(f"登录后URL: {current_url}")

        # 只要不在登录页，就认为登录成功
        if "login" not in current_url:
            print("✅ 正常登录测试通过")
        else:
            assert False, "登录失败，仍在登录页"

    def test_login_empty_username(self):
        """TC-LOGIN-002: 用户名为空"""
        self.login_page.login("", "123456", "8888")
        time.sleep(2)
        assert "login" in self.driver.current_url
        print("✅ 用户名为空测试通过")

    def test_login_empty_password(self):
        """TC-LOGIN-003: 密码为空"""
        self.login_page.login("13800138006", "", "8888")
        time.sleep(2)
        assert "login" in self.driver.current_url
        print("✅ 密码为空测试通过")

    def test_login_wrong_password(self):
        """TC-LOGIN-004: 密码错误"""
        self.login_page.login("13800138006", "111111", "8888")
        time.sleep(2)
        assert "login" in self.driver.current_url
        print("✅ 密码错误测试通过")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])