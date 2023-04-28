class Student:
    __slots__ = ("_name", "_id", "_year", "_major")

    # class-level variable
    _num_students: int = 0 
    
    # initializer method that is implicitly called whenever we construct
    # a Student object
    def __init__(self, name: str, student_id: str, year: int, major: str) -> None:
        # set up the instance variables (i.e., data inside the object 'self')
        self._name  = name  # setting the instance variable _name inside self to parameter name
        self._id    = student_id
        self._year  = year
        self._major = major

        Student._num_students += 1

    @classmethod
    def getNumStudents(cls) -> int:
        print(f"The class is {cls}")
        return cls._num_students

    def __str__(self) -> str:
        value = f"Student: ({self._name}, {self._id}, {self._year}, {self._major})"
        return value

    def reverse(self) -> None:
        self._name = self._name[::-1]

    def getMajor(self) -> str:
        return self._major

    def setYear(self, year: int) -> None:
        self._year = year
        #self._yaer = year  # not caught unless you use __slots__

def main() -> None:
    print(Student.getNumStudents())
    sokona = Student("Sokona M", "12345678", 3, "math")
    abe    = Student("Abe M", "98765432", 4, "neuro")

    print(Student.getNumStudents())
    print(sokona.getNumStudents())
    print(abe.getNumStudents())

    #print(Student.getMajor())  # won't work -- no argument to self!

'''
def main() -> None:
    # create two different _objects_ of the _class_ Student
    # create two different _instances_ of the _class_ Student
    sokona = Student("Sokona M", "12345678", 3, "math")
    abe    = Student("Abe M", "98765432", 4, "neuro")

    abe.reverse()

    print(f"What is Sokona's major? {sokona.getMajor()}")

    print(f"sokona = {sokona}")
    print(f"abe    = {abe}")

    print(f"type(sokona) = {type(sokona)}")
    print(f"type(abe)    = {type(abe)}")

    sokona.setYear(4)
    Student.setYear(sokona, 4)
    Student.setYear(abe, 3)
    
    print(f"sokona = {sokona}")

    #name = str("Snowball")
    #print(f"type(name) = {type(name)}")
'''


if __name__ == "__main__":
    main()
