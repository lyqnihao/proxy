import os
import time
import git
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# 定义文件路径
output_path = os.path.join("xConfig", "output.yaml")

def log_message(message):
    """
    记录日志信息
    """
    with open("xConfig/update.log", "a", encoding="utf-8") as log_file:
        log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

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

        # 等待内容复制到剪贴板
        time.sleep(2)

        # 从剪贴板获取内容
        content = pyperclip.paste()
        log_message("已从剪贴板获取内容")

        # 关闭浏览器
        driver.quit()
        return content
    except (NoSuchElementException, TimeoutException) as e:
        log_message(f"网页内容提取失败: {e}")
        raise Exception(f"网页内容提取失败: {e}")

def update_output_file(new_content):
    """
    更新 output.yaml 文件
    """
    try:
        # 检查文件是否存在
        if not os.path.exists(output_path):
            log_message("output.yaml 文件不存在，创建新文件")
            with open(output_path, "w", encoding="utf-8") as file:
                file.write("# 自动更新的配置内容\n")

        # 读取现有内容
        with open(output_path, "r", encoding="utf-8") as file:
            old_content = file.read()

        # 检查内容是否有变化
        if old_content == new_content:
            log_message("内容无变化，跳过更新")
            return False
        else:
            log_message("内容有变化，更新文件")
            with open(output_path, "w", encoding="utf-8") as file:
                file.write(new_content)
            return True
    except Exception as e:
        log_message(f"文件更新失败: {e}")
        raise Exception(f"文件更新失败: {e}")

def push_to_github():
    """
    将更改推送到 GitHub 仓库
    """
    try:
        repo = git.Repo(os.getcwd())
        repo.git.pull()  # 拉取最新更改
        repo.git.add(output_path)
        repo.git.commit("-m", "自动更新 output.yaml")
        repo.git.push()
        log_message("更改已推送到 GitHub")
    except Exception as e:
        log_message(f"推送失败: {e}")
        raise Exception(f"推送失败: {e}")

def main():
    """
    主函数
    """
    log_message("开始运行脚本")

    # 从网页中提取内容
    new_content = get_web_content()

    # 更新 output.yaml 文件
    if update_output_file(new_content):
        # 如果有变化，推送到 GitHub
        push_to_github()

    log_message("脚本运行结束")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log_message(f"脚本运行出错: {e}")
        raise  # 抛出异常，由 GitHub Actions 捕获并发送邮件
