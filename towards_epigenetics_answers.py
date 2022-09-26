import numpy as np
from scipy.stats import uniform
import matplotlib.pyplot as plt

from util import print_simulated_donors


# simulate one random value from uniform distribution
random_variable = uniform(loc=0, scale=1)
beta_value = random_variable.rvs()


# moving it to a function: this is how we simulate one beta value
def simulate_beta_value() -> float:
    random_variable = uniform(loc=0, scale=1)
    beta_value = random_variable.rvs()
    return beta_value


simulate_beta_value()


# simulate multiple beta values (1 donor)
def simulate_betas(size):
    return np.array([simulate_beta_value() for _ in range(size)])


size = 100
simulate_betas(size)


# plot a histogram of simulated values
def plot_betas(betas):
    plt.hist(betas, 10, density=False, facecolor='b', alpha=0.8)
    plt.xlabel("beta value")
    plt.ylabel("counts of beta value in range")
    plt.show()


# plot_betas(betas=simulate_betas(100))


# simulate multiple donors
def simulate_donors(donor_count, size):
    donors = []
    for i in range(1, donor_count+1):
        donor = simulate_betas(size)
        donors.append(donor)
    return donors


simulated_donors = simulate_donors(donor_count=60, size=size)
# print(simulated_donors)

# plot_betas(simulated_donors[10])


# simulate a signal as a vector where one beta value will be different
def simulate_signal(size):
    signal_vector = np.zeros(size)
    signal_vector[5] = 0.4
    return signal_vector


# add signal to a simulated donor vector of beta values (ensure it's still valid value)
def add_signal_to_donor(donor, signal):
    return np.maximum(np.minimum(donor + signal, 1), 0)


signal = simulate_signal(size=size)


# add signal to some of donors -> construct a dataset
def make_donors_with_signal(donors, signal, donors_with_signal_percentage):
    donor_indices = list(range(len(donors)))
    donors_with_signal_count = round(len(donors) * donors_with_signal_percentage)
    donor_indices_with_signal = np.random.choice(donor_indices, size=donors_with_signal_count, replace=False)

    donors_with_signal = []

    for index in donor_indices:
        if index in donor_indices_with_signal:
            label = 1
            new_betas = add_signal_to_donor(donors[index], signal)
        else:
            label = 0
            new_betas = donors[index]
        donor = np.concatenate([np.array([label]), new_betas])
        donors_with_signal.append(donor)

    return donors_with_signal


donors = make_donors_with_signal(simulated_donors, signal, 0.5)
# print_simulated_donors(donors)


# show avg beta values in cases vs controls (showing top 10 most different betas)
def plot_case_vs_controls(donors, show_n: int = 10):
    cases = np.mean([donor[1:] for donor in donors if donor[0] == 1], axis=0)
    controls = np.mean([donor[1:] for donor in donors if donor[0] == 0], axis=0)

    interesting_betas = np.abs(cases-controls).argsort()[::-1][:show_n]

    x = np.arange(interesting_betas.shape[0])
    width = 0.3  # the width of the bars

    fig, ax = plt.subplots()
    fig.set_size_inches(16, 8, forward=True)

    rects1 = ax.bar(x - width / 2, cases[interesting_betas].round(3), width, label='cases')
    rects2 = ax.bar(x + width / 2, controls[interesting_betas].round(3), width, label='controls')

    ax.set_ylabel('average beta values')
    ax.set_xticks(x, [f'beta{i+1}' for i in interesting_betas])
    ax.legend()

    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)

    fig.tight_layout()

    plt.show()


plot_case_vs_controls(donors)
