from pages.base_page import BasePage
from selenium.webdriver.common.by import By
import time


class LoginPage(BasePage):
    # 元素定位器
    USERNAME_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, "password")
    VERIFY_CODE_INPUT = (By.NAME, "verify_code")
    LOGIN_BTN = (By.CLASS_NAME, "J-login-submit")  # 修改为正确的class
    ERROR_MSG = (By.CSS_SELECTOR, ".layui-layer-content, .error-message")

    def __init__(self, driver):
        super().__init__(driver)

    def open_login_page(self):
        """打开登录页面"""
        self.driver.get("https://hmshop-test.itheima.net/Home/user/login.html")
        time.sleep(3)
        print(f"✅ 页面已打开，标题：{self.driver.title}")

    def login(self, username, password, verify_code="8888"):
        """执行登录操作"""
        print(f"正在登录：{username}")

        # 输入用户名
        user_input = self.find_element(self.USERNAME_INPUT, timeout=10)
        user_input.clear()
        user_input.send_keys(username)
        print("✅ 用户名已输入")

        # 输入密码
        pwd_input = self.find_element(self.PASSWORD_INPUT, timeout=10)
        pwd_input.clear()
        pwd_input.send_keys(password)
        print("✅ 密码已输入")

        # 输入验证码
        code_input = self.find_element(self.VERIFY_CODE_INPUT, timeout=10)
        code_input.clear()
        code_input.send_keys(verify_code)
        print(f"✅ 验证码已输入：{verify_code}")

        # 点击登录按钮（修改后的定位器）
        login_btn = self.find_element(self.LOGIN_BTN, timeout=10)
        login_btn.click()
        print("✅ 登录按钮已点击")

        time.sleep(3)

    def get_error_message(self):
        """获取错误提示"""
        try:
            return self.get_text(self.ERROR_MSG, timeout=3)
        except:
            return ""

    def is_login_success(self):
        """判断是否登录成功"""
        time.sleep(2)
        current_url = self.driver.current_url
        print(f"当前URL: {current_url}")
        # 登录成功会跳转到首页
        if "index" in current_url or "home" in current_url:
            return True
        # 如果还在登录页，说明登录失败
        return False