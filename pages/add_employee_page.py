from __future__ import annotations

from playwright.sync_api import expect

from pages.base_page import BasePage
from pages.employee_details_page import EmployeeDetailsPage
from utils.data_factory import Employee


class AddEmployeePage(BasePage):
    path = "/web/index.php/pim/addEmployee"

    FIRST_NAME = 'input[name="firstName"]'
    MIDDLE_NAME = 'input[name="middleName"]'
    LAST_NAME = 'input[name="lastName"]'
    SAVE = 'button[type="submit"]'
    FIELD_ERROR = ".oxd-input-field-error-message"

    def expect_loaded(self) -> None:
        expect(self.page.locator(self.FIRST_NAME)).to_be_visible()
        expect(self.page.get_by_role("heading", name="Add Employee")).to_be_visible()

    def fill_employee(self, employee: Employee) -> AddEmployeePage:
        self.page.fill(self.FIRST_NAME, employee.first_name)
        self.page.fill(self.MIDDLE_NAME, employee.middle_name)
        self.page.fill(self.LAST_NAME, employee.last_name)
        return self

    def click_save(self) -> None:
        self.page.locator(self.SAVE).click()

    def create(self, employee: Employee) -> EmployeeDetailsPage:
        self.fill_employee(employee).click_save()
        details = EmployeeDetailsPage(self.page)
        details.wait_until_loaded(employee)
        return details

    def required_errors(self) -> list[str]:
        errors = self.page.locator(self.FIELD_ERROR)
        expect(errors.first).to_be_visible()
        return errors.all_inner_texts()
