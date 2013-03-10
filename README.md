Setup MPTCP and POX
===================

Installing MPTCP on Ubuntu 12.10 (EC2)
--------------------------------------

Run the following:

`sudo ./install_mptcp_quantal.sh` 

Read the output! There is some manual verification and rebooting to be done.       

### Verify MPTCP works properly
This script configures the routing tables automatically, and should 
yield throughput proportional to n, the number of interfaces.

Running a throughput test:

* MPTCP disabled; bandwidth should be around 10Mbps

`sudo ./test_mptcp.py --bw 10`

* MPTCP enabled with two flows; bandwidth should be around 20Mbps

`sudo ./test_mptcp.py --bw 10 --mptcp -n 2`

Installing RiplPox and its dependencies
---------------------------------------

Run the following:

`sudo ./install_pox.sh`

### Verify RiplPox works properly
Testing the controller with a FatTree topology using ECMP routing

`sudo ./ecmp_routing.py`

The script runs a ping reachability test between all hosts. The test should pass (no X's). 
Then, it opens the Mininet CLI where you can run your tests. Type `exit` to quit, and the 
script will tear down everything.

Other things to install
-----------------------

Install **sysstat** to view system utilization information

`sudo apt-get install sysstat`
