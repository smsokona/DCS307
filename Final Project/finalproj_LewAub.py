#! pip install simulus
from enum import IntEnum
import simulus
import random
from collections import namedtuple
from matplotlib import pyplot as plt


class City(IntEnum):
    Auburn   = 0
    Lewiston = 1

class AuburnStop(IntEnum):
    BatesA       = 0
    Walmart     = 1
    Kohls       = 2
    Goodwill    = 3
    AuburnPlaza = 4
    Target      = 5
    Lotus       = 6

class LewistonStop(IntEnum):
    BatesL       = 0
    LisbonSt    = 1
    Squash      = 2
    Sea40       = 3
    Hannaford   = 4


class QueueStats: 
    max_time = 10800 #6 hours of the bus running 4:00 pm - 10:00 pm * 30 = 10,800 hours a.k.a. 30 days of running
    num_arrivals = 0
    num_in_system = 0
    num_in_queue = 0
    runsL = -1
    runsA = -1
    storeWait = []
    #BatesWait = []
    numTimes = []
    vanMilesA = 0
    vanMilesL = 0
    num_peopleA = 0
    num_peopleL = 0
    num_loops = 0

    # BatesArrivals = 0
    # WalmartArrivals = 0
    # KohlsArrivals = 0
    # GoodwillArrivals = 0
    # AuburnPlazaArrivals = 0
    # TargetArrivals = 0
    # LotusArrivals = 0
    BatesLWait = []
    BatesAWait = []
    WalmartWait = []
    KohlsWait = []
    GoodwillWait = []
    AuburnPlazaWait = []
    TargetWait = []
    LotusWait = []
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
    __slots__ = ('_route', '_city')

    def __init__(self, city: City) -> None:
        self._city  : City = city
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
        if self._city == City.Auburn:
            route[Leg(BatesA,       Walmart)]      =  [2.64,7,0]
            route[Leg(Walmart,     Kohls)]        =  [0.362,2,0]
            route[Leg(Kohls,       Goodwill)]     =  [0.314,1,0]
            route[Leg(Goodwill,    AuburnPlaza)]  =  [0.565,3,0]
            route[Leg(AuburnPlaza, Target)]       =  [0.308,2,0]
            route[Leg(Target,      Lotus)]        =  [0.975,3,0]
            route[Leg(Lotus,       BatesA)]        =  [2.39,5,0]
        else:
            route[Leg(BatesL,       LisbonSt)]     =  [1.14,4,1]
            route[Leg(LisbonSt,    Squash)]       =  [3.1,7,1]
            route[Leg(Squash,      Sea40)]        =  [2.42,6,1]
            route[Leg(Sea40,       Hannaford)]    =  [1.89,6,1]
            route[Leg(Hannaford,   BatesL)]        =  [1.34,4,1]
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
    __slots__ = ('capacity', 'riders', 'current_stop_index', 'city')
    def __init__(self, capacity: int, city: City):
        self.capacity : int           = capacity
        self.city     : City          = city
        self.riders   : list[Person]  = []
        self.current_stop_index : int = 0

    def move_to_next_stop(self):
        '''moves the bus to the next stop in the order. It also handles picking up and
            dropping off riders going to and coming from their destination. The van is moved by
            indexing through the stops list. Wait times for riders at their destination are also 
            calculated. 
        '''
        this_town_stops = stops[self.city]  # stops is global (below)
        current_stop    = this_town_stops[self.current_stop_index]
        if queue_stats.debug: print(f'\n{current_stop.name}')

        if queue_stats.debug: print(f"The {self.city.name} bus has {len(self.riders)} riders")
        if queue_stats.debug: print(f"{current_stop.name} has {len(current_stop.queue)} riders waiting")
        if queue_stats.debug: print(f"{current_stop.name} has {len(current_stop.inside)} riders inside")
        # Drop off any riders whose destination is the current stop
        for rider in self.riders[:]:
            if rider.destination == current_stop:
                self.riders.remove(rider)
                current_stop.debus(rider)
                rider.times.append(sim.now)
            elif queue_stats.debug:
                print(f"Rider with destination {rider.destination.name} stays on the bus.")
        # Board new riders waiting at the current stop whose city matches the city of the van
        while len(self.riders) < self.capacity and len(current_stop.queue) > 0:
            for rider in current_stop.queue[:]:
                if rider.city == self.city:
                  new_rider = current_stop.queue[0]
                  current_stop.remove_rider(new_rider)
                  self.riders.append(new_rider)
                  new_rider.times.append(sim.now)
                  
                  #update each of the waiting lists in queue_stats. Calculates and stores the amount of time that each person had to wait for the bus (time in  the outside queue until the bus comes)
                  if rider.city == City.Auburn:
                     WaitList = [queue_stats.BatesAWait, queue_stats.WalmartWait, queue_stats.KohlsWait, queue_stats.GoodwillWait, queue_stats.AuburnPlazaWait, queue_stats.TargetWait, queue_stats.LotusWait]
                     waitTimestore = new_rider.times[-1] - new_rider.times[-2]
                     WaitList[self.current_stop_index].append(waitTimestore)
                  else:
                    WaitList = [queue_stats.BatesLWait, queue_stats.LisbonStWait, queue_stats.SquashWait, queue_stats.Sea40Wait, queue_stats.HannafordWait]
                    waitTimestore = new_rider.times[-1] - new_rider.times[-2]
                    WaitList[self.current_stop_index].append(waitTimestore)
                    
                # elif queue_stats.debug:
                #   print(f"Rider with destination in {rider.city.name} waits for other bus.")
            # waitTime = new_rider.times[-1] - new_rider.times[-2]
            # waitList = [queue_stats.WalmartWait, queue_stats.KohlsWait]
            # waitList[self.current_stop_index].append(waitTime)
        #update total miles traveled by the van
        # Move to the next stop
        self.current_stop_index = (self.current_stop_index + 1) % len(this_town_stops)
        if queue_stats.debug: print(f"The {self.city.name} bus has {len(self.riders)} riders")
        if queue_stats.debug: print(f"{current_stop.name} has {len(current_stop.queue)} riders waiting")
        if queue_stats.debug: print(f"{current_stop.name} has {len(current_stop.inside)} riders inside")

class ShuttleStop:
    def __init__(self, name):
        self.name = name
        self.inside = []
        self.queue = []

    def __str__(self) -> str:
        return f"stop: {self.name}  (# in queue:{len(self.queue)})  (# inside:{len(self.inside)})"

    def anyoneLeft(self) -> bool:
        if len(self.inside) > 0 or len(self.queue) > 0:
            return True
        return False

    def debus(self, rider):
        '''If the current stop the bus is not bates and the bus is at their destination, this function adds them
            to the list that contains people that are inside that specific store. It then adds the current drop-off
            time to the person's data, and schedules a pick up time for the person by adding the storeTime() function 
            to the current time. 
        '''
        if self == BatesL or self == BatesA:
            statsCalc(rider)
        else:
            self.inside.append(rider)
            rider.times.append(sim.now)
            sim.sched(exitStore, self, rider, until = sim.now + storeTime())
            if queue_stats.debug: print(f"One rider is added to inside {self.name}")

    def add_rider(self, rider):
        '''Adds a rider to the store's outside queue, where they wait for the Van to arrive the next time around the loop. 
        '''
        self.queue.append(rider)
        if queue_stats.debug: print(f"One rider is added to {self.name}'s queue")

    def remove_rider(self, rider):
        '''Removes rider from the Store's queue (would occur when the person is picked up. )
        '''
        self.queue.remove(rider)
        if queue_stats.debug: print("One rider is added to the bus")

    def inQueue(self, rider):
        ''''When the person is finished at the store, removes them from the list of people inside the stores, and moves them into the 
            the queue list where they are waiting for the Van. Also appends the current time (when they start waiting for the bus) in order
            to calculate wait times.
        '''
        self.inside.remove(rider)
        self.queue.append(rider)
        rider.times.append(sim.now)

class Person:
    # add the city when a person is created so that you can match
    # a person's city to a van's city so the person does not get
    # onto the wrong van
    __slots__ = ('source', 'destination', 'times', 'inStore', 'city')
    def __init__(self, source = None, destination = None, arrival = None, city = None):
        self.source = source
        self.destination = destination
        self.city = city
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
    print(f"A person is moved to waiting queue at {stop.name}")
    if person.city == City.Lewiston:
        person.destination = BatesL
    else:
        person.destination = BatesA
    person.source = stop
    stop.inside.remove(person)
    stop.queue.append(person)
    person.times.append(sim.now)
    #return lambda: stop.inQueue(rider=person)
    #stop.inQueue(rider=person)
    # person.destination = Bates
    # person.source = stop

def statsCalc(person: Person):
    Wait_at_store = person.times[4] - person.times[3]
    queue_stats.storeWait.append(Wait_at_store)
    # Wait_at_Bates = person.times[1] - person.times[0]
    # queue_stats.BatesWait.append(Wait_at_Bates)
    # queue_stats.numTimes.append(len(person.times))

def handleStop(van: Van):
    # stop_list = ['Bates','Walmart','Kohls','Goodwill','AuburnPlaza','Target','Lotus']
    # loc = Van._source
    # index = stop_list.index(loc)
    # dest = stop_list[index + 1]
    # Van.updateLoc(loc,dest)
    this_town_stops = stops[van.city]  # stops is global (below)
    from_ = this_town_stops[van.current_stop_index]
    to_ = this_town_stops[(van.current_stop_index + 1) % len(this_town_stops)]
    timeBetween = routes[van.city].getLegTime(from_, to_)

    #update the total miles the van traveled statistic inside the queue_stats using the getLetDistance() function
    if van.city == City.Auburn:
      queue_stats.vanMilesA += routes[van.city].getLegDistance(from_, to_)  
    else:
      queue_stats.vanMilesL += routes[van.city].getLegDistance(from_, to_)
    

    if from_ == BatesA:
        queue_stats.runsA += 1
    else:
        queue_stats.runsL += 1

    van.move_to_next_stop()
    print(f"The bus will take {driveTime(timeBetween)} minutes to drive from {from_.name} to {to_.name}")
    
    #if the current time is less than the designated stopping time, schedule another arrival
    if sim.now < queue_stats.max_time:
        sim.sched(handleStop, van, until = sim.now + driveTime(timeBetween))
    else:
        for stop in this_town_stops:
            if stop.anyoneLeft():
                sim.sched(handleStop, van, until = sim.now + driveTime(timeBetween))
                break  # leave the for loop if you find any non-zero length queue @ any stop

def arrival():
    global num_people
    global people

    # pick a city at random, and then from the corresponding
    # (global) stops sublist, chose a ShuttleStop destination
    # at random
    city : int = random.choice([City.Auburn, City.Lewiston])
    this_town_stops = stops[city]  # stops is global (below)
    dest : ShuttleStop = random.choice(this_town_stops[1:])
    if city == City.Auburn:
      p = Person(source=BatesA, destination=dest, arrival=sim.now, city=city)
      BatesA.add_rider(p)
      queue_stats.num_peopleA += 1
    else:
      p = Person(source=BatesL, destination=dest, arrival=sim.now, city=city)
      BatesL.add_rider(p)
      queue_stats.num_peopleL += 1
    people.append(p)
    #num_people += 1

    #print(f"{p._id} has arrived at {sim.now}")

    if sim.now < queue_stats.max_time: #- 100
        sim.sched(arrival, offset = interarrival())


# Example usage
# stop_a = ShuttleStop('Stop A')  (These are created by for loops below)
# stop_b = ShuttleStop('Stop B')
# stop_c = ShuttleStop('Stop C')
# stop_a.add_rider(Person(source=stop_a, destination=stop_c, generate_time=0))
# stop_a.add_rider(Person(source=stop_a, destination=stop_b, generate_time=0))
# stop_b.add_rider(Person(source=stop_b, destination=stop_a, generate_time=1))
# bus = Van(capacity=2, city=City.Auburn)
# bus.move_to_next_stop()  # Riders 1 and 2 board the bus
# bus.move_to_next_stop()  # Rider 3 boards the bus, rider 1 disembarks
# bus.move_to_next_stop()  # Rider 2 disembarks, no new riders

sim = simulus.simulator()
queue_stats = QueueStats()

#if queue_stats.SEED is not None:
#    random.seed(queue_stats.SEED)

auburn_stops   = []
lewiston_stops = []
# this for loop will create a ShuttleStop object for each entry in the
# enumeration AuburnStop, and will append that object to the auburn_stops list
for stop in AuburnStop:
    exec_str_make_ShuttleStop   = f"{stop.name} = ShuttleStop({repr(stop.name)})"
    exec_str_append_ShuttleStop = f"auburn_stops.append({stop.name})"
    exec(exec_str_make_ShuttleStop)
    exec(exec_str_append_ShuttleStop)
# similar to above, but for Lewiston
for stop in LewistonStop:
    exec_str_make_ShuttleStop = f"{stop.name} = ShuttleStop({repr(stop.name)})"
    exec_str_append_ShuttleStop = f"lewiston_stops.append({stop.name})"
    exec(exec_str_make_ShuttleStop)
    exec(exec_str_append_ShuttleStop)

# confirm that the lists of ShuttleStops are built and available
#print([str(stop) for stop in auburn_stops])
#print([str(stop) for stop in lewiston_stops])


# routes will be a list of Route objects.  Each Route object is
# created according to the particular city, and will be accessible
# from inside the routes list using the City enum, e.g.
#           auburn_routes = routes[City.Auburn]
# or if you have the city stored as an instance variable in some
# other object (e.g., Van), 
#           auburn_routes = routes[self.city]
# Similarly, stops is a global list of two lists of ShuttleStops.
routes : list[Route] = [Route(City.Auburn), Route(City.Lewiston)]
stops  : list[ list[ShuttleStop] ] = [auburn_stops, lewiston_stops]

van1 = Van(capacity = 12, city = City.Auburn)
van2 = Van(capacity = 6,  city = City.Lewiston)


# num_peopleA = 0
# num_peopleL = 0
people : list[Person] = []

sim.sched(handleStop, van1, until = sim.now + 10)
sim.sched(handleStop, van2, until = sim.now + 10)
sim.sched(arrival, until = sim.now + interarrival())
sim.run()


#to check if there's anyone left in the queue or the stores at the end of the simulation
# print("__________________________")
# print(len(BatesL.queue))
# print(len(BatesA.queue))
# print(len(Walmart.queue))
# print(len(Kohls.queue))
# print(len(Goodwill.queue))
# print(len(AuburnPlaza.queue))
# print(len(Target.queue))
# print(len(Lotus.queue))
# print("INSIDE")
# print(len(BatesL.inside))
# print(len(BatesA.inside))
# print(len(Walmart.inside))
# print(len(Kohls.inside))
# print(len(Goodwill.inside))
# print(len(AuburnPlaza.inside))
# print(len(Target.inside))
# print(len(Lotus.inside))



#FOR 12 PERSON VAN
# calculate CO2 emissions per rider
# 2022 Ford Transit Passenger Wagon Van = 15 MPG or 6.38 liters per 100 kilometers
#carbon emissions for gasoline = ~2.31 kg/L
distanceKm = queue_stats.vanMilesA * 1.609
amountFuelUsed = distanceKm / 6.38
totalCarbonEmissions = amountFuelUsed * 2.31 #kg CO2 emitted for gasoline
co2PerRider = totalCarbonEmissions / queue_stats.num_peopleA 

#FOR 6 PERSON VAN
distanceKm2 = queue_stats.vanMilesL * 1.609
amountFuelUsed2 = distanceKm2 / 9.353
totalCarbonEmissions2 = amountFuelUsed2 * 2.31
co2PerRider2 = totalCarbonEmissions2 / queue_stats.num_peopleL


#create histograms
#figure, axis = plt.subplots(4, 2)

plt.hist(queue_stats.BatesAWait)
plt.title("Bates Wait (going to Auburn) Times")
plt.show()

plt.hist(queue_stats.BatesLWait)
plt.title("Bates Wait (going to Lewiston) Times")
plt.show()

plt.hist(queue_stats.WalmartWait)
plt.title("Walmart Wait Times")
plt.show()

plt.hist(queue_stats.KohlsWait)
plt.title("Kohls Wait Times")
plt.show()

plt.hist(queue_stats.GoodwillWait)
plt.title("Goodwill Wait Times")
plt.show()

plt.hist(queue_stats.AuburnPlazaWait)
plt.title("Auburn Plaza Wait Times")
plt.show()

plt.hist(queue_stats.TargetWait)
plt.title("Target Wait Times")
plt.show()

plt.hist(queue_stats.LotusWait)
plt.title("Lotus Wait Times")
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


print("AUBURN VAN STATS:")
print(f"Distance traveled by van (miles)             : {queue_stats.vanMilesA}")
print(f"Number of loops driven by van                : {queue_stats.runsA}")
print(f"Total number of riders was                   : {queue_stats.num_peopleA}")
print(f"Total Carbon Emissions for time period (kg)  : {totalCarbonEmissions}")
print(f"Average co2 emissions per rider (kg)         : {co2PerRider} ")
print(" ")
print("LEWISTON VAN STATS:")
print(f"Distance traveled by van (miles)             : {queue_stats.vanMilesL}")
print(f"Number of loops driven by van                : {queue_stats.runsL}")
print(f"Total number of riders was                   : {queue_stats.num_peopleL}")
print(f"Total Carbon Emissions for time period (kg)  : {totalCarbonEmissions2}")
print(f"Average co2 emissions per rider (kg)         : {co2PerRider2} ")


print(" ")
print(f"AVERAGE WAIT TIMES:")
Waits = ["BatesAWait", "BatesLWait", "WalmartWait", "KohlsWait", "GoodwillWait", "AuburnPlazaWait", "TargetWait", "LotusWait", "LisbonStWait", "SquashWait", "Sea40Wait", "HannafordWait"]

for w in Waits:
  denom =  f"len(queue_stats.{w})"
  denomact = eval(denom)
  if denomact == 0:
    pass
  else:
    eval_strw = f"sum(queue_stats.{w})/len(queue_stats.{w})"
    computed_waitw = eval(eval_strw)
    print(f"The average wait at {w[:-4]}: {computed_waitw:.3f}")
