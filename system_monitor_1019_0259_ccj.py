# 代码生成时间: 2025-10-19 02:59:39
import psutil
from quart import Quart, jsonify

# 创建Quart应用
app = Quart(__name__)

# 系统资源监控器路由
@app.route('/monitor', methods=['GET'])
def monitor_system_resources():
    try:
        # 收集CPU信息
        cpu_usage = psutil.cpu_percent(interval=1)
        # 收集内存信息
        memory = psutil.virtual_memory()
        memory_usage = memory.percent
        # 收集磁盘信息
        disk_usage = psutil.disk_usage('/')
        disk_usage_percent = disk_usage.percent
        # 收集网络信息
        net_io = psutil.net_io_counters()
        # 返回系统资源信息
        return jsonify({
            'CPU Usage': cpu_usage,
            'Memory Usage': memory_usage,
            'Disk Usage': disk_usage_percent,
            'Network IO': {
                'Bytes Sent': net_io.bytes_sent,
                'Bytes Received': net_io.bytes_recv
            }
        })
    except Exception as e:
        # 错误处理
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)