# 代码生成时间: 2025-11-03 00:40:23
import quart
import random

# 创建一个Quart应用
app = quart.Quart(__name__)

# 定义路由和视图函数
@app.route("/generate", methods=["GET"])
def generate_random_number():
    # 获取请求参数
    try:
        min_value = int(quart.request.args.get("min", 0))
        max_value = int(quart.request.args.get("max", 100))
        
        # 参数校验
        if min_value > max_value:
            return {"error": "Invalid range. Minimum value cannot be greater than maximum value."}, 400
        
        # 生成随机数
        random_number = random.randint(min_value, max_value)
        return {"random_number": random_number}
    
    # 错误处理
    except ValueError:
        return {"error": "Invalid input. Ensure minimum and maximum values are integers."}, 400
    
    # 处理其他异常
    except Exception as e:
        return {"error": str(e)}, 500

# 主函数
if __name__ == '__main__':
    # 启动Quart应用
    app.run(debug=True)