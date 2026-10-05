# OOP with Python: Assignment 1 mini-projects

Mini-projects from Assignment 1 (Advent 2026). Each one has its own notebook, with the reusable classes in `src/` and pytest tests in `tests/`.

| Notebook | Mini-project |
|---|---|
| `project1_population.ipynb` | 1. District population forecaster: forecasts five Ugandan districts to 2029 and estimates the primary-school classrooms each one needs |
| `project2_solar.ipynb` | 2. Solar micro-grid dispatch planner: splits a health centre's daily energy demand between solar panels and batteries |
| `project3_fish_stock.ipynb` | 3. Lake Victoria fish stock and export risk model: tests whether a harvesting rate is sustainable and how risky the revenue is |
| `project4_rainfall_pattern.ipynb` | 4. Rainfall pattern and crop suitability analyser: compares rainfall in Kampala, Gulu and Mbarara and advises which months suit which crops |
| `project5_taxi_route.ipynb` | 5. Taxi route revenue, pricing and fleet planner: forecasts demand on three matatu routes out of Kampala and sizes each route's fleet |

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
jupyter notebook project3_fish_stock.ipynb
jupyter notebook project4_rainfall_pattern.ipynb
jupyter notebook project5_taxi_route.ipynb
```

Then choose **Kernel > Restart Kernel and Run All Cells**.

- **Mini-project 1** prints each table and saves the forecast figure as `district_forecasts.png`.
- **Mini-project 2** stops at the interactive input cell and asks for a daytime load and a critical-equipment load in kWh. It then writes 30 days of demand data to `files/solar_data.csv`, and a second file with deliberately bad days to `files/solar_bad_data.csv`.
- **Mini-project 3** prints each table and draws the stock trajectories and the revenue histogram. The Monte Carlo cells simulate 1,000 price paths each and take a few seconds.
- **Mini-project 4** prints the statistics, crop classification and similarity tables, and draws the rainfall line chart and the crop suitability heatmap. Its extension downloads 2016–2025 monthly rainfall from the NASA POWER API and saves it to `files/<region>_rain_data.csv`, so it needs an internet connection.
- **Mini-project 5** prints the revenue, equilibrium, backtesting, forecast and fleet tables, and draws the day 11 forecast and the 60-day seasonal comparison.

Mini-project 1 uses no random numbers. Mini-project 2 generates its demand data with a fixed seed (36), and its sensitivity analysis uses numpy's generator with a fixed seed (42), so every run writes the same CSV files and gives the same results. Mini-project 3 seeds every price path (seed 50 for the single path, seeds 0 to 999 for the Monte Carlo paths), so it also gives the same results every run. Mini-project 4 uses no random numbers. Mini-project 5 simulates its 60 days with numpy's generator and a fixed seed (42). Only the benchmark timings change from one machine to another.

To run the tests:

```bash
pytest
```

## Project structure

| Path | Contents |
|---|---|
| `project1_population.ipynb` | Mini-project 1: statistics, growth rates, model comparison, forecasts, variance, figure, classroom planning, findings |
| `project2_solar.ipynb` | Mini-project 2: determinant and condition number, interactive input, CSV generation, loop and vectorised solving, infeasible days, usage statistics, cost model, usage and cost chart, and both extensions (diesel generator, sensitivity analysis) |
| `project3_fish_stock.ipynb` | Mini-project 3: Fibonacci baseline, logistic growth model, price model, revenue statistics, risk classification and VaR, harvest-rate scenarios, charts, and the closed-season extension |
| `project4_rainfall_pattern.ipynb` | Mini-project 4: region statistics, crop classification, cosine similarity checked against scipy, similarity and distance matrices, rainy-season detection, line chart, heatmap, advisory note for Mbarara farmers, findings and limitations, and the NASA POWER extension with box plots per month |
| `project5_taxi_route.ipynb` | Mini-project 5: route revenue statistics, supply and demand equilibrium, walk-forward backtesting with a tuned α, day 11 forecast, fleet planning, and the 60-day seasonal extension |
| `src/district_population.py` | `DistrictPopulation`: statistics, growth rates, predictions and error metrics for one district |
| `src/forecaster.py` | `Forecaster`: abstract base class for the forecasting models |
| `src/linear.py`, `src/cagr.py`, `src/fibonacci_ratio.py` | The three forecasting models |
| `src/plots.py` | Actual, fitted and forecast figure for every district |
| `src/planning.py` | `ClassroomPlanner`: classroom estimates from population |
| `src/microgrid.py` | `MicroGrid`: the two demand equations, their determinant and condition number, and the solver |
| `src/hybrid_microgrid.py` | `HybridMicroGrid`: a `MicroGrid` subclass that adds a diesel generator and a night-time load (3×3 system) |
| `src/sensitivity.py` | `SensitivityAnalysis`: Monte Carlo test of how ±5% errors in the demand readings move the dispatch |
| `src/csv_generator.py` | `CsvGenerator`: seeded 30-day demand data with a weekly pattern and noise, optionally with bad days |
| `src/fish_stock.py` | `FishStock`: logistic growth with harvesting, plus the Fibonacci baseline |
| `src/closed_season_fish_stock.py` | `ClosedSeasonFishStock`: a `FishStock` subclass with no harvesting in weeks 1 to 8 of each year |
| `src/price_model.py` | `PriceModel`: seeded, bounded random walk of the weekly fish price |
| `src/risk_assesor.py` | `RiskAssessor`: Monte Carlo revenue simulation, risk class by coefficient of variation, 5% Value-at-Risk |
| `src/region.py` | `Region`: one region's monthly rainfall, its statistics, similarity and distance measures, and rainy-season detection |
| `src/crop_rule.py` | `CropRule`: monthly rainfall ranges for maize, beans and coffee, and each month's classification |
| `src/rain_data.py` | `RainData`: downloads monthly rainfall from NASA POWER, saves it as CSV and loads it by year |
| `src/matrix_equation.py` | `MatrixEquation`: a 2×2 linear system with its determinant, condition number and solver, shared by `MicroGrid` and the taxi equilibrium |
| `src/route.py` | `Route`: one route's passenger counts and fare, with daily and total revenue and their statistics |
| `src/moving_average.py`, `src/exponential_smoothing.py`, `src/seasonal_naive.py` | The taxi demand forecasters, subclasses of `Forecaster` |
| `src/validate.py` | Input validation for mini-projects 1 and 2 |
| `files/` | CSV files written by mini-projects 2 and 4 |
| `tests/` | pytest tests for every mini-project, including invalid-input edge cases |

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
- **Extension, diesel generator:** adding diesel and a night-time load gives a 3×3 system with a determinant of −19 and a condition number of 5.91, so it stays well-posed. If the new equation is the sum of the other two, the rank drops to 2 and there is either no solution or infinitely many, depending on the night-time load. A nearly dependent equation still solves, but its condition number is 2,146, and a 1% error in one load moves solar from 8 kWh to −94 kWh.
- **Extension, sensitivity:** with random errors of up to ±5% in D1 and D2 (1,000 draws), solar moves by up to 28% and battery by up to 16%. The largest amplification of the demand error was 3.40, inside the limit of 5.83 set by the condition number. Solar is the least reliable figure, because it is a small difference between two large loads.

### Mini-project 3: Lake Victoria fish stock and export risk model

- **Why the old model fails:** Fibonacci numbers grow without limit and have no harvest term. The logistic model caps growth at the lake's carrying capacity (10,000 t) and subtracts the catch each week.
- **Why a variance threshold is meaningless:** revenue variance is measured in square shillings (about 8.9 × 10¹⁷ UGX² at h = 0.20), so a fixed limit of 50,000 flags every scenario. The coefficient of variation is a plain percentage: weekly revenue varies by about 9% on one price path.
- **Risk:** at h = 0.20, over 1,000 simulated price paths, the median weekly coefficient of variation is 7.5%, so the risk class is LOW. Expected annual revenue is 613 billion UGX, and the 5% Value-at-Risk is 519 billion UGX: about one year in 20 earns roughly 15% less than normal.
- **Sustainable harvest:** h = 0.20 is the best rate. The stock settles at 5,000 t (half the capacity) and the weekly catch reaches the maximum sustainable yield of rK/4 = 1,000 t. Lighter harvesting (0.05 and 0.10) leaves the lake fuller but catches less, and h = 0.30 drains the stock to about 2,500 t and earns 512 billion UGX a year against 613 billion.
- **Extension, closed season:** an 8-week break each year cuts 5-year revenue by 9% at h = 0.20 (from 3,174 to 2,891 billion UGX), because the stock is already at its most productive level. At h = 0.30 it raises revenue by 6% (from 2,432 to 2,579 billion UGX), because the break lets an overfished lake recover. The model has no breeding season, so it shows the cost of a closed season but not its main benefit.

### Mini-project 4: Rainfall pattern and crop suitability analyser

- **Rainfall:** Kampala is the wettest region (1,600 mm a year), then Gulu (1,388 mm) and Mbarara (1,040 mm). Gulu's rain is the most uneven, with a coefficient of variation of 0.61 against 0.37 for Kampala, because its dry season (December to February) is almost rainless.
- **Cosine similarity, corrected:** last year's method used `math.cos()`, which is the cosine of an angle. Cosine similarity is the dot product of two rainfall vectors divided by the product of their lengths. The NumPy version matches `scipy.spatial.distance.cosine` (0.787 for Kampala and Gulu).
- **Why cosine can mislead:** cosine similarity compares when the rain falls, not how much. Kampala and Mbarara score 0.89 although Kampala gets 54% more rain, and a region with double Kampala's rain every month scores a perfect 1.0. Pearson correlation gives the same pair only 0.21, and only Euclidean distance measures the amount: 250 mm between Kampala and Mbarara, and 493 mm between Kampala and its doubled copy.
- **Rainy seasons:** Mbarara is bimodal (peaks in April and October) and Gulu is unimodal (peak in August), which matches Uganda's south-western and northern climate zones. Kampala comes out unimodal (peak in May) because its illustrative data has no clear dry break between seasons, although Kampala has two rainy seasons in reality.
- **Advice:** Mbarara farmers should grow beans and plant in September, when the monthly rain (100 to 125 mm from September to November) sits inside the beans range.
- **Extension, real rainfall:** NASA POWER data for 2016–2025 averages 1,434 mm a year in Kampala, 1,412 mm in Gulu and 1,310 mm in Mbarara, and single years range widely (Mbarara from 880 mm to 1,904 mm). Averaged over the ten years, Kampala comes out bimodal (peaks in April and November), which matches its real climate, unlike the illustrative data.

### Mini-project 5: Taxi route revenue, pricing and fleet planner

- **Revenue:** over the 10 days, Kampala–Entebbe earns the most (UGX 3,390,000, UGX 339,000 a day), then Kampala–Mukono (UGX 1,560,000) and Kampala–Ntinda (UGX 948,000).
- **Fare:** on the Ntinda route, supply meets demand at a fare of UGX 2,200 and 76 passengers per trip-hour. The current fare of UGX 2,000 is below that, so 80 passengers want a seat for every 70 offered, a shortage of 10.
- **Forecasting:** in walk-forward backtesting over days 4 to 10, simple exponential smoothing had the lowest error on every route (MAE 3.7 to 5.9 passengers), and the grid search chose α = 1.0. That is the same as forecasting each day as the day before.
- **Fleet:** the day 11 forecasts are 45, 64 and 50 passengers. With a 15% buffer, one vehicle (112 seats a day) covers each route, at 40% to 57% of its seats.
- **Extension, weekly pattern:** on 60 simulated days with a busy Friday and a quiet Sunday, the seasonal-naive forecaster was off by 2.2 to 3.0 passengers a day, against 7.9 to 11.3 for the 3-day moving average.

## AI-use declaration

I used AI tools while working on this project:

- **ChatGPT (OpenAI):** explanations of Python concepts, including `.gitkeep` files, dunder methods, return type hints and docstrings, and a check of the CAGR formula.
- **Claude (Anthropic):**
  - Mini-project 1: writing the forecast figure (`src/plots.py`), the `fitted()` methods, `ClassroomPlanner` (`src/planning.py`), the tests, the corrected loop and table in the best-model forecast cell, and the variance comparison cell. Explaining the errors I hit (import paths, autoreload, statistics results losing their decimals, a validation object shared between cells) and reviewing the project against the brief. Fixing bugs, including the relative imports in `src/`, the missing brackets in `Linear().fit`, the standard deviation mismatch, first-year growth, length checks, detached docstrings and type hints. Drafting parts of the notebook's markdown.
  - Mini-project 2: writing the tests (`tests/test_microgrid.py`, `tests/test_hybrid_microgrid.py`, `tests/test_sensitivity.py`). Building both extensions: `HybridMicroGrid` (`src/hybrid_microgrid.py`), `SensitivityAnalysis` (`src/sensitivity.py`), and the extension cells and their discussion in the notebook. Reviewing the notebook's results, including finding that `scipy.optimize.nnls` returned a wrong answer for day 20. For the benchmark, which I wrote myself: understanding `timeit` and why one vectorised `numpy.linalg.solve` call on a 2×30 right-hand side is faster than solving each day in a loop, interpreting the timings (about 30 times faster, and different on every machine), and re-running the benchmark to check the speed-up figure used in the notebook and this README.
  - Mini-project 3: writing the tests in `tests/test_fish_stock.py`, and finding the import that broke `ClosedSeasonFishStock`. Fixing `RiskAssessor` for a zero catch, validating the harvest portion in `FishStock`, and separating total from annual revenue.
  - Mini-project 4: writing the tests in `tests/test_rainfall.py`, adding input validation to `Region` and `CropRule`, and drafting the Findings & Limitations section. Writing the tests in `tests/test_rain_data.py`.
  - Mini-project 5: writing the tests in `tests/test_taxi_route.py`.
  - All mini-projects:
    - Understanding the extension questions in the brief, and analysing what each extension asks for and how its results should be used and interpreted.
    - Understanding the forecasting models (linear trend, CAGR, Fibonacci ratio, moving average, simple exponential smoothing and seasonal naive) and how to run them: fitting on training data, predicting a horizon, walk-forward backtesting, and choosing a model by its error metrics.
    - Code review of the code I developed, checked against the brief, including finding bugs that I then fixed, such as the `MatrixEquation` change that broke `HybridMicroGrid` and the offline fallback in `RainData`.
    - Drafting this README and updating `requirements.txt`.

I wrote the original code and analysis. I reviewed all AI-generated code and text, ran the notebook and tests myself, and corrected errors in the AI output, such as the rounding explanation and missing axis labels.
