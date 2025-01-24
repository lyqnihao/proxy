def get_web_content():
    """
    从网页中提取内容
    """
    try:
        # 设置浏览器驱动（无头模式）
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(options=options)

        # 打开目标网页
        driver.get("https://xconfig.pages.dev/index2")
        time.sleep(5)  # 等待页面加载

        # 定位按钮（通过文本内容定位）
        button = driver.find_element(By.XPATH, "//button[contains(text(), 'List 14 - Mix')]")
        log_message("找到按钮: List 14 - Mix")

        # 点击按钮
        button.click()
        log_message("已点击按钮")

        # 等待内容加载
        time.sleep(2)

        # 获取内容（假设内容显示在某个元素中，class 是 'content'）
        content_element = driver.find_element(By.CLASS_NAME, "content")
        content = content_element.text
        log_message("已从页面获取内容")

        # 关闭浏览器
        driver.quit()
        return content
    except (NoSuchElementException, TimeoutException) as e:
        log_message(f"网页内容提取失败: {e}")
        raise Exception(f"网页内容提取失败: {e}")
