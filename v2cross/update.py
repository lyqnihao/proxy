# 版本：2.0
# 修订原因：Python 脚本仅用于获取目标网址和网址内容，不处理文件操作。
# 版本：1.1
# 修订原因：Python 脚本仅用于获取目标网址和网址内容，不处理文件操作。
# 版本：1.0
# 修订原因：初始版本，实现抓取网页内容、提取目标网址功能。

import requests
from bs4 import BeautifulSoup
import re
import sys

# 抓取网页内容并提取目标网址
def fetch_subscription_url():
    url = "https://v2cross.com/1884.html"  # 目标网页地址
    response = requests.get(url)  # 发送 HTTP 请求
    if response.status_code == 200:  # 检查请求是否成功
        soup = BeautifulSoup(response.text, 'html.parser')  # 解析网页内容
        # 查找包含“本次节点订阅地址：”的文本
        target_text = soup.find(text=re.compile(r'本次节点订阅地址：'))
        if target_text:
            # 使用正则表达式提取网址
            match = re.search(r'https?://[^\s]+', target_text)
            if match:
                return match.group(0)  # 返回提取的网址
    return None  # 如果提取失败，返回 None

# 读取目标网址的内容
def fetch_url_content(url):
    response = requests.get(url)  # 发送 HTTP 请求
    if response.status_code == 200:  # 检查请求是否成功
        return response.text  # 返回网页内容
    return None  # 如果请求失败，返回 None

# 主函数
def main():
    # 获取目标网址
    subscription_url = fetch_subscription_url()
    if not subscription_url:
        print("错误：无法提取订阅地址。")  # 输出错误信息
        sys.exit(1)  # 返回状态码 1 表示失败
    
    # 读取目标网址的内容
    url_content = fetch_url_content(subscription_url)
    if not url_content:
        print("错误：无法读取目标网址内容。")  # 输出错误信息
        sys.exit(1)  # 返回状态码 1 表示失败
    
    # 输出目标网址的内容
    print(url_content)

if __name__ == "__main__":
    main()
