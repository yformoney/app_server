#!/bin/bash

# 阿里云服务器部署脚本
# Django Android App 后台服务部署

set -e

echo "🚀 开始部署 Django Android App 后台服务..."

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查Python版本
echo -e "${YELLOW}检查Python环境...${NC}"
python3 --version

# 创建虚拟环境（如果不存在）
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}创建虚拟环境...${NC}"
    python3 -m venv venv
fi

# 激活虚拟环境
echo -e "${YELLOW}激活虚拟环境...${NC}"
source venv/bin/activate

# 升级pip
echo -e "${YELLOW}升级pip...${NC}"
pip install --upgrade pip

# 安装依赖
echo -e "${YELLOW}安装项目依赖...${NC}"
pip install -r requirements.txt

# 检查环境变量
echo -e "${YELLOW}检查环境变量...${NC}"
if [ -z "$SECRET_KEY" ]; then
    echo -e "${RED}警告: SECRET_KEY 环境变量未设置${NC}"
    echo "建议设置: export SECRET_KEY='your-secret-key'"
fi

if [ -z "$ALLOWED_HOSTS" ]; then
    echo -e "${YELLOW}使用默认ALLOWED_HOSTS设置${NC}"
fi

# 数据库迁移
echo -e "${YELLOW}执行数据库迁移...${NC}"
python manage.py makemigrations
python manage.py migrate

# 收集静态文件
echo -e "${YELLOW}收集静态文件...${NC}"
python manage.py collectstatic --noinput

# 检查Django配置
echo -e "${YELLOW}检查Django配置...${NC}"
python manage.py check --deploy

# 创建超级用户（可选）
echo -e "${YELLOW}是否创建超级用户？(y/n)${NC}"
read -r create_superuser
if [ "$create_superuser" = "y" ]; then
    python manage.py createsuperuser
fi

echo -e "${GREEN}✅ 部署完成！${NC}"
echo ""
echo -e "${GREEN}启动服务:${NC}"
echo "  开发模式: python manage.py runserver 0.0.0.0:8000"
echo "  生产模式: gunicorn app_server.wsgi:application --bind 0.0.0.0:8000"
echo ""
echo -e "${GREEN}API测试:${NC}"
echo "  python test_apis.py"
echo ""
echo -e "${GREEN}访问地址:${NC}"
echo "  API: http://your-server-ip:8000/api/"
echo "  管理后台: http://your-server-ip:8000/admin/"