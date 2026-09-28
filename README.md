# District population forecasting

Forecasts the population of five Ugandan districts (Kampala, Wakiso, Gulu, Kabale and Masindi) to 2029 from 2015–24 data. The project compares three forecasting models (Linear, CAGR and Fibonacci ratio), picks the best one for each district, and estimates how many primary-school classrooms each district needs by 2029.

Population figures are in thousands.

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

Open the notebook from the project folder, so that `src` can be imported:

```bash
jupyter notebook project1_population.ipynb
```

Then choose **Kernel > Restart & Run All**. The notebook prints each table and saves the forecast figure as `district_forecasts.png`.

To run the tests:

```bash
pytest
```

## Project structure

| Path | Contents |
|---|---|
| `project1_population.ipynb` | Analysis: statistics, growth rates, model comparison, forecasts, variance, figure, classroom planning, findings |
| `src/district_population.py` | `DistrictPopulation`: statistics, growth rates, predictions and error metrics for one district |
| `src/forecaster.py` | `Forecaster`: abstract base class for the models |
| `src/linear.py`, `src/cagr.py`, `src/fibonacci_ratio.py` | The three forecasting models |
| `src/validate.py` | Input validation |
| `src/plots.py` | Actual, fitted and forecast figure for every district |
| `src/planning.py` | `ClassroomPlanner`: classroom estimates from population |
| `tests/` | pytest tests, including invalid-input edge cases |

## Findings

- **Growth:** Wakiso grows fastest, with a 2015–24 CAGR of 6.5%. Kabale grows slowest, at 3.7%.
- **Model accuracy:** CAGR was the most accurate model on the 2022–24 test years for Kampala, Wakiso, Gulu and Kabale, and Linear for Masindi. The Fibonacci ratio model was the least accurate everywhere, with a MAPE of 53% to 66%.
- **2029 forecast:** Wakiso overtakes Kampala in 2029, at 2,285 thousand against 2,255 thousand.
- **Classrooms:** the five districts need 4,878 more primary-school classrooms by 2029, led by Wakiso (2,088) and Kampala (1,544). This assumes 18% of the population is of primary-school age, 53 pupils per classroom, and existing classrooms that exactly meet 2024 need.
- **Main limitation:** each forecast rests on ten years of data and assumes a constant trend. Kabale's growth has slowed, so its forecast and classroom figure are likely too high.

The full findings and limitations are at the end of the notebook.

## AI-use declaration

I used AI tools while working on this project:

- **ChatGPT (OpenAI):** explanations of Python concepts, including `.gitkeep` files, dunder methods, return type hints and docstrings, and a check of the CAGR formula.
- **Claude (Anthropic):** writing the forecast figure (`src/plots.py`), the `fitted()` methods, `ClassroomPlanner` (`src/planning.py`) and the tests. Also fixing bugs I identified (the standard deviation mismatch, first-year growth, length checks, detached docstrings and type hints), and drafting parts of the notebook's markdown and this README.

I wrote the original code and analysis. I reviewed all AI-generated code and text, ran the notebook and tests myself, and corrected errors in the AI output, such as the rounding explanation and missing axis labels.