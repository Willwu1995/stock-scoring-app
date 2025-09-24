import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# 样本股票数据 (沪深300 + 高成长赛道个股)
sample_stocks = [
    # 沪深300成分股
    {'code': '000001', 'name': '平安银行', 'industry': '银行', 'price': 12.50},
    {'code': '000002', 'name': '万科A', 'industry': '房地产', 'price': 18.30},
    {'code': '000858', 'name': '五粮液', 'industry': '白酒', 'price': 168.50},
    {'code': '000895', 'name': '双汇发展', 'industry': '食品加工', 'price': 28.90},
    {'code': '002415', 'name': '海康威视', 'industry': '安防设备', 'price': 35.20},
    {'code': '002594', 'name': '比亚迪', 'industry': '新能源汽车', 'price': 268.80},
    {'code': '002714', 'name': '牧原股份', 'industry': '养殖业', 'price': 58.60},
    {'code': '300059', 'name': '东方财富', 'industry': '互联网金融服务', 'price': 22.40},
    {'code': '300750', 'name': '宁德时代', 'industry': '动力电池', 'price': 198.50},
    {'code': '600000', 'name': '浦发银行', 'industry': '银行', 'price': 8.90},
    {'code': '600036', 'name': '招商银行', 'industry': '银行', 'price': 42.30},
    {'code': '600519', 'name': '贵州茅台', 'industry': '白酒', 'price': 1680.00},
    {'code': '600887', 'name': '伊利股份', 'industry': '乳制品', 'price': 32.80},
    {'code': '600958', 'name': '中国平安', 'industry': '保险', 'price': 48.50},
    {'code': '601318', 'name': '中国平安', 'industry': '保险', 'price': 48.50},
    # 高成长赛道个股
    {'code': '300015', 'name': '爱尔眼科', 'industry': '医疗服务', 'price': 88.20},
    {'code': '300122', 'name': '智飞生物', 'industry': '生物制品', 'price': 145.60},
    {'code': '300142', 'name': '沃森生物', 'industry': '生物制品', 'price': 56.80},
    {'code': '300347', 'name': '泰格医药', 'industry': '医疗服务', 'price': 128.90},
    {'code': '300408', 'name': '三环集团', 'industry': '电子元件', 'price': 42.30},
    {'code': '300454', 'name': '深信服', 'industry': '软件服务', 'price': 185.60},
    {'code': '300498', 'name': '温氏股份', 'industry': '养殖业', 'price': 18.90},
    {'code': '300601', 'name': '康泰生物', 'industry': '生物制品', 'price': 78.50},
    {'code': '300628', 'name': '亿联网络', 'industry': '通信设备', 'price': 65.40},
    {'code': '300661', 'name': '圣邦股份', 'industry': '半导体', 'price': 235.80},
    {'code': '300676', 'name': '华大基因', 'industry': '生物制品', 'price': 98.60},
    {'code': '300760', 'name': '迈瑞医疗', 'industry': '医疗器械', 'price': 358.90},
    {'code': '300782', 'name': '卓胜微', 'industry': '半导体', 'price': 268.50},
    {'code': '300896', 'name': '爱美客', 'industry': '医美', 'price': 458.90},
    {'code': '002180', 'name': '纳思达', 'industry': '计算机设备', 'price': 45.60},
    {'code': '002371', 'name': '北方华创', 'industry': '半导体设备', 'price': 268.90},
    {'code': '002410', 'name': '广联达', 'industry': '软件服务', 'price': 68.50},
    {'code': '002460', 'name': '赣锋锂业', 'industry': '锂电池', 'price': 128.60},
    {'code': '002475', 'name': '立讯精密', 'industry': '电子制造', 'price': 38.50},
    {'code': '002624', 'name': '完美世界', 'industry': '游戏', 'price': 28.90},
]

# 生成指标数据
def generate_indicator_data(stock_code, industry):
    indicators = []
    
    # 行业维度指标
    lifecycle_stage = random.choice(['growth', 'mature', 'decline'])
    market_growth = random.uniform(10, 40)
    concentration = random.uniform(30, 80)
    policy_support = random.choice(['strong', 'medium', 'weak'])
    barrier_to_entry = random.choice(['high', 'medium', 'low'])
    
    indicators.extend([
        {'code': 'industry_lifecycle', 'value_text': lifecycle_stage, 'value': None},
        {'code': 'market_growth_rate', 'value': market_growth, 'value_text': None},
        {'code': 'industry_concentration', 'value': concentration, 'value_text': None},
        {'code': 'policy_support', 'value_text': policy_support, 'value': None},
        {'code': 'barrier_to_entry', 'value_text': barrier_to_entry, 'value': None},
    ])
    
    # 企业竞争力指标
    market_share = random.uniform(5, 35)
    revenue_growth = random.uniform(10, 45)
    profit_margin = random.uniform(8, 25)
    roe = random.uniform(12, 28)
    rd_intensity = random.uniform(3, 15)
    brand_value = random.choice(['strong', 'medium', 'weak'])
    management_team = random.choice(['excellent', 'good', 'average'])
    
    indicators.extend([
        {'code': 'market_share', 'value': market_share, 'value_text': None},
        {'code': 'revenue_growth', 'value': revenue_growth, 'value_text': None},
        {'code': 'profit_margin', 'value': profit_margin, 'value_text': None},
        {'code': 'roe', 'value': roe, 'value_text': None},
        {'code': 'r_d_intensity', 'value': rd_intensity, 'value_text': None},
        {'code': 'brand_value', 'value_text': brand_value, 'value': None},
        {'code': 'management_team', 'value_text': management_team, 'value': None},
    ])
    
    # 成长潜力指标
    future_growth = random.uniform(15, 35)
    new_business = random.choice(['high', 'medium', 'low'])
    market_expansion = random.choice(['strong', 'medium', 'weak'])
    innovation_capability = random.choice(['strong', 'medium', 'weak'])
    
    indicators.extend([
        {'code': 'future_growth', 'value': future_growth, 'value_text': None},
        {'code': 'new_business', 'value_text': new_business, 'value': None},
        {'code': 'market_expansion', 'value_text': market_expansion, 'value': None},
        {'code': 'innovation_capability', 'value_text': innovation_capability, 'value': None},
    ])
    
    # 时机维度指标
    valuation_level = random.choice(['low', 'medium', 'high'])
    market_sentiment = random.choice(['positive', 'neutral', 'negative'])
    technical_trend = random.choice(['uptrend', 'sideways', 'downtrend'])
    
    indicators.extend([
        {'code': 'valuation_level', 'value_text': valuation_level, 'value': None},
        {'code': 'market_sentiment', 'value_text': market_sentiment, 'value': None},
        {'code': 'technical_trend', 'value_text': technical_trend, 'value': None},
    ])
    
    return indicators

# 生成SQL插入语句
def generate_sql_inserts():
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 股票基础信息插入语句
    stock_inserts = []
    for stock in sample_stocks:
        market_cap = stock['price'] * random.uniform(10, 100)  # 模拟市值
        listing_date = (datetime.now() - timedelta(days=random.randint(365, 3650))).strftime('%Y-%m-%d')
        
        stock_inserts.append(f"""
INSERT INTO stock_info (code, name, industry, current_price, market_cap, listing_date) 
VALUES ('{stock['code']}', '{stock['name']}', '{stock['industry']}', {stock['price']}, {market_cap:.2f}, '{listing_date}');
""")
    
    # 指标数据插入语句
    indicator_inserts = []
    for stock in sample_stocks:
        indicators = generate_indicator_data(stock['code'], stock['industry'])
        for indicator in indicators:
            if indicator['value'] is not None:
                indicator_inserts.append(f"""
INSERT INTO indicator_data (stock_code, indicator_code, value, date) 
VALUES ('{stock['code']}', '{indicator['code']}', {indicator['value']:.2f}, '{today}');
""")
            else:
                indicator_inserts.append(f"""
INSERT INTO indicator_data (stock_code, indicator_code, value_text, date) 
VALUES ('{stock['code']}', '{indicator['code']}', '{indicator['value_text']}', '{today}');
""")
    
    # 生成一些评分结果（模拟）
    score_inserts = []
    for stock in sample_stocks:
        total_score = random.uniform(45, 92)
        industry_score = random.uniform(50, 85)
        competitiveness_score = random.uniform(45, 90)
        growth_score = random.uniform(40, 88)
        timing_score = random.uniform(35, 80)
        
        if total_score >= 80:
            potential_level = 'very_high'
        elif total_score >= 60:
            potential_level = 'high'
        elif total_score >= 40:
            potential_level = 'medium'
        else:
            potential_level = 'low'
        
        score_inserts.append(f"""
INSERT INTO score_result (stock_code, date, total_score, industry_score, competitiveness_score, growth_score, timing_score, potential_level) 
VALUES ('{stock['code']}', '{today}', {total_score:.2f}, {industry_score:.2f}, {competitiveness_score:.2f}, {growth_score:.2f}, {timing_score:.2f}, '{potential_level}');
""")
    
    return stock_inserts, indicator_inserts, score_inserts

if __name__ == "__main__":
    stock_sql, indicator_sql, score_sql = generate_sql_inserts()
    
    print("-- 股票基础信息插入语句")
    for sql in stock_sql:
        print(sql)
    
    print("\n-- 指标数据插入语句")
    for sql in indicator_sql:
        print(sql)
    
    print("\n-- 评分结果插入语句")
    for sql in score_sql:
        print(sql)