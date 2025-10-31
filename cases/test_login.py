import pytest
from pages.login_page import LoginPage
from playwright.sync_api import expect

class TestLoginPage:
    """登录用例"""

    @pytest.fixture(scope="function", autouse=True)
    def for_each(self, page):
        self.login = LoginPage(page)
        self.login.navigate()   # 进入登录页面
        yield
        print('后置操作------------------')


    def test_login_username_1(self):
        """用户名为空，点登录"""
        self.login.fill_username("")
        self.login.fill_password("123456")
        self.login.click_login_button()
        # 断言
        expect(self.login.locator_username_tip1).to_be_visible()
        expect(self.login.locator_username_tip1).to_have_text("不能为空")

    def test_login_2(self):
        """用户名大于30字符"""
        self.login.fill_username('hello world hello world hello world')
        # 断言
        expect(self.login.locator_username_tip2).to_be_visible()
        expect(self.login.locator_username_tip2).to_contain_text("用户名称1-30位字符")
        # 断言 登录按钮不可点击
        expect(self.login.locator_login_btn).not_to_be_enabled()

    def test_login_3(self):
        """用户名有特殊字符"""
        self.login.fill_username('hello!@#')
        # 断言
        expect(self.login.locator_username_tip3).to_be_visible()
        expect(self.login.locator_username_tip3).to_contain_text("用户名称不能有特殊字符,请用中英文数字")
        # 断言 登录按钮不可点击
        expect(self.login.locator_login_btn).not_to_be_enabled()

    @pytest.mark.parametrize("username, password", [
        ['test', 'qqqass'],
        ['zvgva', '123456']
    ])
    def test_login_error(self, username, password):
        """登录失败场景"""
        self.login.fill_username(username)
        self.login.fill_password(password)
        self.login.click_login_button()
        # 断言提示语可见
        expect(self.login.locator_login_error).to_be_visible()  # 账号或密码不正确

    def test_login_success(self):
        """登录正常流程，登录成功"""
        self.login.fill_username("test")
        self.login.fill_password('123456')
        self.login.click_login_button()
        # 断言页面跳转到首页
        expect(self.login.page).to_have_title('首页')
        expect(self.login.page).to_have_url('/index.html')

    def test_login_success_2(self):
        """登录正常流程，登录成功"""
        self.login.fill_username("test")
        self.login.fill_password('123456')
        # 显示断言重定向
        with self.login.page.expect_navigation(url='**/index.html'):
            self.login.click_login_button()

    def test_login_ajax(self):
        """登录正常流程， 获取异步ajax 请求"""
        self.login.fill_username("test")
        self.login.fill_password('123456')
        # 拦截登录的ajax请求
        with self.login.page.expect_request('**/api/login') as req:
            self.login.click_login_button()
        print(req.value) # 获取请求对象
        # 断言请求内容
        assert req.value.method == 'POST'
        assert req.value.header_value('content-type') == 'application/json'
        assert req.value.post_data_json == {"username":"test","password":"123456"}

    def test_login_ajax_response(self):
        """登录正常流程， 获取异步ajax 请求返回结果"""
        self.login.fill_username("test")
        self.login.fill_password('123456')
        # 拦截登录的ajax请求响应
        with self.login.page.expect_response('**/api/login') as res:
            self.login.click_login_button()
        print(res.value) # 获取响应对象
        print(res.value.url)
        print(res.value.status)
        print(res.value.ok)
        assert res.value.status == 200
        assert res.value.ok is True

    def test_login_link(self):
        """没有账号？点这注册"""
        expect(self.login.locator_register_link).to_have_attribute('href', 'register.html')
        # 点击
        self.login.click_register_link()
        expect(self.login.page).to_have_url('/register.html')
        expect(self.login.page).to_have_title('注册')

