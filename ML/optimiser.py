import numpy as np
from numpy.random import MT19937
from numpy.random import RandomState, SeedSequence
import pandas as pd
import timeit
import warnings

warnings.filterwarnings("ignore")

# Super important: set the random seed for reproducibility
# Otherwise the results will be different every time you run the code
rs = RandomState(MT19937(SeedSequence(42)))
np.random.set_state(rs.get_state())

# Params & parameter bounds
windows = np.arange(10, 100, 10)
thresholds = np.arange(0.5, 5.0, 0.5)

n_points = 2000
initial_price = 100
trend = 0.5
noise_level = 2

trend_component = np.linspace(0, trend * n_points, n_points)
noise = np.random.normal(0, noise_level, n_points)

df = pd.DataFrame({"price": initial_price + trend_component + np.cumsum(noise)})

# This is a hyperparameter for the random grid search optimiser
# Assuming coverage 50% for simplicity
# Maximum = 1, Minimum = 0
# You can try adjusting this value to see how it affects the optimisation time
coverage = 0.5


# Backtest function
def backtest(df, window, threshold, metric_annualizer=365 * 24):
    df["zscores"] = (df["price"] - df["price"].rolling(window).mean()) / df[
        "price"
    ].rolling(window).std()

    price_chg = df["price"].pct_change().values
    signals = df["zscores"].values
    positions = np.zeros_like(price_chg)

    for i in range(1, len(price_chg)):
        if signals[i] > threshold:
            positions[i] = 1
        elif signals[i] < -threshold:
            positions[i] = -1

    pnl = np.zeros_like(price_chg)
    trades = np.zeros_like(price_chg)
    for i in range(1, len(price_chg)):
        pnl[i] = positions[i - 1] * price_chg[i]
        trades[i] = np.abs(positions[i] - positions[i - 1])

    df["pnl"] = pnl
    df["positions"] = positions
    df["trades"] = trades
    df["equity"] = df["pnl"].cumsum()

    sharpe_ratio = np.mean(pnl) / np.std(pnl) * np.sqrt(metric_annualizer)
    trades_per_interval = np.sum(trades) / df.shape[0]
    max_drawdown = np.min(df["equity"] - df["equity"].cummax())
    metrics = {
        "sharpe_ratio": sharpe_ratio,
        "trades_per_interval": trades_per_interval,
        "max_drawdown": max_drawdown,
    }

    return metrics


# Objective function
def objective_function(params):
    window, threshold = params
    # Objective: Sharpe ratio
    metrics = backtest(df, window, threshold)
    objective = metrics["sharpe_ratio"]

    # Constraints
    # Soft constraint: trades per interval should be more than 0.01
    trades_per_interval = metrics["trades_per_interval"]
    if trades_per_interval < 0.01:
        # It's a maximisation problem, so we penalise the objective like this
        # This is a soft constraint because we don't directly set the objective to -infinity. The optimiser will still consider this parameter and its neighbourhood.
        objective -= 1 - trades_per_interval

    # Hard constraint: max drawdown should be less than -0,5
    max_drawdown = metrics["max_drawdown"]
    if max_drawdown < -0.5:
        # It's a maximisation problem, so we penalise the objective like this
        # This is a hard constraint because we directly set the objective to -infinity. The optimiser will never select this parameter or its neighbourhood.
        objective = -np.inf

    return objective


# Optimiser
def random_grid_search(
    objective_function,
    windows,
    thresholds,
    n_iter=int(len(windows) * len(thresholds) * coverage),
):
    best_params = None
    # Maximisation problem: start with negative infinity
    best_score = -np.inf
    for _ in range(n_iter):
        window = np.random.choice(windows)
        threshold = np.random.choice(thresholds)
        score = objective_function((window, threshold))
        # Maximisation problem: higher score is better
        if score > best_score:
            best_score = score
            best_params = (window, threshold)
    return best_params, best_score


def grid_search(objective_function, windows, thresholds):
    best_params = None
    # Maximisation problem: start with negative infinity
    best_score = -np.inf
    for window in windows:
        for threshold in thresholds:
            score = objective_function((window, threshold))
            # Maximisation problem: higher score is better
            if score > best_score:
                best_score = score
                best_params = (window, threshold)
    return best_params, best_score


# Optimisation
print("Unoptimised (grid search)")
best_params, best_score = grid_search(objective_function, windows, thresholds)
best_metrics = backtest(df, *best_params)
print(f"Best parameters: {best_params}")
print(f"Best score: {best_score}")
print(f"Metrics for best parameters: {best_metrics}")

print()
print("Optimised (random grid search)")
best_params, best_score = random_grid_search(objective_function, windows, thresholds)
best_metrics = backtest(df, *best_params)
print(f"Best parameters: {best_params}")
print(f"Best score: {best_score}")
print(f"Metrics for best parameters: {best_metrics}")

unoptimised_time = timeit.timeit(
    lambda: grid_search(objective_function, windows, thresholds), number=1
)
optimised_time = timeit.timeit(
    lambda: random_grid_search(objective_function, windows, thresholds), number=1
)

print()
print(f"Unoptimised time: {unoptimised_time * 1000}:.2f ms")
print(f"Optimised time: {optimised_time * 1000:.2f} ms")
print(f"Speedup: {(unoptimised_time - optimised_time) / unoptimised_time * 100:.2f}%")

