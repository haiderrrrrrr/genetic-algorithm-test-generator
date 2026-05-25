# Genetic Algorithm Test Generator

A Python tool that uses genetic algorithms to generate and evolve date-validation test cases. It runs candidate dates through selection, crossover, and mutation to maximize category coverage, then refines the result with a local search pass.

## Features

- Generates date-validation test cases with a genetic algorithm.
- Supports seeded and non-seeded population strategies.
- Uses frequency-based fitness scoring to reward rare and uncovered categories.
- Applies local search after the GA phase to improve final coverage.
- Covers 21 valid, boundary, and invalid date categories.
- Exports evolved test cases to CSV.
- Prints coverage progress in the terminal.
- Plots GA and local-search coverage with Matplotlib.

## How It Works

| Phase | Description |
| --- | --- |
| Initialization | Builds a population of `(day, month, year)` candidates |
| Fitness | Scores candidates by category rarity and coverage value |
| Selection | Uses rank-based selection to preserve stronger candidates |
| Crossover | Swaps month and year genes between parent pairs |
| Mutation | Applies small random changes to candidate dates |
| Injection | Adds random dates during evolution to keep population diversity |
| Local Search | Refines the best population after GA convergence |
| Export | Writes the final sorted test cases to CSV |

## Date Categories

The generator targets 21 categories across boundary, valid, and invalid dates.

```text
Boundary - 01/01/0000, 31/12/9999, 29/02/2020, 28/02/1900, 31/01/0000
Valid    - 31-day month, 30-day month, 28-day Feb, 29-day Feb (leap), other
Invalid  - day < 1, day > 31, month < 1, month > 12, year out of range,
           exceeded month length, exceeded February rules, and other invalid dates
```

## Project Structure

```text
.
|-- seeded_genetic_algorithm_date_tests.py       # Boundary-seeded GA run
|-- non_seeded_genetic_algorithm_date_tests.py   # Fully random GA run
|-- requirements.txt                             # Python dependencies
|-- sample_output/
|   `-- seeded_evolved_test_cases.csv            # Example CSV output
`-- README.md
```

## Tech Stack

| Part | Tech |
| --- | --- |
| Language | Python |
| Algorithm | Genetic Algorithm + Local Search |
| Plotting | Matplotlib |
| Output | CSV |
| Domain | Search-Based Software Testing |

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Locally

Run the seeded version:

```bash
python seeded_genetic_algorithm_date_tests.py
```

Run the non-seeded version:

```bash
python non_seeded_genetic_algorithm_date_tests.py
```

Both scripts will:

1. Print generation-by-generation coverage.
2. Run a local search refinement pass.
3. Print the top evolved test cases with fitness scores.
4. Export the final evolved test suite to CSV.
5. Display a Matplotlib coverage chart.

## Sample Output

Terminal:

```text
Generation   0 => Coverage: 38.10%
Generation   1 => Coverage: 61.90%
Generation   2 => Coverage: 76.19%
Generation   3 => Coverage: 90.48%
Generation   4 => Coverage: 95.24%

Stopped at generation 5 with coverage: 100.00%

Top 15 Evolved Test Cases:
 1. 01/01/0000 => Boundary: 01/01/0000 (fitness=10.500)
 2. 31/12/9999 => Boundary: 31/12/9999 (fitness=10.500)
 3. 29/02/2020 => Boundary: 29/02/2020 (fitness=10.500)
```

CSV:

```text
Date,Category,Fitness
01/01/0000,Boundary: 01/01/0000,10.500
31/12/9999,Boundary: 31/12/9999,10.500
29/02/2020,Boundary: 29/02/2020,10.500
31/01/2023,Valid: 31-day Month,10.250
00/06/2021,Invalid: Day < 1,10.333
```

See [sample_output/seeded_evolved_test_cases.csv](sample_output/seeded_evolved_test_cases.csv) for a full example.

## Configuration

Both scripts expose tuning values inside `run_genetic_algorithm()` and `local_search()`.

| Parameter | Seeded Default | Non-Seeded Default | Description |
| --- | --- | --- | --- |
| `pop_size` | 500 | 500 | Number of individuals per generation |
| `coverage_target` | 0.95 | 0.97 | Stop GA when this coverage ratio is reached |
| `max_generations` | 1000 | 100 | Hard cap on GA iterations |
| `iterations` | 500 | 1000 | Local search refinement steps |

## Seeded vs Non-Seeded

| | Seeded | Non-Seeded |
| --- | --- | --- |
| Starting population | Random dates plus known boundaries | Fully random dates |
| Fitness bonus | Rewards rare categories | Rewards rare categories more aggressively |
| Coverage target | 95% | 97% |
| Convergence speed | Faster | Slower |
| Use case | Boundary-aware testing | Black-box discovery |
