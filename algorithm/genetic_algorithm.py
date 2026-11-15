
import random
import copy
from algorithm.chromosome import Chromosome


class GeneticAlgorithm:

    def __init__(self, data_model, population_size=50,
                 generations=100, mutation_rate=0.1):

        """
        Khởi tạo thuật toán di truyền.

        data_model: Dữ liệu đầu vào.
        population_size: Số cá thể trong quần thể.
        generations: Số thế hệ tiến hóa.
        mutation_rate: Tỷ lệ đột biến.
        """

        self.data_model = data_model
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate

        self.population = []

    def initialize_population(self):
        """
        Khởi tạo quần thể ban đầu.
        """

        self.population = []

        for _ in range(self.population_size):

            chromosome = Chromosome(self.data_model)

            chromosome.generate_random()

            self.population.append(chromosome)

    def selection(self):
        """
        Chọn cá thể tốt để làm cha mẹ.
        Sử dụng phương pháp chọn lọc giải đấu.
        """

        if not self.population:
            return None

        candidates = random.sample(
            self.population,
            min(3, len(self.population))
        )

        best = max(
            candidates,
            key=lambda chrom: chrom.calculate_fitness()
        )

        return best

    def crossover(self, parent1, parent2):
        """
        Lai ghép hai cá thể cha mẹ
        để tạo ra cá thể con.
        """

        child = Chromosome(self.data_model)

        schedule1 = parent1.schedule
        schedule2 = parent2.schedule

        length = min(len(schedule1), len(schedule2))

        if length < 2:

            child.schedule = copy.deepcopy(schedule1)

        else:

            # Chọn vị trí lai ghép
            point = random.randint(1, length - 1)

            # Kết hợp gene từ hai cá thể cha mẹ
            child.schedule = (
                copy.deepcopy(schedule1[:point])
                + copy.deepcopy(schedule2[point:])
            )

        return child

    def mutate(self, chromosome):
        """
        Đột biến cá thể bằng cách thay đổi
        phòng học hoặc khung giờ.
        """

        if random.random() > self.mutation_rate:
            return chromosome

        if not chromosome.schedule:
            return chromosome

        rooms = chromosome.get_data("rooms")
        timeslots = chromosome.get_data("timeslots")

        if not rooms and not timeslots:
            return chromosome

        # Chọn ngẫu nhiên một gene
        gene = random.choice(chromosome.schedule)

        # Thay đổi phòng hoặc khung giờ
        if random.random() < 0.5:

            if rooms:
                gene["room"] = random.choice(rooms)

            elif timeslots:
                gene["timeslot"] = random.choice(timeslots)

        else:

            if timeslots:
                gene["timeslot"] = random.choice(timeslots)

            elif rooms:
                gene["room"] = random.choice(rooms)

        return chromosome

    def clone_chromosome(self, chromosome):
        """
        Sao chép một cá thể mà không sao chép module dữ liệu.
        """

        new_chromosome = Chromosome(self.data_model)

        new_chromosome.schedule = copy.deepcopy(
            chromosome.schedule
        )

        new_chromosome.fitness = chromosome.fitness

        return new_chromosome

    def run(self):
        """
        Chạy vòng lặp tiến hóa của thuật toán di truyền.
        """

        # Bước 1: Khởi tạo quần thể
        self.initialize_population()

        if not self.population:
            return None

        # Bước 2: Tính Fitness ban đầu
        for chromosome in self.population:
            chromosome.calculate_fitness()

        # Bước 3: Tìm cá thể tốt nhất ban đầu
        best_chromosome = self.clone_chromosome(
            max(
                self.population,
                key=lambda chrom: chrom.calculate_fitness()
            )
        )

        # Bước 4: Tiến hóa qua các thế hệ
        for generation in range(self.generations):

            new_population = []

            # Giữ lại cá thể tốt nhất
            new_population.append(
                self.clone_chromosome(best_chromosome)
            )

            # Tạo các cá thể mới
            while len(new_population) < self.population_size:

                # Chọn hai cá thể cha mẹ
                parent1 = self.selection()
                parent2 = self.selection()

                # Lai ghép
                child = self.crossover(parent1, parent2)

                # Đột biến
                child = self.mutate(child)

                # Tính điểm Fitness
                child.calculate_fitness()

                new_population.append(child)

            # Cập nhật quần thể
            self.population = new_population

            # Tìm cá thể tốt nhất của thế hệ
            current_best = max(
                self.population,
                key=lambda chrom: chrom.calculate_fitness()
            )

            # Cập nhật cá thể tốt nhất toàn bộ quá trình
            if (
                current_best.calculate_fitness()
                > best_chromosome.calculate_fitness()
            ):

                best_chromosome = self.clone_chromosome(
                    current_best
                )

        # Bước 5: Trả về thời khóa biểu tốt nhất
        return best_chromosome
