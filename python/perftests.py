from collections import defaultdict
import time
import random
import copy
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import functools

DEFAULT_MAX_VALUE = 1000
DEFAULT_START_SIZE = 2**6


def DEFAULT_STEP_FUNCTION(x):
    return x*2


def test_and_plot(test_size, *test_cases, **kwargs):
    run_tests = init_multi_test(test_size, **kwargs)
    results = run_tests(*test_cases)
    plot_multi_results(results, **kwargs)
    return markdown_multi_results(results)


def init_test(test_size, external_results=None):
    results = external_results or dict()
    test_arr = build_test_input(test_size)

    def run_tests(*test_cases, initialization=None):
        arr = copy.copy(test_arr)
        results.update(time_tests(arr, *test_cases))
        return results

    return run_tests


def init_multi_test(test_size, external_results=None, steps=None, start=None, **kwargs):
    results = defaultdict(list)
    results.update(external_results)
    steps = steps or DEFAULT_STEP_FUNCTION
    start = start or DEFAULT_START_SIZE
    test_arrs = [build_test_input(int(s)) for s in krange(start, test_size, steps)]

    def run_tests(*test_cases, initialization=None):
        arr = [copy.copy(a) for a in test_arrs]
        tests_sizes = [len(a) for a in arr]
        tests_results = [time_tests(a, *test_cases) for a in arr]
        for size, experiments in zip(tests_sizes, tests_results):
            for f_name, exec_time in experiments:
                results[f_name].append((size, exec_time))
        return results

    return run_tests


def build_test_input(test_size, max_value=None, **kwargs):
    max_value = max_value or DEFAULT_MAX_VALUE
    return [random.randint(0, max_value) for _ in range(test_size)]


def time_tests(arr, *test_cases):
    for test_fun in test_cases:
        try:
            input_arr = test_fun.init(arr)
        except AttributeError:
            input_arr = arr
        # TODO: use timeit module instead:
        t0 = time.time()
        test_fun(input_arr)
        exec_time = time.time() - t0
        yield (test_fun.__name__, exec_time*1e3)


def markdown_results(results):
    markdown =  "| Function | Time (ms) | slower by a factor |\n"
    markdown += "|----------|-----------|--------------------|\n"

    fastest_exec = min(results.values())
    for f_name, f_exec_time in sorted(results.items(), key=lambda r: r[1]):
        markdown += f"| {f_name} | **{f_exec_time:.2f}** ms |"
        markdown += f" {f_exec_time/fastest_exec:.1f} |\n"

    return markdown


def markdown_multi_results(results):
    largest_test_results = {k: v[-1] for k, v in results.items()}
    test_sizes = [size for size, exec_time in largest_test_results.values()]
    if not all(s == test_sizes[0] for s in test_sizes):
        raise ValueError(f"Not all tests where ran on the same input sizes. {test_sizes}")
    markdown = f"Results for the largest test, n={test_sizes[0]}\n\n"
    results_exec_times = {k: v[1] for k, v in largest_test_results.items()}
    return markdown + markdown_results(results_exec_times)


def plot_simple_results(results, plot_only=None, **kwargs):
    if plot_only:
        results = {k: v for k, v in results.items() if k in plot_only}
    labels, exec_time = zip(*sorted(results, key=lambda i: i[1]))
    df = pd.DataFrame.from_dict({
        "function name": list(labels),
        "execution time (ms)": list(exec_time),
    })
    plt.figure(figsize=(10, 10))
    g = sns.barplot(data=df, x="function name", y="execution time (ms)", log=True)
    g.set_xticklabels(df["function name"], rotation=30, ha="right")


def plot_multi_results(results, plot_only=None, **kwargs):
    func_name = []
    test_size = []
    exec_time = []
    for name, test_info in results.items():
        if plot_only and name not in plot_only:
            continue
        for s, t in test_info:
            func_name.append(name)
            test_size.append(s)
            exec_time.append(t)

    df = pd.DataFrame({
        "function name": func_name,
        "execution time (ms)": exec_time,
        "test size": test_size
    })
    plt.figure(figsize=(10, 10))
    plt.xscale('log')
    plt.yscale('log')
    sns.lineplot(data=df, x="test size", y="execution time (ms)", hue="function name")


class FunctionWithInit:
    def __init__(self, init_function, test_function):
        self.init_function = init_function
        self.test_function = test_function
        functools.update_wrapper(self, test_function)

    def init(self, *args, **kwargs):
        return self.init_function(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        return self.test_function(*args, **kwargs)


def init_with(init_function):
    def decorator(test_function):
        return FunctionWithInit(init_function, test_function)
    return decorator


def krange(start, stop, key, force=False):
    """Returns an iterator that moves from `start` to end `progressing`
    to the next step using function `key` (step i + 1 = `key(step i)`).

    Usage:
    >>> print(list(krange(1, 10, lambda x:x*2)))
    [1, 2, 4, 8]
    """
    err_msg = (
        "The provided function doesn't seem to allo sequence progression, "
        "you can use the `force=True` if you are certain this is the range "
        "you need."
    )
    i = start
    while i < stop:
        yield i
        prev = i
        i = key(i)
        if prev == i and not force:
            raise ValueError(f"Error: {i}={prev}. {err_msg}")
