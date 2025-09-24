#!/bin/bash

# 十倍股潜力评分工具快速部署脚本
# 使用方法: bash deploy.sh [dev|prod]

set -e

ENV=${1:-dev}
PROJECT_ROOT=$(pwd)

echo "🚀 开始部署十倍股潜力评分工具 v1.0"
echo "环境: $ENV"
echo "项目根目录: $PROJECT_ROOT"

# 检查依赖
check_dependencies() {
    echo "📋 检查系统依赖..."
    
    # 检查Python
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python3 未安装"
        exit 1
    fi
    
    # 检查Node.js
    if ! command -v node &> /dev/null; then
        echo "❌ Node.js 未安装"
        exit 1
    fi
    
    # 检查MySQL
    if ! command -v mysql &> /dev/null; then
        echo "❌ MySQL 未安装"
        exit 1
    fi
    
    echo "✅ 系统依赖检查通过"
}

# 创建数据库
setup_database() {
    echo "🗄️  设置数据库..."
    
    # 询问数据库配置
    read -p "请输入MySQL用户名 (默认: root): " DB_USER
    DB_USER=${DB_USER:-root}
    
    read -s -p "请输入MySQL密码: " DB_PASSWORD
    echo
    
    read -p "请输入数据库名 (默认: stock_scoring): " DB_NAME
    DB_NAME=${DB_NAME:-stock_scoring}
    
    # 创建数据库
    mysql -u $DB_USER -p$DB_PASSWORD -e "CREATE DATABASE IF NOT EXISTS $DB_NAME CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
    
    # 导入表结构
    mysql -u $DB_USER -p$DB_PASSWORD $DB_NAME < database/schema.sql
    
    # 生成并导入样本数据
    if [ "$ENV" = "dev" ]; then
        echo "📊 生成样本数据..."
        python3 database/generate_sample_data.py | mysql -u $DB_USER -p$DB_PASSWORD $DB_NAME
    fi
    
    # 更新后端配置
    sed "s/DATABASE_URL=mysql+pymysql:\/\/root:password@localhost\/stock_scoring/DATABASE_URL=mysql+pymysql:\/\/$DB_USER:$DB_PASSWORD@localhost\/$DB_NAME/" backend/.env.example > backend/.env
    
    echo "✅ 数据库设置完成"
}

# 安装后端依赖
setup_backend() {
    echo "🔧 设置后端..."
    
    cd backend
    
    # 创建虚拟环境
    if [ ! -d "venv" ]; then
        python3 -m venv venv
    fi
    
    # 激活虚拟环境并安装依赖
    source venv/bin/activate
    pip install -r requirements.txt
    
    cd ..
    echo "✅ 后端设置完成"
}

# 安装前端依赖
setup_frontend() {
    echo "🎨 设置前端..."
    
    cd frontend/stock-scoring-app
    
    # 安装依赖
    npm install
    
    # 构建生产版本
    if [ "$ENV" = "prod" ]; then
        npm run build
    fi
    
    cd ../..
    echo "✅ 前端设置完成"
}

# 启动服务
start_services() {
    echo "🚀 启动服务..."
    
    # 启动后端服务
    cd backend
    source venv/bin/activate
    nohup python main.py > ../backend.log 2>&1 &
    BACKEND_PID=$!
    echo "后端服务PID: $BACKEND_PID"
    cd ..
    
    # 启动前端服务
    if [ "$ENV" = "dev" ]; then
        cd frontend/stock-scoring-app
        nohup npm start > ../../frontend.log 2>&1 &
        FRONTEND_PID=$!
        echo "前端服务PID: $FRONTEND_PID"
        cd ../..
    fi
    
    echo "✅ 服务启动完成"
    echo "后端地址: http://localhost:8000"
    echo "前端地址: http://localhost:3000"
    echo "API文档: http://localhost:8000/docs"
    
    # 保存PID文件
    echo $BACKEND_PID > backend.pid
    if [ "$ENV" = "dev" ]; then
        echo $FRONTEND_PID > frontend.pid
    fi
}

# 停止服务
stop_services() {
    echo "🛑 停止服务..."
    
    if [ -f "backend.pid" ]; then
        kill $(cat backend.pid)
        rm backend.pid
    fi
    
    if [ -f "frontend.pid" ]; then
        kill $(cat frontend.pid)
        rm frontend.pid
    fi
    
    echo "✅ 服务已停止"
}

# 显示状态
show_status() {
    echo "📊 服务状态..."
    
    if [ -f "backend.pid" ]; then
        if ps -p $(cat backend.pid) > /dev/null; then
            echo "✅ 后端服务运行中 (PID: $(cat backend.pid))"
        else
            echo "❌ 后端服务已停止"
        fi
    else
        echo "❌ 后端服务未启动"
    fi
    
    if [ -f "frontend.pid" ]; then
        if ps -p $(cat frontend.pid) > /dev/null; then
            echo "✅ 前端服务运行中 (PID: $(cat frontend.pid))"
        else
            echo "❌ 前端服务已停止"
        fi
    else
        echo "❌ 前端服务未启动"
    fi
}

# 主函数
main() {
    case $1 in
        "setup")
            check_dependencies
            setup_database
            setup_backend
            setup_frontend
            echo "🎉 环境设置完成！"
            echo "使用 './deploy.sh start' 启动服务"
            ;;
        "start")
            start_services
            ;;
        "stop")
            stop_services
            ;;
        "restart")
            stop_services
            sleep 2
            start_services
            ;;
        "status")
            show_status
            ;;
        "logs")
            echo "📋 查看日志..."
            echo "后端日志: tail -f backend.log"
            echo "前端日志: tail -f frontend.log"
            ;;
        "clean")
            echo "🧹 清理环境..."
            stop_services
            rm -rf backend/venv
            rm -rf frontend/stock-scoring-app/node_modules
            rm -f backend.pid frontend.pid
            rm -f backend.log frontend.log
            echo "✅ 环境清理完成"
            ;;
        *)
            echo "用法: $0 {setup|start|stop|restart|status|logs|clean}"
            echo ""
            echo "命令说明:"
            echo "  setup   - 初始化环境和依赖"
            echo "  start   - 启动服务"
            echo "  stop    - 停止服务"
            echo "  restart - 重启服务"
            echo "  status  - 查看服务状态"
            echo "  logs    - 查看日志"
            echo "  clean   - 清理环境"
            exit 1
            ;;
    esac
}

# 检查参数
if [ -z "$1" ]; then
    main "help"
else
    main $1
fi