#!/bin/sh python3

import matplotlib.pyplot as plt

# TODO: check the distribution of TTS for 600W - were there some outlier results that we need to filter?

results = {
        "icon-sol": {
            "powercap": [520,540,560,580,600,620],
            "mintime" : [511.05,497.97,484.16,480.62,479.51,474.92],
            "maxtime" : [527.46,517.56,506.28,501.26,588.81,491.49],
            "meantime": [518.85,507.27,495.14,490.70,489.24,482.60],
            # note 620W we only have 111 nodes by the end, due to failures
            "members" : [126,126,126,125,126,126],
            "cabinet-power" : [306,317,324,335,345,352]
         },
         "icon-acc": {
            "powercap": [560,600],
            "mintime" : [855.28,824.99],
            "maxtime" : [883.43,856.94],
            "meantime": [856.94,841.11],
            "members" : [123,123],
            "cabinet-power" : [319,339]
         },
}

# power consumption in kW with all nodes idle
idle_cabinet = 111
# power consumption in kW that is constant irrespective of population
base_cabinet = 5

idle_per_node = (idle_cabinet-base_cabinet)/128

# energy consumption per node, minus the base_cabinet load
def per_node(cabinet, members):
    return (cabinet - idle_cabinet)/members + idle_per_node

def cab_128(cabinet, members):
    pn = per_node(cabinet, members)
    return 128*pn + base_cabinet

def cab_112(cabinet, members):
    pn = per_node(cabinet, members)
    return 112*pn + base_cabinet

def power_from(model):
    pwr = model["cabinet-power"]
    members = model["members"]
    pwr128 = [int(cab_128(pwr[i], members[i])) for i in range(len(pwr))]
    pwr112 = [int(cab_112(pwr[i], members[i])) for i in range(len(pwr))]

    return pwr128, pwr112

def ets_eff(time, cab_pwr, idx, ref_ets, nodes_per_cabinet):
    n = len(time)
    ets = [time[i]*cab_pwr[i]*(128/nodes_per_cabinet)/3600 for i in range(n)]
    eff = [100*(ets[i]-ref_ets)/ref_ets for i in range(n)]

    return ets, eff

def report_cab(label):
    r = results[label]
    full,partial = power_from(r)
    cap = r["powercap"]
    n = len(cap)
    measured = r["cabinet-power"]
    time = r["meantime"]
    idx = cap.index(560)
    speedup = [100*(time[idx]-time[i])/time[idx] for i in range(n)]
    # ETS for 560W at 128 nodes/cabinet is the reference
    # units are kWhr
    ref_ets = time[idx]*full[idx]/3600
    ETS_full, EFF_full = ets_eff(time, full, idx, ref_ets, 128)
    ETS_part, EFF_part = ets_eff(time, partial, idx, ref_ets, 112)
    #ETS_part, EFF_part = ets_eff(time, partial, idx, ref_ets*112/128)

    print(f"================ {label} ================")
    print()
    print(f"cap     128-nodes 112-nodes speedup     ETS")
    print(f"(W)     (kW)      (kW)      (%)         (%)")
    print()
    for i in range(len(full)):
        print(f"{cap[i]}     {full[i]}         {partial[i]}    {speedup[i]:4.1f}    {EFF_full[i]:4.1f}")
    print()

    # plot: cabinet power at different power caps
    fig, ax = plt.subplots()

    width = 6
    ax.axhline(y=339, color='red')
    ax.bar([cap[i]-width/2 for i in range(n)], full, width, color='blue',label="128-node cabinet")
    ax.bar([cap[i]+width/2 for i in range(n)], partial, width, color='green',label="112-node cabinet")
    ax.set_ylabel('cabinet power (kW)')
    ax.set_xlabel('power cap (W)')
    ax.set_title(f"Cabinet Power for {label}")
    ax.legend(loc='lower right')
    plt.savefig(f'{label}_cabinet.png')

    # plot: energy to solution (J) at different power caps
    fig, ax = plt.subplots()

    width = 6
    ax.bar([cap[i]-width/2 for i in range(n)], ETS_full, width, color='blue',label="128-node cabinet")
    ax.bar([cap[i]+width/2 for i in range(n)], ETS_part, width, color='green',label="112-node cabinet")
    ax.set_ylabel('ETS (kWhr)')
    ax.set_xlabel('power cap (W)')
    ax.set_title(f"Energy to Solution for {label}")
    ymin = min(min(ETS_full),min(ETS_part))*0.95
    ymax = max(max(ETS_full),max(ETS_part))*1.01
    ax.set_ylim(ymin, ymax)
    ax.legend(loc='lower right')
    plt.savefig(f'{label}_ets.png')

    # plot: relative time and energy to solution at different power caps
    fig, ax = plt.subplots()

    width = 6
    offset = 3
    ax.bar([cap[i]-offset for i in range(n)], speedup, width, color='blue',label="relative TTS")
    ax.bar([cap[i]+offset/2 for i in range(n)], EFF_full, width/2, color='red', label="relative ETS 128/cab")
    ax.bar([cap[i]+offset*3/2 for i in range(n)], EFF_part, width/2, color='green', label="relative ETS 112/cab")
    ax.set_xlabel('power cap (W)')
    ax.legend(loc='upper left')
    ax.set_title(f"Relative TTS and ETS for {label}")
    ax.yaxis.grid(True)
    ax.axhline(y=0, color='black')
    plt.savefig(f'{label}_relative.png')

report_cab("icon-sol")
report_cab("icon-acc")

#plt.plot(powercap, mintime)
#plt.plot(powercap, maxtime)
#plt.plot(powercap, meantime)

#plt.ylim(0, 530)
plt.show()
