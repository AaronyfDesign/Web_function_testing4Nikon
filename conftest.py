#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Pytest配置文件和共享fixtures
"""

import pytest
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def pytest_configure(config):
    """Pytest配置"""
    # 创建报告目录
    os.makedirs("reports", exist_ok=True)
    
    # 设置标记
    config.addinivalue_line("markers", "smoke: 冒烟测试标记")
    config.addinivalue_line("markers", "regression: 回归测试标记")
    config.addinivalue_line("markers", "ui: UI测试标记")
    config.addinivalue_line("markers", "api: API测试标记")


def pytest_collection_modifyitems(config, items):
    """修改测试项收集"""
    for item in items:
        # 为所有测试添加UI标记
        if "test_" in item.name:
            item.add_marker(pytest.mark.ui)


@pytest.fixture(scope="session")
def test_config():
    """测试配置fixture"""
    return {
        "base_url": "https://my.nikon.com.cn",
        "timeout": 10,
        "implicit_wait": 5
    }


@pytest.fixture(scope="session")
def test_data():
    """加载测试数据"""
    try:
        with open("test_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        # 返回默认测试数据
        return {
            "test_users": [
                {
                    "username": "test_user_1",
                    "phone": "13800138001",
                    "email": "test1@example.com",
                    "password": "Test123456"
                }
            ],
            "search_keywords": ["相机", "镜头"],
            "navigation_items": ["首页", "照片"]
        }


@pytest.fixture(scope="session")
def chrome_driver():
    """Chrome WebDriver fixture"""
    options = Options()
    
    # 设置Chrome选项
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # 启用性能日志
    options.add_experimental_option('perfLoggingPrefs', {
        'enableNetwork': True,
        'enablePage': False,
        'enableTimeline': False
    })
    options.add_argument("--enable-logging")
    options.add_argument("--log-level=0")
    
    # 自动下载ChromeDriver
    service = Service(ChromeDriverManager().install())
    
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(5)
    
    # 执行脚本移除webdriver标识
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    yield driver
    
    driver.quit()


@pytest.fixture(scope="function")
def browser(chrome_driver, test_config):
    """浏览器fixture，每个测试函数都会重新打开页面"""
    driver = chrome_driver
    driver.get(test_config["base_url"])
    return driver


@pytest.fixture
def api_client():
    """API客户端fixture"""
    import requests
    
    class APIClient:
        def __init__(self, base_url):
            self.base_url = base_url
            self.session = requests.Session()
            self.session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            })
        
        def get(self, endpoint, **kwargs):
            url = f"{self.base_url}{endpoint}"
            return self.session.get(url, **kwargs)
        
        def post(self, endpoint, **kwargs):
            url = f"{self.base_url}{endpoint}"
            return self.session.post(url, **kwargs)
    
    return APIClient("https://my.nikon.com.cn")


def pytest_html_report_title(report):
    """自定义HTML报告标题"""
    report.title = "尼康网站自动化测试报告"


def pytest_html_results_summary(prefix, summary, postfix):
    """自定义HTML报告摘要"""
    prefix.extend([
        "<h2>测试摘要</h2>",
        "<p>本报告包含尼康网站的自动化测试结果</p>"
    ])
