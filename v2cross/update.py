import os
import requests
from bs4 import BeautifulSoup
import re
import sys  # 用于退出时返回状态码

# 抓取网页内容并提取目标网址
def fetch_subscription_url():
    url = "https://v2cross.com/1884.html"
    response = requests.get(url)
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
    response = requests.get(url)
    if response.status_code == 200:  # 检查请求是否成功
        return response.text  # 返回网页内容
    return None  # 如果请求失败，返回 None

# 更新 output.yaml 文件
def update_output_file(content):
    output_file = "output.yaml"  # 输出文件路径
    
    # 检查文件是否存在
    if os.path.exists(output_file):
        with open(output_file, "r", encoding="utf-8") as file:
            existing_content = file.read()  # 读取现有内容
        # 如果内容无变化，则跳过更新
        if existing_content == content:
            print("内容无变化，跳过更新。")
            return False  # 返回 False 表示内容未更新
    
    # 清除旧内容并写入新内容
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(content)  # 写入新内容
    print("output.yaml 文件已更新。")
    return True  # 返回 True 表示内容已更新

# 主函数
def main():
    # 获取目标网址
    subscription_url = fetch_subscription_url()
    if not subscription_url:
        print("无法提取订阅地址。")
        sys.exit(1)  # 返回状态码 1 表示失败
    
    # 读取目标网址的内容
    url_content = fetch_url_content(subscription_url)
    if not url_content:
        print("无法读取目标网址内容。")
        sys.exit(1)  # 返回状态码 1 表示失败
    
    # 更新 output.yaml 文件
    if not update_output_file(url_content):
        print("内容未更新。")
        sys.exit(1)  # 返回状态码 1 表示内容未更新

if __name__ == "__main__":
    main()
