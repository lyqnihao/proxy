#!/usr/bin/env python3
"""
DanFeng 订阅链接生成器
从 https://sniweb.danfeng.eu.org/ 获取动态订阅链接
"""

import re
import subprocess
import sys
import random
import urllib.parse

def fetch_page_content(url: str) -> tuple:
    """获取网页内容"""
    try:
        result = subprocess.run(
            ["curl", "-s", "-L", "-A", "Mozilla/5.0", url],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0 and result.stdout:
            return True, result.stdout
        return False, ""
    except Exception as e:
        return False, ""

def extract_variables(content: str) -> tuple:
    """从页面内容中提取 authToken 和 domains"""
    # 提取 authToken
    auth_match = re.search(r"const\s+authToken\s*=\s*['\"]([^'\"]+)['\"]", content)
    if not auth_match:
        return None, None
    auth_token = auth_match.group(1)

    # 提取 domains 数组
    domains_match = re.search(r"const\s+domains\s*=\s*\[(.*?)\];", content, re.DOTALL)
    if not domains_match:
        return None, None

    # 解析域名数组
    domains_str = domains_match.group(1)
    domains = re.findall(r"['\"]([^'\"]+)['\"]", domains_str)

    return auth_token, domains

def random_label(length: int) -> str:
    """生成符合域名标签语法的随机字符串"""
    letters = 'abcdefghijklmnopqrstuvwxyz'
    letters_digits = 'abcdefghijklmnopqrstuvwxyz0123456789'
    letters_digits_hyphen = 'abcdefghijklmnopqrstuvwxyz0123456789-'

    if length < 2:
        return letters[random.randint(0, len(letters) - 1)]

    # 首字符
    s = letters[random.randint(0, len(letters) - 1)]
    # 中间字符
    for _ in range(length - 2):
        s += letters_digits_hyphen[random.randint(0, len(letters_digits_hyphen) - 1)]
    # 末字符
    s += letters_digits[random.randint(0, len(letters_digits) - 1)]

    return s

def generate_subscription_url(auth_token: str, domains: list) -> str:
    """生成订阅链接"""
    random_sub = random_label(12)
    random_domain = random.choice(domains)

    # 对 path 参数进行编码，避免嵌套的 ? 导致 URL 格式错误
    path_value = "/danfeng?ed=2560"
    url = f"https://{random_sub}.chinat.eu.org/sub?uuid={urllib.parse.quote(auth_token)}&host={urllib.parse.quote(random_domain)}&path={urllib.parse.quote(path_value, safe='')}&ech=1"

    return url

def main():
    url = "https://sniweb.danfeng.eu.org/"

    # 静默获取页面（不要输出调试信息，以免影响 stdout 的 URL 输出）

    success, content = fetch_page_content(url)
    if not success or not content:
        print("获取页面失败")
        return 1

    auth_token, domains = extract_variables(content)
    if not auth_token or not domains:
        print("解析页面变量失败")
        return 1

    subscription_url = generate_subscription_url(auth_token, domains)

    # 只输出 URL 到 stdout（供外部脚本使用），不要有其他输出
    print(subscription_url)

    return 0

if __name__ == "__main__":
    sys.exit(main())
