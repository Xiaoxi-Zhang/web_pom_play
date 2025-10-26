
def test_x(page):
    page.goto('http://47.116.12.183/index.html')
    print('页面标题：', page.title())
