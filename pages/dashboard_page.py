from __future__ import annotations

import re

from playwright.sync_api import expect

from pages.base_page import BasePage


class DashboardPage(BasePage):
    path = "/web/index.php/dashboard/index"

    HEADING = "h6"
    MENU_ITEM = ".oxd-main-menu-item"
    USER_DROPDOWN = ".oxd-userdropdown-tab"

    def expect_loaded(self) -> None:
        # 共享演示环境偶尔较慢，Dashboard 首次加载给更长的等待时间
        expect(self.page).to_have_url(
            re.compile(r"/dashboard/index$"), timeout=60_000
        )
        expect(
            self.page.locator(self.HEADING).filter(has_text="Dashboard")
        ).to_be_visible(timeout=60_000)
        expect(self.page.locator(self.MENU_ITEM).first).to_be_visible(
            timeout=60_000
        )

    def menu_items(self) -> list[str]:
        return [
            item.strip()
            for item in self.page.locator(self.MENU_ITEM).all_inner_texts()
            if item.strip()
        ]

    def open_module(self, name: str) -> None:
        self.page.get_by_role("link", name=name, exact=True).click()

    def heading(self) -> str:
        return self.page.locator(self.HEADING).first.inner_text()

    def logout(self) -> "LoginPage":
        from pages.login_page import LoginPage

        self.page.locator(self.USER_DROPDOWN).click()
        self.page.get_by_role("menuitem", name="Logout").click()
        return LoginPage(self.page)
