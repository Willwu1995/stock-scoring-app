import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class StockScoreCalculator:
    """股票评分计算器"""
    
    def __init__(self):
        self.indicator_weights = {
            'industry': 0.30,
            'competitiveness': 0.40,
            'growth': 0.20,
            'timing': 0.10
        }
        
        self.scoring_rules = {
            'industry_lifecycle': {
                'growth': (18, 20),
                'mature': (12, 17),
                'decline': (0, 11)
            },
            'market_growth_rate': {
                'high': (12, 15),
                'medium': (8, 11),
                'low': (0, 7)
            },
            'revenue_growth': {
                'high': (10, 12),
                'medium': (6, 9),
                'low': (0, 5)
            },
            'roe': {
                'high': (8, 10),
                'medium': (5, 7),
                'low': (0, 4)
            },
            'valuation_level': {
                'low': (12, 15),
                'medium': (8, 11),
                'high': (0, 7)
            }
        }
    
    def calculate_indicator_score(self, indicator_code: str, value: float, value_text: str = None) -> float:
        """计算单个指标得分"""
        try:
            if indicator_code in self.scoring_rules:
                rules = self.scoring_rules[indicator_code]
                
                if value_text:
                    # 分类型指标
                    if value_text in rules:
                        min_score, max_score = rules[value_text]
                        return np.random.uniform(min_score, max_score)
                else:
                    # 数值型指标
                    if indicator_code == 'market_growth_rate':
                        if value > 30:
                            return np.random.uniform(12, 15)
                        elif value > 15:
                            return np.random.uniform(8, 11)
                        else:
                            return np.random.uniform(0, 7)
                    
                    elif indicator_code == 'revenue_growth':
                        if value > 30:
                            return np.random.uniform(10, 12)
                        elif value > 15:
                            return np.random.uniform(6, 9)
                        else:
                            return np.random.uniform(0, 5)
                    
                    elif indicator_code == 'roe':
                        if value > 15:
                            return np.random.uniform(8, 10)
                        elif value > 8:
                            return np.random.uniform(5, 7)
                        else:
                            return np.random.uniform(0, 4)
            
            # 默认评分规则
            return np.random.uniform(5, 8)
            
        except Exception as e:
            logger.error(f"计算指标得分失败 {indicator_code}: {e}")
            return 0
    
    def calculate_dimension_score(self, indicators: List[Dict], dimension: str) -> float:
        """计算维度得分"""
        dimension_indicators = [i for i in indicators if i['dimension'] == dimension]
        
        if not dimension_indicators:
            return 0
        
        total_weighted_score = 0
        total_weight = 0
        
        for indicator in dimension_indicators:
            weight = indicator.get('weight', 1.0)
            score = indicator.get('score', 0)
            total_weighted_score += score * weight
            total_weight += weight
        
        if total_weight == 0:
            return 0
        
        return total_weighted_score / total_weight
    
    def calculate_total_score(self, stock_code: str, indicators: List[Dict]) -> Dict:
        """计算总分和各维度得分"""
        try:
            # 计算各维度得分
            dimension_scores = {}
            for dimension in ['industry', 'competitiveness', 'growth', 'timing']:
                dimension_scores[dimension] = self.calculate_dimension_score(indicators, dimension)
            
            # 计算总分
            total_score = sum(dimension_scores[dim] * self.indicator_weights[dim] 
                            for dim in dimension_scores)
            
            # 确定潜力等级
            if total_score >= 80:
                potential_level = 'very_high'
            elif total_score >= 60:
                potential_level = 'high'
            elif total_score >= 40:
                potential_level = 'medium'
            else:
                potential_level = 'low'
            
            return {
                'stock_code': stock_code,
                'total_score': round(total_score, 2),
                'industry_score': round(dimension_scores['industry'], 2),
                'competitiveness_score': round(dimension_scores['competitiveness'], 2),
                'growth_score': round(dimension_scores['growth'], 2),
                'timing_score': round(dimension_scores['timing'], 2),
                'potential_level': potential_level,
                'score_date': datetime.now().strftime('%Y-%m-%d')
            }
            
        except Exception as e:
            logger.error(f"计算总分失败 {stock_code}: {e}")
            return None
    
    def analyze_strengths_weaknesses(self, indicators: List[Dict]) -> Dict:
        """分析优势和劣势"""
        try:
            sorted_indicators = sorted(indicators, key=lambda x: x.get('score', 0), reverse=True)
            
            strengths = sorted_indicators[:3]
            weaknesses = sorted_indicators[-2:]
            
            return {
                'strengths': strengths,
                'weaknesses': weaknesses
            }
        except Exception as e:
            logger.error(f"分析优劣失败: {e}")
            return {'strengths': [], 'weaknesses': []}
    
    def batch_calculate_scores(self, stock_codes: List[str], indicator_data: Dict) -> List[Dict]:
        """批量计算评分"""
        results = []
        
        for stock_code in stock_codes:
            try:
                stock_indicators = indicator_data.get(stock_code, [])
                if stock_indicators:
                    # 计算每个指标的得分
                    for indicator in stock_indicators:
                        score = self.calculate_indicator_score(
                            indicator['code'],
                            indicator.get('value'),
                            indicator.get('value_text')
                        )
                        indicator['score'] = score
                    
                    # 计算总分
                    score_result = self.calculate_total_score(stock_code, stock_indicators)
                    if score_result:
                        results.append(score_result)
                        
            except Exception as e:
                logger.error(f"批量计算评分失败 {stock_code}: {e}")
                continue
        
        return results