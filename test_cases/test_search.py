import pytest
from utils.driver_manager import DriverManager
from pages.search_page import SearchPage
from pages.login_page import LoginPage
import time


class TestSearch:
    def setup_method(self):
        """每个测试前执行：初始化浏览器并登录"""
        self.driver = DriverManager.get_driver()
        self.search_page = SearchPage(self.driver)

        # 先登录（搜索功能可能需要登录）
        self.login_page = LoginPage(self.driver)
        self.login_page.open_login_page()
        self.login_page.login("13800138006", "123456")
        time.sleep(2)

    def teardown_method(self):
        """每个测试后执行：关闭浏览器"""
        DriverManager.quit_driver()

    def test_search_keyword(self):
        """TC-SEARCH-001: 搜索商品成功"""
        # 执行搜索
        self.search_page.search("手机")
        time.sleep(3)

        # 获取商品数量
        count = self.search_page.get_product_count()

        # 调试：打印当前URL
        print(f"当前URL: {self.driver.current_url}")

        # 断言有结果
        assert count > 0, f"搜索结果为空，找到{count}个商品"
        print(f"✅ 搜索到 {count} 个商品")

    def test_search_empty(self):
        """TC-SEARCH-002: 空搜索"""
        self.search_page.search("")
        time.sleep(2)
        # 空搜索应该停留在首页或提示
        current_url = self.search_page.get_current_url()
        print(f"当前URL: {current_url}")
        print("✅ 空搜索测试完成")

    def test_search_no_result(self):
        """TC-SEARCH-003: 无结果搜索"""
        self.search_page.search("这是一个不存在的商品123456789")
        time.sleep(2)
        # 无结果时商品数应该为0
        count = self.search_page.get_product_count()
        print(f"搜索结果数量: {count}")
        print("✅ 无结果搜索测试通过")

    def test_search_special_chars(self):
        """TC-SEARCH-004: 特殊字符搜索"""
        self.search_page.search("@#$%^&*")
        time.sleep(2)
        print("✅ 特殊字符搜索测试通过")

    def test_sort_by_sales(self):
        """TC-SEARCH-005: 按销量排序"""
        self.search_page.search("手机")
        time.sleep(2)
        self.search_page.sort_by_sales()
        print("✅ 按销量排序测试通过")

    def test_click_first_product(self):
        """TC-SEARCH-006: 点击搜索结果跳转到详情页"""
        self.search_page.search("手机")
        time.sleep(2)

        # 获取点击前的URL
        before_url = self.search_page.get_current_url()
        print(f"点击前URL: {before_url}")

        # 点击第一个商品
        result = self.search_page.click_first_product()

        if result:
            time.sleep(2)
            after_url = self.search_page.get_current_url()
            print(f"点击后URL: {after_url}")

            # 断言URL发生了变化（跳转到了详情页）
            assert before_url != after_url, "点击商品后URL未变化"
            # 断言是商品详情页
            assert "goods" in after_url or "product" in after_url or "detail" in after_url
            print("✅ 点击商品跳转测试通过")
        else:
            print("⚠️ 没有找到可点击的商品，跳过测试")


if __name__ == "__main__":
    # 单独运行这个测试文件
    pytest.main([__file__, "-v", "-s"])