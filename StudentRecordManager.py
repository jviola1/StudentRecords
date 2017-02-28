import sqlite3
import json #Used to convert the "grades" attribute between a string and a list

#Creates the database RecordsMF in the current directory if it doesn't already exist
def createDatabase():
    try:
        conn = sqlite3.connect('RecordsMF')
        c = conn.cursor()
        c.execute("CREATE TABLE Records (ID integer PRIMARY KEY, name text, grades text, average real)")
        conn.commit()
        conn.close()
    except sqlite3.OperationalError:
        print("DB already exists")

#If the database is empty, populate it with two fake students
def populateDatabase():
    conn = sqlite3.connect('RecordsMF')
    c = conn.cursor()
    c.execute("SELECT * FROM Records")
    if len(c.fetchall()) == 0:
        c.execute("INSERT INTO Records VALUES (?,?,?,?)", (10235, "John Smith", json.dumps([90,80,85,86,57,94]), 82))
        c.execute("INSERT INTO Records VALUES (?,?,?,?)", (10999, "Justin Jackson", json.dumps([80, 80, 56, 75, 100, 92]), 80.5))
        c.execute("INSERT INTO Records VALUES (?,?,?,?)", (501, "Jeremy Johnson", json.dumps([100, 80, 88]), 89.3))
    conn.commit()
    conn.close()

#Add a given student object
def addStudent(newStudent):
    conn = sqlite3.connect('RecordsMF')
    c = conn.cursor()
    c.execute("INSERT INTO Records VALUES (?,?,?,?)", (newStudent.ID, newStudent.name, json.dumps(newStudent.grades), newStudent.calculateAvg()))
    conn.commit()
    conn.close()

#Given a particular ID, returns the record of the student with that ID
def findStudent(studentID):
    conn = sqlite3.connect('RecordsMF')
    c = conn.cursor()
    c.execute("SELECT * FROM Records WHERE ID =:fid", {"fid": studentID})
    tempHolder = c.fetchone()
    conn.close()
    return tempHolder

#Returns all the records within the table
def allRecords():
    conn = sqlite3.connect('RecordsMF')
    c = conn.cursor()
    c.execute("SELECT ID, name, ROUND(average, 2) FROM Records")
    fullList = c.fetchall()
    conn.close()
    return fullList

#Given a student object, finds the record of the student and then edits the grade and average attributes accordingly
def updateGrades(chgStudent):
    conn = sqlite3.connect('RecordsMF')
    c = conn.cursor()
    try:
        c.execute("UPDATE Records SET grades =:newg, average =:navg WHERE ID =:fid", {"newg" : json.dumps(chgStudent.grades), "navg" : chgStudent.calculateAvg(), "fid" : chgStudent.ID})
    except Exception as e:
        raise
        print("Student not found with ID {}".format(chgStudent.ID))
    conn.commit()
    conn.close()

#Given a student object, deletes that student's record
def deleteStudent(delStudent):
    conn = sqlite3.connect('RecordsMF')
    c = conn.cursor()
    try:
        c.execute("DELETE FROM Records WHERE ID =:fid", {"fid" : delStudent.ID})
    except Exception:
        print("Student not found")
    conn.commit()
    conn.close()
