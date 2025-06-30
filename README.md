# 尼康网站自动化测试项目

本项目为尼康网站 (https://my.nikon.com.cn) 的自动化测试框架，基于 Selenium WebDriver 和 Pytest 构建。

## 功能特性

- ✅ 完整的UI自动化测试
- ✅ API接口测试
- ✅ 响应式设计测试
- ✅ 性能测试
- ✅ 错误处理测试
- ✅ 多浏览器支持
- ✅ 并行测试执行
- ✅ 详细的HTML测试报告
- ✅ 数据驱动测试

## 项目结构

```
web-test-plan/
├── test_nikon_website.py      # 主测试文件
├── conftest.py               # Pytest配置和fixtures
├── run_tests.py              # 测试运行脚本
├── requirements.txt          # 项目依赖
├── pytest.ini              # Pytest配置文件
├── test_data.json           # 测试数据
├── README.md               # 项目说明
└── reports/                # 测试报告目录
```

## 安装和配置

### 1. 环境要求

- Python 3.8+
- Chrome浏览器
- ChromeDriver (自动下载)

### 2. 安装依赖

```bash
# 克隆项目
git clone [项目地址]
cd web-test-plan

# 安装依赖
pip install -r requirements.txt

# 或者使用运行脚本安装
python run_tests.py --install-deps
```

### 3. 验证安装

```bash
python -m pytest --version
```

## 使用方法

### 快速开始

```bash
# 运行所有测试
python run_tests.py

# 运行指定类型的测试
python run_tests.py --type smoke    # 冒烟测试
python run_tests.py --type ui       # UI测试
python run_tests.py --type api      # API测试

# 并行执行
python run_tests.py --parallel

# 生成Allure报告
python run_tests.py --report allure
```

### 直接使用Pytest

```bash
# 运行所有测试
pytest test_nikon_website.py

# 运行特定测试类
pytest test_nikon_website.py::TestWebsiteAccess

# 运行特定测试方法
pytest test_nikon_website.py::TestWebsiteAccess::test_website_accessibility

# 使用标记运行测试
pytest -m smoke
pytest -m "ui and not slow"

# 并行执行
pytest -n auto

# 生成详细报告
pytest --html=reports/report.html --self-contained-html
```

## 测试覆盖范围

### 1. 网站访问性测试
- [x] 网站可访问性检查
- [x] 页面加载性能测试
- [x] HTTPS安全性验证

### 2. 导航功能测试
- [x] 主导航元素检查
- [x] Logo点击functionality
- [x] 菜单交互测试

### 3. 用户认证测试
- [x] 登录页面访问
- [x] 登录表单元素检查
- [x] 表单验证测试

### 4. 内容展示测试
- [x] 首页内容加载
- [x] 图片画廊显示
- [x] 内容完整性检查

### 5. 响应式设计测试
- [x] 多分辨率适配测试
- [x] 移动端兼容性
- [x] 布局响应性验证

### 6. 表单交互测试
- [x] 搜索功能测试
- [x] 表单提交验证
- [x] 输入验证测试

### 7. API接口测试
- [x] API健康检查
- [x] 页面API调用监控
- [x] 响应状态验证

### 8. 错误处理测试
- [x] 404错误处理
- [x] JavaScript错误检查
- [x] 异常情况处理

## 配置说明

### pytest.ini 配置

```ini
[tool:pytest]
testpaths = .
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v 
    --strict-markers 
    --tb=short
    --html=reports/report.html 
    --self-contained-html
    --maxfail=5
```

### 测试数据配置

在 `test_data.json` 中配置测试数据：

```json
{
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
```

## 报告查看

### HTML报告
测试完成后，在 `reports/` 目录下生成HTML报告文件。

### Allure报告
```bash
# 安装Allure
npm install -g allure-commandline

# 运行测试并生成Allure报告
python run_tests.py --report allure

# 查看报告
allure serve reports/allure-results
```

## 最佳实践

### 1. 测试标记使用
```python
@pytest.mark.smoke
def test_critical_function():
    pass

@pytest.mark.ui
@pytest.mark.slow  
def test_complex_ui():
    pass
```

### 2. 数据驱动测试
```python
@pytest.mark.parametrize("keyword", ["相机", "镜头", "摄影"])
def test_search_keywords(browser, keyword):
    # 测试代码
```

### 3. 错误处理
```python
try:
    element = driver.find_element(By.ID, "element_id")
except NoSuchElementException:
    pytest.skip("元素未找到，跳过测试")
```

## 持续集成

### Jenkins配置示例
```groovy
pipeline {
    agent any
    
    stages {
        stage('Setup') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        
        stage('Test') {
            steps {
                sh 'python run_tests.py --type smoke --report html'
            }
        }
        
        stage('Report') {
            steps {
                publishHTML([
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'reports',
                    reportFiles: '*.html',
                    reportName: '测试报告'
                ])
            }
        }
    }
}
```

## 故障排除

### 常见问题

1. **ChromeDriver版本不匹配**
   ```bash
   # 更新ChromeDriver
   pip install --upgrade webdriver-manager
   ```

2. **元素找不到**
   - 检查页面加载是否完成
   - 增加等待时间
   - 使用显式等待

3. **测试不稳定**
   - 增加重试机制
   - 使用更可靠的定位策略
   - 添加适当的等待

### 调试模式

```bash
# 关闭无头模式进行调试
# 在conftest.py中注释掉 options.add_argument("--headless")

# 添加详细日志
pytest --log-cli-level=DEBUG
```

## 贡献指南

1. Fork项目
2. 创建功能分支
3. 编写测试用例
4. 提交Pull Request

## 许可证

MIT License

## 联系方式

如有问题，请联系项目维护者或提交Issue。
