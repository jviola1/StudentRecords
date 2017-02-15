import StudentApplication as SA
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

class mainGUI:
    def __init__(self, master):
        master.resizable(width=False, height=False)
        master.minsize(width=400, height = 100)
        master.title("Student Management System")

        self.topFrame = ttk.Frame(master, padding="25 15")
        self.topFrame.pack(fill=BOTH)

        self.bottomFrame = ttk.Frame(master, padding="25 5")
        self.bottomFrame.pack(side=BOTTOM)

        self.selectedVal = StringVar()
        self.comboSelect = ttk.Combobox(self.topFrame, textvariable = self.selectedVal, state = 'readonly')
        self.comboSelect.pack(side=TOP, fill=X)
        self.populateCombo()
        self.comboSelect.bind("<<ComboboxSelected>>", self.changeSelection)

        self.buttonAdd = ttk.Button(self.bottomFrame, text = "Add Student", command=lambda: newStudentInput(master, self))
        self.buttonAdd.pack(side=LEFT)

        self.buttonDel = ttk.Button(self.bottomFrame, text = "Delete Student", command = self.deleteStudent)
        self.buttonDel.pack(side=LEFT)

        self.buttonAddGrade = ttk.Button(self.bottomFrame, text = "Add Grade", command = lambda: self.addGrade(master))
        self.buttonAddGrade.pack(side=LEFT)

        self.buttonViewGrades = ttk.Button(self.bottomFrame, text = "View Grades", command = lambda: self.viewGrade(master))
        self.buttonViewGrades.pack(side=LEFT)

    def populateCombo(self):
        self.comboSelect['values'] = SA.allRecords()
        if len(self.comboSelect['values']) > 0:
            self.comboSelect.current(0)
            self.changeSelection(None)
        else:
            self.comboselect.set('')
            self.changeSelection(None)

    def IDofSelected(self):
        tempSplitString = self.selectedVal.split(" ")
        return tempSplitString[0]

    def changeSelection(self, event):
        self.selectedVal = self.comboSelect.get()

    def deleteStudent(self):
        if messagebox.askquestion(message = "Are you sure you wish to delete a student?  This is cannot be undone.", title="Continue?", icon="warning") == "yes":
            try:
                SA.deleteStudent(self.IDofSelected())
                self.populateCombo()
            except Exception:
                messagebox.showerror(message="There are no records to delete")

    def addGrade(self, master):
        if self.IDofSelected().isdigit():
            gradeInput(master, SA.findStudent(self.IDofSelected()), self)

    def viewGrade(self, master):
        self.viewGradeWin = Toplevel(master)

        self.viewText = Text(self.viewGradeWin, width = 50, height = 10, wrap="word")
        self.tempStudent = SA.findStudent(self.IDofSelected())
        self.viewText.insert("1.0", "ID: {}\nName: {}\nGrades: {}\nAverage: {}".format(self.tempStudent.ID, self.tempStudent.name, self.tempStudent.grades, self.tempStudent.calculateAvg()))
        self.viewText.pack()

        self.returnButton = ttk.Button(self.viewGradeWin, text="Return", command = lambda: self.viewGradeWin.destroy())
        self.returnButton.pack(side=BOTTOM)

class gradeInput:

    def __init__(self, master, selectedStudent, mainWindow):

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

    def confirmAddGrade(self, selectedStudent, mainWindow):
        selectedStudent.addGrade(self.textNewGrade.get())
        mainWindow.populateCombo()
        self.addGradeWin.destroy()


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


root = Tk()
run = mainGUI(root)
root.mainloop()
