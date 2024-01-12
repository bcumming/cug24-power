Systems with tightly-integrated CPU and GPU on the same module or package will be deployed in 2024, based on NVIDIA GH200 and AMD Mi300a processors. There are some significant differences from current systems, of which the key ones for this presentation are:
- each processor consumes greater than 650W per component _under normal workloads_, which requires power capping of devices to stay within nominal power limit of 340 kW and 400 kW in the EU and US respectively;
- tight integration of memory between CPU and GPU opens new opportunities for application optimization, and changes some fundamental application design concepts.

Engineers at CSCS and HPE spent a week testing application performance and power consumption at the node and cabinet level on two cabinets in Chippewa Falls, in preparation for the installation of over 10'000 GH200 in the Cray EX system Alps at CSCS.

This pressentation will focus on the results of this work. First, the power measurement at the node and cabinet level, with a detailed description of measurement methodology and the results.  Then performance results of a applications and micro-benchmarks, with discussion on:
- optimizing power consumption and performance;
- time and energy to solution;
- and the counter-intuitive effects of of power sloshing between CPU and GPU.

