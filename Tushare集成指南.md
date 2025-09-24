# Tushare Pro集成指南

## 🚀 Tushare配置完成

我已经为您完成了Tushare的初始化配置，包括：

### ✅ 已完成的工作

1. **配置文件创建** - `tushare_config.py`
   - API地址配置
   - 请求参数设置
   - 行业评分基准
   - 评分模型权重

2. **API客户端** - `tushare_client.py`
   - 完整的Tushare Pro API封装
   - 自动重试机制
   - 模拟数据支持
   - 错误处理和日志

3. **Token管理工具** - `setup_token.py`
   - 便捷的Token设置
   - 配置验证功能
   - 连接测试工具

4. **配置测试工具** - `test_config.py`
   - 配置文件检查
   - 状态显示
   - 使用说明

## 🔧 如何设置您的Token

### 方法一：使用配置工具（推荐）
```bash
cd "/Users/will/Desktop/十倍股手册/backend"
python3 setup_token.py set 您的Token字符串
```

### 方法二：手动编辑
1. 打开 `backend/tushare_config.py`
2. 找到这行：`TUSHARE_TOKEN = "请在此处填入您的Tushare Pro Token"`
3. 替换为您的Token：`TUSHARE_TOKEN = "您的实际Token"`

### 方法三：通过API设置
您可以直接告诉我您的Token，我会帮您设置。

## 📋 Token获取步骤

1. **注册账号**
   - 访问：https://tushare.pro
   - 点击"注册"创建账号

2. **获取Token**
   - 登录账号
   - 进入"个人中心"
   - 复制API Token

3. **积分要求**
   - 免费版：100积分/天
   - 基础数据接口可用
   - 建议控制调用频率

## 🧪 测试配置

### 检查当前状态
```bash
python3 test_config.py
```

### 测试连接
```bash
python3 setup_token.py test
```

### 查看配置
```bash
python3 setup_token.py show
```

## 📊 支持的数据接口

### 基础数据
- ✅ 股票基本信息 (`stock_basic`)
- ✅ 日线行情 (`daily`)
- ✅ 财务指标 (`fina_indicator`)
- ✅ 资金流向 (`moneyflow`)

### 扩展数据
- 🔄 周线行情 (`weekly`)
- 🔄 月线行情 (`monthly`)
- 🔄 利润表 (`income`)
- 🔄 资产负债表 (`balancesheet`)
- 🔄 现金流量表 (`cashflow`)
- 🔄 业绩预告 (`forecast`)
- 🔄 分红配送 (`dividend`)

## 🎯 评分模型特色

### 四大维度评分
1. **行业维度 (30%)**
   - 行业生命周期阶段
   - 市场规模增速
   - 行业集中度

2. **企业竞争力 (40%)**
   - 市场份额
   - 营收增速
   - 净利润率
   - 净资产收益率

3. **成长潜力 (20%)**
   - 未来3年预期增速
   - 研发投入强度

4. **时机维度 (10%)**
   - 估值水平
   - 市场情绪

### 智能评分算法
- 基于真实财务数据
- 行业对比分析
- 动态权重调整
- 风险评估

## 🔧 API使用示例

### 更新数据
```python
from tushare_client import StockDataUpdater

updater = StockDataUpdater()
success = updater.update_all_data()
```

### 获取股票列表
```python
from tushare_client import TushareProAPI

api = TushareProAPI()
df = api.get_stock_basic()
```

### 获取价格数据
```python
df = api.get_daily_data(ts_code='000001.SZ')
```

## 📡 集成到现有系统

### 后端API接口
系统已经集成了以下API端点：

- `POST /api/data/update` - 更新股票数据
- `GET /api/data/status` - 获取数据状态
- `GET /api/stocks/search` - 搜索股票
- `GET /api/scores/{code}` - 获取评分

### 前端集成
前端应用已经配置好，可以直接使用：
- 搜索功能支持真实数据
- 评分结果基于真实指标
- 图表展示实时更新

## 🚨 注意事项

### Token安全
- 不要将Token提交到代码仓库
- 定期更换Token
- 监控使用情况

### 调用限制
- 免费版有次数限制
- 建议控制请求频率
- 错峰获取数据

### 数据更新
- 建议每日收盘后更新
- 避免交易时间频繁调用
- 本地缓存减少API调用

## 🛠️ 故障排除

### 常见问题
1. **Token无效**
   - 检查Token是否正确
   - 确认账号是否有效
   - 查看积分是否充足

2. **网络问题**
   - 检查网络连接
   - 尝试使用代理
   - 增加重试次数

3. **数据为空**
   - 检查股票代码格式
   - 确认交易日期
   - 查看API文档

### 日志查看
系统会记录详细的操作日志：
- API调用记录
- 错误信息
- 数据更新状态

## 📞 获取帮助

### 官方资源
- Tushare官网：https://tushare.pro
- API文档：https://tushare.pro/document/2
- 社区论坛：https://tushare.pro/forum

### 技术支持
- 查看错误日志
- 检查配置文件
- 测试网络连接

---

**现在请提供您的Tushare Token，我将帮您完成最终配置！**