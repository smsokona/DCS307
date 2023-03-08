#run python -m pip install simulus in Terminal FIRST

import simulus
import random


class QueueStats: #writing a class 
  time = []
  area_system = []
  area_queue = []
  num_in_system = 0
  num_in_queue = 0
  arrivals = 0 
  departures = 0
  servertimes = []
  total_time = 0
  serviceold = 0
  servicenew = 0
  def show(self):
    print(f"The number in the system @ the end: {self.num_in_system}")
    print(f"The total number of arrivals: {self.arrivals}")
    print(f"The total number of departures: {self.departures}")
    print(f"The average number in the system: {sum(self.area_system)/self.total_time}")
    print(f"The average queue in the system: {sum(self.area_queue)/self.total_time}")
    print(f"Utilization: {sum(self.servertimes)/self.total_time}")
    

    
  

def getInterarrival() -> float:
  return random.expovariate(1.0)

def getService() -> float: #returns a float
  return random.expovariate(10/9) #has to be faster than the arrival rate or things wil get backed up

def completionOfService(queue_stats: QueueStats, show_output: bool = False) -> None: #is a departure equal to a complete?
  if show_output: print(f"Completion @ {sim.now}")
  
  queue_stats.time.append(sim.now) #to calculate the average num and queue in system
  if len(queue_stats.time) > 1:
    change = (queue_stats.time[-1] - queue_stats.time[-2])
    queue_stats.area_system.append(change*queue_stats.num_in_system) #calculating rectangles (integration) anytime there's a change in the system
    queue_stats.area_queue.append(change*queue_stats.num_in_queue) #same calculation but for the queue
    
  if queue_stats.num_in_system == 0:
    queue_stats.num_in_queue = 0
  elif queue_stats.num_in_system == 1:
    queue_stats.servicenew = sim.now #for utilization, right before there's no one in the system
    queue_stats.servertimes.append(queue_stats.servicenew - queue_stats.serviceold)
    queue_stats.num_in_queue = queue_stats.num_in_system - 1
  else:
    queue_stats.num_in_queue = queue_stats.num_in_system - 1
  
  queue_stats.num_in_system -= 1
  queue_stats.departures += 1
  if queue_stats.departures == maxArrivals:
    queue_stats.total_time = sim.now
    
  if queue_stats.num_in_system > 0:
    service_time = getService()
    sim.sched(completionOfService, queue_stats, until = sim.now + service_time) #schedules a time of complete at t + service_time
  else:
    pass



def arrival(queue_stats: QueueStats, show_output: bool = False) -> None: #show output is a boolean that automatically evaluates to true unless we specifiy otherwise
    if show_output: print(f"Arrival @ {sim.now}")
      
    queue_stats.time.append(sim.now)
    if len(queue_stats.time) > 1:
      change = (queue_stats.time[-1] - queue_stats.time[-2])
      queue_stats.area_system.append(change*queue_stats.num_in_system) #calculating rectangles (integration) anytime there's a change in the system
      queue_stats.area_queue.append(change*queue_stats.num_in_queue) #same calculation but for the queue
      
    if queue_stats.num_in_system == 0:
      queue_stats.num_in_queue = 0
      queue_stats.serviceold = sim.now #for utilization, right before we add someone to system
    else:
      queue_stats.num_in_queue = queue_stats.num_in_system - 1  
      
    queue_stats.num_in_system += 1 #like n(t) += 1
    queue_stats.arrivals += 1 
    if queue_stats.num_in_system == 1: 
      service_time = getService()
      sim.sched(completionOfService, queue_stats, until = sim.now + service_time) #schedules a time of complete at t + service_time
      
    if queue_stats.arrivals < maxArrivals: #to ensure we're not doing more than max arrivlas
      sim.sched(arrival, queue_stats, offset = getInterarrival()) #starts an arrival at the get interarrival time??? 

    # if len(arrivals) > 1:
    #   area_system.append(arrivals[-1] - arrivals[-2])
    


sim = simulus.simulator()

#making an object out of the class
queue_stats = QueueStats()

sim.sched(arrival, queue_stats, until = sim.now + getInterarrival())


maxArrivals = 10000
sim.run()
queue_stats.show()


