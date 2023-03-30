from __future__ import annotations
from enum import Enum
import time

# allows us to use Person as a type hint while avoiding circular import
from typing import TYPE_CHECKING
if TYPE_CHECKING: from person import Person

# allows us to define a simple struct-like class while having auto-created
# __init__ etc. (see https://docs.python.org/3/library/dataclasses.html)
from dataclasses import dataclass

@dataclass
class Location:
    ''' class to represent a location within the overall room '''
    row_col: tuple                      # tuple ==> immutable
    occupant: Person = None
    is_entry: bool = False
    def row(self) -> int: return self.row_col[0]
    def col(self) -> int: return self.row_col[1]

class Room:
    ''' class to represent the overall room '''

    locations: tuple[Location] = None   # tuple ==> immutable
    rows:  int = 0
    cols:  int = 0
    entry: Location = None

    @classmethod
    def createRoom(cls, num_rows: int, num_cols: int) -> None:
        ''' class-level method to initialially create a room
        Parameters:
            num_rows: integer number of rows of locations in the Room
            num_cols: integer number of columns of locations in the Room
        Returns:
            nothing -- updates class-level locations tuple
        '''
        # make a 2D list of initially-empty (occupant is None) Location objects
        cls.locations: list[Location] = [[] for r in range(num_rows)]
        for r in range(num_rows):
            cls.locations[r] = [Location((r,c),None,False) for c in range(num_cols)]

        entry_row = num_rows - 1;  entry_col = num_cols // 2
        cls.entry = Location((entry_row, entry_col), None, True)
        cls.locations[entry_row][entry_col] = cls.entry

        # convert the list-of-lists of locations to tuple-of-tuples of locations
        # so that they cannot be inadvertently changed
        cls.locations = tuple(tuple(row) for row in cls.locations)  
        cls.rows = num_rows
        cls.cols = num_cols

    @classmethod
    def show(cls, t: int or float, clear_screen: bool = True, delay: float = 0.0) -> None:
        ''' class-level method to display the current Room contents
        Parameters:
            t: current clock time (int or float)
            clear_screen: whether to clear the screen between each print
            delay: time to delay between prints
        '''
        unicode = True
        if unicode:
            empty_location = "  "
            max_person_len = 2
        else:
            max_person_len = len(str(cls.rows * cls.cols)) + 1
            empty_location = " " * max_person_len

        room_str = (("-" + ("-" * max_person_len)) * cls.cols) + "-\n"
        width = (len(room_str) - 1)
        if clear_screen:
            clear = "\033[2J\033[H"
            room_str = clear + room_str
        for r in range(cls.rows):
            for c in range(cls.cols):
                occupant = empty_location if cls.locations[r][c].occupant is None \
                                else str(cls.locations[r][c].occupant)
                room_str += f"|{occupant}"
            room_str += "|\n"
        room_str += (("-" + ("-" * max_person_len)) * cls.cols) + "-\n"
        if isinstance(t, int):
            time_str = f"time: {t}"
        else:
            time_str = f"time: {t:.3f}"
        half_width = (width + len(time_str)) // 2
        room_str += f"{time_str:>{half_width}}\n"
        print(room_str)
        time.sleep(delay)

    @classmethod
    def arrival(cls, person: Person) -> None:
        ''' class-level method to handle an arrival to the room, placing
            the given person into the Room's entry location
        Parameters:
            person: a Person object
        '''
        cls.entry.occupant = person
        person.setLocation(cls.entry)  # updates ._loc inside Person

    @classmethod
    def isEntryOccupied(cls) -> bool:
        ''' returns True if the Room's entry location is currently occupied
            (in which case, no additional arrivals are allowed); False o/w
        '''
        return bool(cls.entry.occupant)

    @classmethod
    def getEntryCoords(cls) -> tuple[int,int]:
        ''' returns the Room's entry location row and column as a tuple,
            for easy comparison --- movement into the entry is not allowed
            (see use of this method in Room.getNeighborhood)
        '''
        return cls.entry.row_col
    
    @classmethod
    def isLocationOccupied(cls, row: int, col: int) -> bool:
        ''' returns True if the Room's location at the given (row,col) is
            currently occupied; False o/w
        '''
        return bool(cls.locations[row][col].occupant)

    @classmethod
    def occupyNewLocation(cls, person: Person, row: int, col: int, debug: bool = False) -> None:
        ''' method to occupy the Room's location at the given (row,col) with the
            given Person, also setting that Person object's ._loc location
        Parameters:
            person: Person object to occupy the location
            row: integer row of the location to occupy
            col: integer columng of the location to occupy
            debug: if True, prints debugging information
        '''
        assert(row >= 0 and row < cls.rows)
        assert(col >= 0 and col < cls.cols)
        assert(not bool(cls.locations[row][col].occupant))
        if debug: print(f"\t{person} occupying ({row},{col})")
        cls.locations[row][col].occupant = person
        person.setLocation(cls.locations[row][col])

    @classmethod
    def departCurrentLocation(cls, person: Person, debug: bool = False) -> None:
        ''' method to unoccupy the current location occupied by the given
            Person, also (un)setting that Person object's ._loc location
        Parameters:
            person: Person object to occupy the location
            debug: if True, prints debugging information
        '''
        row = person.row(); col = person.col()
        if debug: print(f"\t{person} departing ({row},{col})")
        cls.locations[row][col].occupant = None
        person.setLocation(None)

    @classmethod
    def getNeighborCount(cls, location: Location, person: Person, debug: bool = False) -> int:
        ''' method to return the number of occupied locations in the eight locations
            immediately surrounding the given location, with the given Person's
            location excluded
        Parameters:
            location: a valid Location object
            person: Person object considering movement, not to be included in
                    the count
            debug: if True, prints debugging information
        Returns:
            the number of occupied locations in the eight locations surrounding
            the given location, not including the given person in the count
        '''
        count = 0
        row = location.row(); col = location.col()
        for r in range(-1, 2, 1):
            for c in range(-1, 2, 1):
                rr = row + r;  cc = col + c
                if rr == person.row() and cc == person.col(): continue
                if rr < 0 or rr >= cls.rows: continue
                if cc < 0 or cc >= cls.cols: continue
                if cls.isLocationOccupied(rr, cc):
                    count += 1

        if debug: print(f"\t# people around ({row},{col}): {count}")
        return count

    @classmethod
    def getNeighborhood(cls, person: Person, debug: bool = False) -> list[Location]:
        ''' method to return a list of unoccupied locations within the Room
            that are within the Moore neighborhood of the given Person's
            location, as defined by the Person's vision
        Parameters:
            person: Person object considering movement
            debug: if True, prints debugging information
        Returns:
            a list of unoccupied locations (valid locations within the room)
            within the Moore neighborhood of the given Person
        '''
        row    = person.row()
        col    = person.col()
        vision = person.vision()

        neighborhood = []
        string = "["
        for r in range(-vision, vision + 1, 1):
            for c in range(-vision, vision + 1, 1):
                if r == 0 and c == 0: continue
                rr = row + r;  cc = col + c
                if (rr,cc) == cls.getEntryCoords(): continue
                if rr < 0 or rr >= cls.rows: continue
                if cc < 0 or cc >= cls.cols: continue
                if not cls.isLocationOccupied(rr, cc):
                    neighborhood.append(cls.locations[rr][cc])
                    string += f"({rr},{cc}),"
        if len(string) > 1: string = string[:-1]
        string += "]"

        if debug: print(f"\tneighborhood around ({row},{col}): {string}")
        return neighborhood 
