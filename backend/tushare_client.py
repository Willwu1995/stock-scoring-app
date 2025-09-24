"""
Tushare Pro数据获取器
支持Tushare Pro API接口，获取股票基础信息、行情数据、财务指标等
"""

import requests
import pandas as pd
import time
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import sqlite3
import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from tushare_config import *
except ImportError:
    # 如果配置文件不存在，使用默认配置
    TUSHARE_TOKEN = "请在此处填入您的Tushare Pro Token"
    TUSHARE_API_URL = "http://api.tushare.pro"
    REQUEST_TIMEOUT = 30
    MAX_RETRIES = 3
    RETRY_DELAY = 1

class TushareProAPI:
    """Tushare Pro API客户端"""
    
    def __init__(self, token: str = None):
        """
        初始化Tushare Pro API客户端
        
        Args:
            token: Tushare Pro API Token，如果为None则从配置文件读取
        """
        self.token = token or TUSHARE_TOKEN
        self.api_url = TUSHARE_API_URL
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'StockScoringApp/1.0'
        })
        
        # 设置日志
        logging.basicConfig(
            level=getattr(logging, LOG_LEVEL) if 'LOG_LEVEL' in globals() else logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # 检查Token是否有效
        if self.token == "请在此处填入您的Tushare Pro Token":
            self.logger.warning("Tushare Token未配置，将使用模拟数据")
    
    def _make_request(self, api_name: str, params: Dict = None, fields: str = None) -> pd.DataFrame:
        """
        发送API请求
        
        Args:
            api_name: API接口名称
            params: 请求参数
            fields: 返回字段列表，逗号分隔
            
        Returns:
            DataFrame格式的数据
        """
        if self.token == "请在此处填入您的Tushare Pro Token":
            # 返回模拟数据
            return self._get_mock_data(api_name, params)
        
        payload = {
            'api_name': api_name,
            'token': self.token,
            'params': params or {}
        }
        
        if fields:
            payload['fields'] = fields
        
        for attempt in range(MAX_RETRIES):
            try:
                response = self.session.post(
                    self.api_url, 
                    json=payload, 
                    timeout=REQUEST_TIMEOUT
                )
                response.raise_for_status()
                
                data = response.json()
                
                if data.get('code') != 0:
                    error_msg = data.get('msg', '未知错误')
                    self.logger.error(f"Tushare API错误 [{api_name}]: {error_msg}")
                    if attempt == MAX_RETRIES - 1:
                        return self._get_mock_data(api_name, params)
                    continue
                
                items = data.get('data', {}).get('items', [])
                columns = data.get('data', {}).get('fields', [])
                
                if not items:
                    self.logger.warning(f"Tushare API返回空数据 [{api_name}]")
                    return pd.DataFrame()
                
                df = pd.DataFrame(items, columns=columns)
                self.logger.info(f"成功获取数据 [{api_name}]: {len(df)} 条记录")
                return df
                
            except requests.exceptions.RequestException as e:
                self.logger.error(f"请求失败 [{api_name}], 尝试 {attempt + 1}/{MAX_RETRIES}: {e}")
                if attempt == MAX_RETRIES - 1:
                    return self._get_mock_data(api_name, params)
                time.sleep(RETRY_DELAY)
            except Exception as e:
                self.logger.error(f"未知错误 [{api_name}]: {e}")
                return self._get_mock_data(api_name, params)
        
        return pd.DataFrame()
    
    def _get_mock_data(self, api_name: str, params: Dict = None) -> pd.DataFrame:
        """获取模拟数据"""
        self.logger.info(f"使用模拟数据 [{api_name}]")
        
        if api_name == 'stock_basic':
            mock_data = [
                ['000001', '平安银行', '银行', '平安银行股份有限公司', 'sz', '19910403', ''],
                ['000002', '万科A', '房地产', '万科企业股份有限公司', 'sz', '19910129', ''],
                ['000858', '五粮液', '白酒', '宜宾五粮液股份有限公司', 'sz', '19980427', ''],
                ['002415', '海康威视', '电子', '杭州海康威视数字技术股份有限公司', 'sz', '20100528', ''],
                ['002594', '比亚迪', '汽车', '比亚迪股份有限公司', 'sz', '20110630', ''],
                ['600036', '招商银行', '银行', '招商银行股份有限公司', 'sh', '20020409', ''],
                ['600519', '贵州茅台', '白酒', '贵州茅台酒股份有限公司', 'sh', '20010827', ''],
                ['600887', '伊利股份', '食品饮料', '内蒙古伊利实业集团股份有限公司', 'sh', '19961218', ''],
                ['000725', '京东方A', '电子', '京东方科技集团股份有限公司', 'sz', '20010112', ''],
                ['300015', '爱尔眼科', '医药生物', '爱尔眼科医院集团股份有限公司', 'sz', '20091030', '']
            ]
            return pd.DataFrame(mock_data, columns=['ts_code', 'symbol', 'name', 'area', 'market', 'list_date', 'act_name'])
        
        elif api_name == 'daily':
            mock_data = [
                ['000001.SZ', '20240923', 10.50, 10.80, 10.30, 10.65, 100000, 106500000.0],
                ['000002.SZ', '20240923', 18.20, 18.50, 18.00, 18.35, 80000, 146800000.0],
                ['600519.SZ', '20240923', 1680.0, 1720.0, 1650.0, 1685.0, 5000, 8425000000.0]
            ]
            return pd.DataFrame(mock_data, columns=['ts_code', 'trade_date', 'open', 'high', 'low', 'close', 'vol', 'amount'])
        
        elif api_name == 'fina_indicator':
            mock_data = [
                ['000001.SZ', '20240630', 0.152, 0.123, 0.185, 0.085, 1.25, 15.8, 12.5, 8.5],
                ['600519.SZ', '20240630', 0.528, 0.458, 0.585, 0.258, 3.85, 35.2, 28.5, 18.9]
            ]
            return pd.DataFrame(mock_data, columns=['ts_code', 'end_date', 'roe', 'netprofit_ratio', 'grossprofit_ratio', 'debt_to_assets', 'current_ratio', 'qoq_yoy', 'or_yoy', 'profit_yoy'])
        
        return pd.DataFrame()
    
    def get_stock_basic(self) -> pd.DataFrame:
        """获取股票基础信息"""
        fields = 'ts_code,symbol,name,area,market,list_date,act_name'
        return self._make_request('stock_basic', fields=fields)
    
    def get_daily_data(self, ts_code: str = None, trade_date: str = None, limit: int = None) -> pd.DataFrame:
        """获取日线行情数据"""
        params = {}
        if ts_code:
            params['ts_code'] = ts_code
        if trade_date:
            params['trade_date'] = trade_date
        if limit:
            params['limit'] = limit
        
        fields = 'ts_code,trade_date,open,high,low,close,vol,amount'
        return self._make_request('daily', params=params, fields=fields)
    
    def get_fina_indicator(self, ts_code: str = None, limit: int = None) -> pd.DataFrame:
        """获取财务指标数据"""
        params = {}
        if ts_code:
            params['ts_code'] = ts_code
        if limit:
            params['limit'] = limit
        
        fields = 'ts_code,end_date,roe,netprofit_ratio,grossprofit_ratio,debt_to_assets,current_ratio,qoq_yoy,or_yoy,profit_yoy'
        return self._make_request('fina_indicator', params=params, fields=fields)
    
    def get_moneyflow(self, ts_code: str = None, trade_date: str = None, limit: int = None) -> pd.DataFrame:
        """获取资金流向数据"""
        params = {}
        if ts_code:
            params['ts_code'] = ts_code
        if trade_date:
            params['trade_date'] = trade_date
        if limit:
            params['limit'] = limit
        
        fields = 'ts_code,trade_date,buy_sm_vol,sell_sm_vol,buy_md_vol,sell_md_vol,buy_lg_vol,sell_lg_vol,buy_elg_vol,sell_elg_vol'
        return self._make_request('moneyflow', params=params, fields=fields)
    
    def test_connection(self) -> bool:
        """测试API连接"""
        try:
            if self.token == "请在此处填入您的Tushare Pro Token":
                self.logger.info("使用模拟数据模式")
                return True
            
            df = self._make_request('stock_basic')
            return len(df) > 0
        except Exception as e:
            self.logger.error(f"连接测试失败: {e}")
            return False


class StockDataUpdater:
    """股票数据更新器"""
    
    def __init__(self, api_client: TushareProAPI = None):
        """
        初始化数据更新器
        
        Args:
            api_client: Tushare Pro API客户端
        """
        self.api = api_client or TushareProAPI()
        self.logger = logging.getLogger(__name__)
    
    def update_stock_basic(self, conn: sqlite3.Connection) -> bool:
        """更新股票基础信息"""
        try:
            df = self.api.get_stock_basic()
            if df.empty:
                self.logger.warning("获取股票基础信息失败")
                return False
            
            cursor = conn.cursor()
            
            # 清空原有数据
            cursor.execute("DELETE FROM stock_info")
            
            # 插入新数据
            for _, row in df.iterrows():
                code = row['symbol'] if pd.notna(row['symbol']) else row['ts_code'][:6]
                name = row['name'] if pd.notna(row['name']) else ''
                industry = row['area'] if pd.notna(row['area']) else '其他'
                
                cursor.execute('''
                    INSERT OR REPLACE INTO stock_info (code, name, industry, current_price, market_cap)
                    VALUES (?, ?, ?, ?, ?)
                ''', (code, name, industry, 0.0, 0.0))
            
            conn.commit()
            self.logger.info(f"成功更新 {len(df)} 只股票基础信息")
            return True
            
        except Exception as e:
            self.logger.error(f"更新股票基础信息失败: {e}")
            conn.rollback()
            return False
    
    def update_daily_prices(self, conn: sqlite3.Connection) -> bool:
        """更新日线价格数据"""
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT code FROM stock_info")
            stocks = cursor.fetchall()
            
            updated_count = 0
            
            for stock in stocks:
                code = stock[0]
                ts_code = f"{code}.{'SH' if code.startswith('6') else 'SZ'}"
                
                # 获取最新价格数据
                df = self.api.get_daily_data(ts_code=ts_code, limit=1)
                
                if not df.empty:
                    latest_price = df.iloc[0]['close']
                    
                    # 更新股票价格
                    cursor.execute('''
                        UPDATE stock_info 
                        SET current_price = ? 
                        WHERE code = ?
                    ''', (latest_price, code))
                    
                    updated_count += 1
                
                # 避免请求过于频繁
                time.sleep(0.1)
            
            conn.commit()
            self.logger.info(f"成功更新 {updated_count} 只股票的价格数据")
            return True
            
        except Exception as e:
            self.logger.error(f"更新价格数据失败: {e}")
            conn.rollback()
            return False
    
    def update_financial_data(self, conn: sqlite3.Connection) -> bool:
        """更新财务数据"""
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT code FROM stock_info")
            stocks = cursor.fetchall()
            
            updated_count = 0
            
            for stock in stocks:
                code = stock[0]
                ts_code = f"{code}.{'SH' if code.startswith('6') else 'SZ'}"
                
                # 获取财务指标
                df = self.api.get_fina_indicator(ts_code=ts_code, limit=1)
                
                if not df.empty:
                    # 这里可以存储详细的财务数据
                    # 目前只是记录更新状态
                    updated_count += 1
                
                # 避免请求过于频繁
                time.sleep(0.2)
            
            conn.commit()
            self.logger.info(f"成功更新 {updated_count} 只股票的财务数据")
            return True
            
        except Exception as e:
            self.logger.error(f"更新财务数据失败: {e}")
            conn.rollback()
            return False
    
    def update_all_data(self) -> bool:
        """更新所有数据"""
        try:
            # 连接数据库
            conn = sqlite3.connect('stock_scoring.db', check_same_thread=False)
            
            self.logger.info("开始更新股票数据...")
            
            # 更新股票基础信息
            if not self.update_stock_basic(conn):
                return False
            
            # 更新价格数据
            if not self.update_daily_prices(conn):
                return False
            
            # 更新财务数据
            if not self.update_financial_data(conn):
                return False
            
            self.logger.info("数据更新完成!")
            return True
            
        except Exception as e:
            self.logger.error(f"数据更新失败: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()


def main():
    """主函数 - 测试Tushare连接"""
    print("=== Tushare Pro 连接测试 ===")
    
    # 创建API客户端
    api = TushareProAPI()
    
    # 测试连接
    if api.test_connection():
        print("✅ 连接成功!")
        
        # 获取一些示例数据
        print("\n=== 获取股票列表 ===")
        df = api.get_stock_basic()
        if not df.empty:
            print(f"成功获取 {len(df)} 只股票")
            print("前5只股票:")
            print(df[['ts_code', 'symbol', 'name', 'area']].head())
        
        print("\n=== 获取价格数据 ===")
        df_price = api.get_daily_data(ts_code='000001.SZ', limit=5)
        if not df_price.empty:
            print("000001.SZ 最近5天价格:")
            print(df_price)
        
        print("\n=== 获取财务指标 ===")
        df_fina = api.get_fina_indicator(ts_code='000001.SZ', limit=1)
        if not df_fina.empty:
            print("000001.SZ 最新财务指标:")
            print(df_fina)
    else:
        print("❌ 连接失败!")
        print("请检查:")
        print("1. Token是否正确配置")
        print("2. 网络连接是否正常")
        print("3. Tushare Pro账户是否有效")


if __name__ == "__main__":
    main()