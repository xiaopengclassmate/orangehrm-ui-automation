import uuid

import allure
import pytest

from pages.employee_details_page import EmployeeDetailsPage
from pages.pim_page import PIMPage


@allure.feature("员工管理")
@pytest.mark.employee
class TestEmployeeManagement:
    @allure.story("新增员工")
    @allure.title("可以新增员工并在列表中按姓名搜索到")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_add_and_search_employee(self, dashboard_page, created_employee):
        employee, details = created_employee

        assert isinstance(details, EmployeeDetailsPage)
        assert details.name_values() == {
            "first": employee.first_name,
            "middle": employee.middle_name,
            "last": employee.last_name,
        }

        pim = PIMPage(dashboard_page.page).open()
        pim.search_employee(employee)
        assert pim.has_employee(employee)

    @allure.story("删除员工")
    @allure.title("可以按姓名精确删除员工")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_delete_employee(self, dashboard_page, created_employee):
        employee, _ = created_employee

        pim = PIMPage(dashboard_page.page).open()
        assert pim.delete_employee(employee) is True

        pim.search_employee(employee)
        assert not pim.has_employee(employee)

    @allure.story("表单校验")
    @allure.title("新增员工时姓名必填")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.negative
    def test_add_employee_requires_name(self, dashboard_page):
        pim = PIMPage(dashboard_page.page).open()
        add_page = pim.open_add_employee()
        add_page.click_save()

        errors = add_page.required_errors()
        assert errors.count("Required") >= 2

    @allure.story("搜索")
    @allure.title("搜索不存在的员工时结果为空")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_search_unknown_employee_returns_empty(self, dashboard_page):
        pim = PIMPage(dashboard_page.page).open()
        pim.search_text(f"NoSuchUser{uuid.uuid4().hex[:6]}")
        assert pim.row_count() == 0
