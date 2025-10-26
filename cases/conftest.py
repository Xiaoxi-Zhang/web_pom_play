import pytest
from pages.login_page import LoginPage

@pytest.fixture(scope="session", autouse=True)
def login_first(browser, base_url, pytestconfig):
    """全局先登录"""
    # base_url 传到 context
    context = browser.new_context(base_url=base_url)
    page = context.new_page()
    login = LoginPage(page)
    login.navigate()
    login.login(username="test", password="123456")
    # 等待加载到指定页面
    page.wait_for_url(url='**/index.html')  # 等登录完成
    # 保存登录的 cookies (获取项目的根目录)
    print('获取项目的根目录：', pytestconfig.rootpath)
    storage_path = pytestconfig.rootpath.joinpath('auth/login_state.json')
    context.storage_state(path=storage_path)
    context.close()

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, playwright, pytestconfig):
    """
    添加context 上下文参数，默认每个页面加载cookies
    :param browser_context_args:
    :param playwright:
    :return:
    """
    return {
        "storage_state": pytestconfig.rootpath.joinpath("auth/login_state.json"),
        **browser_context_args,
    }
