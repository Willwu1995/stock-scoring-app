from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
import json
from datetime import datetime, timedelta
import random
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="十倍股潜力评分工具API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StockInfo(BaseModel):
    code: str
    name: str
    industry: str
    current_price: Optional[float] = None
    market_cap: Optional[float] = None

class ScoreResult(BaseModel):
    stock_code: str
    stock_name: str
    industry: str
    current_price: Optional[float] = None
    total_score: float
    industry_score: float
    competitiveness_score: float
    growth_score: float
    timing_score: float
    potential_level: str
    score_date: str

class IndicatorDetail(BaseModel):
    code: str
    name: str
    dimension: str
    value: Optional[float] = None
    value_text: Optional[str] = None
    score: float
    max_score: float
    weight: float

# 初始化数据库
def init_database():
    conn = sqlite3.connect('stock_scoring.db', check_same_thread=False)
    cursor = conn.cursor()
    
    # 创建股票信息表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock_info (
            code TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            industry TEXT NOT NULL,
            current_price REAL,
            market_cap REAL
        )
    ''')
    
    # 创建评分结果表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS score_result (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_code TEXT NOT NULL,
            stock_name TEXT NOT NULL,
            industry TEXT NOT NULL,
            current_price REAL,
            total_score REAL NOT NULL,
            industry_score REAL NOT NULL,
            competitiveness_score REAL NOT NULL,
            growth_score REAL NOT NULL,
            timing_score REAL NOT NULL,
            potential_level TEXT NOT NULL,
            score_date TEXT NOT NULL,
            FOREIGN KEY (stock_code) REFERENCES stock_info(code)
        )
    ''')
    
    # 创建评分明细表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS score_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_code TEXT NOT NULL,
            code TEXT NOT NULL,
            name TEXT NOT NULL,
            dimension TEXT NOT NULL,
            value REAL,
            value_text TEXT,
            score REAL NOT NULL,
            max_score REAL NOT NULL,
            weight REAL NOT NULL,
            FOREIGN KEY (stock_code) REFERENCES stock_info(code)
        )
    ''')
    
    conn.commit()
    conn.close()

# 生成示例数据
def generate_sample_data():
    stocks = [
        ("000001", "平安银行", "银行业", 12.50, 2400.0),
        ("000002", "万科A", "房地产", 18.30, 2100.0),
        ("000858", "五粮液", "白酒", 165.80, 6400.0),
        ("002415", "海康威视", "安防设备", 35.60, 3300.0),
        ("002594", "比亚迪", "新能源汽车", 268.50, 7800.0),
        ("600036", "招商银行", "银行业", 42.30, 10900.0),
        ("600519", "贵州茅台", "白酒", 1680.0, 21200.0),
        ("600887", "伊利股份", "食品饮料", 32.80, 2100.0),
        ("000725", "京东方A", "电子元件", 3.85, 1500.0),
        ("300015", "爱尔眼科", "医疗服务", 18.90, 820.0)
    ]
    
    indicators = [
        ("IND001", "行业生命周期阶段", "industry", None, "成长期", 85.0, 100, 0.15),
        ("IND002", "行业市场规模增速", "industry", 15.2, None, 78.0, 100, 0.10),
        ("IND003", "行业集中度", "industry", None, "高集中度", 72.0, 100, 0.05),
        ("IND004", "市场份额", "competitiveness", 12.5, None, 88.0, 100, 0.15),
        ("IND005", "营收增速", "competitiveness", 18.6, None, 92.0, 100, 0.10),
        ("IND006", "净利润率", "competitiveness", 15.8, None, 85.0, 100, 0.08),
        ("IND007", "净资产收益率", "competitiveness", 22.3, None, 90.0, 100, 0.07),
        ("IND008", "未来3年预期增速", "growth", 25.4, None, 82.0, 100, 0.12),
        ("IND009", "研发投入强度", "growth", 8.5, None, 75.0, 100, 0.05),
        ("IND010", "估值水平", "timing", None, "合理", 68.0, 100, 0.06),
        ("IND011", "市场情绪", "timing", None, "乐观", 72.0, 100, 0.04),
        ("IND012", "技术趋势", "timing", None, "上升", 76.0, 100, 0.03)
    ]
    
    conn = sqlite3.connect('stock_scoring.db', check_same_thread=False)
    cursor = conn.cursor()
    
    # 检查是否已有数据
    cursor.execute("SELECT COUNT(*) FROM stock_info")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return
    
    # 插入股票信息
    cursor.executemany('''
        INSERT OR REPLACE INTO stock_info (code, name, industry, current_price, market_cap)
        VALUES (?, ?, ?, ?, ?)
    ''', stocks)
    
    # 生成评分结果和明细
    for stock in stocks:
        code, name, industry, price, market_cap = stock
        
        # 生成随机但合理的评分
        industry_score = random.uniform(60, 95)
        competitiveness_score = random.uniform(65, 98)
        growth_score = random.uniform(55, 92)
        timing_score = random.uniform(50, 85)
        
        total_score = (
            industry_score * 0.3 + 
            competitiveness_score * 0.4 + 
            growth_score * 0.2 + 
            timing_score * 0.1
        )
        
        if total_score >= 80:
            potential_level = "very_high"
        elif total_score >= 60:
            potential_level = "high"
        elif total_score >= 40:
            potential_level = "medium"
        else:
            potential_level = "low"
        
        # 插入评分结果
        cursor.execute('''
            INSERT OR REPLACE INTO score_result 
            (stock_code, stock_name, industry, current_price, total_score, 
             industry_score, competitiveness_score, growth_score, timing_score, 
             potential_level, score_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (code, name, industry, price, total_score, 
              industry_score, competitiveness_score, growth_score, timing_score,
              potential_level, datetime.now().strftime("%Y-%m-%d")))
        
        # 插入评分明细
        for indicator in indicators:
            ind_code, ind_name, dimension, value, value_text, base_score, max_score, weight = indicator
            
            # 为每个股票生成略有差异的分数
            score_variation = random.uniform(-10, 10)
            final_score = max(0, min(100, base_score + score_variation))
            
            cursor.execute('''
                INSERT OR REPLACE INTO score_details
                (stock_code, code, name, dimension, value, value_text, score, max_score, weight)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (code, ind_code, ind_name, dimension, value, value_text, final_score, max_score, weight))
    
    conn.commit()
    conn.close()

# 启动时初始化数据库
init_database()
generate_sample_data()

# API端点
@app.get("/")
async def root():
    return {"message": "十倍股潜力评分API v1.0"}

@app.get("/api/stocks/search", response_model=List[StockInfo])
async def search_stocks(q: str = Query(..., description="搜索关键词")):
    """搜索股票"""
    try:
        conn = sqlite3.connect('stock_scoring.db', check_same_thread=False)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT code, name, industry, current_price, market_cap 
            FROM stock_info 
            WHERE name LIKE ? OR code LIKE ?
            LIMIT 10
        ''', (f"%{q}%", f"%{q}%"))
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            StockInfo(
                code=row[0],
                name=row[1],
                industry=row[2],
                current_price=row[3],
                market_cap=row[4]
            )
            for row in results
        ]
    except Exception as e:
        logger.error(f"搜索股票失败: {e}")
        raise HTTPException(status_code=500, detail="搜索股票失败")

@app.get("/api/scores/{stock_code}", response_model=ScoreResult)
async def get_score_result(stock_code: str):
    """获取股票评分结果"""
    try:
        conn = sqlite3.connect('stock_scoring.db', check_same_thread=False)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT stock_code, stock_name, industry, current_price, total_score,
                   industry_score, competitiveness_score, growth_score, timing_score,
                   potential_level, score_date
            FROM score_result 
            WHERE stock_code = ?
            ORDER BY score_date DESC
            LIMIT 1
        ''', (stock_code,))
        
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            raise HTTPException(status_code=404, detail="股票评分结果未找到")
        
        return ScoreResult(
            stock_code=result[0],
            stock_name=result[1],
            industry=result[2],
            current_price=result[3],
            total_score=result[4],
            industry_score=result[5],
            competitiveness_score=result[6],
            growth_score=result[7],
            timing_score=result[8],
            potential_level=result[9],
            score_date=result[10]
        )
    except Exception as e:
        logger.error(f"获取股票评分失败: {e}")
        raise HTTPException(status_code=500, detail="获取股票评分失败")

@app.get("/api/scores/{stock_code}/details", response_model=List[IndicatorDetail])
async def get_score_details(stock_code: str):
    """获取股票评分明细"""
    try:
        conn = sqlite3.connect('stock_scoring.db', check_same_thread=False)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT code, name, dimension, value, value_text, score, max_score, weight
            FROM score_details 
            WHERE stock_code = ?
            ORDER BY dimension, code
        ''', (stock_code,))
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            IndicatorDetail(
                code=row[0],
                name=row[1],
                dimension=row[2],
                value=row[3],
                value_text=row[4],
                score=row[5],
                max_score=row[6],
                weight=row[7]
            )
            for row in results
        ]
    except Exception as e:
        logger.error(f"获取评分明细失败: {e}")
        raise HTTPException(status_code=500, detail="获取评分明细失败")

@app.get("/api/stocks/high-potential")
async def get_high_potential_stocks(
    min_score: float = Query(80, description="最低分数"),
    limit: int = Query(20, description="返回数量限制")
):
    """获取高潜力股票列表"""
    try:
        conn = sqlite3.connect('stock_scoring.db', check_same_thread=False)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT sr.stock_code, sr.stock_name, sr.industry, sr.current_price, 
                   sr.total_score, sr.potential_level, sr.score_date
            FROM score_result sr
            WHERE sr.total_score >= ? AND sr.score_date = (
                SELECT MAX(score_date) FROM score_result WHERE stock_code = sr.stock_code
            )
            ORDER BY sr.total_score DESC
            LIMIT ?
        ''', (min_score, limit))
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                "stock_code": row[0],
                "stock_name": row[1], 
                "industry": row[2],
                "current_price": row[3],
                "total_score": row[4],
                "potential_level": row[5],
                "score_date": row[6]
            }
            for row in results
        ]
    except Exception as e:
        logger.error(f"获取高潜力股票失败: {e}")
        raise HTTPException(status_code=500, detail="获取高潜力股票失败")

@app.get("/api/indicators/explanations")
async def get_indicator_explanations():
    """获取指标说明"""
    explanations = {
        "行业维度": {
            "description": "评估股票所属行业的发展前景和竞争环境",
            "indicators": [
                {
                    "code": "IND001",
                    "name": "行业生命周期阶段",
                    "description": "评估行业所处的发展阶段，包括初创期、成长期、成熟期、衰退期",
                    "scoring": "成长期得分最高，衰退期得分最低"
                },
                {
                    "code": "IND002", 
                    "name": "行业市场规模增速",
                    "description": "评估行业整体市场的增长速度",
                    "scoring": "增速越高得分越高，低于5%开始扣分"
                }
            ]
        },
        "企业竞争力": {
            "description": "评估企业在行业中的竞争地位和盈利能力",
            "indicators": [
                {
                    "code": "IND004",
                    "name": "市场份额", 
                    "description": "企业在行业中的市场占有率",
                    "scoring": "市场份额越高得分越高，龙头公司优势明显"
                }
            ]
        }
    }
    return explanations

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)