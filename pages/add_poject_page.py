from playwright.sync_api import Page


class AddProjectPage:

    def __init__(self, page: Page):
        self.page = page
        self.locator_project_name = page.get_by_label("项目名称:")
        self.locator_publish_app = page.get_by_label("所属应用:")
        self.locator_project_desc = page.get_by_label("项目描述:")
        self.locator_save_button = page.get_by_text('点击提交')

    def navigate(self):
        self.page.goto('/add_project.html')

    def fill_project_name(self, name):
        self.locator_project_name.fill(name)

    def fill_publish_app(self, text):
        self.locator_publish_app.fill(text)

    def fill_project_desc(self, text):
        self.locator_project_desc.fill(text)

    def click_save_button(self):
        self.locator_save_button.click()
