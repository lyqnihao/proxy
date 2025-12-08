#!/usr/bin/env python3
"""
NodeFree 订阅更新器

功能：
- 从 nodefree.githubrowcontent.com 获取每日订阅
- 支持动态日期 URL：根据当前日期自动生成下载链接
- 自动检测变更并提交到 Git

工作流程：
1. 获取北京时间（用于生成日期）
2. 根据日期生成 NodeFree 订阅 URL
3. 下载订阅文件
4. 检测文件是否有变更
5. 如果有变更，提交到 Git

示例：
如果今天是 2025-12-03，会生成 URL：
https://nodefree.githubrowcontent.com/2025/12/20251203.yaml
"""
import os
import sys
import subprocess
# 从同目录的 updater_utils 导入共享函数
sys.path.insert(0, os.path.dirname(__file__))  # 添加当前目录到 Python 路径
from updater_utils import get_beijing_time, fetch_url, git_add_and_check

def main():
    """主函数 - NodeFree 订阅更新"""
    try:
        # 获取北京时间信息
        time_info = get_beijing_time()
        year, month, day = time_info['YEAR'], time_info['MONTH'], time_info['DAY']
        date_str = year + month + day  # 拼接成 YYYYMMDD 格式
        year_month = f"{year}/{month}"  # YYYY/MM 格式
        
        # 根据日期生成 NodeFree 订阅 URL
        # nodefree 每天都会发布一个新的订阅文件
        # 文件名格式为：YYYYMMDD.yaml
        # 文件路径格式为：/YYYY/MM/YYYYMMDD.yaml
        url = f"https://nodefree.githubrowcontent.com/{year_month}/{date_str}.yaml"
        # 指定输出文件位置
        output_file = "nodefree/target.yaml"
        
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        # 删除旧文件（为了检测变更）
        if os.path.exists(output_file):
            os.remove(output_file)
        
        # 下载订阅文件
        success, error = fetch_url(url, output_file)
        if not success:
            print(f"[nodefree] 错误: {error}")
            return 1  # 返回 1（出错）
        
        # 检查文件大小
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            if file_size < 500:  # 文件大小小于500字节认为是无效的
                print(f"[nodefree] 错误: 文件大小异常 ({file_size} 字节)，可能订阅内容无效")
                os.remove(output_file)  # 删除异常的小文件
                return 1
        
        # 检查文件是否有变更，并将其加入 Git 暂存区
        if git_add_and_check(output_file):
            print(f"[nodefree] 已更新: {url}")
            return 0
        else:
            print(f"[nodefree] 检测到无变更")
            return 0
    except Exception as e:
        print(f"[nodefree] 未预期的错误: {str(e)}")
        return 1

# 程序入口
if __name__ == '__main__':
    sys.exit(main())