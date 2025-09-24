#!/bin/bash

echo "🚀 启动十倍股潜力评分工具"
echo "================================"

# 检查Python3
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装，请先安装Python3"
    exit 1
fi

# 检查Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js 未安装，请先安装Node.js"
    exit 1
fi

# 检查并安装Python依赖
echo "📦 检查Python依赖..."
pip3 install fastapi uvicorn &> /dev/null

# 检查后端是否运行
if lsof -i :8000 &> /dev/null; then
    echo "✅ 后端服务已在运行 (端口8000)"
else
    echo "🔧 启动后端服务..."
    cd backend
    python3 main.py &
    cd ..
    sleep 3
    if lsof -i :8000 &> /dev/null; then
        echo "✅ 后端服务启动成功"
    else
        echo "❌ 后端服务启动失败"
        exit 1
    fi
fi

# 检查前端是否运行
if lsof -i :3000 &> /dev/null; then
    echo "✅ 前端服务已在运行 (端口3000)"
else
    echo "🔧 启动前端服务..."
    cd frontend/stock-scoring-app
    npm start &
    cd ../..
    sleep 5
    if lsof -i :3000 &> /dev/null; then
        echo "✅ 前端服务启动成功"
    else
        echo "❌ 前端服务启动失败"
        exit 1
    fi
fi

echo ""
echo "🎉 系统启动完成！"
echo "================================"
echo "📱 前端应用: http://localhost:3000"
echo "🔗 后端API: http://localhost:8000"
echo "📖 API文档: http://localhost:8000/docs"
echo "🧪 测试页面: file://$(pwd)/test.html"
echo ""
echo "按 Ctrl+C 停止服务"

# 等待用户中断
wait