# Android App 后台API接口文档

## 基础信息

- **基础URL**: `http://your-domain.com/api/`
- **认证方式**: Token认证
- **数据格式**: JSON
- **字符编码**: UTF-8

## 认证机制

所有需要认证的接口都需要在请求头中包含Token：

```
Authorization: Token your_token_here
```

---

## 用户认证接口

### 1. 用户注册

**接口**: `POST /api/auth/register/`

**说明**: 创建新用户账户

**请求参数**:
```json
{
    "username": "string",        // 用户名（必填，唯一）
    "email": "string",           // 邮箱（必填，唯一）
    "password": "string",        // 密码（必填，最少8位）
    "password_confirm": "string", // 确认密码（必填）
    "first_name": "string",      // 姓（可选）
    "last_name": "string",       // 名（可选）
    "phone": "string"            // 电话（可选）
}
```

**成功响应** (201):
```json
{
    "success": true,
    "message": "注册成功",
    "token": "your_auth_token",
    "user": {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "first_name": "测试",
        "last_name": "用户",
        "phone": "13800138000",
        "avatar": null,
        "date_joined": "2025-08-14T10:00:00Z"
    }
}
```

### 2. 用户登录

**接口**: `POST /api/auth/login/`

**说明**: 用户登录获取访问令牌

**请求参数**:
```json
{
    "username": "string",  // 用户名
    "password": "string"   // 密码
}
```

**成功响应** (200):
```json
{
    "success": true,
    "message": "登录成功",
    "token": "your_auth_token",
    "user": {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "first_name": "测试",
        "last_name": "用户",
        "phone": "13800138000",
        "avatar": null,
        "date_joined": "2025-08-14T10:00:00Z"
    }
}
```

### 3. 用户登出

**接口**: `POST /api/auth/logout/`

**说明**: 用户登出，删除访问令牌

**认证**: 需要Token认证

**成功响应** (200):
```json
{
    "success": true,
    "message": "退出登录成功"
}
```

### 4. 获取用户信息

**接口**: `GET /api/auth/profile/`

**说明**: 获取当前登录用户的详细信息

**认证**: 需要Token认证

**成功响应** (200):
```json
{
    "success": true,
    "user": {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "first_name": "测试",
        "last_name": "用户",
        "phone": "13800138000",
        "avatar": null,
        "date_joined": "2025-08-14T10:00:00Z"
    }
}
```

### 5. 更新用户信息

**接口**: `PUT /api/auth/profile/`

**说明**: 更新当前登录用户的信息

**认证**: 需要Token认证

**请求参数**:
```json
{
    "first_name": "string",    // 姓（可选）
    "last_name": "string",     // 名（可选）
    "phone": "string",         // 电话（可选）
    "avatar": "string"         // 头像URL（可选）
}
```

**成功响应** (200):
```json
{
    "success": true,
    "message": "个人信息更新成功",
    "user": {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "first_name": "更新后的姓",
        "last_name": "更新后的名",
        "phone": "13900139000",
        "avatar": "https://example.com/avatar.jpg",
        "date_joined": "2025-08-14T10:00:00Z"
    }
}
```

---

## 订单管理接口

### 1. 创建订单

**接口**: `POST /api/orders/`

**说明**: 创建新订单

**认证**: 需要Token认证

**请求参数**:
```json
{
    "receiver_name": "string",      // 收货人姓名（必填）
    "receiver_phone": "string",     // 收货人电话（必填）
    "receiver_address": "string",   // 收货地址（必填）
    "notes": "string",             // 订单备注（可选）
    "items": [                     // 订单商品列表（必填）
        {
            "product_name": "string",    // 商品名称
            "product_sku": "string",     // 商品SKU（可选）
            "product_image": "string",   // 商品图片URL（可选）
            "quantity": 1,               // 数量
            "unit_price": "99.99"        // 单价
        }
    ]
}
```

**成功响应** (201):
```json
{
    "success": true,
    "message": "订单创建成功",
    "data": {
        "id": "uuid",
        "order_number": "ORD1692001234567",
        "status": "pending",
        "status_display": "待付款",
        "user": 1,
        "user_name": "testuser",
        "receiver_name": "张三",
        "receiver_phone": "13900139000",
        "receiver_address": "北京市朝阳区某某街道某某号",
        "total_amount": "6197.00",
        "discount_amount": "0.00",
        "shipping_fee": "0.00",
        "final_amount": "6197.00",
        "notes": "请在工作时间送货",
        "created_at": "2025-08-14T10:00:00Z",
        "updated_at": "2025-08-14T10:00:00Z",
        "paid_at": null,
        "shipped_at": null,
        "delivered_at": null,
        "items": [
            {
                "id": 1,
                "product_name": "iPhone 15",
                "product_sku": "IP15-128G-BLK",
                "product_image": "https://example.com/iphone15.jpg",
                "quantity": 1,
                "unit_price": "5999.00",
                "total_price": "5999.00"
            },
            {
                "id": 2,
                "product_name": "保护壳",
                "product_sku": "CASE-IP15-BLK",
                "product_image": null,
                "quantity": 2,
                "unit_price": "99.00",
                "total_price": "198.00"
            }
        ],
        "logs": [
            {
                "id": 1,
                "action": "CREATE",
                "description": "订单创建成功",
                "operator_name": "testuser",
                "created_at": "2025-08-14T10:00:00Z"
            }
        ]
    }
}
```

### 2. 获取订单列表

**接口**: `GET /api/orders/`

**说明**: 获取当前用户的订单列表

**认证**: 需要Token认证

**查询参数**:
- `status`: 按状态筛选 (pending, paid, processing, shipped, delivered, cancelled, refunded)
- `start_date`: 开始日期 (YYYY-MM-DD)
- `end_date`: 结束日期 (YYYY-MM-DD)
- `order_number`: 订单号模糊搜索
- `page`: 页码
- `page_size`: 每页数量

**成功响应** (200):
```json
{
    "success": true,
    "data": [
        {
            "id": "uuid",
            "order_number": "ORD1692001234567",
            "status": "pending",
            "status_display": "待付款",
            "user": 1,
            "user_name": "testuser",
            "receiver_name": "张三",
            "receiver_phone": "13900139000",
            "receiver_address": "北京市朝阳区某某街道某某号",
            "total_amount": "6197.00",
            "final_amount": "6197.00",
            "created_at": "2025-08-14T10:00:00Z",
            "items": [...],
            "logs": [...]
        }
    ]
}
```

### 3. 获取订单详情

**接口**: `GET /api/orders/{order_id}/`

**说明**: 获取指定订单的详细信息

**认证**: 需要Token认证

**成功响应** (200):
```json
{
    "success": true,
    "data": {
        "id": "uuid",
        "order_number": "ORD1692001234567",
        "status": "pending",
        "status_display": "待付款",
        // ... 完整订单信息
    }
}
```

### 4. 更新订单状态

**接口**: `PATCH /api/orders/{order_id}/update_status/`

**说明**: 更新订单状态

**认证**: 需要Token认证

**请求参数**:
```json
{
    "status": "paid",           // 新状态
    "notes": "用户已付款"       // 备注（可选）
}
```

**成功响应** (200):
```json
{
    "success": true,
    "message": "订单状态更新成功",
    "data": {
        // 更新后的订单信息
    }
}
```

### 5. 取消订单

**接口**: `POST /api/orders/{order_id}/cancel/`

**说明**: 取消订单（仅限pending、paid状态）

**认证**: 需要Token认证

**成功响应** (200):
```json
{
    "success": true,
    "message": "订单取消成功",
    "data": {
        // 更新后的订单信息
    }
}
```

### 6. 订单统计

**接口**: `GET /api/orders/statistics/`

**说明**: 获取用户订单统计信息

**认证**: 需要Token认证

**成功响应** (200):
```json
{
    "success": true,
    "data": {
        "total_orders": 10,
        "pending_orders": 2,
        "paid_orders": 3,
        "processing_orders": 1,
        "shipped_orders": 2,
        "delivered_orders": 1,
        "cancelled_orders": 1
    }
}
```

### 7. 获取订单日志

**接口**: `GET /api/orders/{order_id}/logs/`

**说明**: 获取订单操作日志

**认证**: 需要Token认证

**成功响应** (200):
```json
{
    "success": true,
    "data": [
        {
            "id": 1,
            "action": "CREATE",
            "description": "订单创建成功",
            "operator_name": "testuser",
            "created_at": "2025-08-14T10:00:00Z"
        },
        {
            "id": 2,
            "action": "STATUS_CHANGE",
            "description": "订单状态从 待付款 变更为 已付款。用户已付款",
            "operator_name": "testuser",
            "created_at": "2025-08-14T10:30:00Z"
        }
    ]
}
```

---

## 订单状态说明

| 状态值 | 中文名称 | 说明 |
|--------|----------|------|
| pending | 待付款 | 订单已创建，等待用户付款 |
| paid | 已付款 | 用户已完成付款，等待处理 |
| processing | 处理中 | 订单正在处理中（备货、包装等） |
| shipped | 已发货 | 订单已发货，等待配送 |
| delivered | 已送达 | 订单已成功送达用户 |
| cancelled | 已取消 | 订单已取消 |
| refunded | 已退款 | 订单已退款 |

---

## 错误响应格式

当请求失败时，服务器会返回统一格式的错误响应：

```json
{
    "success": false,
    "message": "错误描述",
    "errors": {
        "字段名": ["具体错误信息"]
    }
}
```

常见HTTP状态码：
- `400` - 请求参数错误
- `401` - 未认证或Token无效
- `403` - 权限不足
- `404` - 资源不存在
- `500` - 服务器内部错误

---

## 使用示例

### Android中使用示例（Java/Kotlin）

```kotlin
// 用户登录
val loginData = mapOf(
    "username" to "testuser",
    "password" to "testpass123"
)

// 发送POST请求
val response = httpClient.post("${baseUrl}/auth/login/") {
    contentType(ContentType.Application.Json)
    setBody(loginData)
}

// 保存token用于后续请求
val token = response.body<LoginResponse>().token

// 创建订单
val orderData = mapOf(
    "receiver_name" to "张三",
    "receiver_phone" to "13900139000",
    "receiver_address" to "北京市朝阳区某某街道",
    "items" to listOf(
        mapOf(
            "product_name" to "iPhone 15",
            "quantity" to 1,
            "unit_price" to "5999.00"
        )
    )
)

val orderResponse = httpClient.post("${baseUrl}/orders/") {
    contentType(ContentType.Application.Json)
    header("Authorization", "Token $token")
    setBody(orderData)
}
```