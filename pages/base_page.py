from __future__ import annotations

import re

from playwright.sync_api import Page, expect


class BasePage:
    """所有页面对象的基类。"""

    path: str = "/"

    def __init__(self, page: Page) -> None:
        self.page = page

    def open(self) -> BasePage:
        self.page.goto(self.path)
        return self

    def expect_loaded(self) -> None:
        expect(self.page).to_have_url(re.compile(re.escape(self.path) + r"$"))

    def screenshot(self, path: str) -> bytes:
        return self.page.screenshot(path=path, full_page=True)
