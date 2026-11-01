# OrangeHRM 企业后台 Web UI 自动化测试

基于 **Python + Playwright + Pytest + Page Object + Allure + GitHub Actions** 的企业后台系统自动化测试项目。

被测站点：[OrangeHRM Open Source Demo](https://opensource-demo.orangehrmlive.com/)（开源 HR 系统官方演示环境）。

## 项目亮点

- **真实企业后台业务**：覆盖登录、主菜单导航、员工新增/搜索/删除，涉及表单、下拉自动补全、数据表格、弹窗确认等复杂控件。
- **测试数据隔离**：每次使用 `uuid` 生成唯一员工姓名，避免共享演示环境的数据冲突。
- **自动清理**：无论用例成功还是失败，fixture 都会按姓名精确定位并删除测试员工，不污染演示环境。
- **稳健的定位与等待**：使用 Playwright `expect` 自动等待，不使用固定 sleep；针对共享环境的慢响应设置分级超时。
- **失败可观测**：失败自动截图、记录页面 URL 与控制台日志，并附加到 Allure 报告。
- **CI 工程化**：GitHub Actions 每日定时回归，共享环境偶发抖动时自动重试一次，Allure 报告发布到 GitHub Pages。

## 测试范围

| 模块 | 用例数 | 覆盖内容 |
|---|---:|---|
| 登录 | 3 | 正常登录、错误密码、用户名/密码必填 |
| 菜单导航 | 3 | 主菜单完整性、PIM/Leave/Dashboard 切换、退出登录 |
| 员工管理 | 4 | 新增并搜索员工、按姓名删除、姓名必填校验、搜索不存在员工 |
| **合计** | **10** | 冒烟 + 回归 + 异常场景 |

## 目录结构

```text
orangehrm-ui-automation/
├── config/
│   └── settings.py              # 环境变量与分级超时
├── pages/                       # Page Object
│   ├── base_page.py
│   ├── login_page.py
│   ├── dashboard_page.py
│   ├── pim_page.py
│   ├── add_employee_page.py
│   └── employee_details_page.py
├── tests/
│   ├── test_login.py
│   ├── test_navigation.py
│   └── test_employee_management.py
├── utils/
│   └── data_factory.py          # 唯一员工数据生成
├── conftest.py                  # fixture、数据清理、失败截图
├── pytest.ini
├── requirements.txt
└── .github/workflows/ui-tests.yml
```

## 快速开始

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
python -m playwright install chromium

cp .env.example .env   # 可选
pytest
```

演示账号（站点公开提供）：`Admin / admin123`。

## 常用命令

```bash
pytest                                      # 全部用例
pytest -m smoke                             # 冒烟
pytest -m employee                          # 员工管理模块
pytest -m negative                          # 异常场景
pytest --headed                             # 有界面调试
pytest --reruns 1 --reruns-delay 5          # 失败重试（应对共享环境抖动）
pytest -n auto                              # 并发（注意共享演示环境限流）
```

## 测试数据与清理策略

1. `utils/data_factory.py` 使用 `uuid4().hex[:8]` 生成唯一后缀，例如 `AutoTest Qa User1a2b3c4d`。
2. `created_employee` fixture 通过 UI 完成新增，并把员工数据传给用例。
3. `cleanup_employee` fixture 在用例结束后：
   - 进入 PIM → Employee List；
   - 输入完整姓名并按姓名精确匹配表格行；
   - 点击行尾删除按钮 → 确认弹窗；
   - 只删除姓名为 `AutoTest ... User<uuid>` 的记录，避免误删演示环境中的其他数据。
4. 即使用例中途失败，fixture teardown 仍会执行清理。

## 报告

```bash
# Pytest HTML
# reports/report.html

# Allure
allure serve allure-results
```

Allure CLI：

```bash
npm install -g allure-commandline
# 或 Windows: scoop install allure
```

## 设计说明（面试可讲）

1. **为什么自动补全输入后按 Escape？**
   OrangeHRM 的员工姓名是 autocomplete，直接点击下拉项可能选中别人；按 Escape 关闭下拉后按输入文本过滤，再用表格行做精确匹配，避免误选和误删。
2. **为什么表格行要按列拆分匹配？**
   表格同时包含 Id、First (& Middle) Name、Last Name 等列，直接用子串匹配可能命中相似姓名；拆行后同时校验 first/last，删除操作才安全。
3. **怎么处理共享演示环境的慢响应？**
   统一默认超时 20s、导航超时 60s；Dashboard 首次加载和新增员工保存单独放宽到 60s/120s；CI 对网络抖动重试一次。
4. **测试数据如何隔离？**
   uuid 唯一姓名 + fixture 自动清理，保证可重复执行、互不影响。
5. **失败如何定位？**
   失败自动截图 + 页面 URL + 浏览器控制台日志，全部附加到 Allure 报告。

## 简历表述参考

> 基于 Playwright + Pytest 搭建 OrangeHRM 企业后台 UI 自动化框架，封装 6 个 Page Object，覆盖登录、菜单导航、员工新增/搜索/删除共 10 条用例；使用 uuid 唯一数据与 fixture 自动清理保证共享环境可重复执行，接入 Allure 报告、失败截图/日志和 GitHub Actions 每日回归。

## 说明

OrangeHRM Demo 是公开演示环境，数据可能被其他用户同时修改；本项目仅用于学习与演示，测试数据均使用 `AutoTest` 前缀并在用例结束后自动删除。
