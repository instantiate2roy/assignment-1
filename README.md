# OOP with Python: Assignment 1 mini-projects

Mini-projects from Assignment 1 (Advent 2026). Each one has its own notebook, with the reusable classes in `src/` and pytest tests in `tests/`.

| Notebook | Mini-project |
|---|---|
| `project1_population.ipynb` | 1. District population forecaster: forecasts five Ugandan districts to 2029 and estimates the primary-school classrooms each one needs |
| `project2_solar.ipynb` | 2. Solar micro-grid dispatch planner: splits a health centre's daily energy demand between solar panels and batteries |

## Setup

You need Python 3.10 or newer.

```bash
git clone https://github.com/instantiate2roy/assignment-1.git
cd assignment-1
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## How to run

Open each notebook from the project folder, so that `src` can be imported:

```bash
jupyter notebook project1_population.ipynb
jupyter notebook project2_solar.ipynb
```

Then choose **Kernel > Restart Kernel and Run All Cells**.

- **Mini-project 1** prints each table and saves the forecast figure as `district_forecasts.png`.
- **Mini-project 2** stops at the interactive input cell and asks for a daytime load and a critical-equipment load in kWh. It then writes 30 days of demand data to `files/solar_data.csv`, and a second file with deliberately bad days to `files/solar_bad_data.csv`.

Mini-project 1 uses no random numbers. Mini-project 2 generates its demand data with a fixed seed (36), so every run writes the same CSV files and gives the same results. Only the benchmark timings change from one machine to another.

To run the tests:

```bash
pytest
```

## Project structure

| Path | Contents |
|---|---|
| `project1_population.ipynb` | Mini-project 1: statistics, growth rates, model comparison, forecasts, variance, figure, classroom planning, findings |
| `project2_solar.ipynb` | Mini-project 2: determinant and condition number, interactive input, CSV generation, loop and vectorised solving, infeasible days, usage statistics, cost model, usage and cost chart |
| `src/district_population.py` | `DistrictPopulation`: statistics, growth rates, predictions and error metrics for one district |
| `src/forecaster.py` | `Forecaster`: abstract base class for the forecasting models |
| `src/linear.py`, `src/cagr.py`, `src/fibonacci_ratio.py` | The three forecasting models |
| `src/plots.py` | Actual, fitted and forecast figure for every district |
| `src/planning.py` | `ClassroomPlanner`: classroom estimates from population |
| `src/microgrid.py` | `MicroGrid`: the two demand equations, their determinant and condition number, and the solver |
| `src/csv_generator.py` | `CsvGenerator`: seeded 30-day demand data with a weekly pattern and noise, optionally with bad days |
| `src/validate.py` | Input validation for both mini-projects |
| `files/` | CSV files written by mini-project 2 |
| `tests/` | pytest tests for both mini-projects, including invalid-input edge cases |

## Findings

### Mini-project 1: District population forecaster

- **Growth:** Wakiso grows fastest, with a 2015–24 CAGR of 6.5%. Kabale grows slowest, at 3.7%.
- **Model accuracy:** CAGR was the most accurate model on the 2022–24 test years for Kampala, Wakiso, Gulu and Kabale, and Linear for Masindi. The Fibonacci ratio model was the least accurate everywhere, with a MAPE of 53% to 66%.
- **2029 forecast:** Wakiso overtakes Kampala in 2029, at 2,285 thousand against 2,255 thousand.
- **Classrooms:** the five districts need 4,878 more primary-school classrooms by 2029, led by Wakiso (2,088) and Kampala (1,544). This assumes 18% of the population is of primary-school age, 53 pupils per classroom, and existing classrooms that exactly meet 2024 need.
- **Main limitation:** each forecast rests on ten years of data and assumes a constant trend. Kabale's growth has slowed, so its forecast and classroom figure are likely too high.

Population figures are in thousands. The full findings and limitations are at the end of the notebook.

### Mini-project 2: Solar micro-grid dispatch planner

- **Well-posed system:** the determinant is −5 and the condition number is 5.83. The two demand equations therefore always have exactly one solution, and a 1% error in a demand reading changes the solar or battery figure by at most about 5.8%.
- **Speed:** solving all 30 days in one vectorised call was about 30 times faster than solving them one at a time in a loop (0.005 ms against 0.16 ms per run, averaged over 5,000 runs).
- **Infeasible days:** in the file with deliberately bad data, 3 of the 30 days have a negative load reading and are rejected as invalid input. Another 3 days would need negative solar or battery output, so they are solved with non-negative least squares instead. That gives the closest supply to demand that uses no negative output, and it comes closer than simply setting the negative value to zero.
- **Volatility:** the battery's daily output varies more in kWh (standard deviation 5.45 kWh against 2.63 kWh for solar), but solar varies more relative to its size (coefficient of variation 0.35 against 0.15). Relative to what each source supplies, solar is the more volatile one.
- **Cost:** over the 30 days the clinic draws 1,298 kWh, 82% of it from the battery, for a total of UGX 515,723, or UGX 17,191 a day on average. The battery makes up 93% of the bill because it costs three times as much per kWh as solar. The two daily loads fix how much each source must supply, so lowering the bill needs a change to the system, such as more solar panels.

## AI-use declaration

I used AI tools while working on this project:

- **ChatGPT (OpenAI):** explanations of Python concepts, including `.gitkeep` files, dunder methods, return type hints and docstrings, and a check of the CAGR formula.
- **Claude (Anthropic):**
  - Mini-project 1: writing the forecast figure (`src/plots.py`), the `fitted()` methods, `ClassroomPlanner` (`src/planning.py`), the tests, the corrected loop and table in the best-model forecast cell, and the variance comparison cell. Explaining the errors I hit (import paths, autoreload, statistics results losing their decimals, a validation object shared between cells) and reviewing the project against the brief. Fixing bugs, including the relative imports in `src/`, the missing brackets in `Linear().fit`, the standard deviation mismatch, first-year growth, length checks, detached docstrings and type hints. Drafting parts of the notebook's markdown.
  - Mini-project 2: writing the tests in `tests/test_microgrid.py`.
  - Both: drafting this README and updating `requirements.txt`.

I wrote the original code and analysis. I reviewed all AI-generated code and text, ran the notebook and tests myself, and corrected errors in the AI output, such as the rounding explanation and missing axis labels.
