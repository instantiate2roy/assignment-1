import math

import matplotlib.pyplot as plt
import numpy
from matplotlib.ticker import MaxNLocator, StrMethodFormatter

from .district_population import DistrictPopulation
from .validate import Validate


def plot_district_forecasts(validate:Validate, years:list, all_populations:dict, train_size:int,
                            predictions:dict, future_years:list, future_forecasts:dict,
                            ncols:int = 3) -> plt.Figure:
    """
    Plot actual, fitted and forecast values for every district in one figure of subplots,
    using each district's best model, with the train/test split marked.

    Args:
        validate: Validate object passed on to DistrictPopulation.
        years: All observed years, e.g. 2015 to 2024.
        all_populations: District name -> list of observed populations.
        train_size: Number of leading years used for training (7 means 2015 to 2021).
        predictions: The notebook's predictions dict. Uses [district]['best-model']
            and [district][model]['forecast'] for the test years.
        future_years: Years forecast after the data ends, e.g. 2025 to 2029.
        future_forecasts: District name -> best-model forecast for future_years
            (bm_prediction in the notebook), fitted on the full series.
        ncols: Number of subplot columns.

    Returns:
        The matplotlib Figure, so the caller can save or show it.
    """
    years = numpy.array(years)
    train_years, test_years = years[:train_size], years[train_size:]
    districts = list(all_populations)

    nrows = math.ceil(len(districts) / ncols)
    fig, axes = plt.subplots(nrows, ncols, figsize=(5 * ncols, 3.6 * nrows), sharex=True, squeeze=False)
    axes = axes.flatten()

    # Halfway between the last train year and the first test year, so the line never sits on a point
    split = (train_years[-1] + test_years[0]) / 2

    for ax, district in zip(axes, districts):
        actual = numpy.array(all_populations[district])
        best = predictions[district]['best-model']

        # Fitted values come from the model trained on the training years only
        train_obj = DistrictPopulation(validate, train_years, actual[:train_size], district)
        fitted = train_obj.fitted(best)

        ax.axvspan(split, test_years[-1] + 0.5, color='grey', alpha=0.12, label='Test period')
        ax.axvline(split, color='grey', linestyle=':', linewidth=1.2)

        ax.plot(years, actual, 'o-', color='black', markersize=3, label='Actual')
        ax.plot(train_years, fitted, '-', color='tab:blue', label='Fitted (train)')
        ax.plot(test_years, predictions[district][best]['forecast'], 's--', color='tab:orange',
                markersize=3, label='Forecast (test)')
        ax.plot(future_years, future_forecasts[district], '--', color='tab:purple',
                label=f'Forecast ({future_years[0]}–{future_years[-1]})')

        ax.set_title(f'{district} (best: {best})')
        ax.grid(alpha=0.3)
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))

    # Hide leftover empty cells when the districts don't fill the grid
    for ax in axes[len(districts):]:
        ax.set_visible(False)

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, 0.95), ncol=len(labels), frameon=False)
    fig.suptitle('District population: actual, fitted and forecast (best model per district)')
    fig.supxlabel('Year')
    fig.supylabel('Population')
    fig.tight_layout(rect=(0, 0, 1, 0.91))
    return fig
