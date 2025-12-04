#!/usr/bin/env python3
"""
ProxyQueen 订阅更新器

功能：
- 从 v2clash.blog 获取 ProxyQueen 订阅
- 支持前置检查：仅当 v2clash.blog 有新文章时才下载更新
- 自动检测变更并提交到 Git

工作流程：
1. 获取北京时间
2. 检查 v2clash.blog 是否有今天的新发布
3. 如果有新发布，下载对应日期的订阅文件
4. 检测文件是否有变更
5. 如果有变更，提交到 Git
"""
import os
import sys
import subprocess
# 从同目录的 updater_utils 导入共享函数
sys.path.insert(0, os.path.dirname(__file__))  # 添加当前目录到 Python 路径
from updater_utils import get_beijing_time, fetch_url, git_add_and_check, check_v2clash_new_post

def main():
    """主函数 - ProxyQueen 订阅更新"""
    try:
        # 获取北京时间信息
        time_info = get_beijing_time()
        year, month, day = time_info['YEAR'], time_info['MONTH'], time_info['DAY']
        date_str = year + month + day  # 拼接成 YYYYMMDD 格式
        
        # 检查 v2clash 是否有新发布
        # 这是一个前置条件：只有 v2clash 有新文章才更新 proxyqueen
        if not check_v2clash_new_post():
            print(f"[proxyqueen] v2clash.blog 无新发布，跳过更新")
            return 0  # 返回 0（成功），但实际没有下载
        
        # 根据日期生成 v2clash 的 ProxyQueen URL
        url = f"https://v2clash.blog/Link/{date_str}-clash.yaml"
        # 指定输出文件位置
        output_file = "proxyqueen/output.yaml"
        
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        # 删除旧文件（为了检测变更）
        if os.path.exists(output_file):
            os.remove(output_file)
        
        # 下载订阅文件
        success, error = fetch_url(url, output_file)
        if not success:
            print(f"[proxyqueen] 错误: {error}")
            return 1  # 返回 1（出错）
            
        # 检查文件大小
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            if file_size < 100:  # 文件小于100字节可能是无效内容
                print(f"[proxyqueen] 错误: 下载的文件大小异常 ({file_size} 字节)，可能不是有效的订阅文件")
                os.remove(output_file)  # 删除异常文件
                return 1
        
        # 检查文件是否有变更，并将其加入 Git 暂存区
        if git_add_and_check(output_file):
            print(f"[proxyqueen] 已更新: {url}")
            return 0
        else:
            print(f"[proxyqueen] 检测到无变更")
            return 0
    except Exception as e:
        print(f"[proxyqueen] 未预期的错误: {str(e)}")
        return 1

# 程序入口
if __name__ == '__main__':
    sys.exit(main())