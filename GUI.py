import StudentApplication as SA
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

#Main window of the GUI
class mainGUI:
    def __init__(self, master):
        master.resizable(width=False, height=False)
        master.minsize(width=400, height=100)
        master.title("Student Management System")

        #Separate the window into a top frame and a bottom frame
        self.topFrame = ttk.Frame(master, padding="25 15")
        self.topFrame.pack(fill=BOTH)

        self.bottomFrame = ttk.Frame(master, padding="25 5")
        self.bottomFrame.pack(side=BOTTOM)

        #Combobox goes into the top frame
        self.selectedVal = StringVar()
        self.comboSelect = ttk.Combobox(self.topFrame, textvariable = self.selectedVal, state = 'readonly')
        self.comboSelect.pack(side=TOP, fill=X)
        self.populateCombo()
        self.comboSelect.bind("<<ComboboxSelected>>", self.changeSelection)

        #Buttons in the bottom frame
        #lambda used for any commands that require an argument to be passed
        self.buttonAdd = ttk.Button(self.bottomFrame, text = "Add Student", command=lambda: newStudentInput(master, self)) #Creates newStudentInput
        self.buttonAdd.pack(side=LEFT)

        self.buttonDel = ttk.Button(self.bottomFrame, text = "Delete Student", command = self.deleteStudent)
        self.buttonDel.pack(side=LEFT)

        self.buttonAddGrade = ttk.Button(self.bottomFrame, text = "Add Grade", command = lambda: self.addGrade(master))
        self.buttonAddGrade.pack(side=LEFT)

        self.buttonViewGrades = ttk.Button(self.bottomFrame, text = "View Grades", command = lambda: self.viewGrade(master))
        self.buttonViewGrades.pack(side=LEFT)

    #Sets the values of the combobox to be all the records within the database
    def populateCombo(self):
        self.comboSelect['values'] = SA.allRecords()
        if len(self.comboSelect['values']) > 0:     #If there are elements in the combobox, the first is selected (visually, however, it'll still just show a blank box)
            self.comboSelect.current(0)
            self.changeSelection(None)
        else:                                       #Otherwise the combobox is set to nothing
            self.comboselect.set('')
            self.changeSelection(None)

    #Takes the ID from the string of the selected student
    def IDofSelected(self):
        tempSplitString = self.selectedVal.split(" ")
        return tempSplitString[0]

    #Event bound to combobox changing
    def changeSelection(self, event):
        self.selectedVal = self.comboSelect.get()

    #The selected student is deleted from the database after a confirmation message
    #If the student is deleted, the combobox is repopulated to show the missing student
    #If the combobox is empty, an error is shown
    def deleteStudent(self):
        if messagebox.askquestion(message = "Are you sure you wish to delete a student?  This is cannot be undone.", title="Continue?", icon="warning") == "yes":
            try:
                SA.deleteStudent(self.IDofSelected())
                self.populateCombo()
            except Exception:
                messagebox.showerror(message="There are no records to delete")

    #Creates a gradeInput object
    def addGrade(self, master):
        if self.IDofSelected().isdigit():
            gradeInput(master, SA.findStudent(self.IDofSelected()), self)

    #Opens a window that displays student information
    def viewGrade(self, master):
        self.viewGradeWin = Toplevel(master)

        self.viewText = Text(self.viewGradeWin, width = 50, height = 10, wrap="word")
        self.tempStudent = SA.findStudent(self.IDofSelected())
        self.sText = "ID: %s\nName: %s\nGrades: %s\nAverage: %.2f" %(self.tempStudent.ID, self.tempStudent.name, self.tempStudent.grades, self.tempStudent.calculateAvg())
        self.viewText.insert("1.0", self.sText)
        self.viewText.pack()

        self.returnButton = ttk.Button(self.viewGradeWin, text="Return", command = lambda: self.viewGradeWin.destroy())
        self.returnButton.pack(side=BOTTOM)


#Window for the user to input a grade for the selected student
class gradeInput:

    #Takes the master window, the student selected in the combobox as well as the mainGUI object
    def __init__(self, master, selectedStudent, mainWindow):

        #Creates a toplevel window for adding a grade
        self.addGradeWin = Toplevel(master)
        self.addGradeWin.minsize(width=225, height=50)
        self.addGradeWin.resizable(width=False, height=False)


        self.labelNewGrade = ttk.Label(self.addGradeWin, text="New Grade:")
        self.labelNewGrade.grid(row=0, column=0)

        self.textNewGrade = ttk.Entry(self.addGradeWin)
        self.textNewGrade.grid(row=0,column=1, pady=25)

        self.confirmButton = ttk.Button(self.addGradeWin, text="Confirm", command=lambda: self.confirmAddGrade(selectedStudent, mainWindow))
        self.confirmButton.grid(row=1, column=0, padx=(10, 0), pady=(0,10))

        self.cancelButton= ttk.Button(self.addGradeWin, text="Cancel", command=lambda: self.addGradeWin.destroy())
        self.cancelButton.grid(row=1, column = 1, sticky=E, pady=(0,10))

    #Adds the grade to the student.  Uses mainWindow so it can access MainGUI and repopulate the combobox
    #This will allow the student list to be updated with the correct averages
    def confirmAddGrade(self, selectedStudent, mainWindow):
        selectedStudent.addGrade(self.textNewGrade.get())
        mainWindow.populateCombo()
        self.addGradeWin.destroy()


#Window for adding new students
class newStudentInput:

    def __init__(self, master, mainWindow):

        self.addStudentWin = Toplevel(master)

        self.labelStudentID = ttk.Label(self.addStudentWin, text="Student ID:")
        self.labelStudentID.grid(row=0, column=0)

        self.textStudentID = ttk.Entry(self.addStudentWin)
        self.textStudentID.grid(row=0, column=1)

        self.labelStudentName = ttk.Label(self.addStudentWin, text="Student Name:")
        self.labelStudentName.grid(row=1, column=0)

        self.textStudentName = ttk.Entry(self.addStudentWin)
        self.textStudentName.grid(row=1, column=1)

        self.addStudentConfirm = ttk.Button(self.addStudentWin, text="Confirm", command=lambda:self.addStudent(mainWindow))
        self.addStudentConfirm.grid(row=2,column=0, sticky=W, padx=(10,0), pady=(0,5))

        self.addStudentCancel = ttk.Button(self.addStudentWin, text="Cancel", command=lambda: self.addStudentWin.destroy())
        self.addStudentCancel.grid(row=2, column=1, sticky=E, padx=(0, 10), pady=(0,5))

    #Adds a student if two conditions are met:
    #1. The student ID only contains digits
    #2. The student name contains no digits
    #After the student is added, the combobox is repopulated
    def addStudent(self, mainWindow):

        if not(self.textStudentID.get().isdigit()):
            messagebox.showerror(message="A student ID may only contain digits")
            return

        if any(iChar.isdigit() for iChar in self.textStudentName.get()):
            messagebox.showerror(message="A student name may not contain digits")
            return

        SA.addStudent(SA.Student(self.textStudentID.get(), self.textStudentName.get()))
        mainWindow.populateCombo()
        self.addStudentWin.destroy()

#Creates a blank Tk window and uses that as the basis for the GUI
root = Tk()
run = mainGUI(root)
root.mainloop()
