import random
import math

# Block definitions
blocks = {
    'ALU': {'width': 5, 'height': 5},
    'Cache': {'width': 7, 'height': 4},
    'Control Unit': {'width': 4, 'height': 4},
    'Register File': {'width': 6, 'height': 6},
    'Decoder': {'width': 5, 'height': 3},
    'Floating Unit': {'width': 5, 'height': 5}
}

block_names = ['ALU', 'Cache', 'Control Unit', 'Register File', 'Decoder', 'Floating Unit']

# Connections (block pairs that need wiring)
connections = [
    ('Register File', 'ALU'),
    ('Control Unit', 'ALU'),
    ('ALU', 'Cache'),
    ('Register File', 'Floating Unit'),
    ('Cache', 'Decoder'),
    ('Decoder', 'Floating Unit')
]

# Parameters
GRID_SIZE = 25
POPULATION_SIZE = 6
MAX_GENERATIONS = 15
MUTATION_RATE = 0.1
ALPHA = 1000  # Overlap penalty weight
BETA = 2      # Wiring length penalty weight
GAMMA = 1     # Bounding area penalty weight

# Function to generate a random chromosome
def generate_random_chromosome():
    chromosome = []
    for block_name in block_names:
        x = random.randint(0, GRID_SIZE - blocks[block_name]['width'])
        y = random.randint(0, GRID_SIZE - blocks[block_name]['height'])
        chromosome.append((x, y))
    return chromosome

# Function to calculate center of a block
def get_center(position, block_name):
    x, y = position
    width = blocks[block_name]['width']
    height = blocks[block_name]['height']
    center_x = x + width / 2
    center_y = y + height / 2
    return center_x, center_y

# Function to calculate Euclidean distance between two centers
def calculate_distance(pos1, block1, pos2, block2):
    center1 = get_center(pos1, block1)
    center2 = get_center(pos2, block2)
    distance = math.sqrt((center1[0] - center2[0])**2 + (center1[1] - center2[1])**2)
    return distance

# Function to calculate total wiring distance
def calculate_wiring_distance(chromosome):
    total_distance = 0
    for block1, block2 in connections:
        idx1 = block_names.index(block1)
        idx2 = block_names.index(block2)
        pos1 = chromosome[idx1]
        pos2 = chromosome[idx2]
        distance = calculate_distance(pos1, block1, pos2, block2)
        total_distance += distance
    return total_distance

# Function to calculate bounding box area
def calculate_bounding_area(chromosome):
    x_coords = []
    y_coords = []

    for i, (x, y) in enumerate(chromosome):
        block_name = block_names[i]
        width = blocks[block_name]['width']
        height = blocks[block_name]['height']
        x_coords.append(x)
        x_coords.append(x + width)
        y_coords.append(y)
        y_coords.append(y + height)

    x_min = min(x_coords)
    x_max = max(x_coords)
    y_min = min(y_coords)
    y_max = max(y_coords)

    area = (x_max - x_min) * (y_max - y_min)
    return area

# Function to check if two blocks overlap
def check_overlap(pos1, block1, pos2, block2):
    x1, y1 = pos1
    x2, y2 = pos2

    width1 = blocks[block1]['width']
    height1 = blocks[block1]['height']
    width2 = blocks[block2]['width']
    height2 = blocks[block2]['height']

    # Calculate boundaries
    a_left = x1
    a_right = x1 + width1
    a_bottom = y1
    a_top = y1 + height1

    b_left = x2
    b_right = x2 + width2
    b_bottom = y2
    b_top = y2 + height2

    # Check for no overlap (then return False)
    no_overlap = (a_right <= b_left or
                  a_left >= b_right or
                  a_bottom >= b_top or
                  a_top <= b_bottom)

    return not no_overlap

# Function to count total overlaps
def count_overlaps(chromosome):
    overlap_count = 0
    for i in range(len(chromosome)):
        for j in range(i + 1, len(chromosome)):
            if check_overlap(chromosome[i], block_names[i],
                           chromosome[j], block_names[j]):
                overlap_count += 1
    return overlap_count

# Function to calculate fitness
def calculate_fitness(chromosome):
    overlaps = count_overlaps(chromosome)
    wiring_distance = calculate_wiring_distance(chromosome)
    bounding_area = calculate_bounding_area(chromosome)

    fitness = -(ALPHA * overlaps + BETA * wiring_distance + GAMMA * bounding_area)
    return fitness, overlaps, wiring_distance, bounding_area

# Function to perform single-point crossover
def single_point_crossover(parent1, parent2):
    split_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:split_point] + parent2[split_point:]
    child2 = parent2[:split_point] + parent1[split_point:]
    return child1, child2

# Function to perform two-point crossover
def two_point_crossover(parent1, parent2):
    point1 = random.randint(1, len(parent1) - 2)
    point2 = random.randint(point1 + 1, len(parent1) - 1)

    child1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
    child2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]
    return child1, child2

# Function to mutate a chromosome
def mutate(chromosome):
    if random.random() < MUTATION_RATE:
        # Pick a random block to mutate
        block_idx = random.randint(0, len(chromosome) - 1)
        block_name = block_names[block_idx]

        # Generate new random position
        new_x = random.randint(0, GRID_SIZE - blocks[block_name]['width'])
        new_y = random.randint(0, GRID_SIZE - blocks[block_name]['height'])

        # Create new chromosome with mutation
        new_chromosome = list(chromosome)
        new_chromosome[block_idx] = (new_x, new_y)
        return new_chromosome
    return chromosome

# Function to print chromosome details
def print_chromosome_details(chromosome, generation, idx):
    fitness, overlaps, wiring, area = calculate_fitness(chromosome)
    print(f"\nGeneration {generation}, Chromosome {idx}:")
    print(f"  Positions: {chromosome}")
    print(f"  Overlaps: {overlaps}")
    print(f"  Wiring Distance: {wiring:.2f}")
    print(f"  Bounding Area: {area}")
    print(f"  Fitness: {fitness:.2f}")

