# 🚀 Django 应用服务器

基于Django REST Framework构建的现代化应用服务器，支持用户认证和API管理。

## ✨ 功能特性

- 🔐 用户认证系统 (注册/登录/登出)
- 🛡️ Token基础的API认证
- 📱 CORS支持，适配移动应用
- 🗄️ SQLite/PostgreSQL数据库支持
- 🐳 Docker容器化部署
- 🔧 开发环境一键启动

## 🛠️ 技术栈

- **后端框架**: Django 4.2.7
- **API框架**: Django REST Framework 3.14.0
- **数据库**: SQLite (开发) / PostgreSQL (生产)
- **认证**: Token Authentication
- **容器化**: Docker & Docker Compose
- **Web服务器**: Gunicorn

## 🚀 快速开始

### 本地开发环境

1. **启动开发服务器**:
   ```bash
   ./start_server.sh
   ```

2. **访问应用**:
   - 🌐 开发服务器: http://127.0.0.1:9000/
   - 🔐 Admin后台: http://127.0.0.1:9000/admin/
   - 📡 API基础路径: http://127.0.0.1:9000/api/

### Docker部署

```bash
# 构建并启动服务
docker-compose up --build

# 后台运行
docker-compose up -d
```

## 📡 API接口

### 认证接口

| 接口 | 方法 | 说明 | 认证 |
|------|------|------|------|
| `/api/login/` | POST | 用户登录 | ❌ |
| `/api/logout/` | POST | 用户登出 | ✅ |
| `/api/profile/` | GET | 获取用户资料 | ✅ |

### 请求示例

```bash
# 登录获取Token
curl -X POST http://127.0.0.1:9000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password"}'

# 使用Token访问受保护接口
curl -X GET http://127.0.0.1:9000/api/profile/ \
  -H "Authorization: Token your-token-here"
```

## 🔧 开发工具

- **测试服务器**: `python test_server.py`
- **代码上传**: `./upload_code.sh`
- **GitHub配置**: `./setup_github.sh`

## 📝 项目结构

```
app_server/
├── app_server/          # Django项目配置
├── authentication/      # 用户认证应用
├── venv/               # Python虚拟环境
├── start_server.sh     # 启动脚本
├── upload_code.sh      # 代码上传脚本
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