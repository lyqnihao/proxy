import os
import requests
from bs4 import BeautifulSoup
import re

# 抓取网页内容并提取目标网址
def fetch_subscription_url():
    url = "https://v2cross.com/1884.html"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # 查找包含“本次节点订阅地址：”的文本
        target_text = soup.find(text=re.compile(r'本次节点订阅地址：'))
        if target_text:
            # 使用正则表达式提取网址
            match = re.search(r'https?://[^\s]+', target_text)
            if match:
                return match.group(0)
    return None

# 读取目标网址的内容
def fetch_url_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return None

# 更新 output.yaml 文件
def update_output_file(content):
    output_dir = "v2cross"
    output_file = os.path.join(output_dir, "output.yaml")
    
    # 检查目录是否存在，若不存在则创建
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"创建目录：{output_dir}")
    
    # 检查文件是否存在
    if os.path.exists(output_file):
        with open(output_file, "r", encoding="utf-8") as file:
            existing_content = file.read()
        # 如果内容无变化，则跳过更新
        if existing_content == content:
            print("内容无变化，跳过更新。")
            return
    
    # 清除旧内容并写入新内容
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(content)
    print("output.yaml 文件已更新。")
    print(f"文件路径：{os.path.abspath(output_file)}")  # 打印文件绝对路径

# 主函数
def main():
    # 获取目标网址
    subscription_url = fetch_subscription_url()
    if not subscription_url:
        print("无法提取订阅地址。")
        return
    
    # 读取目标网址的内容
    url_content = fetch_url_content(subscription_url)
    if not url_content:
        print("无法读取目标网址内容。")
        return
    
    # 更新 output.yaml 文件
    update_output_file(url_content)

if __name__ == "__main__":
    main()
