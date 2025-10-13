# 代码生成时间: 2025-10-14 02:22:35
import random
from quart import Quart, jsonify, request
from functools import reduce
from operator import add

# Genetic Algorithm Framework
class GeneticAlgorithm:
    """遗传算法框架，用于解决优化问题。"""

    def __init__(self, population_size, num_generations, fitness_func, mutation_rate, crossover_rate, selection_method='roulette_wheel'):
        """
        :param population_size: 种群大小
        :param num_generations: 迭代代数
        :param fitness_func: 适应度函数
        :param mutation_rate: 变异率
        :param crossover_rate: 交叉率
        :param selection_method: 选择方法，默认为轮盘赌
        """
        self.population_size = population_size
        self.num_generations = num_generations
        self.fitness_func = fitness_func
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.selection_method = selection_method

    def generate_initial_population(self):
        """生成初始种群"""
        return [[random.randint(0, 1) for _ in range(10)] for _ in range(self.population_size)]  # 假设是10位二进制编码

    def calculate_fitness(self, population):
        """计算种群的适应度"""
        return [self.fitness_func(individual) for individual in population]

    def select_individuals(self, population, fitness_values):
        """根据适应度选择个体"""
        if self.selection_method == 'roulette_wheel':
            # 轮盘赌选择
            max_fitness = reduce(add, fitness_values)
            return sorted(zip(population, fitness_values), key=lambda x: x[1], reverse=True)
        else:
            raise ValueError('Unsupported selection method')

    def crossover(self, parent1, parent2):
        """交叉操作"""
        crossover_point = random.randint(1, len(parent1) - 1)
        return parent1[:crossover_point] + parent2[crossover_point:], parent2[:crossover_point] + parent1[crossover_point:]

    def mutate(self, individual):
        """变异操作"""
        mutation_point = random.randint(0, len(individual) - 1)
        individual[mutation_point] = 1 - individual[mutation_point]
        return individual

    def evolve(self):
        """进化过程"""
        population = self.generate_initial_population()
        fitness_values = self.calculate_fitness(population)
        for generation in range(self.num_generations):
            selected_individuals = self.select_individuals(population, fitness_values)
            new_population = []
            for _ in range(self.population_size):
                parent1, parent2 = random.sample([ind for ind, _ in selected_individuals], 2)
                if random.random() < self.crossover_rate:
                    new_individual1, new_individual2 = self.crossover(parent1, parent2)
                else:
                    new_individual1, new_individual2 = parent1, parent2
                if random.random() < self.mutation_rate:
                    new_individual1 = self.mutate(new_individual1)
                if random.random() < self.mutation_rate:
                    new_individual2 = self.mutate(new_individual2)
                new_population.extend([new_individual1, new_individual2])
            population = new_population[:self.population_size]
            fitness_values = self.calculate_fitness(population)
        return population[0]  # 返回最优解

# Quart 应用
app = Quart(__name__)

@app.route('/evolve', methods=['POST'])
async def evolve():
    try:
        request_data = await request.get_json()
        population_size = request_data.get('population_size', 100)
        num_generations = request_data.get('num_generations', 100)
        fitness_func = request_data.get('fitness_func', lambda x: sum(x))  # 默认适应度函数
        mutation_rate = request_data.get('mutation_rate', 0.01)
        crossover_rate = request_data.get('crossover_rate', 0.7)
        
        genetic_algorithm = GeneticAlgorithm(
            population_size,
            num_generations,
            fitness_func,
            mutation_rate,
            crossover_rate
        )
        best_individual = genetic_algorithm.evolve()
        return jsonify({'best_individual': best_individual})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)