from room import *
from enum import Enum
import random

from termcolor import colored as clr

class Type(Enum):
    WALLFLOWER = 0
    BUTTERFLY  = 1

class Person:
    ''' class to represent a person in the simulation, whether a
        wallflower or butterfly
    '''
    __slots__ = ("_id", "_type", "_loc", "_vision")

    # class-level variable
    count = 0
    str_length = None  # initialized in simulation.py 

    def __init__(self, prop_butterflies: float) -> None:
        ''' initializer for a Person object
        Parameters:
            prop_butterflies: the overall proportion of butterflies
        '''
        self._id    : int  = Person.count
        Person.count += 1
        self._type  : Type = Type(1 if random.uniform(0,1) < prop_butterflies else 0)
        self._vision: int  = 1   # could be random!

        # when person arrives, they appear in the Room' entry location
        Room.arrival(self)  # sets this Person's _loc

    ''' simple getter methods '''
    def row(self)    -> int: return self._loc.row()
    def col(self)    -> int: return self._loc.col()
    def vision(self) -> int: return self._vision
   
    def __str__(self) -> str:
        unicode = True
        if unicode:
            if self._type is Type.BUTTERFLY:
                value = "🦋"
            else:
                value = "🌸"
        else:
            ''' returns str representation of a Person object '''
            id_ = f"{self._id:>{Person.str_length}d}"
            if self._type is Type.BUTTERFLY:
                value = clr(f"B{id_}", "green", attrs = ["bold"])
            else:
                value = clr(f"W{id_}", "red")
        return value

    def setLocation(self, location: Location or None) -> None:
        ''' setter method to update the (new) location of this Person,
            called from methods in room.py
        Parameters:
            location: a Location object, if occupying, or None, if leaving
        '''
        self._loc = location

    def move(self, debug: bool = False) -> None:
              ''' Method to handle a Person moving within the room.  The Person
            should use Room.getNeighborhood (which is based on the Person's
            vision) to have a valid list of currently-unoccupied locations.
            The Person should then use Room.getNeighborCount using each of
            those locations, and:
                - if a butterfly, choose the currently-unoccupied location
                  having the highest neighbor count (ties should be broken
                  at random -- i.e., select one at random from a list)
                - if a wallflower, choose the currently-unoccupied location
                  having the lower neighbor count (break ties at random)
            Relevant methods to consider:
                - Room.getNeighborhood
                - Room.getNeighborCount
                - Room.departCurrentLocation
                - Room.occupyNewLocation
        Parameters:
            debug: boolean indicating whther to print debugging info
        '''
        
        # YOUR CODE GOES HERE
        list1 = Room.getNeighborhood(self)  # list of unoccupied locations
    
        if not list1:  # if list1 is empty, there's nowhere to move
            if debug: print(f"\t{self} stays -- no reasonable location")
            return
    
        if self._type is Type.BUTTERFLY: #for the soc. butterfly
            listNeighborCount = []
            for i in list1:
                listNeighborCount.append(Room.getNeighborCount(self._loc, i)) #adds each neighbor count for each location to a list
            maxnc = max(listNeighborCount)  # stores the maximum neighborhood count
            maxi = listNeighborCount.index(maxnc)
            maxloc = list1[maxi]
            Room.departCurrentLocation(self)
            Room.occupyNewLocation(self, maxloc.row(), maxloc.col()) # occupy the Room's location at the given (row,col) and automatically set's their location
        else:
            listNeighborCount = []
            for i in list1:
                listNeighborCount.append(Room.getNeighborCount(self._loc, i))
            minnc = min(listNeighborCount)  # stores the minimum neighborhood count
            mini = listNeighborCount.index(minnc)
            minloc = list1[mini]
            Room.departCurrentLocation(self)
            Room.occupyNewLocation(self, minloc.row(), minloc.col())
        
         # you may want these debug prints throughout your method...    
        if debug: print(f"\t{self} @ ({self.row()},{self.col()}) looking to move...")
        if debug: print(f"\t{self} moves from ({self.row()},{self.col()}) to ({row},{col})")
        if debug: print(f"\t{self} stays -- no reasonable location")

