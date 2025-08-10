#!/bin/bash
# Django应用服务器启动脚本

echo "🚀 启动Django应用服务器..."

# 激活虚拟环境
source venv/bin/activate

# 检查项目配置
echo "🔧 检查项目配置..."
python manage.py check

if [ $? -ne 0 ]; then
    echo "❌ 项目配置检查失败！"
    exit 1
fi

# 应用数据库迁移
echo "📊 应用数据库迁移..."
python manage.py migrate

# 启动开发服务器
echo "🌐 启动开发服务器在端口 9000..."
echo "📍 访问地址:"
echo "  - Admin后台: http://127.0.0.1:9000/admin/"
echo "  - API基础路径: http://127.0.0.1:9000/api/"
echo ""
echo "按 Ctrl+C 停止服务器"
echo ""

python manage.py runserver 127.0.0.1:9000