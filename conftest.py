from pytest import Item
import allure

# 本地插件注册
pytest_plugins = ['plugins.pytest_playwright']

def pytest_runtest_call(item: Item): # noqa
    # 动态添加测试类的 allure.feature()
    if item.parent._obj.__doc__: # noqa
        allure.dynamic.feature(item.parent._obj.__doc__) # noqa
    # 动态添加测试用例的title 标题 allure.title()
    if item.function.__doc__: # noqa
        allure.dynamic.title(item.function.__doc__) # noqa