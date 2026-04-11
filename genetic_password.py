import random
import string
import sys
import time
import os

TARGET = "Python123"
POPULATION_SIZE = 150
MUTATION_RATE = 0.015
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
    messages = [
        "CREATING PRIMORDIAL SOUP...",
        "SPAWNING FIRST GENERATION...",
        "INITIALIZING NATURAL SELECTION...",
        "ACTIVATING EVOLUTION ENGINE..."
    ]
    for msg in messages:
        for frame in frames[:5]:
            sys.stdout.write(f"\r{COLORS['CYAN']}{frame} {msg}{COLORS['RESET']}")
            sys.stdout.flush()
            time.sleep(0.03)
    print("\n")

def print_banner():
    banner = f"""
{COLORS['CYAN']}╔═════════════════════════════════════════════════════════════════════╗
║                                                                     ║
║  {COLORS['GREEN']}▀█▀ █░█ █▀▀   █▀▀ █▀█ █▀█ █▀▀ █▄▀ █▀▀ █▀█{COLORS['CYAN']}                          ║
║  {COLORS['GREEN']}░█░ █▀█ ██▄   █▄▄ █▀▄ █▀█ █▄▄ █░█ ██▄ █▀▄{COLORS['CYAN']}                          ║
║                                                                     ║
║  {COLORS['YELLOW']}██▀ █▀▀ █▄░█ █▀▀ ▀█▀ █ █▀▀   █▀█ █░░ █▀▀ █▀█ █▀█ █ ▀█▀ █░█ █▀▄▀█{COLORS['CYAN']}   ║
║  {COLORS['YELLOW']}█▄█ ██▄ █░▀█ ██▄ ░█░ █ █▄▄   █▀█ █▄▄ █▄█ █▄█ █▀▄ █ ░█░ █▀█ █░▀░█{COLORS['CYAN']}   ║
║                                                                     ║
╚═════════════════════════════════════════════════════════════════════╝{COLORS['RESET']}
"""
    print(banner)

def explain_genetic_process():
    print(f"{COLORS['DIM']}{COLORS['CYAN']}┌────────────────────────── HOW EVOLUTION WORKS ──────────────────────────┐{COLORS['RESET']}")
    print(f"{COLORS['DIM']}{COLORS['CYAN']}│{COLORS['RESET']} {COLORS['GREEN']}1. POPULATION{COLORS['RESET']}   {COLORS['WHITE']}{POPULATION_SIZE} random creatures born with random DNA{COLORS['RESET']}")
    print(f"{COLORS['DIM']}{COLORS['CYAN']}│{COLORS['RESET']} {COLORS['GREEN']}2. FITNESS{COLORS['RESET']}      Each creature tested - how close to the {COLORS['YELLOW']}perfect form{COLORS['RESET']}?")
    print(f"{COLORS['DIM']}{COLORS['CYAN']}│{COLORS['RESET']} {COLORS['GREEN']}3. SELECTION{COLORS['RESET']}    {COLORS['RED']}Weak creatures die{COLORS['RESET']} - only {COLORS['GREEN']}strongest 50%{COLORS['RESET']} survive to breed")
    print(f"{COLORS['DIM']}{COLORS['CYAN']}│{COLORS['RESET']} {COLORS['GREEN']}4. CROSSOVER{COLORS['RESET']}    Parents {COLORS['MAGENTA']}combine DNA{COLORS['RESET']} - children inherit traits from both")
    print(f"{COLORS['DIM']}{COLORS['CYAN']}│{COLORS['RESET']} {COLORS['GREEN']}5. MUTATION{COLORS['RESET']}     {COLORS['BLUE']}Random changes{COLORS['RESET']} in DNA ({MUTATION_RATE*100:.1f}% chance) - adds diversity")
    print(f"{COLORS['DIM']}{COLORS['CYAN']}│{COLORS['RESET']} {COLORS['GREEN']}6. REPEAT{COLORS['RESET']}       New generation is born - {COLORS['BOLD']}survival of the fittest{COLORS['RESET']}")
    print(f"{COLORS['DIM']}{COLORS['CYAN']}└─────────────────────────────────────────────────────────────────────────┘{COLORS['RESET']}")
    print()

def get_generation_commentary(generation, percent, best_fitness, length):
    if generation == 0:
        return f"{COLORS['DIM']}First generation - pure random chance...{COLORS['RESET']}"
    elif percent < 20:
        return f"{COLORS['RED']}Natural selection is brutal - many die, few survive{COLORS['RESET']}"
    elif percent < 40:
        return f"{COLORS['YELLOW']}Evolution taking hold - species adapting{COLORS['RESET']}"
    elif percent < 60:
        return f"{COLORS['CYAN']}Beneficial mutations spreading through population{COLORS['RESET']}"
    elif percent < 80:
        return f"{COLORS['BLUE']}The perfect form emerges from the chaos{COLORS['RESET']}"
    elif percent < 100:
        return f"{COLORS['GREEN']}Almost there - evolution has nearly perfected this species!{COLORS['RESET']}"
    else:
        return f"{COLORS['GREEN']}{COLORS['BOLD']}PERFECTION ACHIEVED - THE PINNACLE OF EVOLUTION!{COLORS['RESET']}"

def main():
    clear_screen()
    print_banner()
    animate_hacking()
    
    length = len(TARGET)
    population = create_population(POPULATION_SIZE, length)
    generation = 0
    best_fitness = 0
    best_individual = ""
    
    print(f"{COLORS['BOLD']}{COLORS['WHITE']}┌─ THE PERFECT FORM (TARGET DNA) ───────────────────────────────┐{COLORS['RESET']}")
    print(f"{COLORS['BOLD']}{COLORS['WHITE']}│{COLORS['RESET']} {COLORS['YELLOW']}Target Sequence:{COLORS['RESET']} {COLORS['GREEN']}{COLORS['BOLD']}{TARGET}{COLORS['RESET']}                                    {COLORS['BOLD']}{COLORS['WHITE']}{COLORS['RESET']}")
    print(f"{COLORS['BOLD']}{COLORS['WHITE']}│{COLORS['RESET']} {COLORS['YELLOW']}DNA Length:{COLORS['RESET']} {length} base pairs                                         {COLORS['BOLD']}{COLORS['WHITE']}{COLORS['RESET']}")
    print(f"{COLORS['BOLD']}{COLORS['WHITE']}│{COLORS['RESET']} {COLORS['YELLOW']}Population Size:{COLORS['RESET']} {POPULATION_SIZE} organisms                                  {COLORS['BOLD']}{COLORS['WHITE']}{COLORS['RESET']}")
    print(f"{COLORS['BOLD']}{COLORS['WHITE']}│{COLORS['RESET']} {COLORS['YELLOW']}Mutation Chance:{COLORS['RESET']} {MUTATION_RATE*100:.1f}% per gene                                {COLORS['BOLD']}{COLORS['WHITE']}{COLORS['RESET']}")
    print(f"{COLORS['BOLD']}{COLORS['WHITE']}└───────────────────────────────────────────────────────────────┘{COLORS['RESET']}")
    print()
    
    explain_genetic_process()
    
    print(f"{COLORS['BOLD']}{COLORS['WHITE']}┌─ EVOLUTION IN PROGRESS ────────────────────────────────────────┐{COLORS['RESET']}")
    print(f"{COLORS['BOLD']}{COLORS['WHITE']}│{COLORS['RESET']} {COLORS['DIM']}Watch as natural selection finds the perfect DNA sequence...{COLORS['RESET']}   {COLORS['BOLD']}{COLORS['WHITE']}│{COLORS['RESET']}")
    print(f"{COLORS['BOLD']}{COLORS['WHITE']}└────────────────────────────────────────────────────────────────┘{COLORS['RESET']}")
    print()
    
    spinner_frames = ["◜", "◠", "◝", "◞", "◡", "◟"]
    spinner_idx = 0
    last_commentary = ""
    
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
        commentary = get_generation_commentary(generation, percent, best_fitness, length)
        
        sys.stdout.write(f"\r{COLORS['CYAN']}{spinner}{COLORS['RESET']} ")
        sys.stdout.write(f"{COLORS['BOLD']}GEN {generation:04d}{COLORS['RESET']} ")
        sys.stdout.write(f"│ {COLORS['MAGENTA']}DNA Match:{COLORS['RESET']} {COLORS['BOLD']}{best_fitness}/{length}{COLORS['RESET']} ")
        sys.stdout.write(f"│ [{bar}] ")
        sys.stdout.write(f"{COLORS['BOLD']}{percent:5.1f}%{COLORS['RESET']} ")
        sys.stdout.write(f"│ {colored_best}")
        sys.stdout.flush()
        
        if commentary != last_commentary:
            print(f"\n  {COLORS['DIM']}└─ {commentary}{COLORS['RESET']}")
            last_commentary = commentary
        
        if TARGET in population:
            print("\n")
            print(f"{COLORS['GREEN']}{COLORS['BOLD']}╔══════════════════════════════════════════════════════════════════╗{COLORS['RESET']}")
            print(f"{COLORS['GREEN']}{COLORS['BOLD']}║                     EVOLUTION COMPLETE                           ║{COLORS['RESET']}")
            print(f"{COLORS['GREEN']}{COLORS['BOLD']}╚══════════════════════════════════════════════════════════════════╝{COLORS['RESET']}")
            print()
            print(f"{COLORS['YELLOW']}  ▶ Generations to perfection:{COLORS['RESET']} {COLORS['BOLD']}{generation}{COLORS['RESET']}")
            print(f"{COLORS['YELLOW']}  ▶ Perfect DNA sequence:{COLORS['RESET']} {COLORS['GREEN']}{COLORS['BOLD']}{best_individual}{COLORS['RESET']}")
            print(f"{COLORS['YELLOW']}  ▶ Organisms that lived/died:{COLORS['RESET']} {COLORS['DIM']}{generation * POPULATION_SIZE}{COLORS['RESET']}")
            print()
            
            if generation < 50:
                efficiency = f"{COLORS['GREEN']}Extremely efficient evolution!{COLORS['RESET']}"
            elif generation < 200:
                efficiency = f"{COLORS['CYAN']}Natural selection working as expected.{COLORS['RESET']}"
            else:
                efficiency = f"{COLORS['YELLOW']}Evolution took its time - but found the way.{COLORS['RESET']}"
            
            print(f"{COLORS['CYAN']}  ═══════════════════════════════════════════════════════════════{COLORS['RESET']}")
            print(f"  {efficiency}")
            print(f"  {COLORS['DIM']}This is how nature solves complex problems - through countless{COLORS['RESET']}")
            print(f"  {COLORS['DIM']}generations of trial, error, and survival of the fittest.{COLORS['RESET']}")
            print()
            break
        
        population = evolve(population)
        generation += 1
        time.sleep(0.15)

if __name__ == "__main__":
    main()