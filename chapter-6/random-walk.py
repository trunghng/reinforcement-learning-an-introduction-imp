import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

states = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5}
true_value = [1.0 * x / 6 for x in range(1, 6)]

np.random.seed(13)


def temporal_difference(V, alpha, gamma):
    trajectory = []
    state = states['C']

    while True:
        # not agent's action
        action = np.random.choice([-1, 1])
        next_state = state + action
        reward = get_reward(next_state)
        trajectory.append([state, reward])
        V[state] += alpha * (reward + gamma * V[next_state] - V[state])
        state = next_state
        if is_terminal(state):
            break

    return trajectory


def monte_carlo(V, alpha, gamma):
    state = states['C']
    trajectory = [[state, 0]]
    # since returns are the same for all states
    returns = 0

    while True:
        action = np.random.choice([-1, 1])
        state += action
        reward = get_reward(state)
        trajectory.append([state, reward])
        if is_terminal(state):
            if state == 6:
                returns = 1
            break

    for state_, _ in trajectory[:-1]:
        V[state_] += alpha * (returns - V[state_])

    return trajectory


def get_state_values(episodes, alpha, gamma):
    V_TD = np.array([0, 0.5, 0.5, 0.5, 0.5, 0.5, 0])
    eps = [0, 1, 10, 100]

    plt.plot(states.keys(), true_value, label='true values')

    for ep in range(episodes + 1):
        if ep in eps:
            plt.plot(states.keys(), V_TD[1:-1], label=str(ep) + ' episodes')
        _ = temporal_difference(V_TD, alpha, gamma)

    plt.xlabel('State')
    plt.ylabel('Estimated value')
    plt.legend()


def get_rmse(episodes, gamma):
    V_TD = np.array([0, 0.5, 0.5, 0.5, 0.5, 0.5, 0])
    V_MC = np.array([0, 0.5, 0.5, 0.5, 0.5, 0.5, 0])
    td_alphas = [0.05, 0.1, 0.15]
    mc_alphas = [0.01, 0.02, 0.03, 0.04]
    methods = ['TD', 'MC']
    runs = 100

    for method_name in methods:
        if method_name == 'TD':
            linestyle = 'solid'
            alphas = td_alphas
            method = temporal_difference
            values = V_TD
        else:
            linestyle = 'dashdot'
            alphas = mc_alphas
            method = monte_carlo
            values = V_MC

        for alpha in alphas:
            total_errors = np.zeros(episodes)
            for _ in tqdm(range(runs)):
                V = values.copy()
                errors = []
                for ep in range(episodes):
                    rmse = np.sqrt(np.sum(np.power(V[1:-1] - true_value, 2) / 5.0))
                    errors.append(rmse)
                    _ = method(V, alpha, gamma)
                total_errors += np.asarray(errors)
            total_errors /= runs
            plt.plot(total_errors, label=method_name + ', alpha = %.02f' % (alpha), linestyle=linestyle)
    plt.xlabel('Episodes')
    plt.ylabel('RMS')
    plt.legend(loc = 'upper right')


def is_terminal(state):
    return state == 0 or state == 6


def get_reward(state):
    return 1 if state == 6 else 0


if __name__ == '__main__':
    episodes = 100
    alpha = 0.1
    gamma = 1

    plt.figure(figsize=(15, 7))
    plt.subplot(1, 2, 1)
    get_state_values(episodes, alpha, gamma)

    plt.subplot(1, 2, 2)
    get_rmse(episodes, gamma)
    plt.tight_layout()

    plt.savefig('./random_walk.png')
    plt.close()
