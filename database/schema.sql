-- 十倍股潜力评分工具数据库表结构
-- MySQL/PostgreSQL compatible

-- 股票基础信息表
CREATE TABLE stock_info (
    code VARCHAR(6) PRIMARY KEY COMMENT '股票代码(6位数字)',
    name VARCHAR(50) NOT NULL COMMENT '股票名称',
    industry VARCHAR(100) NOT NULL COMMENT '所属行业',
    current_price DECIMAL(10,2) COMMENT '当前股价',
    market_cap DECIMAL(15,2) COMMENT '市值(亿元)',
    listing_date DATE COMMENT '上市日期',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_industry (industry),
    INDEX idx_name (name)
);

-- 指标定义表
CREATE TABLE indicator_definitions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    code VARCHAR(20) UNIQUE NOT NULL COMMENT '指标代码',
    name VARCHAR(100) NOT NULL COMMENT '指标名称',
    dimension VARCHAR(20) NOT NULL COMMENT '所属维度(industry,competitiveness,growth,timing)',
    weight DECIMAL(5,2) NOT NULL COMMENT '权重(0-1)',
    max_score DECIMAL(5,2) NOT NULL COMMENT '满分',
    description TEXT COMMENT '指标说明',
    calculation_rule TEXT COMMENT '计算规则',
    scoring_criteria TEXT COMMENT '评分标准'
);

-- 指标数据表
CREATE TABLE indicator_data (
    id INT PRIMARY KEY AUTO_INCREMENT,
    stock_code VARCHAR(6) NOT NULL COMMENT '股票代码',
    indicator_code VARCHAR(20) NOT NULL COMMENT '指标代码',
    value DECIMAL(15,4) COMMENT '指标值',
    value_text VARCHAR(255) COMMENT '文本值(对于分类型指标)',
    date DATE NOT NULL COMMENT '数据日期',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (stock_code) REFERENCES stock_info(code),
    FOREIGN KEY (indicator_code) REFERENCES indicator_definitions(code),
    UNIQUE KEY uk_stock_indicator_date (stock_code, indicator_code, date),
    INDEX idx_stock_date (stock_code, date),
    INDEX idx_indicator_date (indicator_code, date)
);

-- 评分结果表
CREATE TABLE score_result (
    id INT PRIMARY KEY AUTO_INCREMENT,
    stock_code VARCHAR(6) NOT NULL COMMENT '股票代码',
    date DATE NOT NULL COMMENT '评分日期',
    total_score DECIMAL(5,2) NOT NULL COMMENT '总分(0-100)',
    industry_score DECIMAL(5,2) NOT NULL COMMENT '行业维度得分',
    competitiveness_score DECIMAL(5,2) NOT NULL COMMENT '竞争力维度得分',
    growth_score DECIMAL(5,2) NOT NULL COMMENT '成长潜力维度得分',
    timing_score DECIMAL(5,2) NOT NULL COMMENT '时机维度得分',
    potential_level VARCHAR(20) NOT NULL COMMENT '潜力等级(very_high,high,medium,low)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (stock_code) REFERENCES stock_info(code),
    UNIQUE KEY uk_stock_date (stock_code, date),
    INDEX idx_total_score (total_score),
    INDEX idx_potential_level (potential_level),
    INDEX idx_date (date)
);

-- 评分明细表
CREATE TABLE score_details (
    id INT PRIMARY KEY AUTO_INCREMENT,
    score_result_id INT NOT NULL COMMENT '评分结果ID',
    indicator_code VARCHAR(20) NOT NULL COMMENT '指标代码',
    indicator_value DECIMAL(15,4) COMMENT '指标值',
    score DECIMAL(5,2) NOT NULL COMMENT '得分',
    FOREIGN KEY (score_result_id) REFERENCES score_result(id),
    FOREIGN KEY (indicator_code) REFERENCES indicator_definitions(code),
    INDEX idx_result_id (score_result_id)
);

-- 插入指标定义数据
INSERT INTO indicator_definitions (code, name, dimension, weight, max_score, description, calculation_rule, scoring_criteria) VALUES
-- 行业维度指标 (权重30%)
('industry_lifecycle', '行业生命周期阶段', 'industry', 0.30, 20, '评估行业所处的发展阶段', '根据行业增速、渗透率等综合判断', '成长期:18-20分,成熟期:12-17分,衰退期:0-11分'),
('market_growth_rate', '市场规模增速', 'industry', 0.25, 15, '行业整体市场规模的年化增长率', '(当年市场规模-上年市场规模)/上年市场规模*100%', '>30%:12-15分,15-30%:8-11分,<15%:0-7分'),
('industry_concentration', '行业集中度', 'industry', 0.20, 10, '行业内头部企业的市场份额占比', 'CR4/CR8指标', '高集中度:8-10分,中等集中度:5-7分,低集中度:0-4分'),
('policy_support', '政策支持度', 'industry', 0.15, 8, '国家政策对行业的支持程度', '根据政策文件、规划等评估', '强支持:6-8分,一般支持:3-5分,无支持:0-2分'),
('barrier_to_entry', '行业进入壁垒', 'industry', 0.10, 7, '新企业进入行业的难度', '技术、资金、牌照等壁垒评估', '高壁垒:5-7分,中等壁垒:3-4分,低壁垒:0-2分'),

-- 企业竞争力维度指标 (权重40%)
('market_share', '市场份额', 'competitiveness', 0.20, 15, '企业在行业内的市场占有率', '企业营收/行业总规模*100%', '>20%:12-15分,10-20%:8-11分,<10%:0-7分'),
('revenue_growth', '营收增速', 'competitiveness', 0.15, 12, '企业营业收入的年化增长率', '(当年营收-上年营收)/上年营收*100%', '>30%:10-12分,15-30%:6-9分,<15%:0-5分'),
('profit_margin', '利润率水平', 'competitiveness', 0.15, 10, '企业净利润率水平', '净利润/营业收入*100%', '>20%:8-10分,10-20%:5-7分,<10%:0-4分'),
('roe', '净资产收益率', 'competitiveness', 0.15, 10, '股东权益回报率', '净利润/净资产*100%', '>15%:8-10分,8-15%:5-7分,<8%:0-4分'),
('r_d_intensity', '研发投入强度', 'competitiveness', 0.10, 8, '研发费用占营收比例', '研发费用/营业收入*100%', '>10%:6-8分,5-10%:3-5分,<5%:0-2分'),
('brand_value', '品牌价值', 'competitiveness', 0.10, 8, '企业品牌影响力', '根据品牌知名度、美誉度等评估', '强品牌:6-8分,中等品牌:3-5分,弱品牌:0-2分'),
('management_team', '管理团队', 'competitiveness', 0.15, 12, '管理团队质量评估', '根据团队背景、历史业绩等评估', '优秀:10-12分,良好:6-9分,一般:0-5分'),

-- 成长潜力维度指标 (权重20%)
('future_growth', '未来3年预期增速', 'growth', 0.30, 15, '分析师对未来3年营收增速的预期', '取分析师一致预期均值', '>25%:12-15分,15-25%:8-11分,<15%:0-7分'),
('new_business', '新业务增长', 'growth', 0.25, 12, '新兴业务或产品的增长潜力', '根据新业务占比、增速等评估', '高潜力:10-12分,中等潜力:6-9分,低潜力:0-5分'),
('market_expansion', '市场扩张能力', 'growth', 0.20, 10, '企业扩张市场的能力', '根据历史扩张记录、渠道建设等评估', '强扩张:8-10分,中等扩张:5-7分,弱扩张:0-4分'),
('innovation_capability', '创新能力', 'growth', 0.25, 13, '企业技术创新和产品创新能力', '专利数量、新产品上市频率等', '强创新:10-13分,中等创新:6-9分,弱创新:0-5分'),

-- 时机维度指标 (权重10%)
('valuation_level', '估值水平', 'timing', 0.40, 15, '当前估值相对历史水平', 'PE/PB百分位法', '低估:12-15分,合理:8-11分,高估:0-7分'),
('market_sentiment', '市场情绪', 'timing', 0.30, 10, '市场对该股票的整体情绪', '根据资金流向、关注度等评估', '积极:8-10分,中性:5-7分,消极:0-4分'),
('technical_trend', '技术趋势', 'timing', 0.30, 10, '股价技术走势', '根据均线、MACD等技术指标评估', '上升趋势:8-10分,震荡趋势:5-7分,下降趋势:0-4分')
;