#!/usr/bin/env python3
"""
模块化订阅更新器 - 共享工具函数库

这个模块包含所有订阅更新脚本都需要用到的通用函数：
- 获取北京时间
- 下载文件
- Git 操作
- v2clash.blog 检查
"""
import os          # 操作系统接口
import sys         # 系统特定参数和函数
import subprocess  # 执行外部命令
from typing import Tuple, Optional  # 类型提示

def get_beijing_time() -> dict:
    """
    获取当前北京时间的年月日组件
    
    返回值是一个字典，包含：
    - YEAR: 四位年份（如 2025）
    - MONTH: 两位月份（01-12）
    - DAY: 两位日期（01-31）
    - DATE: 日期字符串 (YYYY-MM-DD)
    - TIME: 时间字符串 (HH:MM:SS)
    """
    # 使用 bash 命令和 date 工具获取北京时间
    result = subprocess.run(
        ["bash", "-c", "TZ='Asia/Shanghai' date +'%Y %m %d %Y-%m-%d %H:%M:%S'"],
        capture_output=True,
        text=True
    )
    # 分割输出字符串
    parts = result.stdout.strip().split()
    return {
        'YEAR': parts[0],      # 年份
        'MONTH': parts[1],     # 月份
        'DAY': parts[2],       # 日期
        'DATE': parts[3],      # YYYY-MM-DD
        'TIME': parts[4]       # HH:MM:SS
    }

def fetch_url(url: str, output_file: str) -> Tuple[bool, Optional[str]]:
    """
    从 URL 下载文件到指定位置
    
    参数：
    - url: 要下载的 URL 地址
    - output_file: 下载文件的保存路径
    
    返回值：
    - (True, None): 下载成功
    - (False, 错误信息): 下载失败，返回错误说明
    """
    # 增强版的下载函数：添加重试、更多的错误上下文以及对空文件的处理
    retries = 2
    last_err = ""
    for attempt in range(1, retries + 1):
        try:
            # 使用 curl 下载文件
            cmd = [
                "curl",
                "-f",  # 失败时返回非 0
                "-L",  # 跟随重定向
                "-H", "Cache-Control: no-cache",
                "-o", output_file,
                url
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

            # 如果 curl 返回码为 0，进一步检查文件是否存在且非空
            if result.returncode == 0:
                if os.path.exists(output_file):
                    try:
                        file_size = os.path.getsize(output_file)
                    except Exception:
                        file_size = None
                    
                    # 检查文件大小，只有大于1KB的文件才认为是有效内容
                    if file_size is None or file_size < 1024:
                        # 文件太小或无法获取大小，视作失败，删除并重试（如果还有剩余重试次数）
                        size_desc = "无法获取大小" if file_size is None else f"大小={file_size}字节"
                        last_err = f"下载成功但文件太小（{output_file}，{size_desc}）: 尝试 {attempt}/{retries}"
                        try:
                            os.remove(output_file)
                        except Exception:
                            pass
                        # 如果不是最后一次尝试，继续重试
                        if attempt < retries:
                            continue
                        else:
                            return False, last_err
                # 文件足够大，视为成功
                return True, None

            # curl 返回非 0：收集 stderr/stdout 帮助排查
            stderr = (result.stderr or "").strip()
            stdout = (result.stdout or "").strip()
            last_err = f"curl 返回码 {result.returncode}; stderr: {stderr[:300]}; stdout: {stdout[:300]}; 尝试 {attempt}/{retries}"
            # 清理可能部分写入的文件以免下次误判
            if os.path.exists(output_file):
                try:
                    os.remove(output_file)
                except Exception:
                    pass
            # 若非最后一次尝试，则继续重试
            if attempt < retries:
                continue
            else:
                # 最后一次尝试仍失败，返回详细错误信息
                # 如果文件存在，附加文件大小信息
                size_info = None
                try:
                    if os.path.exists(output_file):
                        size_info = os.path.getsize(output_file)
                except Exception:
                    size_info = None
                size_suffix = f"; 文件大小={size_info}" if size_info is not None else ""
                return False, f"下载失败: {last_err}{size_suffix}"

        except Exception as e:
            # 捕获 subprocess 以外的异常（例如超时、权限问题等）
            last_err = f"异常: {str(e)[:300]}; 尝试 {attempt}/{retries}"
            if os.path.exists(output_file):
                try:
                    os.remove(output_file)
                except Exception:
                    pass
            if attempt < retries:
                continue
            return False, f"下载异常: {last_err}"

def git_has_changes(file_path: str) -> bool:
    """
    检查文件在工作区或暂存区是否有任何变更
    
    参数：
    - file_path: 要检查的文件路径
    
    返回值：
    - True: 文件有变更
    - False: 文件无变更
    """
    # 使用 git status --porcelain 检查文件状态
    # 如果有输出，则表示文件有变更
    result = subprocess.run(
        ["git", "status", "--porcelain", file_path],
        capture_output=True,
        text=True
    )
    # strip() 去除空白字符，如果有任何内容则表示有变更
    return len(result.stdout.strip()) > 0

def git_add_and_check(file_path: str) -> bool:
    """
    将文件添加到 Git 暂存区并检查是否有变更
    
    参数：
    - file_path: 要添加的文件路径
    
    返回值：
    - True: 文件有变更
    - False: 文件无变更
    """
    # 执行 git add
    add_result = subprocess.run(["git", "add", file_path], capture_output=True, text=True)
    if add_result.returncode != 0:
        # 如果 git add 失败，可以记录错误或抛出异常
        print(f"Error adding {file_path}: {add_result.stderr}", file=sys.stderr)
        return False
    # 检查是否有变更
    return git_has_changes(file_path)

def check_v2clash_new_post() -> bool:
    """
    检查 v2clash.blog 是否有今天的新发布
    
    工作原理：
    1. 获取今天的日期（多种格式）
    2. 访问 v2clash.blog 网站
    3. 用 grep 搜索网页内容中是否包含今天的日期
    4. 如果找到，说明有新文章
    
    返回值：
    - True: 有新发布
    - False: 无新发布或网络错误
    """
    # 获取北京时间信息
    time_info = get_beijing_time()
    # 生成几种日期格式来匹配网页内容
    today = time_info['YEAR'] + time_info['MONTH'] + time_info['DAY']  # YYYYMMDD
    today_alt = time_info['DATE']  # YYYY-MM-DD
    # 中文日期格式（如果网页使用中文）
    today_cn = f"{time_info['YEAR']}年{time_info['MONTH']}月{time_info['DAY']}日"
    
    try:
        # 组合 curl 和 grep 命令：
        # curl 下载网页内容
        # | 管道符传给 grep
        # grep 搜索是否包含日期字符串
        result = subprocess.run(
            ["bash", "-c", f"curl -sL https://v2clash.blog/ | grep -qE '{today}|{today_alt}|{today_cn}'"],
            capture_output=True,
            timeout=15  # 网络操作 15 秒超时
        )
        # 返回码为 0 表示 grep 找到了匹配的内容
        return result.returncode == 0
    except:
        # 网络错误或超时
        return False