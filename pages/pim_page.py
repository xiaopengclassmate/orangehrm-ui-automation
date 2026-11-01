from __future__ import annotations

import re

from playwright.sync_api import Locator, expect

from pages.add_employee_page import AddEmployeePage
from pages.base_page import BasePage
from utils.data_factory import Employee


class PIMPage(BasePage):
    path = "/web/index.php/pim/viewEmployeeList"

    TABLE = ".oxd-table"
    ROWS = ".oxd-table-card"
    SEARCH_BUTTON = "Search"
    ADD_BUTTON = "Add"

    def open(self) -> PIMPage:
        self.page.goto(self.path)
        expect(self.page.locator(self.TABLE)).to_be_visible()
        return self

    def expect_loaded(self) -> None:
        expect(self.page).to_have_url(re.compile(r"/pim/viewEmployeeList$"))
        expect(self.page.locator(self.TABLE)).to_be_visible()

    def open_add_employee(self) -> AddEmployeePage:
        self.page.get_by_role("button", name=self.ADD_BUTTON).click()
        add_page = AddEmployeePage(self.page)
        add_page.expect_loaded()
        return add_page

    def search_text(self, text: str) -> None:
        hint = self.page.get_by_placeholder("Type for hints...").first
        hint.fill(text)
        self.page.wait_for_timeout(1200)
        # 关闭自动补全下拉，仅按输入文本过滤，避免误选其他员工
        self.page.keyboard.press("Escape")
        self.page.get_by_role("button", name=self.SEARCH_BUTTON).click()
        self.page.wait_for_timeout(2500)

    def search_employee(self, employee: Employee) -> None:
        self.search_text(employee.full_name)

    def row_count(self) -> int:
        return self.page.locator(self.ROWS).count()

    def rows(self) -> list[tuple[Locator, list[str]]]:
        cards = self.page.locator(self.ROWS)
        result: list[tuple[Locator, list[str]]] = []
        for index in range(cards.count()):
            card = cards.nth(index)
            lines = [line.strip() for line in card.inner_text().splitlines() if line.strip()]
            result.append((card, lines))
        return result

    @staticmethod
    def _matches(lines: list[str], employee: Employee) -> bool:
        # 表格列：Id | First (& Middle) Name | Last Name | ...
        return (
            len(lines) >= 3
            and lines[1].startswith(employee.first_name)
            and lines[2] == employee.last_name
        )

    def has_employee(self, employee: Employee) -> bool:
        return any(self._matches(lines, employee) for _, lines in self.rows())

    def delete_employee(self, employee: Employee) -> bool:
        """按姓名精确定位并删除员工；返回是否找到并执行删除。"""
        self.open()
        self.search_employee(employee)

        for card, lines in self.rows():
            if not self._matches(lines, employee):
                continue

            action_buttons = card.locator(".oxd-table-cell-actions button")
            action_buttons.nth(action_buttons.count() - 1).click()

            confirm = self.page.get_by_role("button", name="Yes, Delete")
            confirm.wait_for(state="visible", timeout=20_000)
            confirm.click()
            self.page.wait_for_timeout(3000)
            return True

        return False
