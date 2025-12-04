# 版本：1.1
# 修订原因：
# 版本：1.0
# 功能包括：初始版本，实现抓取网页内容、Python 脚本仅用于获取订阅地址。

# 尝试导入依赖库，如果失败则给出明确的错误提示
try:
    import requests  # 导入 requests 库，用于发送 HTTP 请求
except ImportError as e:
    print(f"错误：缺少 requests 库，请安装依赖后重试。", file=sys.stderr)
    sys.exit(1)

try:
    from bs4 import BeautifulSoup  # 导入 BeautifulSoup 库，用于解析 HTML 内容
except ImportError as e:
    print(f"错误：缺少 beautifulsoup4 库，请安装依赖后重试。", file=sys.stderr)
    sys.exit(1)

import re  # 导入 re 库，用于正则表达式匹配
import sys  # 导入 sys 库，用于退出程序时返回状态码

def fetch_subscription_url():
    """从目标网页提取订阅地址（已修复DeprecationWarning）"""
    url = "https://v2cross.com/1884.html"
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 修复点：使用string参数替代已弃用的text参数
            target_text = soup.find(string=re.compile(r'本次节点订阅地址：'))
            
            if target_text:
                # 使用正则精准匹配URL（排除多余字符）
                match = re.search(r'https?://[^\s]+', target_text)
                if match:
                    return match.group(0).rstrip('。')  # 去除中文句号
    except Exception as e:
        print(f"错误：获取订阅地址失败 - {str(e)}", file=sys.stderr)
        return None
    return None

# 读取目标网址的内容
def fetch_url_content(url):
    try:
        response = requests.get(url, timeout=30)  # 发送 HTTP 请求
        if response.status_code == 200:  # 检查请求是否成功
            return response.text  # 返回网页内容
    except Exception as e:
        print(f"错误：获取URL内容失败 - {str(e)}", file=sys.stderr)
        return None  # 如果请求失败，返回 None

# 主函数
def main():
    try:
       # 获取目标网址（增加输出格式控制）
        DYNAMIC_URL = fetch_subscription_url()
        if not DYNAMIC_URL:
            print("错误：无法提取订阅地址。", file=sys.stderr)  # 输出错误信息
            sys.exit(1)  # 返回状态码 1 表示失败
            
        # 输出目标网址的内容：去除换行符确保输出纯净URL
        print(DYNAMIC_URL, end='')
    except Exception as e:
        print(f"v2cross 脚本执行出错: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()