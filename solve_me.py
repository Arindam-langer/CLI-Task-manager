class TasksCommand:
    TASKS_FILE = "tasks.txt"
    COMPLETED_TASKS_FILE = "completed.txt"

    current_items = {} #every item in the list
    completed_items = []   #list of completed items
##### reads the current items in the to do list
    def read_current(self):
        try:
            file = open(self.TASKS_FILE, "r")  ##opening the Task.txt in read mode
            for line in file.readlines():
                 ## splitting the string in different parts
                item = line[:-1].split(" ") 
                #converting them into a dict witha  key 1:"work" but the key is iterable andd not the priority
                self.current_items[int(item[0])] = " ".join(item[1:])  
            file.close()
        except Exception:
            return "list is empty"
#### reads the completed items in the list
    def read_completed(self):
        try:
            file = open(self.COMPLETED_TASKS_FILE, "r")
            self.completed_items = file.readlines()
            file.close()
        except Exception:
            return "list is empty"
###updates the to do list
    def write_current(self):
        #opening file in read and write
        with open(self.TASKS_FILE, "w+") as f:
            #empyting the file viq truncate
            f.truncate(0)
            #writing the file new in a sorted way
            for key in sorted(self.current_items.keys()):
                f.write(f"{key} {self.current_items[key]}\n")
###updates the completed list
    def write_completed(self):
        with open(self.COMPLETED_TASKS_FILE, "w+") as f:
            f.truncate(0)
            for item in self.completed_items:
                f.write(f"{item}\n")

    def run(self, command, args):
        self.read_current()
        self.read_completed()
        if command == "add":
            self.add(args)
        elif command == "done":
            self.done(args)
        elif command == "delete":
            self.delete(args)
        elif command == "ls":
            self.ls()
        elif command == "report":
            self.report()
        elif command == "help":
            self.help()

    def help(self):
        print(
            """Usage :-
$ python tasks.py add 2 hello world # Add a new item with priority 2 and text "hello world" to the list
$ python tasks.py ls # Show incomplete priority list items sorted by priority in ascending order
$ python tasks.py del PRIORITY_NUMBER # Delete the incomplete item with the given priority number
$ python tasks.py done PRIORITY_NUMBER # Mark the incomplete item with the given PRIORITY_NUMBER as complete
$ python tasks.py help # Show usage
$ python tasks.py report # Statistics"""
        )
# it will take arguments in terminal one is the priority and other is the task

    def add(self, args):
        priority = int(args[0])
        tasks = " ".join(args[1:])
        self.read_current()

        # Check if the priority exists and shift tasks down if necessary
        if priority in self.current_items:
            # Shift all tasks starting from the current priority upwards by 1
            temp_items = {}
            for p in sorted(self.current_items.keys(), reverse=True):
                if p >= priority:
                    temp_items[p + 1] = self.current_items[p]
                else:
                    temp_items[p] = self.current_items[p]

            self.current_items = temp_items

        # Assign the new task to the requested priority
        self.current_items[priority] = tasks
        self.write_current()
        print(f"Task: '{tasks}' has been added with priority {priority}")
    # it will take arguments in terminal one is the priority and other is the task

    def done(self, args):
        #for done we need to pop it in the current list and update the completed list
        priority = int(args[0])
        self.read_current()
        if priority not in self.current_items:
            print("item not present")
        else:
            completed = self.current_items.pop(priority)
            self.write_current() #updates to do list
            self.completed_items.append(completed)
            self.write_completed() # updates completed list
            print(f"task: {completed} is done")

    def delete(self, args):
        number = int(args[0])
        if number not in self.current_items.keys():
            print(f"Priority: {number} does not exist.")            
        else:
            x = self.current_items.pop(number,None)
            self.write_current()
            print(f"item:{x} of priority: {number} is deleted ")
 
    
    def ls(self):
        self.read_current()
        if not self.current_items:
            print("empty")
        else:
            for key in sorted(self.current_items):
                print(f"{key}:{self.current_items[key]}")
    def report(self):
        self.read_completed()
        self.read_current()
        print(f"Completed : {len(self.completed_items)} ")
        for i,j in enumerate(self.completed_items,1):
            print(f"{i}:{j}")
        
        print(f"Pending : {len(self.current_items)} ")
        for keys in sorted(self.current_items):
            print(f"priority:{keys}->{self.current_items[keys]}")
        

