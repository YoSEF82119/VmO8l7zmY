# 代码生成时间: 2025-10-10 02:33:13
from quart import Quart, jsonify, request

# 创建一个 Quart 应用
app = Quart(__name__)

# 定义一个虚拟实验室的实验数据结构
class VirtualLab:
    def __init__(self):
        # 初始化实验数据
        self.experiments = []

    def add_experiment(self, experiment_name, experiment_data):
        # 添加实验
        experiment = {"name": experiment_name, "data": experiment_data}
        self.experiments.append(experiment)
        return experiment

    def get_experiment(self, experiment_name):
        # 根据名称获取实验数据
        for experiment in self.experiments:
            if experiment['name'] == experiment_name:
                return experiment
        return None

    def update_experiment(self, experiment_name, new_data):
        # 更新实验数据
        for experiment in self.experiments:
            if experiment['name'] == experiment_name:
                experiment['data'] = new_data
                return experiment
        return None

    def delete_experiment(self, experiment_name):
        # 删除实验
        for i, experiment in enumerate(self.experiments):
            if experiment['name'] == experiment_name:
                return self.experiments.pop(i)
        return None

# 实例化虚拟实验室
virtual_lab = VirtualLab()

# 路由：添加实验
@app.route('/experiments', methods=['POST'])
async def add_experiment_api():
    try:
        experiment_data = await request.get_json()
        experiment_name = experiment_data['name']
        experiment = virtual_lab.add_experiment(experiment_name, experiment_data['data'])
        return jsonify(experiment), 201
    except KeyError as e:
        return jsonify({'error': 'Missing data'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 路由：获取实验数据
@app.route('/experiments/<experiment_name>', methods=['GET'])
async def get_experiment_api(experiment_name):
    experiment = virtual_lab.get_experiment(experiment_name)
    if experiment:
        return jsonify(experiment)
    else:
        return jsonify({'error': 'Experiment not found'}), 404

# 路由：更新实验数据
@app.route('/experiments/<experiment_name>', methods=['PUT'])
async def update_experiment_api(experiment_name):
    try:
        new_data = await request.get_json()
        experiment = virtual_lab.update_experiment(experiment_name, new_data)
        if experiment:
            return jsonify(experiment)
        else:
            return jsonify({'error': 'Experiment not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 路由：删除实验
@app.route('/experiments/<experiment_name>', methods=['DELETE'])
async def delete_experiment_api(experiment_name):
    experiment = virtual_lab.delete_experiment(experiment_name)
    if experiment:
        return jsonify({'message': 'Experiment deleted'}), 200
    else:
        return jsonify({'error': 'Experiment not found'}), 404

# 运行应用
if __name__ == '__main__':
    app.run(debug=True)