#! pip install simulus
from enum import Enum
import simulus
import random
from collections import namedtuple
from matplotlib import pyplot as plt

class QueueStats: 
    max_time = 10800 #6 hours of the bus running 4:00 pm - 10:00 pm?? #set this to be much bigger
    van_capacity = 12
    num_arrivals = 0
    num_in_system = 0
    num_in_queue = 0
    runs = -1
    storeWait = []
    BatesWait = []
    numTimes = []
    vanMiles = 0

    # BatesArrivals = 0
    # WalmartArrivals = 0
    # KohlsArrivals = 0
    # GoodwillArrivals = 0
    # AuburnPlazaArrivals = 0
    # TargetArrivals = 0
    # LotusArrivals = 0
    BatesWait = []
    LisbonStWait = []
    SquashWait = []
    Sea40Wait = []
    HannafordWait = []
    #SEED = 8675309
    debug = True

''' allows Leg to be used as a type, which can then facilitiate accessing
    .from_ and .to_ for readability (rather than [0] and [1])
  Example:
    leg = Leg("a","b")
    print(f"{leg.from_}")   # prints 'a'
    print(f"{leg.to_}")     # prints 'b'
'''
Leg = namedtuple("Leg", "from_ to_")  # "from" is a keyword -- can't use

class Route:
    ''' class to implement data structure for storing the route'''
    __slots__ = ('_route')

    def __init__(self) -> None:
        self._route : dict[Leg, list] = self._initializeRoute()
        
    def _initializeRoute(self) -> dict[Leg, list]:
        ''' initializes the route dictionary, where keys are Leg namedtuples
            (from_, to_) and the values are the expected time between from_
            and _to
        Returns:
            a dictionary of Leg:list[float,int,int] (key:value) entries
        '''
        # (distance in miles, time in minutes, routetype == Auburn, Lewiston)
        route = {}
        # route[Leg(Stop.Bates,       Stop.Walmart)]      =  [2.64,7,0]
        # route[Leg(Stop.Walmart,     Stop.Kohls)]        =  [0.362,2,0]
        # route[Leg(Stop.Kohls,       Stop.Goodwill)]     =  [0.314,1,0]
        # route[Leg(Stop.Goodwill,    Stop.AuburnPlaza)]  =  [0.565,3,0]
        # route[Leg(Stop.AuburnPlaza, Stop.Target)]       =  [0.308,2,0]
        # route[Leg(Stop.Target,      Stop.Lotus)]        =  [0.975,3,0]
        # route[Leg(Stop.Lotus,       Stop.Bates)]        =  [2.39,5,0]
        # route[Leg(Stop.Bates,       Stop.LisbonSt)]     =  [1.14,4,1]
        # route[Leg(Stop.LisbonSt,    Stop.Squash)]       =  [3.1,7,1]
        # route[Leg(Stop.Squash,      Stop.Sea40)]        =  [2.42,6,1]
        # route[Leg(Stop.Sea40,       Stop.Hannaford)]    =  [1.89,6,1]
        # route[Leg(Stop.Hannaford,   Stop.Bates)]        =  [1.34,4,1]
        # route[Leg(Bates,       Walmart)]      =  [2.64,7,0]
        # route[Leg(Walmart,     Kohls)]        =  [0.362,2,0]
        # route[Leg(Kohls,       Goodwill)]     =  [0.314,1,0]
        # route[Leg(Goodwill,    AuburnPlaza)]  =  [0.565,3,0]
        # route[Leg(AuburnPlaza, Target)]       =  [0.308,2,0]
        # route[Leg(Target,      Lotus)]        =  [0.975,3,0]
        # route[Leg(Lotus,       Bates)]        =  [2.39,5,0]
        route[Leg(Bates,       LisbonSt)]     =  [1.14,4,1]
        route[Leg(LisbonSt,    Squash)]       =  [3.1,7,1]
        route[Leg(Squash,      Sea40)]        =  [2.42,6,1]
        route[Leg(Sea40,       Hannaford)]    =  [1.89,6,1]
        route[Leg(Hannaford,   Bates)]        =  [1.34,4,1]
        return route

    def getLegDistance(self, from_, to_) -> float:
        ''' returns the expected distance of one leg in the route
        Parameters:
            from_: a valid Stop entry (see Stop enumeration)
            to_:   a valid Stop entry (see Stop enumeration)
        Returns:
            floating-point value of expected distance in miles on that leg
        Raise:
            KeyError Exception if Stops do not form a valid Leg tuple
        '''
        return self._route[Leg(from_, to_)][0]

    def getLegTime(self, from_, to_) -> int:
        ''' returns the expected time of one leg in the route
        Parameters:
            from_: a valid Stop entry (see Stop enumeration)
            to_:   a valid Stop entry (see Stop enumeration)
        Returns:
            integer value of expected travel time on that leg
        Raise:
            KeyError Exception if Stops do not form a valid Leg tuple
        '''
        return self._route[Leg(from_, to_)][1]
      
    def getLegRouteType(self, from_, to_) -> int:
        ''' returns the route type one leg in the route
        Parameters:
            from_: a valid Stop entry (see Stop enumeration)
            to_:   a valid Stop entry (see Stop enumeration)
        Returns:
            integer value representing the route type of that leg, 0 being Auburn,
            1 being Lewiston
        Raise:
            KeyError Exception if Stops do not form a valid Leg tuple
        '''
        return self._route[Leg(from_, to_)][2]

    def __str__(self) -> str:
        ''' returns a string representation of the routes dictionary '''
        route_str = ""
        for leg,stats in self._route.items():
            route_str += f"{leg.from_:<10} to {leg.to_:<10}: {stats[0]}\n"
        return route_str.strip()


class Van:
    __slots__ = ('capacity', 'stops', 'riders', 'current_stop_index') #, 'city'
    def __init__(self, capacity, stops): #city
        self.capacity = capacity
        self.stops = stops
        self.riders = []
        self.current_stop_index = 0
        #self.city = city

    def move_to_next_stop(self):
        '''moves the bus to the next stop in the order. It also handles picking up and
            dropping off riders going to and coming from their destination. The van is moved by
            indexing through the stops list. Wait times for riders at their destination are also 
            calculated. 
        '''
        current_stop = self.stops[self.current_stop_index]
        if queue_stats.debug: print(f'\n{current_stop.name}')

        if queue_stats.debug: print(f"The bus has {len(self.riders)} riders")
        if queue_stats.debug: print(f"{current_stop.name} has {len(current_stop.inQueue)} riders waiting")
        if queue_stats.debug: print(f"{current_stop.name} has {len(current_stop.Inside)} riders inside")
        # Drop off any riders whose destination is the current stop
        for rider in self.riders[:]:
            if rider.destination == current_stop:
                self.riders.remove(rider)
                current_stop.debus(rider)
                rider.times.append(sim.now)
            elif queue_stats.debug:
                print(f"Rider with destination {rider.destination.name} stays on the bus.")
        # Board new riders waiting at the current stop
        while len(self.riders) < self.capacity and current_stop.inQueue:
            new_rider = current_stop.inQueue[0]
            current_stop.remove_rider(new_rider)
            self.riders.append(new_rider)
            new_rider.times.append(sim.now)

            #update each of the waiting lists in queue_stats. Calculates and stores the amount of time that each person had to wait for the bus (time in  the outside queue until the bus comes)
            WaitList = [queue_stats.BatesWait, queue_stats.LisbonStWait, queue_stats.SquashWait, queue_stats.Sea40Wait, queue_stats.HannafordWait]
            waitTimestore = new_rider.times[-1] - new_rider.times[-2]
            WaitList[self.current_stop_index].append(waitTimestore)
            # waitTime = new_rider.times[-1] - new_rider.times[-2]
            # waitList = [queue_stats.WalmartWait, queue_stats.KohlsWait]
            # waitList[self.current_stop_index].append(waitTime)
        #update total miles traveled by the van
        # Move to the next stop
        self.current_stop_index = (self.current_stop_index + 1) % len(self.stops)
        if queue_stats.debug: print(f"The bus has {len(self.riders)} riders")
        if queue_stats.debug: print(f"{current_stop.name} has {len(current_stop.inQueue)} riders waiting")
        if queue_stats.debug: print(f"{current_stop.name} has {len(current_stop.Inside)} riders inside")

class ShuttleStop:
    def __init__(self, name):
        self.name = name
        self.Inside = []
        self.inQueue = []

    def anyoneLeft(self) -> bool:
        return len(self.Inside) > 0 or len(self.inQueue) > 0

    def debus(self, rider):
        '''If the current stop the bus is not bates and the bus is at their destination, this function adds them
            to the list that contains people that are inside that specific store. It then adds the current drop-off
            time to the person's data, and schedules a pick up time for the person by adding the storeTime() function 
            to the current time. 
        '''
        if self == Bates:
            statsCalc(rider)
        else:
            self.Inside.append(rider)
            rider.times.append(sim.now)
            sim.sched(exitStore, self, rider, until = sim.now + storeTime())
            if queue_stats.debug: print(f"One rider is added to inside {self.name}")

    def add_rider(self, rider):
        '''Adds a rider to the store's outside queue, where they wait for the Van to arrive the next time around the loop. 
        '''
        self.inQueue.append(rider)
        if queue_stats.debug: print(f"One rider is added to {self.name}'s queue")

    def remove_rider(self, rider):
        '''Removes rider from the Store's queue (would occur when the person is picked up. )
        '''
        self.inQueue.remove(rider)
        if queue_stats.debug: print("One rider is added to the bus")

    def inQueue(self, rider):
        ''''When the person is finished at the store, removes them from the list of people inside the stores, and moves them into the 
            the queue list where they are waiting for the Van. Also appends the current time (when they start waiting for the bus) in order
            to calculate wait times.
        '''
        self.Inside.remove(rider)
        self.inQueue.append(rider)
        rider.times.append(sim.now)

class Person:
    def __init__(self, source = None, destination = None, arrival = None):
        self.source = source
        self.destination = destination
        self.times = [arrival]
        self.inStore = storeTime()

def interarrival() -> float:
    '''
    Returns: Gets interarrival time from a random exponential distribution with rate of 0.1, which means that an arrival should come approximately every 10 minutes.
    '''
    return random.expovariate(0.1)

def driveTime(routeTime) -> float:
    '''
    Returns: Calculated time from the from_ and to_ locations. Adds a random amount of time to the drive time to account for variation in drive time and 
                pickup/dropoff time.
    '''
    return routeTime + random.uniform(1, 5) #Add some random noise to account for pickup and dropoff time

def storeTime():
    '''Amount of time a rider spends in the store.
    returns: 
    '''
    while True:
        randStoreTime = random.normalvariate(30,0.75)
        if randStoreTime > 0:
            return randStoreTime

def exitStore(stop: ShuttleStop, person: Person):
    '''moves person at particular stop from inside waiting list to the outside queue, where they will 
        wait to get picked up.
    '''
    print(f"A person is moved to waiting queue at {stop.name}")
    person.destination = Bates
    person.source = stop
    stop.Inside.remove(person)
    stop.inQueue.append(person)
    person.times.append(sim.now)
    #return lambda: stop.inQueue(rider=person)
    #stop.inQueue(rider=person)
    # person.destination = Bates
    # person.source = stop

def statsCalc(person: Person):
    '''Calculates some queueing statistics
    '''
    Wait_at_store = person.times[4] - person.times[3]
    Wait_at_Bates = person.times[1] - person.times[0]
    queue_stats.storeWait.append(Wait_at_store)
    queue_stats.BatesWait.append(Wait_at_Bates)
    queue_stats.numTimes.append(len(person.times))

def handleStop(van: Van):
    '''moves the van from location to location by scheduling a stop using simulus. Schedules another handleStop
        if the maximum time is not up.
    '''
    # stop_list = ['Bates','Walmart','Kohls','Goodwill','AuburnPlaza','Target','Lotus']
    # loc = Van._source
    # index = stop_list.index(loc)
    # dest = stop_list[index + 1]
    # Van.updateLoc(loc,dest)
    from_ = van.stops[van.current_stop_index]
    to_ = van.stops[(van.current_stop_index + 1) % len(van.stops)]
    timeBetween = route.getLegTime(from_, to_)

    #update the total miles the van traveled statistic inside the queue_stats using the getLetDistance() function
    queue_stats.vanMiles += route.getLegDistance(from_, to_) # I ADDED 
    

    if from_ == Bates:
        queue_stats.runs += 1

    van.move_to_next_stop()
    print(f"The bus will take {driveTime(timeBetween)} minutes to drive from {from_.name} to {to_.name}")
    
    #if the current time is less than the designated stopping time, schedule another arrival
    if sim.now < queue_stats.max_time:
        sim.sched(handleStop, van, until = sim.now + driveTime(timeBetween))
    else:
        for stop in van.stops:
            if stop.anyoneLeft():
                 sim.sched(handleStop, van, until = sim.now + driveTime(timeBetween))
                 break #leave the for loop if you find any non-zero length queue @ any stop
               

def arrival():
    '''Schedules arrival, choses random destination from the list for each arrival
    '''
    global num_people
    global people

    #if random.randint(0,1) == City.AUBURN:
    stops = [Bates, LisbonSt, Squash, Sea40, Hannaford]
    dest = random.choice(stops[1:])
    p = Person(source=Bates, destination=dest, arrival=sim.now)
    people.append(p)
    Bates.add_rider(p)
    num_people += 1

    #print(f"{p._id} has arrived at {sim.now}")

    if sim.now < queue_stats.max_time: #- 100
        sim.sched(arrival, offset = interarrival())
    #add else statement to pick people up still in the queue



sim = simulus.simulator()
queue_stats = QueueStats()


#define each stop
Bates = ShuttleStop('Bates')
LisbonSt = ShuttleStop('LisbonSt')
Squash = ShuttleStop('Squash')
Sea40 = ShuttleStop('Sea40')
Hannaford = ShuttleStop('Hannaford')
stops = [Bates, LisbonSt, Squash, Sea40, Hannaford]

route = Route()

Van1 = Van(capacity = queue_stats.van_capacity, stops = stops)

num_people = 0
people : list[Person] = []

#random.seed(8675309)

#sim.sched(handleStop, Van1, until = sim.now + 10)
#sim.sched(arrival, until = sim.now + interarrival())
#sim.run()

BatesWaitList = []
#for i in range(100):

sim.sched(handleStop, Van1, until = sim.now + 10)
sim.sched(arrival, until = sim.now + interarrival()) 
sim.run()


print("__________________________")

'''
print(len(Bates.inQueue))
print(len(Bates.Inside))
print(len(Walmart.inQueue))
print(len(Kohls.inQueue))
print(len(Goodwill.inQueue))
print(len(AuburnPlaza.inQueue))
print(len(Target.inQueue))
print(len(Lotus.inQueue))
print("INSIDE")
print(len(Bates.Inside))
print(len(Walmart.Inside))
print(len(Kohls.Inside))
print(len(Goodwill.Inside))
print(len(AuburnPlaza.Inside))
print(len(Target.Inside))
print(len(Lotus.Inside))
'''




# meanBatesWait = sum(queue_stats.BatesWait)/len(queue_stats.BatesWait)
# meanStoreWait = sum(queue_stats.storeWait)/len(queue_stats.storeWait)

#FOR 12 PERSON VAN
# calculate CO2 emissions per rider
# 2022 Ford Transit Passenger Wagon Van = 15 MPG or 6.38 liters per 100 kilometers
#carbon emissions for gasoline = ~2.31 kg/L
distanceKm = queue_stats.vanMiles * 1.609
amountFuelUsed = distanceKm / 6.38
totalCarbonEmissions = amountFuelUsed * 2.31 #kg CO2 emitted for gasoline
co2PerRider = totalCarbonEmissions / num_people 

#FOR 6 PERSON VAN
distanceKm2 = queue_stats.vanMiles * 1.609
amountFuelUsed2 = distanceKm2 / 9.353
totalCarbonEmissions2 = amountFuelUsed2 * 2.31
co2PerRider2 = totalCarbonEmissions2 / num_people


#create histograms
figure, axis = plt.subplots(4, 2)


plt.hist(queue_stats.BatesWait)
plt.title("Bates Wait Times")
plt.show()

plt.hist(queue_stats.LisbonStWait)
plt.title("LisbonSt Wait Times")
plt.show()

plt.hist(queue_stats.SquashWait)
plt.title("Squash Wait Times")
plt.show()

plt.hist(queue_stats.Sea40Wait)
plt.title("Sea40 Wait Times")
plt.show()

plt.hist(queue_stats.HannafordWait)
plt.title("Hannaford Wait Times")
plt.show()


print("VAN STATS:")
print(f"Distance traveled by van (miles)             : {queue_stats.vanMiles}")
print(f"Number of loops driven by van                : {queue_stats.runs}")
print(f"Total number of riders was                   : {num_people}")
print(f"Total Carbon Emissions for time period (kg)  : {totalCarbonEmissions}")
print(f"Average co2 emissions per rider (kg)         : {co2PerRider} ")


print(" ")
print(f"AVERAGE WAIT TIMES:")
Waits = ["BatesWait", "LisbonStWait", "SquashWait", "Sea40Wait", "HannafordWait"]

for w in Waits:
  denom =  f"len(queue_stats.{w})"
  denomact = eval(denom)
  if denomact == 0:
    pass
  else:
    eval_strw = f"sum(queue_stats.{w})/len(queue_stats.{w})"
    computed_waitw = eval(eval_strw)
    print(f"The average wait at {w[:-4]}            : {computed_waitw:.3f}")


