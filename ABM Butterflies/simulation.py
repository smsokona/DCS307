from room import Room
from person import Person, Type
from calendar import Calendar
import simulus
import random

#################################################################
class Parameters:
    ''' simple class to define simulation parameter values '''
    CLEAR_SCREEN = True
    DEBUG = False

    MAX_T = 500
    ROOM_ROWS = 20
    ROOM_COLS = 15
    MAX_PEOPLE = (ROOM_ROWS * ROOM_COLS) // 3
    PROP_BUTTERFLIES = 0.5

    SEED = 8675309  # or None

    PRINT_DELAY = 0.001
#################################################################

def interarrival() -> float:
    return random.expovariate(1.0)

def intermove() -> float:
    return random.uniform(0.5, 2.5)

def arrival(debug: bool = False) -> None:
    ''' function to handle an arrival of a Person to the Room
    Parameters:
        debug: if True, prints debugging information
    '''
    global num_people
    global people
    # new person shows up at the Room's entry location; 
    # make sure there is no one in the entry, otherwise reject
    if not Room.isEntryOccupied(): # checks if the entry is already occupied
        p = Person(Parameters.PROP_BUTTERFLIES)
        people.append(p)
        Room.show(sim.now, clear_screen = Parameters.CLEAR_SCREEN, delay = Parameters.PRINT_DELAY)
        if debug: print(f"\t{p} arrives @ {sim.now:.3f}") #prints if DEBUG = TRUE
        if debug: print(f"\t{p} @ ({p.row()},{p.col()}) scheduled to move @ {sim.now:.3f}")
        # upon arrival, schedule an immediate movement for this Person
        sim.sched(move, p, Parameters.DEBUG, until = sim.now)
        num_people += 1
    else:
        print(f"\tNo arrival allowed -- entry is filled")

    # schedule the next arrival only if not at maximum Room capacity
    if num_people < Parameters.MAX_PEOPLE:
        sim.sched(arrival, Parameters.DEBUG, offset = interarrival())

    if debug: Calendar.printCalendar(sim)

def move(p: Person, debug: bool = False) -> None:
    ''' function to handle movement of a given Person
    Parameters:
        person: the Person object that is moving
        debug: if True, prints debugging information
    '''
    p.move()  # call the Person's move method
    Room.show(sim.now, clear_screen = Parameters.CLEAR_SCREEN, delay = Parameters.PRINT_DELAY)
    intermove_time = intermove()
    if debug:
        print(f"\t{p} @ ({p.row()},{p.col()}) scheduled to move @ {(sim.now + intermove_time):.3f}")
    # schedule the next movement for this Person
    sim.sched(move, p, Parameters.DEBUG, offset = intermove_time)

    if debug: Calendar.printCalendar(sim)

######################################################################
######################################################################

num_people = 0
people : list[Person] = []

Person.str_length = len(str(Parameters.ROOM_ROWS * Parameters.ROOM_COLS))
Room.createRoom(Parameters.ROOM_ROWS, Parameters.ROOM_COLS)

if Parameters.SEED is not None:
    random.seed(Parameters.SEED)

#
# create a simulator object, schedule the first arrival, and then 
# kick off the simulation for the maximum simulation time
#
sim = simulus.simulator()
sim.sched(arrival, Parameters.DEBUG, offset = interarrival())
sim.run(Parameters.MAX_T)
