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
    try:
        # 使用 curl 下载文件
        result = subprocess.run(
            ["curl", "-f", "-L", "-o", output_file, url],
            capture_output=True,
            text=True,
            timeout=30  # 30 秒超时
        )
        # 检查 curl 是否执行成功
        if result.returncode != 0:
            return False, f"curl 失败: {result.stderr}"
        
        # 检查下载的文件大小
        if not os.path.getsize(output_file) > 0:
            return False, "下载的文件为空"
        
        return True, None
    except Exception as e:
        return False, str(e)

def git_has_changes(file_path: str) -> bool:
    """
    检查文件是否有暂存的变更
    
    参数：
    - file_path: 要检查的文件路径
    
    返回值：
    - True: 文件有变更
    - False: 文件无变更
    """
    # 使用 git diff 检查暂存区中的变更
    result = subprocess.run(
        ["git", "diff", "--staged", "--quiet", file_path],
        capture_output=True
    )
    # 返回码为 0 表示无变更，非 0 表示有变更
    return result.returncode != 0

def git_add_and_check(file_path: str) -> bool:
    """
    将文件添加到 Git 暂存区并检查是否有变更
    
    参数：
    - file_path: 要添加的文件路径
    
    返回值：
    - True: 文件有变更
    - False: 文件无变更
    """
    # 将文件加入 Git 暂存区
    subprocess.run(["git", "add", file_path], capture_output=True)
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
