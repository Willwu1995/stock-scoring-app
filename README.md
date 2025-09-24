# 十倍股潜力评分工具 v1.0

## 项目简介

这是一个基于量化评分模型的A股上市公司"十倍股潜力"评分工具，通过四大维度（行业、企业竞争力、成长潜力、时机）对股票进行综合评分，帮助投资者快速筛选高潜力标的。

## 技术架构

### 后端技术栈
- **框架**: FastAPI 0.104.1
- **数据库**: MySQL/PostgreSQL
- **ORM**: SQLAlchemy 2.0.23
- **数据处理**: Pandas 2.1.4, NumPy 1.25.2

### 前端技术栈
- **框架**: React 18 + TypeScript
- **UI组件库**: Ant Design
- **图表库**: ECharts + echarts-for-react
- **HTTP客户端**: Axios

### 数据存储
- **关系型数据库**: MySQL/PostgreSQL
- **核心表结构**: 
  - `stock_info` - 股票基础信息
  - `indicator_definitions` - 指标定义
  - `indicator_data` - 指标数据
  - `score_result` - 评分结果
  - `score_details` - 评分明细

## 项目结构

```
十倍股手册/
├── backend/                 # 后端服务
│   ├── main.py             # FastAPI主程序
│   ├── score_calculator.py # 评分算法
│   ├── requirements.txt    # Python依赖
│   └── .env               # 环境变量配置
├── frontend/
│   └── stock-scoring-app/  # React应用
│       ├── src/
│       │   ├── App.tsx     # 主应用组件
│       │   └── components/ # 组件库
│       └── package.json    # Node.js依赖
├── database/
│   ├── schema.sql          # 数据库表结构
│   └── generate_sample_data.py # 样本数据生成器
└── docs/                   # 文档目录
```

## 快速开始

### 环境要求
- Python 3.8+
- Node.js 16+
- MySQL 8.0+ / PostgreSQL 12+

### 1. 数据库设置

```bash
# 创建数据库
mysql -u root -p
CREATE DATABASE stock_scoring CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 导入表结构
cd database
mysql -u root -p stock_scoring < schema.sql

# 生成样本数据（可选）
python generate_sample_data.py > sample_data.sql
mysql -u root -p stock_scoring < sample_data.sql
```

### 2. 后端服务启动

```bash
cd backend
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，设置数据库连接信息

# 启动服务
python main.py
# 或使用 uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. 前端应用启动

```bash
cd frontend/stock-scoring-app
npm install

# 启动开发服务器
npm start

# 构建生产版本
npm run build
```

## API接口文档

后端服务启动后，可通过以下地址访问：

- **API文档**: http://localhost:8000/docs
- **交互式API**: http://localhost:8000/redoc

### 主要接口

1. **股票搜索**
   ```
   GET /api/stocks/search?q={关键词}
   ```

2. **获取评分结果**
   ```
   GET /api/scores/{股票代码}
   ```

3. **获取评分明细**
   ```
   GET /api/scores/{股票代码}/details
   ```

4. **获取高潜力股票列表**
   ```
   GET /api/stocks/high-potential?min_score=80&limit=20
   ```

5. **获取指标说明**
   ```
   GET /api/indicators/explanations
   ```

## 核心功能

### 1. 股票搜索与评分查询
- 支持股票代码（6位数字）和名称模糊搜索
- 实时显示匹配结果（最多10个候选）
- 点击股票卡片获取详细评分

### 2. 评分结果展示
- **总分展示**: 0-100分制，四级潜力等级标签
- **雷达图**: 四大维度得分可视化
- **明细表格**: 各细分指标得分、权重、满分
- **优劣分析**: 自动提取3个优势点和2个风险点

### 3. 高潜力股票列表
- 展示评分≥80分的股票
- 支持按总分排序
- 点击可跳转至详情页

### 4. 指标说明系统
- 每个指标都有详细说明
- 包含定义、计算方式、评分标准
- 通过"?"图标快速查看

## 评分模型

### 四大维度权重分配
- **行业维度**: 30%
  - 行业生命周期阶段
  - 市场规模增速
  - 行业集中度
  - 政策支持度
  - 行业进入壁垒

- **企业竞争力维度**: 40%
  - 市场份额
  - 营收增速
  - 利润率水平
  - 净资产收益率
  - 研发投入强度
  - 品牌价值
  - 管理团队

- **成长潜力维度**: 20%
  - 未来3年预期增速
  - 新业务增长
  - 市场扩张能力
  - 创新能力

- **时机维度**: 10%
  - 估值水平
  - 市场情绪
  - 技术趋势

### 潜力等级划分
- **80-100分**: 极高潜力
- **60-79分**: 高潜力
- **40-59分**: 一般潜力
- **<40分**: 低潜力

## 部署说明

### Docker部署（推荐）

1. **构建镜像**
```bash
# 后端
cd backend
docker build -t stock-scoring-backend .

# 前端
cd frontend/stock-scoring-app
docker build -t stock-scoring-frontend .
```

2. **使用Docker Compose**
```yaml
version: '3.8'
services:
  backend:
    image: stock-scoring-backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=mysql+pymysql://root:password@db:3306/stock_scoring
    depends_on:
      - db

  frontend:
    image: stock-scoring-frontend
    ports:
      - "3000:80"
    depends_on:
      - backend

  db:
    image: mysql:8.0
    environment:
      - MYSQL_ROOT_PASSWORD=password
      - MYSQL_DATABASE=stock_scoring
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:
```

### 生产环境部署

1. **Nginx配置**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端静态文件
    location / {
        root /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;
    }

    # API代理
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

2. **后端服务配置**
```bash
# 使用gunicorn启动
cd backend
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 数据更新策略

### 数据来源
- **财务数据**: 季度更新（财报发布后3日内）
- **行情数据**: 每日收盘后更新
- **行业数据**: 月度更新
- **评分结果**: 每日凌晨批量计算

### 自动化脚本
```bash
# 添加到crontab
0 2 * * * /usr/bin/python3 /path/to/backend/update_scores.py
0 16 * * 1-5 /usr/bin/python3 /path/to/backend/update_market_data.py
```

## 性能优化

### 数据库优化
- 为常用查询字段添加索引
- 使用连接池提高并发性能
- 定期清理历史数据

### 缓存策略
- Redis缓存热门股票的评分结果
- 前端静态资源CDN加速
- API响应缓存（5分钟）

### 前端优化
- 代码分割和懒加载
- 图片压缩和格式优化
- 服务端渲染（SSR）可选

## 监控与日志

### 日志配置
```python
# logging.conf
[loggers]
keys=root,app

[handlers]
keys=consoleHandler,fileHandler

[formatters]
keys=simpleFormatter

[logger_root]
level=INFO
handlers=consoleHandler

[logger_app]
level=DEBUG
handlers=consoleHandler,fileHandler
qualname=app
propagate=0

[handler_consoleHandler]
class=StreamHandler
level=INFO
formatter=simpleFormatter
args=(sys.stdout,)

[handler_fileHandler]
class=FileHandler
level=DEBUG
formatter=simpleFormatter
args=('app.log',)
```

### 监控指标
- API响应时间
- 数据库查询性能
- 错误率统计
- 用户访问量

## 扩展功能

### v1.1 规划
- [ ] 用户注册登录系统
- [ ] 个人投资组合管理
- [ ] 评分历史趋势分析
- [ ] 自定义评分模型
- [ ] 移动端适配

### v1.2 规划
- [ ] 实时行情数据接入
- [ ] 更多数据源集成
- [ ] 智能推荐算法
- [ ] 社区分享功能
- [ ] 专业版订阅服务

## 常见问题

### Q: 如何添加新的股票？
A: 在`stock_info`表中插入新的股票记录，然后通过`generate_sample_data.py`生成相应的指标数据。

### Q: 如何修改评分权重？
A: 在`score_calculator.py`中修改`indicator_weights`字典，或在数据库中更新`indicator_definitions`表的weight字段。

### Q: 数据从哪里获取？
A: MVP版本使用模拟数据，生产环境可接入Tushare、Wind等金融数据服务。

### Q: 如何自定义评分规则？
A: 在`score_calculator.py`中的`scoring_rules`字典中添加或修改评分规则。

## 贡献指南

1. Fork本项目
2. 创建功能分支
3. 提交代码
4. 发起Pull Request

## 许可证

MIT License

## 联系方式

如有问题或建议，请通过以下方式联系：
- Email: your-email@example.com
- GitHub Issues: [项目Issues页面]

---

**注意**: 本工具仅供投资参考，不构成投资建议。投资有风险，决策需谨慎。