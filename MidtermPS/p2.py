
import simulus
import random
from tabulate import tabulate
from RNG import RNG, Stream

class QueueStats: #writing a class 
  time = []
  area_system = []
  area_queue = []
  num_in_system = 0
  num_in_queue = 0
  arrivals = 0 
  departures = 0
  servertimes = []
  service_times = []
  total_time = 0
  serviceold = 0
  servicenew = 0
  nodecapacity = 0
  rejection = 0
  def show(self):
    print(f"For the service node capacity {self.nodecapacity}:")
    print(f"The number in the system @ the end: {self.num_in_system}")
    print(f"The total number of arrivals: {self.arrivals}")
    print(f"The total number of departures: {self.departures}")
    print(f"The average number in the system: {sum(self.area_system)/self.total_time}")
    print(f"The average queue in the system: {sum(self.area_queue)/self.total_time}")
    print(f"Utilization: {sum(self.servertimes)/self.total_time}")
    print(f"The average sojourn time: {sum(self.area_system)/self.arrivals}")
    print(f"The probability of rejection: {self.rejection/self.arrivals}")
    print("######")
    

    
  

def getInterarrival() -> float: #the arrival process
  return RNG.exponential(1/0.5, Stream.ARRIVAL)

def getService() -> float: #the service process
  #the number of service tasks equal to 1 + η, defined by rng.geometric
  totaltasks = RNG.geometric(0.1, Stream.COMPLETION) + 1 
  totalservicetime = 0.0
  for t in range(totaltasks):
    #the time for each of the service tasks within a service process is,(independent of e.o.) is defined by rng.uniform
    totalservicetime += RNG.uniform(0.1, 0.2, Stream.SERVICE_TASK)
  return totalservicetime


#when someone completes a service
def completionOfService(queue_stats: QueueStats, show_output: bool = False) -> None: #is a departure equal to a complete?
  if show_output: print(f"Completion @ {sim.now}")
  
  #records current time (for step below)
  queue_stats.time.append(sim.now) 
  
  #calculating the area of rectangles (integration) anytime there's a change (completion in this case) in the system
  #to calculate the average num and queue in system
  if len(queue_stats.time) > 1:
    change = (queue_stats.time[-1] - queue_stats.time[-2]) #difference 
    queue_stats.area_system.append(change*queue_stats.num_in_system)
    queue_stats.area_queue.append(change*queue_stats.num_in_queue) #same calculation but for the queue
    
  #updating queue and max queue before we add the depature  
  if queue_stats.num_in_system == 0:
    queue_stats.num_in_queue = 0
    #queue_stats.maxqueue = 0
  elif queue_stats.num_in_system == 1:
    #for utilization (if the server is BUSY), right before there's no one in the system, 
    #servicenew = time when # in system goes from 1 to 0
    queue_stats.servicenew = sim.now 
    #servertimes = area of rectangles for when the system is idle or busy
    queue_stats.servertimes.append(queue_stats.servicenew - queue_stats.serviceold) 
    queue_stats.num_in_queue = queue_stats.num_in_system - 1
    #queue_stats.maxqueue = queue_stats.nodecapacity - 1
  else:
    queue_stats.num_in_queue = queue_stats.num_in_system - 1
    #queue_stats.maxqueue = queue_stats.nodecapacity - 1
  
  #now we actually remove someone from the system, and add them as a departure
  queue_stats.num_in_system -= 1
  queue_stats.departures += 1
  
  #if we've processed max. # of arrivals, record the total simulation time now
  if queue_stats.arrivals == maxArrivals:
    queue_stats.total_time = sim.now
   
  #if there's still more ppl in the system, schedule the next completion of service  
  if queue_stats.num_in_system > 0:
    service_time = getService()
    queue_stats.service_times.append(service_time)
    sim.sched(completionOfService, queue_stats, until = sim.now + service_time) #schedules a time of complete at t + service_time
  else:
    pass


#when someone arrives
def arrival(queue_stats: QueueStats, show_output: bool = False) -> None: #show output is a boolean that automatically evaluates to true unless we specifiy otherwise
    if show_output: print(f"Arrival @ {sim.now}")
      
    #records current time (for step below)
    queue_stats.time.append(sim.now)
    
    #calculating the area of rectangles (integration) anytime there's a change (arrival in this case) in the system
    #to calculate the average num and queue in system
    if len(queue_stats.time) > 1:
      change = (queue_stats.time[-1] - queue_stats.time[-2])
      queue_stats.area_system.append(change*queue_stats.num_in_system)
      queue_stats.area_queue.append(change*queue_stats.num_in_queue) 
    
    #updating queue and max queue before we add the arrival   
    if queue_stats.num_in_system == 0:
      queue_stats.num_in_queue = 0
      #queue_stats.maxqueue = 0
      #for utilization, right before we add someone to system
      #servicold = when # in system goes from 0 to 1
      queue_stats.serviceold = sim.now 
    else:
      queue_stats.num_in_queue = queue_stats.num_in_system - 1 
      #queue_stats.maxqueue = queue_stats.nodecapacity - 1 
      
    
    #now we actually add someone from the system 
    queue_stats.num_in_system += 1
    
    #but if we're at capacity, then remove them from the system
    if queue_stats.num_in_system > queue_stats.nodecapacity:
      queue_stats.departures += 1
      queue_stats.rejection += 1
      queue_stats.num_in_system -= 1
    else: #if we're not, if there's someone in the system, schedule the next completion of service
      if queue_stats.num_in_system == 1: 
        service_time = getService()
        queue_stats.service_times.append(service_time)
        sim.sched(completionOfService, queue_stats, until=sim.now + service_time)
    
    queue_stats.arrivals += 1  
    
    #if we haven't reached max # of arrivals, schedule the next arrival  
    if queue_stats.arrivals < maxArrivals: 
      sim.sched(arrival, queue_stats, offset = getInterarrival()) #starts an arrival at the get interarrival time??? 

    if queue_stats.arrivals == maxArrivals:
      queue_stats.total_time = sim.now

      
       
#code to print table for (a) and (b)  
  
# results = []  
# Capacities = [1, 2, 3, 4, 5, 6]  
# for capacitiy in Capacities:
#   sim = simulus.simulator()
#   #making an object out of the class
#   queue_stats = QueueStats()
#   queue_stats.nodecapacity = capacitiy
#   sim.sched(arrival, queue_stats, until = sim.now + getInterarrival())
#   maxArrivals = 10000
#   sim.run()
#   #queue_stats.show()
#   prob_rejection = queue_stats.rejection/queue_stats.arrivals
#   avg_sojourn = (sum(queue_stats.area_system))/queue_stats.arrivals
#   results.append([capacitiy, prob_rejection, avg_sojourn])
#   
# 
# head = ["Service Node Capacity [Uniform(0.1,0.3)]", "Est. Prob. of Rejection", "Est. Avg. Sojourn Time"]
# print(tabulate(results, headers = head, tablefmt = 'fancy_grid'))
  

#code to save service times, with capacity at 10000, (c)

# sim = simulus.simulator()
# queue_stats = QueueStats()
# sim.sched(arrival, queue_stats, until = sim.now + getInterarrival())
# maxArrivals = 1000000
# sim.run()
# for i in range(len(queue_stats.service_times)):
#   print(queue_stats.service_times[i])





