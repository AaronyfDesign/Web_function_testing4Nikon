#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试运行脚本
使用方法: python run_tests.py [选项]
"""

import os
import sys
import subprocess
import argparse
from datetime import datetime


def run_tests(test_type="all", browser="chrome", parallel=False, report_type="html"):
    """
    运行测试
    
    Args:
        test_type: 测试类型 (all, smoke, regression, ui, api)
        browser: 浏览器类型 (chrome, firefox)
        parallel: 是否并行执行
        report_type: 报告类型 (html, allure)
    """
    
    # 基础pytest命令
    cmd = ["python", "-m", "pytest"]
    
    # 根据测试类型添加参数
    if test_type == "smoke":
        cmd.extend(["-m", "smoke"])
    elif test_type == "regression":
        cmd.extend(["-m", "regression"])
    elif test_type == "ui":
        cmd.extend(["-m", "ui"])
    elif test_type == "api":
        cmd.extend(["-m", "api"])
    
    # 并行执行
    if parallel:
        cmd.extend(["-n", "auto"])
    
    # 报告设置
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if report_type == "html":
        cmd.extend([
            "--html=reports/test_report_{}.html".format(timestamp),
            "--self-contained-html"
        ])
    elif report_type == "allure":
        cmd.extend([
            "--alluredir=reports/allure-results"
        ])
    
    # 其他选项
    cmd.extend([
        "-v",
        "--tb=short",
        "--strict-markers"
    ])
    
    print(f"运行命令: {' '.join(cmd)}")
    
    # 创建报告目录
    os.makedirs("reports", exist_ok=True)
    
    # 执行测试
    try:
        result = subprocess.run(cmd, check=False)
        
        if report_type == "allure" and result.returncode == 0:
            # 生成allure报告
            print("生成Allure报告...")
            subprocess.run([
                "allure", "generate", "reports/allure-results", 
                "-o", "reports/allure-report", "--clean"
            ])
            print("Allure报告已生成: reports/allure-report/index.html")
        
        return result.returncode
        
    except KeyboardInterrupt:
        print("\n测试被用户中断")
        return 1
    except Exception as e:
        print(f"测试执行失败: {str(e)}")
        return 1


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="尼康网站自动化测试运行器")
    
    parser.add_argument(
        "--type", "-t",
        choices=["all", "smoke", "regression", "ui", "api"],
        default="all",
        help="测试类型 (默认: all)"
    )
    
    parser.add_argument(
        "--browser", "-b",
        choices=["chrome", "firefox"],
        default="chrome",
        help="浏览器类型 (默认: chrome)"
    )
    
    parser.add_argument(
        "--parallel", "-p",
        action="store_true",
        help="并行执行测试"
    )
    
    parser.add_argument(
        "--report", "-r",
        choices=["html", "allure"],
        default="html",
        help="报告类型 (默认: html)"
    )
    
    parser.add_argument(
        "--install-deps",
        action="store_true",
        help="安装依赖包"
    )
    
    args = parser.parse_args()
    
    # 安装依赖
    if args.install_deps:
        print("安装依赖包...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("依赖包安装完成")
        return 0
    
    # 运行测试
    return run_tests(
        test_type=args.type,
        browser=args.browser,
        parallel=args.parallel,
        report_type=args.report
    )


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
