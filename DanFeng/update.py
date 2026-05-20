#!/usr/bin/env python3
"""
DanFeng 订阅链接生成器
从 https://2sniweb.danfeng.eu.org/ 获取动态订阅链接
支持网页自动获取、环境变量、或硬编码备选值
"""

import re
import subprocess
import sys
import os
import random
import urllib.parse

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0.0.0 Safari/537.36"
)
ACCEPT_HEADERS = (
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,"
    "image/webp,*/*;q=0.8"
)

# 硬编码的备选配置（用户手动更新的值）
DEFAULT_AUTH_TOKEN = os.environ.get(
    "DANFENG_AUTH_TOKEN",
    "26524cce-d514-4014-a426-365fb266a14d"
)
DEFAULT_DOMAINS = os.environ.get(
    "DANFENG_DOMAINS",
    "_acme-challenge.443888.xyz,vtxpxgne.mirror-node.sh21.eu.org,wsm52.gateway-api-01.chinav.indevs.in,ar2m.api-backend.sh21.eu.org,qrqt.backend-edge.sh21.eu.org,sguj46k.static-node-01.chinav.eu.org,t39sed.gateway-api.sh21.eu.org,omn15.files-cdn.chinat.indevs.in,mz0tgmxz.user-api.chinav.eu.org,tq0iwf.user-service.chinav.eu.org,v3wdc.app-node.chinam.indevs.in,y4z.cdn-a.chinav.indevs.in,nai3.api-gateway-01.chinat.indevs.in,ii5.static-node-01.chinav.indevs.in,la463cv6.static-cache.chinam.indevs.in,y0wkd.app-edge.chinav.indevs.in,nxahk.media-cdn.sh21.eu.org,n76.api-node-sg.chinav.indevs.in,sg156m.cdn-edge-eu.sh21.eu.org,jek.media-cdn.chinav.eu.org,srd0l.monitor-edge.chinav.indevs.in,pkw.download.fgfw.qzz.io,le8535x4.data-stream.sh21.eu.org,vfa9.cdn-stream.fgfw.indevs.in,eedu7.mail.danfeng.qzz.io,nlrkld.files-api.danfeng.cyou,fo5xj.monitor-edge.chinat.indevs.in,c1mxc.api-gateway.fgfw.qzz.io,zllj95qn.api-node-sg.chinat.indevs.in,v8mbk9s.node-stream.danfeng.qzz.io,w9rw8g1k.node-c.danfeng.gv.uy,z8c.node-01.fgfw.qzz.io,n8wra.edge-a.danfeng.cyou,mv7wx5dn.node.chinat.indevs.in,munbd.user-node.sh21.eu.org,txunvh.api-node-02.danfeng.gv.uy,a44.static-node-01.chinav.eu.org,mrdt2a.node-01.danfeng.qzz.io,nmdul.node-cache.chinat.indevs.in,a36k.media-cdn-sg.chinav.indevs.in,x6n3ydn.mirror-cdn.danfeng.bond,yv4a7gbe.backend-api.chinam.indevs.in,lmy.node-cache-01.sh21.eu.org,bbyvxzyc.stream-cdn.danfeng.cyou,zt7onv.auth-node.chinam.indevs.in,qznql.node-proxy.chinat.indevs.in"
).split(",")



def _is_cloudflare_or_blocked(content: str) -> bool:
    lower = content.lower()
    return any(
        token in lower
        for token in (
            "checking your browser",
            "please verify you are",
            "正在进行安全验证",
            "cloudflare",
            "jschl_vc",
            "cf-challenge",
            "access denied",
            "forbidden",
        )
    )


def _fetch_with_curl(url: str) -> tuple:
    base_command = [
        "curl",
        "-s",
        "-L",
        "-A",
        USER_AGENT,
        "-H",
        f"Accept: {ACCEPT_HEADERS}",
        url,
    ]

    for extra in ([], ["--compressed"]):
        try:
            result = subprocess.run(
                base_command[:-1] + extra + [base_command[-1]],
                capture_output=True,
                text=True,
                timeout=30,
            )
            stdout = (result.stdout or "")
            if result.returncode == 0 and stdout:
                return True, stdout
            stderr = (result.stderr or "").strip()
            stdout = stdout.strip()
            if result.returncode != 0:
                return False, f"curl 返回码 {result.returncode}; stderr={stderr[:300]}; stdout={stdout[:300]}"
        except Exception as e:
            return False, str(e)
    return False, "curl 返回空结果"


def _install_package(package: str) -> None:
    subprocess.run(
        [sys.executable, "-m", "pip", "install", package],
        check=True,
        capture_output=True,
        text=True,
        timeout=300,
    )


def _install_playwright() -> None:
    _install_package("playwright")
    subprocess.run(
        [sys.executable, "-m", "playwright", "install", "chromium"],
        check=True,
        capture_output=True,
        text=True,
        timeout=600,
    )


def _fetch_with_cloudscraper(url: str) -> tuple:
    try:
        try:
            import cloudscraper
        except ImportError:
            _install_package("cloudscraper")
            import cloudscraper

        browser_options = (
            None,
            "chrome",
            {"browser": "chrome", "platform": "windows", "mobile": False},
            {"custom": USER_AGENT},
        )
        for browser_option in browser_options:
            try:
                scraper = (
                    cloudscraper.create_scraper(browser=browser_option)
                    if browser_option is not None
                    else cloudscraper.create_scraper()
                )
                r = scraper.get(url, timeout=30, headers={"Accept": ACCEPT_HEADERS})
                if r.status_code == 200 and r.text:
                    return True, r.text
                if r.status_code != 403:
                    return False, f"cloudscraper 返回状态 {r.status_code}"
            except Exception:
                continue
        return False, "cloudscraper 返回状态 403"
    except Exception as e:
        return False, str(e)


def _fetch_with_playwright(url: str) -> tuple:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        try:
            _install_playwright()
            from playwright.sync_api import sync_playwright
        except Exception as e:
            return False, f"playwright 安装失败: {e}"

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])
            page = browser.new_page(user_agent=USER_AGENT)
            page.goto(url, timeout=60000)
            content = page.content()
            browser.close()
            if content:
                return True, content
            return False, "playwright 获取页面内容失败"
    except Exception as e:
        return False, str(e)


def fetch_page_content(url: str) -> tuple:
    """获取网页内容"""
    success, content = _fetch_with_curl(url)
    if success and content:
        if _is_cloudflare_or_blocked(content):
            success, content = _fetch_with_cloudscraper(url)
            if success and content:
                return True, content
            if content and "403" in content:
                browser_success, browser_content = _fetch_with_playwright(url)
                if browser_success and browser_content:
                    return True, browser_content
            return False, (
                "检测到 Cloudflare 验证页面或禁止访问，且 cloudscraper 无法成功获取。"
                " 请安装 playwright 并运行 `python -m playwright install chromium`，"
                " 或手动在浏览器中完成验证。"
                f" (cloudscraper 结果: {content})"
            )
        return True, content

    if not success:
        success, content = _fetch_with_cloudscraper(url)
        if success and content:
            return True, content
        if content and "403" in content:
            browser_success, browser_content = _fetch_with_playwright(url)
            if browser_success and browser_content:
                return True, browser_content
        return False, (
            "无法通过 curl 或 cloudscraper 获取页面。"
            " 请检查网络或安装 playwright。"
            f" (详情: {content})"
        )

    return False, "未知错误：无法获取页面内容"


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
    url = "https://2sniweb.danfeng.eu.org/"

    # 静默获取页面（不要输出调试信息，以免影响 stdout 的 URL 输出）

    success, content = fetch_page_content(url)
    auth_token = None
    domains = None

    if success and content:
        auth_token, domains = extract_variables(content)

    # 如果网页获取失败或提取失败，使用硬编码的备选值
    if not auth_token or not domains:
        auth_token = DEFAULT_AUTH_TOKEN
        domains = DEFAULT_DOMAINS
        if not auth_token or not domains:
            print(
                "错误：无法获取 authToken 和 domains。"
                " 请手动在浏览器访问 https://2sniweb.danfeng.eu.org/ 并获取，"
                " 或设置环境变量 DANFENG_AUTH_TOKEN 和 DANFENG_DOMAINS。",
                file=sys.stderr
            )
            return 1

    subscription_url = generate_subscription_url(auth_token, domains)

    # 只输出 URL 到 stdout（供外部脚本使用），不要有其他输出
    print(subscription_url)

    return 0

if __name__ == "__main__":
    sys.exit(main())
