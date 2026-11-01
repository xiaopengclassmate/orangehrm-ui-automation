from __future__ import annotations

from playwright.sync_api import expect

from pages.base_page import BasePage
from pages.dashboard_page import DashboardPage


class LoginPage(BasePage):
    path = "/web/index.php/auth/login"

    USERNAME = 'input[name="username"]'
    PASSWORD = 'input[name="password"]'
    SUBMIT = 'button[type="submit"]'
    ALERT = ".oxd-alert-content-text"
    FIELD_ERROR = ".oxd-input-field-error-message"

    def open(self) -> LoginPage:
        super().open()
        expect(self.page.locator(self.USERNAME)).to_be_visible()
        return self

    def expect_loaded(self) -> None:
        expect(self.page.locator(self.USERNAME)).to_be_visible()
        expect(self.page.locator(self.SUBMIT)).to_be_visible()

    def login(self, username: str, password: str) -> DashboardPage:
        self.page.fill(self.USERNAME, username)
        self.page.fill(self.PASSWORD, password)
        self.page.click(self.SUBMIT)
        return DashboardPage(self.page)

    def submit_empty(self) -> None:
        self.page.click(self.SUBMIT)

    def error_message(self) -> str:
        alert = self.page.locator(self.ALERT)
        expect(alert).to_be_visible()
        return alert.inner_text()

    def required_errors(self) -> list[str]:
        errors = self.page.locator(self.FIELD_ERROR)
        expect(errors.first).to_be_visible()
        return errors.all_inner_texts()
