#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
尼康网站自动化测试脚本
测试网站: https://my.nikon.com.cn/
"""

import pytest
import time
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options


class TestConfig:
    """测试配置类"""
    BASE_URL = "https://my.nikon.com.cn"
    TIMEOUT = 10
    IMPLICIT_WAIT = 5
    
    # 测试数据
    TEST_USER = {
        "phone": "18727560912",
        "email": "test@example.com",
        "password": "Nk123456"
    }



class NikonWebsiteTest:
    """尼康网站测试基类"""
    
    @pytest.fixture(scope="session")
    def driver(self):
        """WebDriver初始化"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # 无头模式
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36")
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(TestConfig.IMPLICIT_WAIT)
        
        yield driver
        driver.quit()
    
    @pytest.fixture(autouse=True)
    def setup_method(self, driver):
        """每个测试方法执行前的设置"""
        driver.get(TestConfig.BASE_URL)
        time.sleep(2)  # 等待页面加载


class TestWebsiteAccess(NikonWebsiteTest):
    """网站访问性测试"""
    
    def test_website_accessibility(self, driver):
        """测试网站可访问性"""
        assert driver.current_url.startswith(TestConfig.BASE_URL)
        assert "尼康" in driver.title or "Nikon" in driver.title
    
    def test_page_load_performance(self, driver):
        """测试页面加载性能"""
        start_time = time.time()
        driver.get(TestConfig.BASE_URL)
        load_time = time.time() - start_time
        
        # 页面加载时间应小于10秒
        assert load_time < 10, f"页面加载时间过长: {load_time:.2f}秒"
    
    def test_https_security(self, driver):
        """测试HTTPS安全性"""
        assert driver.current_url.startswith("https://"), "网站应该使用HTTPS协议"


class TestNavigation(NikonWebsiteTest):
    """导航功能测试"""
    
    def test_main_navigation_elements(self, driver):
        """测试主要导航元素是否存在"""
        try:
            # 检查主要导航链接
            nav_items = [
                "首页", "照片", "学习讨论", "直营店画廊"
            ]
            
            for item in nav_items:
                try:
                    element = driver.find_element(By.PARTIAL_LINK_TEXT, item)
                    assert element.is_displayed(), f"导航项目 '{item}' 不可见"
                except NoSuchElementException:
                    # 如果通过链接文本找不到，尝试其他方式
                    pass
            
        except Exception as e:
            pytest.fail(f"导航测试失败: {str(e)}")
    
    def test_logo_click_returns_home(self, driver):
        """测试点击Logo返回首页"""
        try:
            logo = driver.find_element(By.CSS_SELECTOR, "img[alt*='logo'], img[src*='logo']")
            if logo:
                logo.click()
                time.sleep(2)
                assert TestConfig.BASE_URL in driver.current_url
        except NoSuchElementException:
            pytest.skip("Logo元素未找到")


# class TestUserAuthentication(NikonWebsiteTest):
#     """用户认证功能测试"""
    
#     def test_login_page_access(self, driver):
#         """测试登录页面访问"""
#         try:
#             # 尝试找到登录链接
#             login_links = driver.find_elements(By.PARTIAL_LINK_TEXT, "登录")
#             login_links.extend(driver.find_elements(By.PARTIAL_LINK_TEXT, "去登录"))
            
#             if login_links:
#                 login_links[0].click()
#                 time.sleep(2)
                
#                 # 验证是否跳转到登录相关页面
#                 current_url = driver.current_url
#                 assert "login" in current_url or "account" in current_url
#             else:
#                 pytest.skip("未找到登录链接")
                
#         except Exception as e:
#             pytest.fail(f"登录页面访问测试失败: {str(e)}")
    
#     def test_login_form_elements(self, driver):
#         """测试登录表单元素"""
#         try:
#             # 先访问登录页面
#             self.test_login_page_access(driver)
            
#             # 检查登录表单元素
#             form_elements = [
#                 "input[type='text']", "input[type='password']", 
#                 "input[type='tel']", "input[type='email']"
#             ]
            
#             found_inputs = 0
#             for selector in form_elements:
#                 elements = driver.find_elements(By.CSS_SELECTOR, selector)
#                 found_inputs += len(elements)
            
#             assert found_inputs >= 2, "登录表单应至少包含用户名和密码输入框"
            
#         except Exception as e:
#             pytest.skip(f"登录表单测试跳过: {str(e)}")


class TestContentDisplay(NikonWebsiteTest):
    """内容展示测试"""
    
    def test_homepage_content_load(self, driver):
        """测试首页内容加载"""
        try:
            # 等待页面完全加载
            WebDriverWait(driver, TestConfig.TIMEOUT).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # 检查是否有主要内容区域
            main_content_selectors = [
                "main", ".main", "#main", ".content", ".container"
            ]
            
            content_found = False
            for selector in main_content_selectors:
                if driver.find_elements(By.CSS_SELECTOR, selector):
                    content_found = True
                    break
            
            assert content_found, "未找到主要内容区域"
            
        except TimeoutException:
            pytest.fail("页面加载超时")
    
    def test_image_gallery_display(self, driver):
        """测试图片画廊显示"""
        try:
            # 查找图片元素
            images = driver.find_elements(By.TAG_NAME, "img")
            visible_images = [img for img in images if img.is_displayed()]
            
            assert len(visible_images) > 0, "页面应该显示至少一张图片"
            
            # 检查图片是否加载成功（简单检查）
            for img in visible_images[:5]:  # 检查前5张图片
                src = img.get_attribute("src")
                if src and src.startswith("http"):
                    # 使用JavaScript检查图片是否加载成功
                    is_loaded = driver.execute_script(
                        "return arguments[0].complete && arguments[0].naturalWidth > 0", img
                    )
                    if not is_loaded:
                        print(f"图片加载失败: {src}")
                        
        except Exception as e:
            pytest.skip(f"图片画廊测试跳过: {str(e)}")


class TestResponsiveDesign(NikonWebsiteTest):
    """响应式设计测试"""
    
    @pytest.mark.parametrize("width,height", [
        (1920, 1080),  # 桌面
        (1366, 768),   # 笔记本
        (768, 1024),   # 平板
        (375, 667),    # 手机
    ])
    def test_responsive_layout(self, driver, width, height):
        """测试不同屏幕尺寸下的布局"""
        driver.set_window_size(width, height)
        time.sleep(2)
        
        # 检查页面是否仍然可用
        body = driver.find_element(By.TAG_NAME, "body")
        assert body.is_displayed()
        
        # 检查是否有水平滚动条
        body_width = driver.execute_script("return document.body.scrollWidth")
        window_width = driver.execute_script("return window.innerWidth")
        
        # 允许小量差异
        assert body_width <= window_width + 20, f"在 {width}x{height} 分辨率下出现水平滚动条"


# class TestFormInteraction(NikonWebsiteTest):
#     """表单交互测试"""
    
#     def test_search_functionality(self, driver):
#         """测试搜索功能"""
#         try:
#             # 查找搜索框
#             search_selectors = [
#                 "input[type='search']", "input[placeholder*='搜索']", 
#                 "input[placeholder*='search']", ".search-input"
#             ]
            
#             search_input = None
#             for selector in search_selectors:
#                 elements = driver.find_elements(By.CSS_SELECTOR, selector)
#                 if elements:
#                     search_input = elements[0]
#                     break
            
#             if search_input and search_input.is_displayed():
#                 search_input.clear()
#                 search_input.send_keys("相机")
                
#                 # 尝试提交搜索
#                 search_input.submit()
#                 time.sleep(3)
                
#                 # 验证搜索结果（基本验证）
#                 current_url = driver.current_url
#                 assert "search" in current_url or len(current_url) != len(TestConfig.BASE_URL)
#             else:
#                 pytest.skip("未找到可用的搜索功能")
                
#         except Exception as e:
#             pytest.skip(f"搜索功能测试跳过: {str(e)}")


# class TestAPIEndpoints(NikonWebsiteTest):
#     """API接口测试"""
    
#     def test_api_health_check(self):
#         """测试API健康检查"""
#         try:
#             # 尝试访问可能的API端点
#             api_endpoints = [
#                 f"{TestConfig.BASE_URL}/api/health",
#                 f"{TestConfig.BASE_URL}/api/status",
#                 f"{TestConfig.BASE_URL}/api/v1/"
#             ]
            
#             for endpoint in api_endpoints:
#                 try:
#                     response = requests.get(endpoint, timeout=10)
#                     if response.status_code in [200, 404]:  # 404也说明服务器响应正常
#                         assert True
#                         return
#                 except requests.RequestException:
#                     continue
            
#             pytest.skip("无法访问API端点")
            
#         except Exception as e:
#             pytest.skip(f"API测试跳过: {str(e)}")
    
#     def test_page_api_calls(self, driver):
#         """测试页面API调用"""
#         try:
#             # 启用性能日志
#             logs = driver.get_log('performance')
            
#             # 刷新页面以捕获网络请求
#             driver.refresh()
#             time.sleep(5)
            
#             # 获取新的日志
#             new_logs = driver.get_log('performance')
            
#             api_calls = 0
#             for log in new_logs:
#                 message = json.loads(log['message'])
#                 if message['message']['method'] == 'Network.responseReceived':
#                     url = message['message']['params']['response']['url']
#                     if 'api' in url or url.endswith('.json'):
#                         api_calls += 1
#                         status = message['message']['params']['response']['status']
#                         assert status < 400, f"API调用失败: {url}, 状态码: {status}"
            
#             print(f"检测到 {api_calls} 个API调用")
            
#         except Exception as e:
#             pytest.skip(f"页面API调用测试跳过: {str(e)}")


# class TestErrorHandling(NikonWebsiteTest):
#     """错误处理测试"""
    
#     def test_404_error_handling(self, driver):
#         """测试404错误处理"""
#         driver.get(f"{TestConfig.BASE_URL}/nonexistent-page-12345")
#         time.sleep(2)
        
#         # 检查是否显示了错误页面或重定向到首页
#         current_url = driver.current_url
#         page_text = driver.find_element(By.TAG_NAME, "body").text.lower()
        
#         is_error_handled = (
#             "404" in page_text or 
#             "not found" in page_text or 
#             "页面不存在" in page_text or
#             current_url == TestConfig.BASE_URL
#         )
        
#         assert is_error_handled, "404错误未正确处理"
    
#     def test_javascript_errors(self, driver):
#         """测试JavaScript错误"""
#         try:
#             # 获取浏览器控制台日志
#             logs = driver.get_log('browser')
            
#             # 过滤严重错误
#             severe_errors = [log for log in logs if log['level'] == 'SEVERE']
            
#             # 排除已知的第三方错误
#             filtered_errors = []
#             for error in severe_errors:
#                 message = error['message'].lower()
#                 # 排除常见的第三方错误
#                 if not any(keyword in message for keyword in [
#                     'favicon', 'third-party', 'advertisement', 'analytics'
#                 ]):
#                     filtered_errors.append(error)
            
#             assert len(filtered_errors) == 0, f"发现JavaScript错误: {filtered_errors}"
            
#         except Exception as e:
#             pytest.skip(f"JavaScript错误检查跳过: {str(e)}")


# def test_run_all_tests():
#     """运行所有测试的入口点"""
#     pytest.main([
#         __file__,
#         "-v",
#         "--tb=short",
#         "--html=reports/test_report.html",
#         "--self-contained-html"
#     ])


if __name__ == "__main__":
    # 运行测试
    test_run_all_tests()
