import random
import csv
import os
import matplotlib.pyplot as plt

# ANSI For Styling Display
RESET   = "\033[0m"
BOLD    = "\033[1m"
DIM     = "\033[2m"
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
RED     = "\033[91m"
CYAN    = "\033[96m"
MAGENTA = "\033[95m"
BLUE    = "\033[94m"
PARTY   = "\U0001F389"
SEARCH  = "\U0001F50E"

# All Categories
ALL_CATEGORIES = {
    "Valid: 31-day Month",
    "Valid: 30-day Month",
    "Valid: 28-day Feb (Non-Leap)",
    "Valid: 29-day Feb (Leap)",
    "Valid: Other",

    "Boundary: 01/01/0000",
    "Boundary: 31/12/9999",
    "Boundary: 29/02/2020",
    "Boundary: 28/02/1900",  
    "Boundary: 31/01/0000",  

    "Invalid: Day < 1",
    "Invalid: Day > 31",
    "Invalid: Month < 1",
    "Invalid: Month > 12",
    "Invalid: Year < 0",
    "Invalid: Year > 9999",
    "Invalid: 30-day Month Exceeded",
    "Invalid: 31-day Month Exceeded",
    "Invalid: Feb > 28 in Non-Leap",
    "Invalid: Feb > 29 in Leap",
    "Invalid: Other"
}

# Data Validation and Categorization
def is_leap_year(year):
    return (year % 400 == 0) or (year % 4 == 0 and year % 100 != 0)

def days_in_month(month, year):
    if month < 1 or month > 12:
        return 0
    if month == 2:
        return 29 if is_leap_year(year) else 28
    elif month in [4, 6, 9, 11]:
        return 30
    else:
        return 31

def is_valid_date(day, month, year):
    if not (0 <= year <= 9999): 
        return False
    if not (1 <= month <= 12): 
        return False
    return (1 <= day <= days_in_month(month, year))

def categorize_date(day, month, year):
    # Boundaries
    if day == 1 and month == 1 and year == 0:
        return "Boundary: 01/01/0000" if is_valid_date(day, month, year) else "Invalid: Other"
    if day == 31 and month == 12 and year == 9999:
        return "Boundary: 31/12/9999" if is_valid_date(day, month, year) else "Invalid: Other"
    if day == 29 and month == 2 and year == 2020:
        return "Boundary: 29/02/2020" if is_valid_date(day, month, year) else "Invalid: Other"
    if day == 28 and month == 2 and year == 1900:
        return "Boundary: 28/02/1900" if is_valid_date(day, month, year) else "Invalid: Other"
    if day == 31 and month == 1 and year == 0:
        return "Boundary: 31/01/0000" if is_valid_date(day, month, year) else "Invalid: Other"
    # Invalid
    if year < 0:
        return "Invalid: Year < 0"
    if year > 9999:
        return "Invalid: Year > 9999"
    if month < 1:
        return "Invalid: Month < 1"
    if month > 12:
        return "Invalid: Month > 12"
    if day < 1:
        return "Invalid: Day < 1"
    if day > 31:
        return "Invalid: Day > 31"
    dmax = days_in_month(month, year)
    if day > dmax:
        if month in [4, 6, 9, 11] and day == 31:
            return "Invalid: 30-day Month Exceeded"
        if month in [1, 3, 5, 7, 8, 10, 12] and day == 32:
            return "Invalid: 31-day Month Exceeded"
        if month == 2 and not is_leap_year(year) and day == 29:
            return "Invalid: Feb > 28 in Non-Leap"
        if month == 2 and is_leap_year(year) and day > 29:
            return "Invalid: Feb > 29 in Leap"
        return "Invalid: Other"
    # Valid
    if month == 2 and is_leap_year(year) and day == 29:
        return "Valid: 29-day Feb (Leap)"
    if month == 2 and not is_leap_year(year) and day == 28:
        return "Valid: 28-day Feb (Non-Leap)"
    if day == 31 and month in [1, 3, 5, 7, 8, 10, 12]:
        return "Valid: 31-day Month"
    if day == 30 and month in [4, 6, 9, 11]:
        return "Valid: 30-day Month"
    return "Valid: Other"

# Fitness Function
def compute_population_fitness(pop):
    cat_count = {}
    for c in pop:
        cat = categorize_date(*c)
        cat_count[cat] = cat_count.get(cat, 0) + 1

    fits = []
    for c in pop:
        cat = categorize_date(*c)
        freq = cat_count[cat]
        score = 1.0 / freq
        if freq < 2:
            score += 15.0
        fits.append(score)
    return fits

# Rank-Based Selection
def rank_based_selection(pop, fits):
    paired = list(zip(pop, fits))
    paired.sort(key=lambda x: x[1], reverse=True)
    n = len(paired)
    total_rank = n * (n + 1) / 2.0
    cprobs, run = [], 0.0
    for i, (_, fitv) in enumerate(paired):
        rank = i + 1
        run += (n - rank + 1) / total_rank
        cprobs.append(run)

    new_pop = []
    for _ in range(n):
        r = random.random()
        for i, cp in enumerate(cprobs):
            if r <= cp:
                new_pop.append(paired[i][0])
                break
    return new_pop

# Crossover and Mutation
def crossover(pop, rate=0.9):
    random.shuffle(pop)
    kids = []
    for i in range(0, len(pop), 2):
        if i+1 >= len(pop):
            kids.append(pop[i])
            break
        p1, p2 = pop[i], pop[i+1]
        if random.random() < rate:
            d1,m1,y1 = p1; d2,m2,y2 = p2
            kids += [(d1,m2,y2), (d2,m1,y1)]
        else:
            kids += [p1, p2]
    return kids

def mutate(pop, rate=0.2):
    mutated = []
    for d,m,y in pop:
        if random.random() < rate: d += random.randint(-3,3)
        if random.random() < rate: m += random.randint(-1,1)
        if random.random() < rate: y += random.randint(-100,100)
        mutated.append((d,m,y))
    return mutated

# Coverage
def get_population_coverage(pop):
    cats = set(categorize_date(*c) for c in pop)
    return len(cats) / len(ALL_CATEGORIES), cats

# Local Search
def local_search(pop, iterations=1000):
    best_pop = pop[:]
    best_fit = compute_population_fitness(best_pop)
    best_cov, _ = get_population_coverage(best_pop)
    coverage_ls = []

    for _ in range(iterations):
        coverage_ls.append(best_cov)
        idx = random.randrange(len(best_pop))
        d,m,y = best_pop[idx]
        gene = random.choice(["day","month","year"])
        if gene=="day":   d += random.randint(-1,1)
        elif gene=="month": m += random.randint(-1,1)
        else:             y += random.randint(-10,10)

        candidate = best_pop[:]
        candidate[idx] = (d,m,y)
        c_fit = compute_population_fitness(candidate)
        c_cov, _ = get_population_coverage(candidate)

        if c_cov > best_cov or sum(c_fit)/len(c_fit) > sum(best_fit)/len(best_fit):
            best_pop, best_fit, best_cov = candidate, c_fit, c_cov

    coverage_ls.append(best_cov)
    return best_pop, coverage_ls

# GA Routine
def run_genetic_algorithm(pop_size=500, coverage_target=0.97, max_generations=100):
    def random_date():
        return (
            random.randint(-5, 40),
            random.randint(-2, 14),
            random.randint(-100, 11000)
        )

    boundary_pool = [
        (1,1,0), (31,12,9999), (29,2,2020),
        (28,2,1900), (31,1,0)
    ]

    pop = [random_date() for _ in range(pop_size)]
    coverage_timeline = []
    coverage, _ = get_population_coverage(pop)
    gen = 0

    while coverage < coverage_target and gen < max_generations:
        fit_scores = compute_population_fitness(pop)
        coverage_timeline.append(coverage)

        color = GREEN if coverage>=0.7 else (YELLOW if coverage>=0.4 else RED)
        print(f"{CYAN}Generation {gen:3d}{RESET} => Coverage: {color}{coverage*100:.2f}%{RESET}")

        selected = rank_based_selection(pop, fit_scores)
        crossed  = crossover(selected, 0.9)
        mutated  = mutate(crossed, 0.2)

        # random injection
        inj = int(pop_size * 0.3)
        for i in range(inj):
            mutated[-(i+1)] = random_date()

        # keep boundary cases
        for i, bc in enumerate(boundary_pool):
            if i < len(mutated):
                mutated[i] = bc

        pop = mutated
        coverage, _ = get_population_coverage(pop)
        gen += 1

    coverage_timeline.append(coverage)
    print(f"\n{MAGENTA}{BOLD}Stopped at generation {gen} with coverage: {coverage*100:.2f}%{PARTY}{RESET}")

    sorted_pop = sorted(
        zip(pop, compute_population_fitness(pop)),
        key=lambda x: x[1], reverse=True
    )
    return pop, sorted_pop, coverage_timeline

# Main
def format_date(d,m,y):
    return f"{d:02d}/{m:02d}/{y:04d}"

def main():
    print(f"{BOLD}{RED}{'Genetic Algorithm'.center(60)}{RESET}\n")
    print(f"{BOLD}{BLUE}Starting Genetic Algorithm for Date Validation Test Cases (Non-Seeded){RESET}\n")

    # Run GA with max_generations=100
    final_pop, fit_by_chrom, coverage_timeline = run_genetic_algorithm(
        pop_size=500,
        coverage_target=0.97,
        max_generations=100
    )

    baseline_cov = coverage_timeline[-1]
    print(f"{BOLD}{BLUE}\n[Local Search]{RESET} Refining from baseline coverage {baseline_cov*100:.2f}% {SEARCH}\n")

    improved_pop, local_search_coverage = local_search(
        [p for (p,_) in fit_by_chrom], iterations=1000
    )
    improved_cov, _ = get_population_coverage(improved_pop)

    if improved_cov > baseline_cov:
        print(f"{GREEN}Coverage improved from {baseline_cov*100:.2f}% to {improved_cov*100:.2f}%!{RESET} {PARTY}")
        final_pop = improved_pop
    else:
        print(f"{YELLOW}No improvement; coverage remains {baseline_cov*100:.2f}%.{RESET}")

    final_fitness = compute_population_fitness(final_pop)
    final_sorted  = sorted(zip(final_pop, final_fitness), key=lambda x: x[1], reverse=True)

    # Print results...
    print(f"{BOLD}{GREEN}\nTop 15 Evolved Test Cases:{RESET}")
    for i, (c, s) in enumerate(final_sorted[:15]):
        d,m,y = c
        print(f"{i+1:2d}. {format_date(d,m,y)} => {categorize_date(d,m,y)} {DIM}(fitness={s:.3f}){RESET}")

    # categorize and print boundary/valid/invalid slices
    boundary_cases = [(c,cat,s) for (c,s) in final_sorted if (cat:=categorize_date(*c)).startswith("Boundary")][:5]
    valid_cases    = [(c,cat,s) for (c,s) in final_sorted if (cat:=categorize_date(*c)).startswith("Valid")][:10]
    invalid_cases  = [(c,cat,s) for (c,s) in final_sorted if (cat:=categorize_date(*c)).startswith("Invalid")][:10]

    print(f"{BOLD}{BLUE}\nTop 5 Boundary Cases:{RESET}")
    for i,(c,cat,s) in enumerate(boundary_cases,1):
        print(f" {i}. {format_date(*c)} => {cat} {DIM}(fitness={s:.3f}){RESET}")

    print(f"{BOLD}{GREEN}\nTop 10 Valid Cases:{RESET}")
    for i,(c,cat,s) in enumerate(valid_cases,1):
        print(f" {i}. {format_date(*c)} => {cat} {DIM}(fitness={s:.3f}){RESET}")

    print(f"{BOLD}{RED}\nTop 10 Invalid Cases:{RESET}")
    for i,(c,cat,s) in enumerate(invalid_cases,1):
        print(f" {i}. {format_date(*c)} => {cat} {DIM}(fitness={s:.3f}){RESET}")

    # Export CSV
    csv_filename = "nonseeded_final_evolved_test_cases.csv"
    with open(csv_filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Date","Category","Fitness"])
        for c,s in final_sorted:
            writer.writerow([format_date(*c), categorize_date(*c), f"{s:.3f}"])
    print(f"\n{BLUE}{BOLD}Exported final test cases to: {os.path.abspath(csv_filename)}{RESET}\n")

    # Plot coverage
    plt.figure(figsize=(10,6))
    plt.plot(range(len(coverage_timeline)), coverage_timeline, marker='.', linestyle='-', label="GA Coverage")
    plt.plot(range(len(local_search_coverage)), local_search_coverage, marker='.', linestyle='-', label="Local Search Coverage")
    plt.xlabel("Generation / Iteration")
    plt.ylabel("Coverage (fraction)")
    plt.title("Coverage Over Generations and Local Search")
    plt.grid(True)
    plt.xlim([0, 100])
    plt.legend()
    plt.show()

    print(f"{BOLD}{BLUE}Process completed successfully!{RESET} {PARTY}")

if __name__ == "__main__":
    main()
