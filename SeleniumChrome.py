def get_page_source(my_url):

    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    import time


    # configure webdriver
    options = Options()
    #options.add_argument("--headless")  # hide GUI
    options.add_argument("--window-size=1920,1080")  # set window size to native GUI size
    options.add_argument("start-maximized")  # ensure window is full-screen
    options.add_argument("start-minimized")

    ...
    # configure chrome browser to not load images and javascript
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option(
        # this will disable image loading
        "prefs", {"profile.managed_default_content_settings.images": 2}
    )


    driver = webdriver.Chrome(options=options)
    #                         ^^^^^^^^^^^^^^^
    driver.get(my_url)

    time.sleep(2)
    return driver.page_source