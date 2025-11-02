import pytest
from pages.login_page import LoginPage

"""
全局默认账号使用"test"/"123456"登录
在cases目录的conftest.py文件下涉及多个账号切换操作的时候，我们可以创建新的上下文，用其他账号登录
"""


@pytest.fixture(scope="session", autouse=True)
def save_admin_cookies(browser, base_url, pytestconfig):
    """
    admin 用户登录后保存 admin.json   cookies信息
    :param browser:
    :param base_url:
    :param pytestconfig:
    :return:
    """
    context = browser.new_context(base_url=base_url, no_viewport=True)
    page = context.new_page()
    LoginPage(page).navigate()
    LoginPage(page).login("admin", "123456")
    # 等待登录成功页面重定向
    page.wait_for_url(url='**/index.html')
    # 保存 storage_state 到指定文件
    storage_path = pytestconfig.rootpath.joinpath('auth/admin.json')
    context.storage_state(path=storage_path)
    context.close()

@pytest.fixture(scope="module")
def admin_context(browser, base_url, pytestconfig):
    """
    创建admin上下文，加载admin.json数据
    """
    context = browser.new_context(
        base_url=base_url,
        no_viewport=True,
        storage_state=pytestconfig.rootpath.joinpath("auth/admin.json")
    )
    yield context
    context.close()

