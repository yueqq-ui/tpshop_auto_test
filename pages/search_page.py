from pages.base_page import BasePage
from selenium.webdriver.common.by import By
import time
import re


class SearchPage(BasePage):
    # 元素定位器
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[name='q']")
    SEARCH_INPUT_BY_ID = (By.ID, "q")
    SEARCH_ICON = (By.CSS_SELECTOR, ".search-icon, .icon-search, .ecsc-search-icon, .search-btn")
    SEARCH_BTN = (By.XPATH, "//button[contains(text(),'搜索')]")
    PRODUCT_LIST = (By.CSS_SELECTOR, ".goods-list .item, .product-item, .shop-item")
    NO_RESULT = (By.XPATH, "//div[contains(text(),'未找到')]")
    SORT_SALES = (By.XPATH, "//div[contains(text(),'销量')]")
    SORT_PRICE = (By.XPATH, "//div[contains(text(),'价格')]")
    FIRST_PRODUCT = (By.CSS_SELECTOR, ".goods-list .item:first-child, .product-item:first-child")

    def __init__(self, driver):
        super().__init__(driver)

    def search(self, keyword):
        """方法一：直接通过URL搜索（最稳定）"""
        search_url = f"https://hmshop-test.itheima.net/Home/Goods/search.html?q={keyword}"
        self.driver.get(search_url)
        time.sleep(2)
        print(f"✅ 搜索URL: {search_url}")

    def search_by_click(self, keyword):
        """方法二：通过点击搜索图标再输入（备用）"""
        # 先打开首页
        self.driver.get("https://hmshop-test.itheima.net/")
        time.sleep(2)

        # 点击搜索图标显示搜索框
        try:
            icon = self.driver.find_element(*self.SEARCH_ICON)
            icon.click()
            time.sleep(1)
            print("✅ 已点击搜索图标")
        except:
            print("⚠️ 未找到搜索图标，尝试直接找搜索框")

        # 找到搜索框并输入
        try:
            search_input = self.driver.find_element(*self.SEARCH_INPUT)
        except:
            search_input = self.driver.find_element(*self.SEARCH_INPUT_BY_ID)

        search_input.clear()
        search_input.send_keys(keyword)
        time.sleep(1)

        # 提交搜索
        try:
            search_btn = self.driver.find_element(*self.SEARCH_BTN)
            search_btn.click()
        except:
            search_input.submit()

        time.sleep(2)
        print(f"✅ 搜索关键词: {keyword}")

    def get_product_count(self):
        """获取搜索结果数量 - 从页面文字中提取"""
        time.sleep(2)

        # 方法1：查找页面中"共X个商品"的文本（最稳定）
        page_text = self.driver.page_source
        match = re.search(r'共\s*(\d+)\s*个商品', page_text)
        if match:
            count = int(match.group(1))
            print(f"✅ 从文本中获取到商品数量: {count}")
            return count

        # 方法2：查找"找到X个商品"
        match = re.search(r'找到\s*(\d+)\s*个商品', page_text)
        if match:
            count = int(match.group(1))
            print(f"✅ 从文本中获取到商品数量: {count}")
            return count

        # 方法3：尝试多种商品列表定位器
        locators = [
            (By.CSS_SELECTOR, ".goods-list .item"),
            (By.CSS_SELECTOR, ".product-list .product"),
            (By.CSS_SELECTOR, "[class*='item']"),
            (By.XPATH, "//div[contains(@class, 'goods')]"),
            (By.XPATH, "//li[contains(@class, 'product')]"),
        ]

        for locator in locators:
            try:
                products = self.driver.find_elements(*locator)
                if len(products) > 0:
                    print(f"✅ 找到 {len(products)} 个商品")
                    return len(products)
            except:
                continue

        print("⚠️ 未找到商品，返回0")
        return 0

    def has_no_result(self):
        """是否无结果"""
        try:
            return len(self.driver.find_elements(*self.NO_RESULT)) > 0
        except:
            return False

    def click_first_product(self):
        """点击第一个商品"""
        try:
            # 尝试多种定位器
            locators = [
                (By.CSS_SELECTOR, ".goods-list .item:first-child a"),
                (By.CSS_SELECTOR, ".product-item:first-child a"),
                (By.XPATH, "//div[contains(@class, 'item')]//a[@class='goods-name']"),
                (By.XPATH, "(//div[contains(@class, 'goods')]//a)[1]"),
            ]

            for locator in locators:
                try:
                    product = self.driver.find_element(*locator)
                    product.click()
                    time.sleep(2)
                    print("✅ 已点击第一个商品")
                    return True
                except:
                    continue

            # 如果都找不到，报错
            print("❌ 未找到可点击的商品")
            return False
        except Exception as e:
            print(f"❌ 点击商品失败: {e}")
            return False

    def sort_by_sales(self):
        """按销量排序"""
        try:
            self.click(self.SORT_SALES)
            time.sleep(2)
            print("✅ 按销量排序完成")
        except:
            print("⚠️ 销量排序按钮未找到")

    def sort_by_price(self):
        """按价格排序"""
        try:
            self.click(self.SORT_PRICE)
            time.sleep(2)
            print("✅ 按价格排序完成")
        except:
            print("⚠️ 价格排序按钮未找到")

    def get_current_url(self):
        """获取当前URL"""
        return self.driver.current_url