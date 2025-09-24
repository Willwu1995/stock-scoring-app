# Tushare配置文件
# 请将您的Tushare Token填入下方

TUSHARE_TOKEN = "0f23d9afb6524ea0dc1af511b91d1840cb5df1d55d6aea63f3920769"

# Tushare Pro API地址
TUSHARE_API_URL = "http://api.tushare.pro"

# 数据请求配置
REQUEST_TIMEOUT = 30  # 请求超时时间（秒）
MAX_RETRIES = 3      # 最大重试次数
RETRY_DELAY = 1      # 重试延迟（秒）

# 日志配置
LOG_LEVEL = "INFO"   # 日志级别：DEBUG, INFO, WARNING, ERROR

# 数据更新配置
UPDATE_INTERVAL = 86400  # 数据更新间隔（秒），默认24小时
BATCH_SIZE = 100         # 批量处理大小
SAVE_TO_DATABASE = True  # 是否保存到数据库

# 数据源配置
DATA_SOURCES = {
    "stock_basic": True,      # 股票基本信息
    "daily": True,           # 日线行情
    "weekly": False,         # 周线行情
    "monthly": False,        # 月线行情
    "fina_indicator": True,   # 财务指标
    "income": False,         # 利润表
    "balancesheet": False,   # 资产负债表
    "cashflow": False,       # 现金流量表
    "forecast": False,       # 业绩预告
    "express": False,        # 业绩快报
    "dividend": False,       # 分红配送
    "moneyflow": False,      # 资金流向
}

# 评分模型配置
SCORING_WEIGHTS = {
    "industry": 0.30,         # 行业维度权重
    "competitiveness": 0.40,  # 企业竞争力权重
    "growth": 0.20,          # 成长潜力权重
    "timing": 0.10           # 时机维度权重
}

# 行业评分基准
INDUSTRY_BASE_SCORES = {
    "白酒": 85,
    "银行": 75,
    "房地产": 65,
    "电子": 80,
    "汽车": 78,
    "食品饮料": 82,
    "医药生物": 88,
    "安防": 75,
    "新能源汽车": 90,
    "半导体": 85,
    "互联网": 82,
    "新能源": 88,
    "人工智能": 92,
    "医疗器械": 86,
    "消费电子": 79,
    "化工": 70,
    "钢铁": 60,
    "煤炭": 58,
    "电力": 68,
    "交通运输": 72,
    "建筑": 65,
    "机械": 75,
    "农业": 70,
    "纺织服装": 65,
    "轻工制造": 68,
    "商业贸易": 70,
    "休闲服务": 75,
    "计算机": 83,
    "通信": 80,
    "非银金融": 77,
    "综合": 60
}