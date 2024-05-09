from playwright import sync_api as pw_api


def main() -> int:
    print("Hello from crawler-demo!")
    playwright_fetch()
    return 0


def expect_page(url: str, browser_context: pw_api.BrowserContext) -> None:
    # 跳转到new page, 等待新页面加载完成
    with browser_context.expect_page() as event_page:
        # goto a empty page, page_new is exactly the page
        # page.locator('a[target="_blank"]').click()

        page_new = event_page.value
        page_new.goto(url)

        print(page_new.title())


def download(page: pw_api.Page) -> None:
    with page.expect_download() as downlowd_info:
        page.locator("button#xxx").click()
        dl = downlowd_info.value
        print(dl.path())
        dl.save_as("./dl.txt")


def document_or_window_handle(page: pw_api.Page) -> None:
    # window_js_handle = page.evaluate_handle('window')
    # keys = window_js_handle.get_properties().keys()

    body_js_handle = page.evaluate_handle("document.body")
    body_inner_html_js_handle = page.evaluate_handle(
        "body => body.innerHTML", body_js_handle
    )
    print("-->" + body_inner_html_js_handle.json_value())

    a = body_inner_html_js_handle.as_element().wait_for_selector('div#song-list-pre-cache')

    body_inner_html_js_handle.dispose()
    # error
    # cannot call json_value() again after dispose
    # print('-->', body_inner_html_js_handle.json_value())


def playwright_fetch():
    with pw_api.sync_playwright() as pw:
        browser_type_chrome = pw.chromium

        # browser_chrome = browser_type.launch()
        browser_chrome = browser_type_chrome.launch(
            # headless=False, slow_mo=100,
            # devtools=True
        )

        browser_context = browser_chrome.new_context()
        # default to 30000 ms, 0 to disable timeout
        browser_context.set_default_timeout(50000)

        # page =browser_chrome.new_page()
        page = browser_context.new_page()

        page.goto("https://music.163.com/#/discover/toplist")
        # page.screenshot(path=f'example-{browser_type_chrome.name}.png')
        # 全屏
        # page.screenshot(path=f'example-{browser_type_chrome.name}.png', full_page=True)

        # expect_page("https://www.baidu.com", browser_context)

        # download(page)

        document_or_window_handle(page)

        browser_chrome.close()
