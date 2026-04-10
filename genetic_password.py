import random
import string
import sys
import time
import os

TARGET = "Python123456789."
POPULATION_SIZE = 200
MUTATION_RATE = 0.02
ELITE_SIZE = 2

CHARSET = string.ascii_letters + string.digits + string.punctuation

COLORS = {
    'RED': '\033[91m',
    'GREEN': '\033[92m',
    'YELLOW': '\033[93m',
    'BLUE': '\033[94m',
    'MAGENTA': '\033[95m',
    'CYAN': '\033[96m',
    'WHITE': '\033[97m',
    'RESET': '\033[0m',
    'BOLD': '\033[1m',
    'DIM': '\033[2m'
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def random_char():
    return random.choice(CHARSET)

def create_individual(length):
    return ''.join(random_char() for _ in range(length))

def create_population(size, length):
    return [create_individual(length) for _ in range(size)]

def fitness(individual):
    return sum(1 for a, b in zip(individual, TARGET) if a == b)

def select_parents(population, fitnesses):
    paired = list(zip(population, fitnesses))
    paired.sort(key=lambda x: x[1], reverse=True)
    cutoff = max(2, len(population) // 2)
    selected = [ind for ind, fit in paired[:cutoff]]
    return selected

def crossover(parent1, parent2):
    if len(parent1) < 2:
        return parent1, parent2
    point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

def mutate(individual):
    individual = list(individual)
    for i in range(len(individual)):
        if random.random() < MUTATION_RATE:
            individual[i] = random_char()
    return ''.join(individual)

def evolve(population):
    fitnesses = [fitness(ind) for ind in population]
    parents = select_parents(population, fitnesses)
    elite = sorted(zip(population, fitnesses), key=lambda x: x[1], reverse=True)[:ELITE_SIZE]
    elite_individuals = [ind for ind, _ in elite]
    next_population = elite_individuals.copy()
    while len(next_population) < POPULATION_SIZE:
        p1, p2 = random.sample(parents, 2)
        c1, c2 = crossover(p1, p2)
        next_population.append(mutate(c1))
        if len(next_population) < POPULATION_SIZE:
            next_population.append(mutate(c2))
    return next_population

def colorize_password(guess, target):
    result = ""
    for g, t in zip(guess, target):
        if g == t:
            result += f"{COLORS['GREEN']}{COLORS['BOLD']}{g}{COLORS['RESET']}"
        else:
            result += f"{COLORS['RED']}{COLORS['DIM']}{g}{COLORS['RESET']}"
    return result

def animate_hacking():
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    for _ in range(3):
        for frame in frames:
            sys.stdout.write(f"\r{COLORS['CYAN']}{frame} INITIALIZING GENETIC ALGORITHM...{COLORS['RESET']}")
            sys.stdout.flush()
            time.sleep(0.05)

def print_banner():
    banner = f"""
{COLORS['CYAN']}╔═════════════════════════════════════════════════════════════════════╗
║                                                                     ║
║  {COLORS['GREEN']}▀█▀ █░█ █▀▀   █▀▀ █░█ █▀█ █▄░█ █▀▀ █▀█ █▀▀ █▄▀ █▀▀ █▀█{COLORS['CYAN']}             ║
║  {COLORS['GREEN']}░█░ █▀█ ██▄   █▄▄ █▀█ █▀▄ █░▀█ ██▄ █▀▄ █▄▄ █░█ ██▄ █▀▄{COLORS['CYAN']}             ║
║                                                                     ║
║  {COLORS['YELLOW']}██▀ █▀▀ █▄░█ █▀▀ ▀█▀ █ █▀▀   █▀█ █░░ █▀▀ █▀█ █▀█ █ ▀█▀ █░█ █▀▄▀█{COLORS['CYAN']}   ║
║  {COLORS['YELLOW']}█▄█ ██▄ █░▀█ ██▄ ░█░ █ █▄▄   █▀█ █▄▄ █▄█ █▄█ █▀▄ █ ░█░ █▀█ █░▀░█{COLORS['CYAN']}   ║
║                                                                     ║
╚═════════════════════════════════════════════════════════════════════╝{COLORS['RESET']}
"""
    print(banner)

def main():
    clear_screen()
    print_banner()
    animate_hacking()
    print("\n")
    length = len(TARGET)
    population = create_population(POPULATION_SIZE, length)
    generation = 0
    best_fitness = 0
    best_individual = ""
    
    print(f"{COLORS['BOLD']}{COLORS['WHITE']}┌─ TARGET CONFIGURATION ─────────────────────────────────────┐{COLORS['RESET']}")
    print(f"{COLORS['BOLD']}{COLORS['WHITE']}│{COLORS['RESET']} {COLORS['YELLOW']}Target Password:{COLORS['RESET']} {COLORS['GREEN']}{COLORS['BOLD']}{TARGET}{COLORS['RESET']}")
    print(f"{COLORS['BOLD']}{COLORS['WHITE']}│{COLORS['RESET']} {COLORS['YELLOW']}Length:{COLORS['RESET']} {length} chars")
    print(f"{COLORS['BOLD']}{COLORS['WHITE']}│{COLORS['RESET']} {COLORS['YELLOW']}Population:{COLORS['RESET']} {POPULATION_SIZE} individuals")
    print(f"{COLORS['BOLD']}{COLORS['WHITE']}│{COLORS['RESET']} {COLORS['YELLOW']}Mutation Rate:{COLORS['RESET']} {MUTATION_RATE*100:.1f}%")
    print(f"{COLORS['BOLD']}{COLORS['WHITE']}└────────────────────────────────────────────────────────────┘{COLORS['RESET']}")
    print()
    
    spinner_frames = ["◜", "◠", "◝", "◞", "◡", "◟"]
    spinner_idx = 0
    
    while True:
        fitnesses = [fitness(ind) for ind in population]
        max_fit = max(fitnesses)
        best_idx = fitnesses.index(max_fit)
        current_best = population[best_idx]
        
        if max_fit > best_fitness:
            best_fitness = max_fit
            best_individual = current_best
        
        percent = (best_fitness / length) * 100
        bar_length = 40
        filled = int(bar_length * best_fitness // length)
        
        if percent < 30:
            bar_color = COLORS['RED']
        elif percent < 70:
            bar_color = COLORS['YELLOW']
        else:
            bar_color = COLORS['GREEN']
        
        bar = f"{bar_color}{'█' * filled}{COLORS['DIM']}{'░' * (bar_length - filled)}{COLORS['RESET']}"
        
        spinner = spinner_frames[spinner_idx % len(spinner_frames)]
        spinner_idx += 1
        
        colored_best = colorize_password(best_individual, TARGET)
        
        sys.stdout.write(f"\r{COLORS['CYAN']}{spinner}{COLORS['RESET']} ")
        sys.stdout.write(f"{COLORS['BOLD']}GEN {generation:04d}{COLORS['RESET']} ")
        sys.stdout.write(f"│ {COLORS['MAGENTA']}Fitness:{COLORS['RESET']} {COLORS['BOLD']}{best_fitness}/{length}{COLORS['RESET']} ")
        sys.stdout.write(f"│ [{bar}] ")
        sys.stdout.write(f"{COLORS['BOLD']}{percent:5.1f}%{COLORS['RESET']} ")
        sys.stdout.write(f"│ {colored_best}")
        sys.stdout.flush()
        
        if TARGET in population:
            print("\n\n")
            print(f"{COLORS['GREEN']}{COLORS['BOLD']}╔════════════════════════════════════════════════════════════╗{COLORS['RESET']}")
            print(f"{COLORS['GREEN']}{COLORS['BOLD']}║                     PASSWORD CRACKED !                     ║{COLORS['RESET']}")
            print(f"{COLORS['GREEN']}{COLORS['BOLD']}╚════════════════════════════════════════════════════════════╝{COLORS['RESET']}")
            print()
            print(f"{COLORS['YELLOW']}  ▶ Generation:{COLORS['RESET']} {COLORS['BOLD']}{generation}{COLORS['RESET']}")
            print(f"{COLORS['YELLOW']}  ▶ Password:{COLORS['RESET']}   {COLORS['GREEN']}{COLORS['BOLD']}{best_individual}{COLORS['RESET']}")
            print(f"{COLORS['YELLOW']}  ▶ Time:{COLORS['RESET']}       {COLORS['DIM']}{time.strftime('%H:%M:%S')}{COLORS['RESET']}")
            print()
            print(f"{COLORS['CYAN']}  ═══════════════════════════════════════════════════════════{COLORS['RESET']}")
            print(f"{COLORS['DIM']}  Evolution complete. Access granted.{COLORS['RESET']}")
            print()
            break
        
        population = evolve(population)
        generation += 1
        time.sleep(0.2)

if __name__ == "__main__":
    main()