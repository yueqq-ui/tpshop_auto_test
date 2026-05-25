# TPshop 电商平台自动化测试项目

## 项目简介
基于 Python + Selenium + Pytest 的电商平台自动化测试框架，覆盖核心业务链路。

## 技术栈
- Python 3.13
- Selenium 4.15
- Pytest 7.4
- POM 设计模式

## 测试覆盖
模块	  用例数	   状态
登录	    4	     通过
搜索	    6	     通过
购物车	    5	     通过
订单	    2	     通过

## 运行方式
```bash
pip install -r requirements.txt
pytest test_cases/ -v -s --html=test_reports/report.html
