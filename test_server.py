#!/usr/bin/env python3
"""
Django应用服务器健康检查脚本
"""
import requests
import sys

def test_server():
    base_url = "http://127.0.0.1:9000"
    
    print("🔍 测试Django应用服务器...")
    
    # 测试服务器是否运行
    try:
        response = requests.get(f"{base_url}/admin/", timeout=5)
        print(f"✅ 服务器运行正常 - Admin页面状态码: {response.status_code}")
    except Exception as e:
        print(f"❌ 服务器连接失败: {e}")
        return False
    
    # 测试API端点
    try:
        response = requests.get(f"{base_url}/api/login/", timeout=5)
        print(f"✅ API端点响应正常 - 登录端点状态码: {response.status_code}")
    except Exception as e:
        print(f"❌ API端点测试失败: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = test_server()
    if success:
        print("\n🎉 Django应用服务器运行正常！")
        print("📍 访问地址:")
        print("  - Admin后台: http://127.0.0.1:9000/admin/")
        print("  - API基础路径: http://127.0.0.1:9000/api/")
        print("  - 登录API: http://127.0.0.1:9000/api/login/")
        print("  - 用户资料API: http://127.0.0.1:9000/api/profile/")
    else:
        print("\n❌ 服务器测试失败！")
        sys.exit(1)