#!/bin/sh python3

import matplotlib.pyplot as plt

results = {
    "a100": {
        "gpu": {
            "power-gpu": [493,489,493,491],
            "power-cpu" : [101],
            "power-total" : 2611,
            "gflop-gpu" : [21820.90, 21664.32, 21489.99, 21659.08],
            "gflop-cpu" : [0,0,0,0],
        },
        "cpugpu": {
            "power-gpu": [496,493,493,491],
            "power-cpu" : [136],
            "power-total" : 2722,
            "gflop-gpu" : [21527.63,21541.83,21867.20,21805.51],
            "gflop-cpu" : [228.27,234.33,276.42,234.99],
        },
    },
}

# plot: cabinet power at different power caps
_, ax = plt.subplots()

def plot_run(r):
    gpucolor="#ffae49"
    cpucolor="#44a5c2"
    othcolor="#c1f7c2"
    #width = 6
    gpupwr = [sum(r["gpu"]["power-gpu"]), sum(r["cpugpu"]["power-gpu"])]
    cpupwr = [sum(r["gpu"]["power-cpu"]), sum(r["cpugpu"]["power-cpu"])]
    totpwr = [r["gpu"]["power-total"], r["cpugpu"]["power-total"]]
    cpgpwr = [cpupwr[i]+gpupwr[i] for i in [0, 1]]
    othpwr = [totpwr[i]-cpgpwr[i] for i in [0, 1]]
    groups = ["gpu", "cpu-gpu"]
    ax.bar(groups, gpupwr, color = gpucolor, edgecolor = "black", linewidth = 1.5, label="gpu")
    ax.bar(groups, cpupwr, color = cpucolor, edgecolor = "black", linewidth = 1.5, label="cpu", bottom = gpupwr)
    ax.bar(groups, othpwr, color = othcolor, edgecolor = "black", linewidth = 1.5, label="other", bottom = cpgpwr)
    ax.set_xlabel('workload')
    ax.set_ylabel('node power (W)')
    ax.legend(loc='upper right')
    #ax.bar([cap[i]-width/2 for i in range(n)], full, width, color='blue',label="128-node cabinet")
    #ax.bar([cap[i]+width/2 for i in range(n)], partial, width, color='green',label="112-node cabinet")
    #ax.set_ylabel('cabinet power (kW)')
    #ax.set_xlabel('power cap (W)')
    #ax.set_title(f"Cabinet Power for {label}")
    #ax.legend(loc='lower right')
    #plt.savefig(f'{label}_cabinet.png')

plot_run(results["a100"])
plt.show()
