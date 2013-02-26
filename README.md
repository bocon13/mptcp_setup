mptcp_setup
===========

Setup and Verify MPTCP on Ubuntu 12.10 (EC2)

First run install script. Then test

This is modified from:
git clone git://gist.github.com/2730049.git
bash 2730049/install_mptcp_precise.sh
and
https://github.com/mininet/mininet-tests
dir: mininet-tests/mptcp/ 

== Running a throughput test:

sudo ./mptcp_test.py --bw 10 --mptcp -n 2

This script configures the routing tables automatically, and should 
yield throughput proportional to n, the number of interfaces.
