class User:
    def __init__(self, username, name):
        self.username = username
        self.name = name

class Student(User):
    def __init__(self, username, name, college, program):
        User.__init__(self, username, name)
        self.college = college
        self.program = program
        self.courses = []  # List of the student's enlisted courses

    def enlist(self, c_code):
        if c_code not in self.courses:
            self.courses.append(c_code)
            return True
        else:
            print(f"{c_code} already enlisted.\n")
            return False
        
    def drop(self, c_code):
        self.courses.remove(c_code)

    def display_courses(self):
        for course in self.courses:
            print(course)

class Admin(User):
    def __init__(self, username, name):
        User.__init__(self, username, name)

    def add_class(self, c_code, c_name, units, limit, prereq=None):
        g_courses[c_code] = Course(c_code, c_name, units, limit, prereq)

    def del_class(self, c_code):
        del g_courses[c_code]

# GLOBAL VARIABLES
credentials = dict([("dan", "v"), ("admin", "123")]) # list of Users
users = {"dan": Student("dan", "Dan John", "CCS", "BS CS"), "admin": Admin("admin", "St. Lasalle")}  # login
g_courses = {
            "CCPROG1":Course("CCPROG1", "Intro to Computer Programming", 3.0, 20),
            "CCDSALG":Course("CCDSALG", "Intro to Algorithms", 3.0, 30, ["CCPROG1"]),
            "CSALGCM": Course("CSALGCM", "CCSDSALG PART 2", 3.0, 30, ["CCDSALG"]),
            "CCPROG2": Course("CCPROG2", "Programming with Structured Data", 3.0, 20)
          }

class Course():
    def __init__(self, c_code, c_name, units, limit, prereq=None):
        self.c_code = c_code
        self.c_name = c_name
        self.units = units
        self.limit = limit
        self.prereq = prereq
        self.enlist_count = 0

    def display_info(self):
        info = '{:>12} {:>40} {:>12} {:>12} {:>12}'.format(
            self.c_code, self.c_name, self.units, self.limit, self.enlist_count)
        print(info)

# Functionalities
def add_user(username, name, college=None, program=None):
    if college != None:
        users[username] = Student(username, name, college, program)
    else:
        users[username] = Admin(username, name)

def register(type):
    print("*****USER REGISTER*****")
    
    while True:
        username = input("Enter username: ")
        if userExists(username):
            print("That username already exists. Please try a different username.\n")
        else: break        
  
    password = input("Enter password: ")
    name = input("Enter your name: ")

    if type == "Student":
        college = input("Enter your college: " )
        program = input("Enter your program: ")
        add_user(username, name, college, program)
    elif type == "Admin":
        add_user(username, name)

    credentials[username] = password
    print("Registration successful!")

def userExists(username):
    if username in credentials:
        return True
    else:
        return False

def courseExists(course):
    if course in g_courses:
        return True
    else:
        return False

def isConfirm():
    while True:
        answer = input("Are you sure? (Y/N): ").upper()
        if answer == 'Y':
            return True
        elif answer == 'N':
            return False

def login():
    print("*****LOG IN*****")
    username = input("Enter username: ")
    password = input("Enter password: ")
    while not (userExists(username) and credentials[username] == password):
        print("Invalid credentials. Please try again.\n")
        username = input("Enter username: ")
        password = input("Enter password: ")
    
    return users[username]

def homepage():
    print("----HOME PAGE----")
    print('{:>12} {:>40} {:>12} {:>12} {:>12}'.format(
            "|COURSE CODE|", "|COURSE NAME|", "|UNITS|", "|LIMIT|", "ENROLLED"))
    for course in g_courses:
        g_courses[course].display_info()

def enlist_mode(studentuser):
    print("----ENLIST MODE----")
    c_code = input("Enter course code: ").upper()
    if courseExists(c_code):
        if isConfirm():
            if studentuser.enlist(c_code):
                g_courses[c_code].enlist_count += 1
                print(f'SUCCESSFULLY ENLISTED {c_code}')
        else:
            print("LEAVING ENLIST MODE")
    else:
        print("Course code doesn't exist.")
        print("LEAVING ENLIST MODE")

def drop_mode(studentuser):
    print("----DROP MODE----")
    c_code = input("Enter course code: ").upper()
    if courseExists(c_code) and c_code in studentuser.courses:
        if isConfirm():
            studentuser.drop(c_code)
            g_courses[c_code].enlist_count-=1
            print(f'SUCCESSFULLY DROPPED {c_code}')
        else:
            print("LEAVING DROP MODE")
    else:
        print("Course code doesn't exist.")
        print("LEAVING DROP MODE")

def inputNumber(question):
    while True:
        userinput = input(question)
        try:
            n = int(userinput)
            return n
        except ValueError:
            print("Please input a valid number.")

def add_class(adminuser):
    print("----ADMIN ADD CLASS MODE----")
    c_code = input("Enter course code: ").upper()
    if courseExists(c_code):
        print("Course code already exists.")
    else:
        c_name = input("Enter course name: ")
        units = float(inputNumber("Enter course units: "))
        limit = inputNumber("Enter course limit: ")
        print("Does this course have prerequisites?")
        if isConfirm():
            n = inputNumber("Number of prerequisites: ")
            prereq = []
            for i in range(n):
                prereq.append(input(f"Enter prerequisite #{i+1}: "))
            adminuser.add_class(c_code, c_name, units, limit, prereq)
        else:
            adminuser.add_class(c_code, c_name, units, limit)

def del_class(adminuser):
    print("----ADMIN DELETE CLASS MODE----")
    c_code = input("Enter course code: ").upper()
    if courseExists(c_code):
        if isConfirm():
            adminuser.del_class(c_code)
    else:
        print("Course code doesn't exists.")
        print("LEAVING ADMIN DELETE CLASS MODE.")

def select_mode(user):
    homepage()
    if type(user)==Student:
        while True:
            print("\nActions: \t[E] Enlist\t[D] Drop\t[X] Exit App")
            action = input("Select action: ").upper()
            if action == 'E':
                enlist_mode(user)
                return True
            elif action == 'D':
                drop_mode(user)
                return True
            elif action == 'X':
                print(f"See you again, {user.name}.")
                print("Closing application...")
                return False
    elif type(user) == Admin:
        while True:
            print("\nActions: \t[A] Add Class\t[D] Delete Class\t[X] Exit App")
            action = input("Select action: ").upper()
            if action == 'A':
                add_class(user)
                return True
            elif action == 'D':
                del_class(user)
                return True
            elif action == 'X':
                print(f"See you again, {user.name}.")
                print("Closing application...")
                return False
                
def welcome():
    while True:
            print("\nActions: \t[L] LOGIN\t[A] REGISTER AS STUDENT\t     [B] REGISTER AS ADMIN")
            action = input("Select action: ").upper()
            if action == 'L':
                return login()
            elif action == 'A':
                register("Student")
            elif action == 'B':
                register("Admin")

def main():
    #register("Student")
    currentUser = welcome() 
    flag = select_mode(currentUser)
    while flag:
        flag = select_mode(currentUser)
    
if __name__== "__main__":
  main()

