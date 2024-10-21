import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
import random

# Cargar el dataset
dataset = pd.read_csv("maquinas_tragamonedas.csv")
N = len(dataset)
d = len(dataset.columns)

# --- Implementación de UCB ---
# Inicialización
number_of_selections_ucb = [0] * d
sums_of_rewards_ucb = [0] * d
machines_selected_ucb = []
total_reward_ucb = 0
rewards_matrix_ucb = np.zeros((N, d))

for n in range(N):
    max_upper_bound = 0
    machine_ucb = 0
    for i in range(d):
        if number_of_selections_ucb[i] > 0:
            average_reward = sums_of_rewards_ucb[i] / number_of_selections_ucb[i]
            delta_i = math.sqrt(2 * math.log(n + 1) / number_of_selections_ucb[i])
            upper_bound = average_reward + delta_i
        else:
            upper_bound = 1e400
        if upper_bound > max_upper_bound:
            max_upper_bound = upper_bound
            machine_ucb = i
    machines_selected_ucb.append(machine_ucb)
    number_of_selections_ucb[machine_ucb] += 1
    reward = dataset.values[n, machine_ucb]
    sums_of_rewards_ucb[machine_ucb] += reward
    total_reward_ucb += reward
    rewards_matrix_ucb[n, machine_ucb] = reward

rewards_per_iteration_ucb = np.cumsum([dataset.values[n, machines_selected_ucb[n]] for n in range(N)])

# --- Implementación de Thompson Sampling ---
# Inicialización
alpha_ts = [1] * d
beta_ts = [1] * d
machines_selected_ts = []
total_reward_ts = 0
rewards_matrix_ts = np.zeros((N, d))

for n in range(N):
    sampled_theta = [np.random.beta(alpha_ts[i], beta_ts[i]) for i in range(d)]
    machine_ts = np.argmax(sampled_theta)
    machines_selected_ts.append(machine_ts)
    reward = dataset.values[n, machine_ts]
    total_reward_ts += reward
    alpha_ts[machine_ts] += reward
    beta_ts[machine_ts] += 1 - reward
    rewards_matrix_ts[n, machine_ts] = reward

rewards_per_iteration_ts = np.cumsum([dataset.values[n, machines_selected_ts[n]] for n in range(N)])

# --- Implementación de Selección Aleatoria ---
total_reward_random = 0
machines_selected_random = []
rewards_matrix_random = np.zeros((N, d))

for n in range(N):
    machine_random = random.randrange(d)
    machines_selected_random.append(machine_random)
    reward = dataset.values[n, machine_random]
    total_reward_random += reward
    rewards_matrix_random[n, machine_random] = reward

rewards_per_iteration_random = np.cumsum([dataset.values[n, machines_selected_random[n]] for n in range(N)])

# --- Visualización Comparativa ---
plt.figure(figsize=(12,6))
plt.plot(range(N), rewards_per_iteration_ucb, label='UCB')
plt.plot(range(N), rewards_per_iteration_ts, label='Thompson Sampling')
plt.plot(range(N), rewards_per_iteration_random, label='Selección Aleatoria')
plt.title("Comparación de Recompensas Acumuladas")
plt.xlabel("Número de Iteraciones")
plt.ylabel("Recompensa Acumulada")
plt.legend()
plt.show()

print(f"Recompensa total obtenida por UCB: {total_reward_ucb}")
print(f"Recompensa total obtenida por Thompson Sampling: {total_reward_ts}")
print(f"Recompensa total obtenida por selección aleatoria: {total_reward_random}")

# --- Visualización de Selecciones ---
# Histograma para UCB
plt.figure(figsize=(12,6))
plt.hist(machines_selected_ucb, bins=np.arange(d+1)-0.5, edgecolor='black')
plt.title("Selecciones de Máquinas por UCB")
plt.xlabel("ID de la Máquina")
plt.ylabel("Número de veces que fue seleccionada")
plt.xticks(range(d))
plt.show()

# Histograma para Thompson Sampling
plt.figure(figsize=(12,6))
plt.hist(machines_selected_ts, bins=np.arange(d+1)-0.5, edgecolor='black')
plt.title("Selecciones de Máquinas por Thompson Sampling")
plt.xlabel("ID de la Máquina")
plt.ylabel("Número de veces que fue seleccionada")
plt.xticks(range(d))
plt.show()

# Histograma para Selección Aleatoria
plt.figure(figsize=(12,6))
plt.hist(machines_selected_random, bins=np.arange(d+1)-0.5, edgecolor='black')
plt.title("Selecciones de Máquinas por Selección Aleatoria")
plt.xlabel("ID de la Máquina")
plt.ylabel("Número de veces que fue seleccionada")
plt.xticks(range(d))
plt.show()

# --- Recompensas Acumuladas por Máquina ---
# UCB
cumulative_rewards_ucb = np.cumsum(rewards_matrix_ucb, axis=0)

plt.figure(figsize=(14, 8))
for i in range(d):
    plt.plot(cumulative_rewards_ucb[:, i], label=f'Máquina {i+1}')
plt.title("Evolución de las Recompensas Acumuladas por Máquina (UCB)")
plt.xlabel("Número de Iteraciones")
plt.ylabel("Recompensa Acumulada")
plt.legend()
plt.grid(True)
plt.show()

# Thompson Sampling
cumulative_rewards_ts = np.cumsum(rewards_matrix_ts, axis=0)

plt.figure(figsize=(14, 8))
for i in range(d):
    plt.plot(cumulative_rewards_ts[:, i], label=f'Máquina {i+1}')
plt.title("Evolución de las Recompensas Acumuladas por Máquina (Thompson Sampling)")
plt.xlabel("Número de Iteraciones")
plt.ylabel("Recompensa Acumulada")
plt.legend()
plt.grid(True)
plt.show()
