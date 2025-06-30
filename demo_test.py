#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
快速演示测试脚本 - 简化版本用于快速验证
"""

import pytest
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException


class TestNikonDemo:
    """尼康网站演示测试"""
    
    @pytest.fixture(scope="class")  
    def driver(self):
        """简化的WebDriver设置"""
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(10)
        
        yield driver
        driver.quit()
    
    @pytest.mark.smoke
    def test_website_access(self, driver):
        """测试网站基本访问"""
        print("\n正在测试网站访问性...")
        
        driver.get("https://my.nikon.com.cn")
        
        # 验证页面加载
        assert "nikon" in driver.current_url.lower()
        print("✓ 网站可以正常访问")
        
        # 验证页面标题
        title = driver.title
        assert len(title) > 0
        print(f"✓ 页面标题: {title}")
        
        # 验证页面内容
        body_text = driver.find_element(By.TAG_NAME, "body").text
        assert len(body_text) > 100  # 页面应该有足够的内容
        print("✓ 页面内容正常加载")
    
    @pytest.mark.smoke  
    def test_navigation_elements(self, driver):
        """测试导航元素"""
        print("\n正在测试导航元素...")
        
        driver.get("https://my.nikon.com.cn")
        time.sleep(3)  # 等待页面完全加载
        
        # 查找导航元素
        nav_found = False
        nav_selectors = ["nav", ".nav", ".navigation", ".navbar"]
        
        for selector in nav_selectors:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            if elements:
                nav_found = True
                print(f"✓ 找到导航元素: {selector}")
                break
        
        # 查找链接
        links = driver.find_elements(By.TAG_NAME, "a")
        visible_links = [link for link in links if link.is_displayed()]
        
        assert len(visible_links) > 0, "页面应该包含可见的链接"
        print(f"✓ 找到 {len(visible_links)} 个可见链接")
    
    @pytest.mark.smoke
    def test_images_load(self, driver):
        """测试图片加载"""
        print("\n正在测试图片加载...")
        
        driver.get("https://my.nikon.com.cn") 
        time.sleep(3)
        
        # 查找页面上的图片
        images = driver.find_elements(By.TAG_NAME, "img")
        visible_images = [img for img in images if img.is_displayed()]
        
        assert len(visible_images) > 0, "页面应该包含可见的图片"
        print(f"✓ 找到 {len(visible_images)} 张可见图片")
        
        # 检查前几张图片的src属性
        loaded_images = 0
        for img in visible_images[:5]:
            src = img.get_attribute("src")
            if src and src.startswith("http"):
                loaded_images += 1
                
        print(f"✓ {loaded_images} 张图片有有效的src属性")
    
    @pytest.mark.smoke
    def test_responsive_design(self, driver):
        """测试响应式设计"""
        print("\n正在测试响应式设计...")
        
        driver.get("https://my.nikon.com.cn")
        
        # 测试不同屏幕尺寸
        sizes = [
            (1920, 1080, "桌面"),
            (768, 1024, "平板"),
            (375, 667, "手机")
        ]
        
        for width, height, device in sizes:
            driver.set_window_size(width, height)
            time.sleep(2)
            
            # 检查页面是否仍然可用
            body = driver.find_element(By.TAG_NAME, "body")
            assert body.is_displayed()
            
            print(f"✓ {device}尺寸 ({width}x{height}) 下页面正常显示")
    
    def test_api_basic_check(self):
        """基本API检查"""
        print("\n正在进行基本API检查...")
        
        try:
            response = requests.get("https://my.nikon.com.cn", timeout=10)
            
            # 检查HTTP状态码
            assert response.status_code == 200, f"HTTP状态码错误: {response.status_code}"
            print(f"✓ HTTP状态码: {response.status_code}")
            
            # 检查内容类型
            content_type = response.headers.get('content-type', '')
            assert 'html' in content_type.lower(), f"内容类型错误: {content_type}"
            print(f"✓ 内容类型: {content_type}")
            
            # 检查响应时间
            response_time = response.elapsed.total_seconds()
            assert response_time < 10, f"响应时间过长: {response_time}秒"
            print(f"✓ 响应时间: {response_time:.2f}秒")
            
        except requests.RequestException as e:
            pytest.fail(f"API请求失败: {str(e)}")


def test_run_demo():
    """运行演示测试"""
    pytest.main([
        __file__,
        "-v",
        "-s",
        "--tb=short",
        "-m", "smoke"
    ])


if __name__ == "__main__":
    # 直接运行演示测试
    test_run_demo()
