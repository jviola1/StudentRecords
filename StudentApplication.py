import StudentRecordManager as SRM
import json

class Student:

    #Initialize a student object with an ID, a name and a list of grades
    def __init__(self, ID, name, grades = []):
        self.ID = ID
        self.name = name
        self.grades = grades

    #Returns a string of information about the object
    def __str__(self):
        return "%s, %s, %.2f" %(self.ID, self.name, self.calculateAvg())

    #Take the mean of the list of grades
    def calculateAvg(self):
        return float(sum(self.grades) / max(len(self.grades), 1)) #Max used to avoid divide by zero case

    #Replaces the current list of grades with a new one, then passes itself as
    #an argument to SRM.updateGraphics to update this student's record on the table
    def changeGrades(self, newGrades):
        self.grades = newGrades
        SRM.updateGrades(self)

    #Adds a grade if 0 <= grade <= 100
    def addGrade(self, addedGrade):
        if float(addedGrade) <= 100 and float(addedGrade) >= 0:
            self.grades.append(int(addedGrade))
            self.changeGrades(self.grades)

#Finds a student given an ID and returns the student object of the student with
#that ID.  If no student is found, return a string saying the student couldn't be found
def findStudent(x):
    tempStud = SRM.findStudent(x)
    if tempStud:
        return Student(tempStud[0], tempStud[1], json.loads(tempStud[2]))
    return "Student not found with id {}".format(x)


#Takes a student object and adds it to the database.  Exception raised if given
#something that isn't a student object
def addStudent(newStud):
    if isinstance(newStud, Student):
        SRM.addStudent(newStud)
    else:
        raise TypeError("Only student objects can be added to the database.")

#Given an ID and a list of grades, finds the student and changes their grade.
#If the student isn't found, print the string returned from findStudent()
def changeStudentGrade(ID, newGrades):
    tempStudent = findStudent(ID)
    if isinstance(tempStudent, Student):
        tempStudent.changeGrades(newGrades)
    else:
        print(tempStudent)

#Adds a student grade with typechecking
def addStudentGrade(ID, newGrade):
    tempStudent = findStudent(ID)
    if isinstance(tempStudent, Student):
        tempStudent.addGrade(newGrade)
    else:
        print(tempStudent)

def allRecords():
    return SRM.allRecords()

def deleteStudent(ID):
    SRM.deleteStudent(findStudent(ID))


SRM.createDatabase()
SRM.populateDatabase()
