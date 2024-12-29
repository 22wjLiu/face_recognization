from app import create_app

# 创建 Flask 应用实例
app = create_app()

# 启动应用
if __name__ == "__main__":
    # 启动 Flask 应用，设置调试模式为 True 方便开发时调试
    app.run(debug=True, host='0.0.0.0', port=5000)