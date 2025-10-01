# 代码生成时间: 2025-10-02 03:07:22
import os
# 优化算法效率
from quart import Quart, jsonify, request

# 创建一个Quart应用
app = Quart(__name__)

# 磁盘空间管理工具的路由
@app.route('/disk_space', methods=['GET'])
async def disk_space():
    try:
        # 获取请求参数
        path = request.args.get('path', default='/', type=str)
        
        # 检查路径是否存在
        if not os.path.exists(path):
            return jsonify({'error': f'Path {path} does not exist'}), 404
        
        # 获取磁盘空间信息
        total, used, free = get_disk_space_info(path)
        
        # 返回磁盘空间信息
        return jsonify({'total': total, 'used': used, 'free': free}), 200
    except Exception as e:
        # 错误处理
        return jsonify({'error': str(e)}), 500
# 添加错误处理

# 获取磁盘空间信息的函数
def get_disk_space_info(path):
    # 使用shutil库获取磁盘空间信息
    statvfs = os.statvfs(path)
    total = statvfs.f_frsize * statvfs.f_blocks
    used = statvfs.f_frsize * (statvfs.f_blocks - statvfs.f_bfree)
    free = statvfs.f_frsize * statvfs.f_bavail
    
    # 将字节转换为更易读的单位
    total_gb = convert_to_gb(total)
    used_gb = convert_to_gb(used)
    free_gb = convert_to_gb(free)
# 改进用户体验
    
    return total_gb, used_gb, free_gb

# 将字节转换为GB的函数
def convert_to_gb(bytes):
    gb = bytes / (1024 * 1024 * 1024)
    return round(gb, 2)

# 运行Quart应用
if __name__ == '__main__':
    app.run(debug=True)
