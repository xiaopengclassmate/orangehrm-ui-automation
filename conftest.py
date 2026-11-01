import os

import allure
import pytest

from config import settings
from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage
from pages.pim_page import PIMPage
from utils.data_factory import Employee, new_employee

_CONSOLE_LOGS: dict[int, list[str]] = {}


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args: dict) -> dict:
    return {**browser_type_launch_args, "slow_mo": int(os.getenv("SLOW_MO", "0"))}


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict) -> dict:
    return {
        **browser_context_args,
        "base_url": settings.BASE_URL,
        "viewport": {"width": 1600, "height": 900},
        "locale": "en-US",
    }


@pytest.fixture
def page(context):
    test_page = context.new_page()
    test_page.set_default_timeout(settings.DEFAULT_TIMEOUT_MS)
    test_page.set_default_navigation_timeout(settings.NAVIGATION_TIMEOUT_MS)

    logs: list[str] = []
    _CONSOLE_LOGS[id(test_page)] = logs
    test_page.on("console", lambda msg: logs.append(f"[{msg.type}] {msg.text}"))

    yield test_page

    _CONSOLE_LOGS.pop(id(test_page), None)
    test_page.close()


@pytest.fixture
def login_page(page) -> LoginPage:
    return LoginPage(page).open()


@pytest.fixture
def dashboard_page(page) -> DashboardPage:
    login = LoginPage(page).open()
    login.login(settings.ADMIN_USER, settings.ADMIN_PASSWORD)
    dashboard = DashboardPage(page)
    dashboard.expect_loaded()
    return dashboard


@pytest.fixture
def employee_data() -> Employee:
    return new_employee()


@pytest.fixture
def cleanup_employee(dashboard_page, employee_data):
    """无论用例成败，结束后都按姓名精确清理测试员工。"""
    yield
    PIMPage(dashboard_page.page).delete_employee(employee_data)


@pytest.fixture
def created_employee(dashboard_page, employee_data, cleanup_employee):
    """通过 UI 创建员工并返回 (员工数据, 详情页对象)。"""
    pim = PIMPage(dashboard_page.page).open()
    details = pim.open_add_employee().create(employee_data)
    return employee_data, details


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item, call):
    report = yield
    if report.when != "call" or not report.failed:
        return report

    test_page = item.funcargs.get("page")
    if test_page is None:
        return report

    try:
        allure.attach(
            test_page.screenshot(full_page=True),
            name="失败截图",
            attachment_type=allure.attachment_type.PNG,
        )
        allure.attach(
            test_page.url,
            name="失败页面 URL",
            attachment_type=allure.attachment_type.TEXT,
        )
        logs = _CONSOLE_LOGS.get(id(test_page), [])
        if logs:
            allure.attach(
                "\n".join(logs[-50:]),
                name="浏览器控制台日志",
                attachment_type=allure.attachment_type.TEXT,
            )
    except Exception:
        pass

    return report
