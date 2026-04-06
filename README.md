# Port Status Monitoring Tool (SDN - Topic 13)

## Problem Statement
Monitor and log switch port status changes in an SDN network using 
a Ryu OpenFlow controller. Detect port up/down events, generate alerts, 
and display live status.

## Tools Used
- Mininet 2.3.0
- Ryu 4.34 (OpenFlow 1.3)
- Open vSwitch 3.3.4
- Python 3.9

## Topology
- 2 switches (s1, s2) connected linearly
- 2 hosts (h1, h2)
- Remote Ryu controller

## Setup & Execution

### Step 1: Start the Ryu controller
```bash
source ryu-env-39/bin/activate
ryu-manager port_monitor.py
```

### Step 2: Start Mininet (in a new terminal)
```bash
sudo python3 topo.py
```

###Normal connectivity
## Controller Started:
![Controller Started](Screenshots/Screenshot_1.jpg)
## Nodes Command:
![Screenshot2]
## Net Command:
![Screenshot7]
## pingall Command:
![Screenshot3]
## link s1 s2 down:
![Screenshot4]
## link s1 s2 up:
![Screenshot5]
## Final pingall:
![Screenshot6]
