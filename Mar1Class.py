
#run python -m pip install simulus in Terminal FIRST

import simulus


# Example in class, creating our own event driven simulation in Python, just like we talked about on Monday

#below is the actual code for this psuedo code

###if arrival:
#  n(t) ++
#  if n(t) == 1:
#    service time
#    schedule a completeion of service
#  schedule a new arrival

  


# n(t) = number in the system


class QueueStats: #writing a class 
  num_in_system = 0

def getInterarrival() -> float:
  return random.expovariate(1.0)

def getService() -> float: #returns a float
  return random.expovariate(10/9) #has to be faster than the arrival rate or things wil get backed up

def arrival(queue_stats: QueueStats, show_output: bool = True) -> None: #show output is a boolean that automatically evaluates to true unless we specifiy otherwise
    if show_output: print(f"Arrival @ {sim.now}"): 
      queue_stats.num_in_system += 1 #like n(t) += 1
    if queue_stats.num_in_system == 1:
      service_time = getService()
      sim.sched(completionOfService, queue_stats, until = sim.now + service_time) #??
    sim.sched(arrival, queue_stats, offset = getInterarrival())  
    
def completionOfService(queue_stats: QueueStats, show_output: bool = True) -> None: #is a departure equal to a complete?
  if show_output: print(f"Completion @ {sim.now}"):
    queue_stats.num_in_system -= 1
  pass


sim = simulus.simulator()

#making an objet out of the class
queue_stats = QueueStats()

sim.sched(arrival, until = sim.now + getInterarrival())


max_time = 100
sim.run(max_time)


#finish completeion of service and then the stats to find the average...
#to find the average in the system, use integration
#should have a skyline plot of the nuber in the system and caculate the area under the curve and divide it by T (the total time)
 
