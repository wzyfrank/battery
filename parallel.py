#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import threading
import queue
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
def optimize(threadName, q):
    while not exitFlag:
        queueLock.acquire()
        if not q.empty():
            data = q.get();
            (obj, gamma, result_P, result_E) = OptimalBatteryDispatch(data.pi_energy, data.E, data.P)
            print("The objective value is: %.2f" % obj)
            queueLock.release()
        else:
            queueLock.release()

    
class myThread (threading.Thread):
    def __init__(self, threadId, name, q):
        threading.Thread.__init__(self)
        self.threadId = threadId
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
    numThread = 5
    numJobs = 100
    exitFlag = False
    queueLock = threading.Lock()
    threadPool = []
    
    threadList = []
    for i in range(numThread):
        threadList.append("Thread" + str(i))
 
    # Start the threads.
    workQueue = queue.Queue(200)
    threadId = 1
    for threadName in threadList:
        print ("Starting %s" % threadName) 
        thread = myThread(threadId, threadName, workQueue)
        thread.start()
        threadPool.append(thread)
        threadId += 1
    
    # Add the tasks to the queue.
    queueLock.acquire()
    seed = 5
    for d in range(numJobs):
        pi_energy = get_lmp_with_data(price_data, seed, d)
        opt = DayAhead(E, P, pi_energy)
        workQueue.put(opt)
    queueLock.release()
    
    # Process until the queue is empty.
    while not workQueue.empty():
        pass
    exitFlag = True
    
    for t in threadPool:
        t.join()
