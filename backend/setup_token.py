#!/usr/bin/env python3
"""
Tushare Token配置工具
用于设置和管理Tushare Pro API Token
"""

import os
import sys

def set_tushare_token(token):
    """设置Tushare Token"""
    config_file = os.path.join(os.path.dirname(__file__), 'tushare_config.py')
    
    if not token or token.strip() == "":
        print("❌ Token不能为空")
        return False
    
    # 读取现有配置文件
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        # 如果配置文件不存在，创建默认配置
        content = '''# Tushare配置文件
# 请将您的Tushare Token填入下方

TUSHARE_TOKEN = "请在此处填入您的Tushare Pro Token"
'''
    
    # 替换Token
    import re
    pattern = r'TUSHARE_TOKEN\s*=\s*["\'][^"\']*["\']'
    replacement = f'TUSHARE_TOKEN = "{token.strip()}"'
    
    new_content = re.sub(pattern, replacement, content)
    
    # 写入文件
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✅ Token配置成功!")
        print(f"📁 配置文件: {config_file}")
        return True
    except Exception as e:
        print(f"❌ 配置文件写入失败: {e}")
        return False

def show_current_config():
    """显示当前配置"""
    config_file = os.path.join(os.path.dirname(__file__), 'tushare_config.py')
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        print("=== 当前配置 ===")
        for line in lines:
            if line.startswith('TUSHARE_TOKEN'):
                # 隐藏Token的部分字符
                if "请在此处填入" in line:
                    print(f"{line.strip()}")
                else:
                    # 提取Token值
                    import re
                    match = re.search(r'TUSHARE_TOKEN\s*=\s*["\']([^"\']*)["\']', line)
                    if match:
                        token = match.group(1)
                        masked_token = token[:8] + "*" * (len(token) - 12) + token[-4:] if len(token) > 12 else "*" * len(token)
                        print(f'TUSHARE_TOKEN = "{masked_token}"')
                    else:
                        print(line.strip())
                break
        
        print(f"\n📁 配置文件: {config_file}")
        
    except FileNotFoundError:
        print("❌ 配置文件不存在")
        print("请先运行此工具设置Token")

def test_connection():
    """测试连接"""
    try:
        from tushare_client import TushareProAPI
        api = TushareProAPI()
        
        print("=== 测试Tushare连接 ===")
        if api.test_connection():
            print("✅ 连接成功!")
            
            # 测试获取数据
            import pandas as pd
            df = api.get_stock_basic()
            if not df.empty:
                print(f"✅ 成功获取 {len(df)} 只股票数据")
            else:
                print("⚠️  获取数据为空")
            
            return True
        else:
            print("❌ 连接失败!")
            return False
            
    except ImportError as e:
        print(f"❌ 导入模块失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def show_help():
    """显示帮助信息"""
    print("""
Tushare Token配置工具

使用方法:
    python3 setup_token.py <command> [arguments]

命令:
    set <token>     - 设置Tushare Token
    show           - 显示当前配置
    test           - 测试连接
    help           - 显示帮助信息

示例:
    python3 setup_token.py set your_tushare_token_here
    python3 setup_token.py show
    python3 setup_token.py test

注意:
1. Token需要从Tushare Pro官网 (https://tushare.pro) 获取
2. 免费版Token有调用次数限制
3. 请妥善保管您的Token
    """)

def main():
    """主函数"""
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "set":
        if len(sys.argv) < 3:
            print("❌ 请提供Token")
            print("使用方法: python3 setup_token.py set <your_token>")
            return
        token = sys.argv[2]
        set_tushare_token(token)
    
    elif command == "show":
        show_current_config()
    
    elif command == "test":
        test_connection()
    
    elif command == "help":
        show_help()
    
    else:
        print(f"❌ 未知命令: {command}")
        show_help()

if __name__ == "__main__":
    main()