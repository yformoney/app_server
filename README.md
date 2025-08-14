# 🚀 Android App 后台服务

基于Django REST Framework构建的现代化Android应用后台服务，提供完整的用户认证和订单管理系统。

## ✨ 功能特性

### 🔐 用户认证系统
- 用户注册、登录、登出
- Token认证机制
- 用户信息管理
- 密码安全验证

### 📦 订单管理系统
- 订单创建和管理
- 订单状态流转 (待付款→已付款→处理中→已发货→已送达)
- 订单商品明细管理
- 订单操作日志记录
- 订单统计和筛选

### 🛡️ 系统特性
- RESTful API设计
- Token基础的API认证
- 📱 CORS支持，完美适配Android应用
- 🗄️ SQLite/PostgreSQL数据库支持
- 🐳 Docker容器化部署
- 🔧 完整的API文档和测试

## 🛠️ 技术栈

- **后端框架**: Django 5.2.5
- **API框架**: Django REST Framework 3.16.1
- **数据库**: SQLite (开发) / PostgreSQL (生产)
- **认证**: Token Authentication
- **跨域**: django-cors-headers 4.7.0
- **容器化**: Docker & Docker Compose
- **Web服务器**: Gunicorn

## 🚀 快速开始

### 本地开发环境

1. **克隆项目**:
   ```bash
   git clone https://github.com/your-username/app_server.git
   cd app_server
   ```

2. **安装依赖**:
   ```bash
   pip install -r requirements.txt
   ```

3. **数据库迁移**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **启动开发服务器**:
   ```bash
   python manage.py runserver
   ```

5. **访问应用**:
   - 🌐 开发服务器: http://127.0.0.1:8000/
   - 🔐 Admin后台: http://127.0.0.1:8000/admin/
   - 📡 API基础路径: http://127.0.0.1:8000/api/

### 阿里云服务器部署

1. **创建虚拟环境**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **安装依赖**:
   ```bash
   pip install -r requirements.txt
   ```

3. **配置环境变量**:
   ```bash
   export SECRET_KEY="your-secret-key"
   export DEBUG="False"
   export ALLOWED_HOSTS="your-domain.com,your-ip"
   export USE_POSTGRES="true"
   export DB_NAME="your_db_name"
   export DB_USER="your_db_user"
   export DB_PASSWORD="your_db_password"
   export DB_HOST="localhost"
   export DB_PORT="5432"
   ```

4. **数据库迁移**:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. **收集静态文件**:
   ```bash
   python manage.py collectstatic
   ```

6. **启动Gunicorn服务**:
   ```bash
   gunicorn app_server.wsgi:application --bind 0.0.0.0:8000
   ```

### Docker部署

```bash
# 构建并启动服务
docker-compose up --build

# 后台运行
docker-compose up -d
```

## 📡 API接口

### 🔐 用户认证接口

| 接口 | 方法 | 说明 | 认证 |
|------|------|------|------|
| `/api/auth/register/` | POST | 用户注册 | ❌ |
| `/api/auth/login/` | POST | 用户登录 | ❌ |
| `/api/auth/logout/` | POST | 用户登出 | ✅ |
| `/api/auth/profile/` | GET/PUT | 获取/更新用户信息 | ✅ |

### 📦 订单管理接口

| 接口 | 方法 | 说明 | 认证 |
|------|------|------|------|
| `/api/orders/` | GET/POST | 获取订单列表/创建订单 | ✅ |
| `/api/orders/{id}/` | GET | 获取订单详情 | ✅ |
| `/api/orders/{id}/update_status/` | PATCH | 更新订单状态 | ✅ |
| `/api/orders/{id}/cancel/` | POST | 取消订单 | ✅ |
| `/api/orders/statistics/` | GET | 订单统计 | ✅ |
| `/api/orders/{id}/logs/` | GET | 订单操作日志 | ✅ |

### 请求示例

```bash
# 用户注册
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com", 
    "password": "testpass123",
    "password_confirm": "testpass123",
    "first_name": "测试",
    "last_name": "用户"
  }'

# 用户登录
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'

# 创建订单
curl -X POST http://127.0.0.1:8000/api/orders/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token your-token-here" \
  -d '{
    "receiver_name": "张三",
    "receiver_phone": "13900139000",
    "receiver_address": "北京市朝阳区某某街道",
    "items": [
      {
        "product_name": "iPhone 15",
        "quantity": 1,
        "unit_price": "5999.00"
      }
    ]
  }'

# 获取订单列表
curl -X GET http://127.0.0.1:8000/api/orders/ \
  -H "Authorization: Token your-token-here"
```

📖 **完整API文档**: 查看项目根目录下的 `API接口文档.md` 文件

## 🔧 开发工具

- **API测试**: `python test_apis.py` - 完整的API接口测试
- **服务器测试**: `python test_server.py` - 基础服务器测试

## 📝 项目结构

```
app_server/
├── app_server/          # Django项目配置
│   ├── settings.py      # 项目设置
│   ├── urls.py          # 主路由配置
│   └── ...
├── authentication/      # 用户认证应用
│   ├── models.py        # 用户模型
│   ├── views.py         # 认证视图
│   ├── serializers.py   # 序列化器
│   └── urls.py          # 认证路由
├── orders/             # 订单管理应用
│   ├── models.py       # 订单模型
│   ├── views.py        # 订单视图
│   ├── serializers.py  # 订单序列化器
│   └── urls.py         # 订单路由
├── test_apis.py        # API测试脚本
├── API接口文档.md       # 完整接口文档
├── requirements.txt    # 生产依赖
├── requirements-dev.txt # 开发依赖
└── docker-compose.yml  # Docker配置
```

## 🌟 开发指南

### 添加新的API接口

1. 在相应的`views.py`中创建视图
2. 在`urls.py`中添加URL路由
3. 更新API文档
4. 编写单元测试

### 数据库操作

```bash
# 创建迁移
python manage.py makemigrations

# 应用迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser
```

## 🔐 安全配置

- ✅ DEBUG模式默认关闭（生产环境）
- ✅ SECRET_KEY通过环境变量配置
- ✅ CORS策略配置
- ✅ Token认证机制
- ✅ SQL注入防护

## 📊 监控和日志

- Django内置日志系统
- 数据库查询监控
- API性能监控

## 🤝 贡献指南

1. Fork项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交变更 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

## 📄 许可证

此项目基于MIT许可证开源 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

- Django团队提供的优秀框架
- Django REST Framework的强大API支持
- Claude Code提供的开发助手

---

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>