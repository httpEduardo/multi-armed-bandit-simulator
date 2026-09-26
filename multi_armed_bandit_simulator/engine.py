import math
import random


def _pull(probability):
    return 1 if random.random() < probability else 0


def epsilon_greedy(arms, rounds=200, epsilon=0.1):
    counts = [0] * len(arms)
    rewards = [0] * len(arms)
    history = []

    for _ in range(rounds):
        if random.random() < epsilon:
            choice = random.randrange(len(arms))
        else:
            averages = [rewards[i] / counts[i] if counts[i] else 0.0 for i in range(len(arms))]
            choice = max(range(len(arms)), key=lambda i: averages[i])
        reward = _pull(arms[choice])
        counts[choice] += 1
        rewards[choice] += reward
        history.append({"arm": choice, "reward": reward})

    averages = [rewards[i] / counts[i] if counts[i] else 0.0 for i in range(len(arms))]
    return {
        "counts": counts,
        "averages": [round(avg, 3) for avg in averages],
        "total_reward": sum(rewards),
        "history": history[-20:],
    }


def ucb1(arms, rounds=200):
    counts = [0] * len(arms)
    rewards = [0] * len(arms)
    history = []

    for t in range(1, rounds + 1):
        if 0 in counts:
            choice = counts.index(0)
        else:
            ucb_scores = [
                (rewards[i] / counts[i]) + math.sqrt(2 * math.log(t) / counts[i])
                for i in range(len(arms))
            ]
            choice = max(range(len(arms)), key=lambda i: ucb_scores[i])
        reward = _pull(arms[choice])
        counts[choice] += 1
        rewards[choice] += reward
        history.append({"arm": choice, "reward": reward})

    averages = [rewards[i] / counts[i] if counts[i] else 0.0 for i in range(len(arms))]
    return {
        "counts": counts,
        "averages": [round(avg, 3) for avg in averages],
        "total_reward": sum(rewards),
        "history": history[-20:],
    }
