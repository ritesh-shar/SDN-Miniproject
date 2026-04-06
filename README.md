# Port Status Monitoring Tool (SDN - Topic 13)
A Ryu SDN controller that monitors OpenFlow switch port events in real-time, 
 logs state changes, and alerts on link failures.

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

## References:
- [Ryu SDN Framework](https://ryu.readthedocs.io/)
- [Mininet Walkthrough](https://mininet.org/walkthrough/)
- [OpenFlow 1.3 Spec](https://opennetworking.org/wp-content/uploads/2014/10/openflow-spec-v1.3.0.pdf)

## Test Scenarios:

## Scenario 1: Normal Connectivity
### Controller Started:
Expected Output: Switch Connected + DPID
![Controller Started](Screenshots/Screenshot_1.jpeg)
### Nodes Command:
Expected Output: All Systems in our Network
![Nodes Command](Screenshots/Screenshot_2.jpeg)
### Net Command:
Expected Output: Shows how the systems are connected in our Network
![Net Command](Screenshots/Screenshot_7.jpeg)
### pingall Command:
Expected Output: 0% packet loss, all ports show UP 
![pingall Command](Screenshots/Screenshot_3.jpeg)

## Scenario 2: Link Failure and Recovery
### link s1 s2 down:
Expected Output: triggers ⚠️ ALERT (port DOWN)
![ link s1 s2 down](Screenshots/Screenshot_4.jpeg)
### link s1 s2 up:
Expected Output: triggers ✅ INFO (port UP)
![link s1 s2 up](Screenshots/Screenshot_5.jpeg)
### Final pingall:
Expected Output: 0% packet loss, all ports show UP 
![Final pingall](Screenshots/Screenshot_6.jpeg)

## Log Documents:
```
[2026-04-06 06:46:58] ✅  INFO | Switch 2 | Port 2 (s2-eth2) | Reason: MODIFIED | State: UP
[2026-04-06 06:46:58] ✅  INFO | Switch 2 | Port 2 (s2-eth2) | Reason: DELETED | State: UP
[2026-04-06 06:46:58] ⚠️  ALERT | Switch 1 | Port 2 (s1-eth2) | Reason: DELETED | State: DOWN
```
