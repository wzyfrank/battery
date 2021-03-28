#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from multiprocessing import Process
from optimize import OptimalBatteryDispatch 
from lmp_reader import read_data, get_lmp_with_data

# data wrapper class for the day-ahead optimization problem
# stores battery energy rating, battery power rating and price.
class DayAhead():
    def __init__(self, E, P, pi_energy):
        self.E = E
        self.P = P
        self.pi_energy = pi_energy


# The task for thread to run.
def optimize(threadName, tasks):
    for t in tasks:
        (obj, gamma, result_P, result_E) = OptimalBatteryDispatch(t.pi_energy, t.E, t.P)
        print("The objective value is: %.2f" % obj)
    
class myProcess (Process):
    def __init__(self, processId, name, q):
        Process.__init__(self)
        self.processId = processId
        self.name = name
        self.q = q
        
    def run(self):
        optimize(self.name, self.q)
        
        
if __name__ == "__main__":
    P = 25 # Power rating of battery
    E = 100 # Energy rating of battery
    H = 24 # horizon of the optimization
    seed = 5 # seed number 
    
    # read the electricity price data.
    price_data = read_data()
    
    # Setup multi-thread.
    numProcess = 5
    numJobs = 100
    exitFlag = False
    
    # Split the tasks into processes.
    tasks = []
    seed = 5
    for i in range(numProcess):
        tasks.append([])
    
    for d in range(numJobs):
        pi_energy = get_lmp_with_data(price_data, seed, d)
        opt = DayAhead(E, P, pi_energy)
        tasks[d % numProcess].append(opt)
        
    processPool = []
    processList = []
    for i in range(numProcess):
        processList.append("Process" + str(i))
 
    # Start the threads.

    processId = 0
    for processName in processList:
        print ("Starting %s" % processName) 
        process = myProcess(processId, processName, tasks[processId])
        process.start()
        processPool.append(process)
        processId += 1
    
    
    for t in processPool:
        t.join()
