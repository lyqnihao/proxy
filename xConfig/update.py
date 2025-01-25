# xConfig/update.py
import requests
from bs4 import BeautifulSoup
import yaml
import os
import sys

url = "https://xconfig.pages.dev/index2"
try:
    response = requests.get(url)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"请求网页失败: {e}")
    with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
        print('FETCH_ERROR=true', file=fh)
    sys.exit(1)

soup = BeautifulSoup(response.text, 'html.parser')
button = soup.find('button', id='copyButton3-13')
if not button:
    print("未找到指定的按钮")
    with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
        print('FETCH_ERROR=true', file=fh)
    sys.exit(1)

data_link = button.get('data-link')
if not data_link:
    print("按钮未包含 data-link 属性")
    with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
        print('FETCH_ERROR=true', file=fh)
    sys.exit(1)

# 将 data-link 的值输出到 DYNAMIC_URL 环境变量
with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
    print(f'DYNAMIC_URL={data_link}', file=fh)

try:
    data_response = requests.get(data_link)
    data_response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"请求 data-link 失败: {e}")
    with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
        print('FETCH_ERROR=true', file=fh)
    sys.exit(1)

data_content = data_response.text
output_dir = "xConfig"
output_file = os.path.join(output_dir, "output.yaml")

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

file_exists = os.path.exists(output_file)
old_content = ""
if file_exists:
    with open(output_file, 'r') as file:
        old_content = file.read()

if data_content == old_content:
    print("内容无修改，无需更新")
    with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
        print('HAS_CHANGES=false', file=fh)
    sys.exit(0)

with open(output_file, 'w') as file:
    yaml.dump({'data': data_content}, file)

print(f"Updated {output_file} with data from {data_link}")
with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
    print('HAS_CHANGES=true', file=fh)
