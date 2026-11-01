import re

import allure
import pytest
from playwright.sync_api import expect


@allure.feature("菜单导航")
@pytest.mark.navigation
class TestNavigation:
    @allure.story("主菜单")
    @allure.title("登录后展示完整主菜单")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_main_menu_is_visible(self, dashboard_page):
        items = dashboard_page.menu_items()
        expected = [
            "Admin",
            "PIM",
            "Leave",
            "Time",
            "Recruitment",
            "My Info",
            "Performance",
            "Dashboard",
            "Directory",
            "Maintenance",
            "Claim",
            "Buzz",
        ]
        for name in expected:
            assert name in items

    @allure.story("模块切换")
    @allure.title("可以在 PIM、Leave、Dashboard 之间切换")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_switch_between_modules(self, dashboard_page):
        dashboard_page.open_module("PIM")
        expect(dashboard_page.page).to_have_url(re.compile(r"/pim/viewEmployeeList$"))
        expect(dashboard_page.page.locator("h6").first).to_have_text("PIM")

        dashboard_page.open_module("Leave")
        expect(dashboard_page.page).to_have_url(re.compile(r"/leave/viewLeaveList$"))
        expect(dashboard_page.page.locator("h6").first).to_have_text("Leave")

        dashboard_page.open_module("Dashboard")
        dashboard_page.expect_loaded()

    @allure.story("退出登录")
    @allure.title("用户可以通过头像菜单退出登录")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_logout(self, dashboard_page):
        login_page = dashboard_page.logout()
        login_page.expect_loaded()
