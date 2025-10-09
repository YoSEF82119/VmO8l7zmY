# 代码生成时间: 2025-10-09 18:02:34
import os
import re
from quart import Quart, request, jsonify

# 创建 Quart 应用
app = Quart(__name__)


# 批量重命名文件的函数
def rename_files(directory, pattern, replacement):
    """
    批量重命名指定目录中的文件。
    
    :param directory: 要重命名文件的目录
    :param pattern: 匹配模式
    :param replacement: 替换字符串
    :return: 重命名结果列表
    """
    renamed_files = []
    try:
        for filename in os.listdir(directory):
            if re.match(pattern, filename):  # 检查文件名是否匹配模式
                new_filename = re.sub(pattern, replacement, filename)
                os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))
                renamed_files.append({'old_name': filename, 'new_name': new_filename})
        return renamed_files
    except Exception as e:  # 处理文件操作中可能出现的异常
        return [{'error': str(e)}]


# API 路由：执行批量重命名
@app.route('/rename', methods=['POST'])
async def rename():
    """
    处理 POST 请求以批量重命名文件。
    
    :return: JSON 响应，包含重命名结果。
    """
    try:  # 尝试获取 JSON 数据
        data = await request.get_json()  # 从请求中获取 JSON 数据
        directory = data.get('directory')  # 要重命名文件的目录
        pattern = data.get('pattern')  # 匹配模式
        replacement = data.get('replacement')  # 替换字符串
        if directory is None or pattern is None or replacement is None:  # 校验数据完整性
            return jsonify({'error': 'Missing parameters'}), 400
        results = rename_files(directory, pattern, replacement)
        return jsonify(results)  # 返回重命名结果
    except Exception as e:  # 处理请求解析中的异常
        return jsonify({'error': str(e)}), 500


# 运行应用
if __name__ == '__main__':
    app.run(debug=True)