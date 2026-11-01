import allure
import pytest

from config import settings


@allure.feature("登录")
@pytest.mark.login
class TestLogin:
    @allure.story("正常登录")
    @allure.title("管理员可以登录并进入 Dashboard")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_valid_login(self, login_page):
        dashboard = login_page.login(settings.ADMIN_USER, settings.ADMIN_PASSWORD)
        dashboard.expect_loaded()
        assert dashboard.heading() == "Dashboard"
        assert len(dashboard.menu_items()) >= 10

    @allure.story("异常登录")
    @allure.title("错误密码登录失败并提示 Invalid credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.negative
    def test_invalid_password(self, login_page):
        login_page.login(settings.ADMIN_USER, "wrong-password")
        assert login_page.error_message() == "Invalid credentials"

    @allure.story("必填校验")
    @allure.title("用户名和密码为空时展示 Required 提示")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.negative
    def test_empty_credentials(self, login_page):
        login_page.submit_empty()
        assert login_page.required_errors() == ["Required", "Required"]
