#!/usr/bin/env python3
"""
Tushare配置测试脚本（简化版）
用于测试Tushare配置是否正确
"""

import os
import sys

def test_config():
    """测试配置文件"""
    config_file = os.path.join(os.path.dirname(__file__), 'tushare_config.py')
    
    print("=== Tushare配置检查 ===")
    
    # 检查配置文件是否存在
    if not os.path.exists(config_file):
        print(f"❌ 配置文件不存在: {config_file}")
        return False
    
    try:
        # 读取配置文件
        with open(config_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查Token
        if "TUSHARE_TOKEN" in content:
            # 提取Token值
            import re
            match = re.search(r'TUSHARE_TOKEN\s*=\s*["\']([^"\']*)["\']', content)
            if match:
                token = match.group(1)
                if token == "请在此处填入您的Tushare Pro Token":
                    print("⚠️  Token未设置，使用模拟数据模式")
                    print("📝 请设置您的Tushare Token:")
                    print("   python3 setup_token.py set <your_token>")
                    return True
                else:
                    print("✅ Token已配置")
                    # 显示部分Token（保护隐私）
                    masked_token = token[:4] + "*" * (len(token) - 8) + token[-4:] if len(token) > 8 else "*" * len(token)
                    print(f"   Token: {masked_token}")
                    return True
            else:
                print("❌ Token格式错误")
                return False
        else:
            print("❌ 配置文件中未找到TUSHARE_TOKEN")
            return False
            
    except Exception as e:
        print(f"❌ 读取配置文件失败: {e}")
        return False

def show_setup_instructions():
    """显示设置说明"""
    print("""
=== Tushare设置说明 ===

1. 获取Token:
   - 访问 https://tushare.pro 注册账号
   - 登录后获取API Token

2. 设置Token:
   python3 setup_token.py set <your_token>

3. 验证配置:
   python3 setup_token.py test

4. 使用说明:
   - 免费版Token有限制，建议控制调用频率
   - Token请妥善保管，不要泄露
   - 遇到问题可查看Tushare官方文档

=== 当前状态 ===
""")

def main():
    """主函数"""
    if len(sys.argv) > 1 and sys.argv[1] == "help":
        show_setup_instructions()
        return
    
    # 检查配置
    config_ok = test_config()
    
    if config_ok:
        print("\n✅ 配置检查完成")
        
        # 显示设置说明
        show_setup_instructions()
    else:
        print("\n❌ 配置检查失败")
        print("请检查配置文件或重新设置")

if __name__ == "__main__":
    main()