from __future__ import annotations

import re

from playwright.sync_api import expect

from pages.base_page import BasePage
from utils.data_factory import Employee


class EmployeeDetailsPage(BasePage):
    FIRST_NAME = 'input[name="firstName"]'
    MIDDLE_NAME = 'input[name="middleName"]'
    LAST_NAME = 'input[name="lastName"]'

    URL_PATTERN = re.compile(r"/pim/viewPersonalDetails/.*")

    def wait_until_loaded(self, employee: Employee, timeout: int = 120_000) -> None:
        expect(self.page).to_have_url(self.URL_PATTERN, timeout=timeout)
        expect(self.page.locator(self.FIRST_NAME)).to_have_value(
            employee.first_name, timeout=timeout
        )
        expect(self.page.locator(self.LAST_NAME)).to_have_value(
            employee.last_name, timeout=timeout
        )

    def name_values(self) -> dict[str, str]:
        return {
            "first": self.page.locator(self.FIRST_NAME).input_value(),
            "middle": self.page.locator(self.MIDDLE_NAME).input_value(),
            "last": self.page.locator(self.LAST_NAME).input_value(),
        }

    def employee_number(self) -> str:
        return self.page.url.rstrip("/").split("/")[-1]
