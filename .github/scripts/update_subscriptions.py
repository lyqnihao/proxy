#!/usr/bin/env python3
"""
通用订阅更新器 - 支持任何订阅配置的自动更新

这个脚本会：
1. 读取 JSON 配置文件中定义的订阅信息
2. 支持三种 URL 类型：固定 URL、包含日期的动态 URL、脚本生成的 URL
3. 自动下载订阅文件并检测变更
4. 将变更提交到 Git 仓库
"""
# 导入必要的模块
import os        # 操作系统接口（文件、环境变量）
import sys       # 系统特定参数和函数（用于 exit）
import json      # JSON 文件解析
import subprocess  # 执行外部命令（curl、git、bash）
import re        # 正则表达式（虽然这里没用到，保留兼容性）
from pathlib import Path  # 路径操作（虽然这里没用到，保留兼容性）
from datetime import datetime  # 日期时间（虽然这里没用到，保留兼容性）
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
    # 使用 bash 命令获取北京时间
    # TZ='Asia/Shanghai' 指定时区为北京时间
    # date +'%Y %m %d ...' 格式化输出
    result = subprocess.run(
        ["bash", "-c", "TZ='Asia/Shanghai' date +'%Y %m %d %Y-%m-%d %H:%M:%S'"],
        capture_output=True,  # 捕获输出
        text=True  # 以文本形式返回
    )
    # 将输出字符串分割成列表
    parts = result.stdout.strip().split()
    # 返回包含时间组件的字典
    return {
        'YEAR': parts[0],      # 年份
        'MONTH': parts[1],     # 月份
        'DAY': parts[2],       # 日期
        'DATE': parts[3],      # YYYY-MM-DD 格式
        'TIME': parts[4]       # HH:MM:SS 格式
    }

def fetch_url(url: str, output_file: str, subscription_name: str = "") -> Tuple[bool, Optional[str]]:
    """
    从 URL 下载文件
    
    参数：
    - url: 要下载的 URL 地址
    - output_file: 下载文件的保存路径
    - subscription_name: 订阅名称，用于特殊处理
    
    返回值：
    - (True, None): 下载成功
    - (False, 错误信息): 下载失败，返回错误说明
    """
    # 增强版的下载函数：添加重试、更多的错误上下文以及对空文件的处理
    # 设计目标：当下载失败时，返回尽可能多的有助于排查的问题信息
    retries = 2
    last_err = ""
    
    # 针对不同订阅源设置不同的超时时间
    timeout = 60 if subscription_name == "cmliu" else 30
    
    for attempt in range(1, retries + 1):
        try:
            # 确保输出文件的目录存在
            output_dir = os.path.dirname(output_file)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
            
            # 使用 curl 命令下载文件
            cmd = [
                "curl",
                "-f",  # 失败时返回非 0
                "-L",  # 跟随重定向
                "-H", "Cache-Control: no-cache",
                "-o", output_file,
                url
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)

            # 如果 curl 返回码为 0，进一步检查文件是否存在且非空
            if result.returncode == 0:
                if os.path.exists(output_file):
                    try:
                        file_size = os.path.getsize(output_file)
                    except Exception:
                        file_size = None
                    
                    # 检查文件大小，对于v2cross只做非空检查，其他订阅按常规500字节限制
                    if file_size is None or file_size == 0:
                        # 文件为空或无法获取大小，视作失败，删除并重试（如果还有剩余重试次数）
                        size_desc = "无法获取大小" if file_size is None else f"大小={file_size}字节"
                        last_err = f"下载成功但文件为空（{output_file}，{size_desc}）: 尝试 {attempt}/{retries}"
                        try:
                            os.remove(output_file)
                        except Exception:
                            pass
                        # 如果不是最后一次尝试，继续重试
                        if attempt < retries:
                            continue
                        else:
                            return False, last_err
                    elif subscription_name == "v2cross" and file_size > 0:
                        # v2cross只需要非空检查
                        return True, None
                    elif file_size < 500:
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

    return False, "下载失败：未知错误"


def git_has_changes(file_path: str) -> Tuple[bool, Optional[str]]:
    """
    检查文件是否有未暂存的变更
    
    参数：
    - file_path: 要检查的文件路径
    
    返回值：
    - True: 文件有变更（与上次提交不同）
    - False: 文件无变更（与上次提交相同）
    """
    # 确保文件存在，如果不存在则创建一个空文件
    if not os.path.exists(file_path):
        file_dir = os.path.dirname(file_path)
        if file_dir:
            os.makedirs(file_dir, exist_ok=True)
        with open(file_path, 'w') as f:
            pass  # 创建空文件
            
    # 使用 git 命令检查工作区中的文件变更
    result = subprocess.run(
        [
            "git", "diff",      # git 差异对比命令
            "--quiet",          # 安静模式（无输出，只返回代码）
            file_path           # 要检查的文件
        ],
        capture_output=True,
        text=True
    )
    # git diff --quiet 的返回码语义：
    # 0 -> 无差异；1 -> 有差异；其他 -> 错误
    if result.returncode == 0:
        return False, None
    if result.returncode == 1:
        return True, None
    # 其他返回码视为命令执行错误，返回 stderr 帮助诊断
    stderr = (result.stderr or "").strip()
    return False, f"git diff 错误, code={result.returncode}, stderr={stderr[:300]}"

def git_add_file(file_path: str) -> Tuple[bool, Optional[str]]:
    """
    检查文件是否有变更（不执行 git add）
    
    参数：
    - file_path: 要检查的文件路径
    
    返回值：
    - True: 文件有变更
    - False: 文件无变更
    """
    # 确保文件所在的目录存在
    file_dir = os.path.dirname(file_path)
    if file_dir:
        os.makedirs(file_dir, exist_ok=True)
    
    # 确保文件存在，如果不存在则创建一个空文件
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            pass  # 创建空文件
        
    # 先检查是否有变更
    has_changes, err = git_has_changes(file_path)
    if err:
        return False, f"git diff 检查失败: {err}"
    
    return has_changes, None

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
    today = time_info['YEAR'] + time_info['MONTH'] + time_info['DAY']  # YYYYMMDD 格式
    today_alt = time_info['DATE']  # YYYY-MM-DD 格式
    # 中文日期格式（如果网页使用中文）
    today_cn = f"{time_info['YEAR']}年{time_info['MONTH']}月{time_info['DAY']}日"
    
    try:
        # 使用 bash 命令组合 curl 和 grep
        result = subprocess.run(
            [
                "bash", "-c",  # 执行 bash 命令
                # 下面是 bash 命令的组合：
                # curl 获取网页，|（管道）传给 grep，grep 搜索日期字符串
                f"curl -sL https://v2clash.blog/ 2>/dev/null | grep -qE '{today}|{today_alt}|{today_cn}'"
            ],
            capture_output=True,
            timeout=15  # 15 秒超时（网络操作）
        )
        # 返回码为 0 表示 grep 找到了匹配的内容
        return result.returncode == 0
    except:
        # 网络错误或超时时返回 False
        return False

def run_url_script(script: str) -> Tuple[bool, Optional[str]]:
    """
    执行脚本以生成 URL
    
    有些订阅的 URL 需要通过运行脚本来生成（而不是固定的 URL）
    例如 v2cross 订阅需要执行 v2cross/update.py 来获取最新的 URL
    
    参数：
    - script: 要执行的脚本命令（如 'python v2cross/update.py'）
    
    返回值：
    - (True, URL): 脚本执行成功，返回生成的 URL
    - (False, 错误信息): 脚本执行失败
    """
    try:
        # 使用 bash 执行脚本
        cmd = ["bash", "-c", script]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

        # 如果脚本执行失败，返回更详细的错误信息帮助排查
        if result.returncode != 0:
            stderr = (result.stderr or "").strip()
            stdout = (result.stdout or "").strip()
            return False, f"命令: {script}; 退出码: {result.returncode}; stderr: {stderr[:300]}; stdout: {stdout[:300]}"

        # 脚本执行成功：输出即 URL
        url = result.stdout.strip()
        if not url:
            return False, f"脚本成功但未输出 URL：命令 {script}，stdout 为空"
        return True, url
    except subprocess.TimeoutExpired:
        return False, f"执行脚本超时: {script}"
    except FileNotFoundError:
        return False, f"找不到脚本或解释器: {script}"
    except Exception as e:
        return False, f"执行脚本异常: {str(e)[:300]}"

def expand_url(template: str, time_info: dict) -> str:
    """
    将 URL 模板中的日期变量替换为实际日期
    
    示例：
    输入: https://example.com/{YEAR}/{MONTH}/{DAY}.yaml
          time_info = {'YEAR': '2025', 'MONTH': '12', 'DAY': '03', ...}
    输出: https://example.com/2025/12/03.yaml
    
    参数：
    - template: 包含占位符的 URL 模板
    - time_info: 包含日期信息的字典
    
    返回值：
    - 替换后的完整 URL
    """
    # Python 的 format() 方法会自动替换 {YEAR}、{MONTH}、{DAY} 等占位符
    return template.format(
        YEAR=time_info['YEAR'],    # 替换 {YEAR}
        MONTH=time_info['MONTH'],  # 替换 {MONTH}
        DAY=time_info['DAY']       # 替换 {DAY}
    )

def get_time_info() -> dict:
    """
    获取时间信息，优先使用环境变量（由 GitHub Actions 设置），否则计算系统时间
    
    这个函数实现了一个"优先级"机制：
    1. 首先检查是否有环境变量 YEAR、MONTH、DAY（在 GitHub Actions 中会设置）
    2. 如果有，直接使用（这样更快，不需要执行外部命令）
    3. 如果没有，调用 get_beijing_time() 计算当前北京时间
    
    返回值：
    - 包含 YEAR、MONTH、DAY 的字典
    """
    # 从环境变量中读取时间信息（优先级最高）
    year = os.environ.get('YEAR')      # 获取 YEAR 环境变量，如果不存在返回 None
    month = os.environ.get('MONTH')    # 获取 MONTH 环境变量，如果不存在返回 None
    day = os.environ.get('DAY')        # 获取 DAY 环境变量，如果不存在返回 None
    
    # 如果环境变量都存在，直接使用它们（更快）
    if year and month and day:
        return {
            'YEAR': year,
            'MONTH': month,
            'DAY': day
        }
    
    # 环境变量不存在时，计算北京时间（备选方案）
    return get_beijing_time()

def update_subscription(config: dict) -> Tuple[int, str]:
    """
    更新单个订阅源 - 这是核心业务逻辑
    
    工作流程：
    1. 从配置中读取订阅信息（名称、目录、输出文件）
    2. 获取当前时间信息
    3. 根据 URL 类型生成或获取 URL
    4. 检查前置条件（如是否需要检查 v2clash 有无新文章）
    5. 下载文件
    6. 检测是否有变更
    7. 如果有变更，提交到 Git
    
    参数：
    - config: 订阅配置字典，包含：
        - name: 订阅名称
        - dir: 存储目录
        - output_file: 输出文件名
        - url_type: URL 类型（static/dynamic_date/dynamic_script）
        - url 或 url_template 或 url_script: URL 相关信息
        - requires_check: 前置检查条件（可选）
    
    返回值：
    - (0, 消息): 成功或无变更
    - (1, 错误信息): 出错
    """
    # 从配置中提取信息
    name = config.get('name')                    # 订阅名称（如 'cmliu'）
    directory = config.get('dir')                # 存储目录（如 'cmliu'）
    output_file_name = config.get('output_file')  # 输出文件名（如 'target.yaml'）
    output_file_path = os.path.join(directory, output_file_name)  # 完整路径
    
    # 创建存储目录（如果不存在）
    # exist_ok=True 表示目录已存在时不报错
    os.makedirs(directory, exist_ok=True)
    
    # 确保输出文件存在，如果不存在则创建一个空文件
    if not os.path.exists(output_file_path):
        with open(output_file_path, 'w') as f:
            pass  # 创建空文件
    
    # 获取当前时间信息（用于动态日期 URL）
    time_info = get_time_info()
    
    # 根据 URL 类型确定要下载的 URL
    url = None
    if config.get('url_type') == 'static':
        # 类型 1: 静态 URL（固定不变）
        url = config.get('url')
    elif config.get('url_type') == 'dynamic_date':
        # 类型 2: 动态日期 URL（包含日期变量，需要替换）
        url = expand_url(config.get('url_template'), time_info)
    elif config.get('url_type') == 'dynamic_script':
        # 类型 3: 脚本生成 URL（需要执行脚本获取）
        success, url = run_url_script(config.get('url_script'))
        if not success:
            # 脚本执行失败
            return 1, f"[{name}] 错误: {url}"
    
    # 检查前置条件（某些订阅需要满足特定条件才能下载）
    if config.get('requires_check') == 'v2clash_blog':
        # 前置条件: v2clash.blog 必须有新文章
        if not check_v2clash_new_post():
            # v2clash 无新文章，跳过这个订阅（不是错误，只是条件不满足）
            return 0, f"[{name}] 跳过: v2clash.blog 无新发布"
    
    # 检查 URL 是否有效
    if not url:
        return 1, f"[{name}] 错误: 无可用 URL"
    
    # 下载到临时文件，避免破坏现有文件
    import tempfile
    with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.yaml') as tmp_file:
        temp_file_path = tmp_file.name
    
    success, error = fetch_url(url, temp_file_path, name)
    if not success:
        # 下载失败，删除临时文件，保留原文件不变
        try:
            os.remove(temp_file_path)
        except Exception:
            pass
        return 1, f"[{name}] 错误: {error}"
    
    # 验证临时文件大小（非空）
    try:
        file_size = os.path.getsize(temp_file_path)
        if file_size == 0:
            os.remove(temp_file_path)
            return 1, f"[{name}] 错误: 下载的文件为空"
        # 对于非v2cross订阅，检查最小大小（500字节）
        if name != "v2cross" and file_size < 500:
            os.remove(temp_file_path)
            return 1, f"[{name}] 错误: 下载的文件太小（{file_size}字节）"
    except Exception as e:
        os.remove(temp_file_path)
        return 1, f"[{name}] 错误: 无法验证文件大小: {e}"
    
    # 检查临时文件与现有文件是否相同
    file_changed = True
    if os.path.exists(output_file_path):
        import filecmp
        if filecmp.cmp(output_file_path, temp_file_path, shallow=False):
            file_changed = False
            # 获取文件大小信息用于日志
            try:
                existing_size = os.path.getsize(output_file_path)
                new_size = file_size
                print(f"[{name}] 文件内容相同，大小: {existing_size} -> {new_size} 字节")
            except Exception:
                pass
    
    if file_changed:
        # 替换原文件
        os.replace(temp_file_path, output_file_path)
        print(f"[{name}] 文件已替换（{file_size} 字节）")
    else:
        # 内容相同，删除临时文件
        os.remove(temp_file_path)
        return 0, f"[{name}] 无变更"
    
    # 检查文件是否有变更（与上次提交比较）
    has_changes, err = git_add_file(output_file_path)
    if err:
        # Git操作出错
        return 1, f"[{name}] Git错误: {err}"
    
    if has_changes:
        # 有变更 -> 提交成功
        return 0, f"[{name}] 已更新: {url}"
    else:
        # 无变更 -> 文件内容与上次相同（理论上不会发生，因为filecmp已检查）
        return 0, f"[{name}] 无变更"

def main():
    """
    主函数 - 程序的入口点
    
    工作流程：
    1. 查找配置文件
    2. 读取 JSON 配置
    3. 可选地过滤特定订阅
    4. 遍历所有订阅并逐个更新
    5. 返回总体结果（有错误返回 1，全部成功返回 0）
    """
    # 配置文件路径
    config_path = '.github/config/subscriptions.json'
    
    # 检查配置文件是否存在
    if not os.path.exists(config_path):
        print(f"配置文件未找到: {config_path}")
        return 1
    
    # 打开并读取 JSON 配置文件
    with open(config_path, 'r', encoding='utf-8') as f:
        subscriptions = json.load(f)  # 解析 JSON，得到订阅列表
    
    # 支持选择性更新：如果设置了 SUB_NAME 环境变量，只处理该订阅
    # 这允许我们在需要时只更新特定订阅而不是全部
    target_name = os.environ.get('SUB_NAME')
    if target_name:
        # 过滤出名称匹配的订阅
        subscriptions = [s for s in subscriptions if s.get('name') == target_name]
        if not subscriptions:
            print(f"订阅未找到: {target_name}")
            return 1
    else:
        # 支持排除特定订阅：如果设置了 EXCLUDE_SUBS 环境变量，排除逗号分隔的订阅列表
        exclude_str = os.environ.get('EXCLUDE_SUBS')
        if exclude_str:
            exclude_list = [name.strip() for name in exclude_str.split(',') if name.strip()]
            original_count = len(subscriptions)
            subscriptions = [s for s in subscriptions if s.get('name') not in exclude_list]
            excluded_count = original_count - len(subscriptions)
            if excluded_count > 0:
                print(f"已排除 {excluded_count} 个订阅: {', '.join(exclude_list)}")
    
    # 标志：是否有任何订阅更新失败
    has_error = False
    failed_subscriptions = []  # 记录失败的订阅
    
    # 逐个处理每个订阅
    for sub_config in subscriptions:
        # 调用 update_subscription 更新单个订阅，获取退出码和消息
        exit_code, message = update_subscription(sub_config)
        # 打印消息（会显示在 GitHub Actions 日志中）
        print(message)
        # 如果返回码为 1（错误），标记有错误并记录失败的订阅
        if exit_code != 0:
            has_error = True
            # 提取订阅名称并添加到失败列表
            sub_name = sub_config.get('name', 'Unknown')
            failed_subscriptions.append(f"{sub_name}")
    
    # 如果有错误，输出失败的订阅信息到环境变量，供后续步骤使用
    if failed_subscriptions:
        failed_list = ", ".join(failed_subscriptions)
        # 将失败的订阅列表写入环境文件，供后续步骤使用
        output_file = os.getenv('GITHUB_OUTPUT')
        if output_file:
            with open(output_file, 'a') as f:
                f.write(f"failed_subscriptions={failed_list}\n")
    
    # 返回总体结果
    # 有错误返回 1，全部成功返回 0
    return 1 if has_error else 0

# Python 文件执行的标准入口
# 这行确保只有当这个文件被直接执行（而不是被 import）时，main() 才会被调用
if __name__ == '__main__':
    sys.exit(main())  # 调用 main()，并将返回值作为程序的退出码