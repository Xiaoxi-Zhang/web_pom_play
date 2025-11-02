"""
整个项目中的上下文对象
page 用例中直接传page,默认使用登录后的context上下文创建的page对象
admin_context 针对admin用户登录后的上下文环境
"""
import pytest
from playwright.sync_api import Page, BrowserContext
from pages.add_poject_page import AddProjectPage
import uuid
from pages.project_list_page import ProjectListPage


class TestMoreAccounts:
    """多账号切换操作示例"""

    @pytest.fixture(autouse=True)
    def start_for_each(self, page: Page, admin_context: BrowserContext):
        print('for each--start: 打开添加项目页')
        # 用户1
        self.user1_project = AddProjectPage(page)
        self.user1_project.navigate()
        # 用户2 admin
        page2 = admin_context.new_page()
        self.user2_project = ProjectListPage(page2)
        self.user2_project.navigate()
        yield
        print('for each--end: 后置操作')
        page.close()
        page2.close()

    def test_delete_project(self):
        """
        测试流程：
        step--A账号登录，创建项目xxx
        step--B账号登录，删除项目xxx
        :return:
        """
        # 账号1添加项目
        test_project_name = str(uuid.uuid4()).replace('-', '')[:25]  # 生成随机项目名称，避免重复
        self.user1_project.fill_project_name(test_project_name)
        self.user1_project.fill_publish_app("测试应用")
        self.user1_project.fill_project_desc("这是一个测试项目，请勿删除")
        # 断言跳转到项目列表页
        with self.user1_project.page.expect_navigation(url='**/list_project.html'):
            self.user1_project.click_save_button()

        # 账号2 操作删除
        self.user2_project.search_project(test_project_name)
        with self.user2_project.page.expect_request('**/api/project**'):
            self.user2_project.click_search_button()
        self.user2_project.page.wait_for_timeout(3000)  # 等待表格刷新
        self.user2_project.locator_table_delete.click()
        # 确认删除
        with self.user2_project.page.expect_response('**/api/project**') as resp:
            self.user2_project.locator_boot_box_accept.click()
        # 断言删除成功
        resp_obj = resp.value
        assert resp_obj.status == 200


