from pages.add_poject_page import AddProjectPage
from playwright.sync_api import expect, Page
import pytest
import uuid
from mocks.mock_api import mock_project_400, mock_project_500


class TestAddProject:
    """添加项目"""

    @pytest.fixture(scope="function", autouse=True)
    def for_each(self, page: Page):
        print("for each--start: 打开新页面访问添加项目页")
        self.add_project = AddProjectPage(page)
        self.add_project.navigate()
        yield
        print("for each--end: 后置操作")

    @pytest.mark.parametrize('name, app, desc', [
        ["abc!@", "", ""],
        ["aaaaabbbbbcccccdddddeeeeefffff1", "", ""],
        ["abc", "aa!@", ""]
    ])
    def test_add_project_disabled(self, name, app, desc):
        """异常场景-项目名称，无效等价：特殊字符/大于30个字符"""
        self.add_project.fill_project_name(name)
        self.add_project.fill_publish_app(app)
        self.add_project.fill_project_desc(desc)
        # 断言 提交按钮不可点击
        expect(self.add_project.locator_save_button).to_be_disabled()

    def test_add_project_null(self):
        """异常场景-项目名称不能为空"""
        self.add_project.fill_project_name("")
        self.add_project.fill_publish_app("")
        self.add_project.fill_project_desc("")
        self.add_project.click_save_button()
        # 断言 提交按钮不可点击
        expect(self.add_project.locator_save_button).to_be_disabled()

    def test_add_project_success(self):
        """提交成功，跳转到项目列表"""
        # 生成随机账号
        self.add_project.fill_project_name("project_" + str(uuid.uuid4()).replace('-', '')[:8])
        self.add_project.fill_publish_app("my_app")
        self.add_project.fill_project_desc("this is a test project")
        # 断言 跳转到项目列表页
        with self.add_project.page.expect_navigation(url='**/list_project.html'):
            # 保存成功后，重定向到列表页
            self.add_project.click_save_button()

    def test_add_project_400(self, page):
        """项目名称重复，弹出模态框"""
        self.add_project.fill_project_name('yo yo')
        self.add_project.fill_publish_app("my_app")
        self.add_project.fill_project_desc("this is a test project")
        # mock 接口返回 400 错误
        page.route(**mock_project_400)
        self.add_project.click_save_button()
        # 检验结果，弹出框文本包含
        expect(page.locator('.bootbox-body')).to_be_visible()
        expect(page.locator('.bootbox-body')).to_contain_text("已存在")

    def test_add_project_500(self, page):
        """服务器异常，500状态码"""
        self.add_project.fill_project_name('test')
        self.add_project.fill_publish_app("my_app")
        self.add_project.fill_project_desc("this is a test project")
        # mock 接口返回 500 错误
        page.route(**mock_project_500)
        self.add_project.click_save_button()
        # 检验结果，弹出框文本包含
        expect(page.locator('.bootbox-body')).to_contain_text("操作异常")

