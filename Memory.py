

class Memory:

    def __init__(self, name): # memory name
        self.name = name
        self.symbols = {}

    def has_key(self, name):  # variable name
        return name in self.symbols

    def get(self, name):         # gets from memory current value of variable <name>
        return self.symbols[name]

    def put(self, name, value):  # puts into memory current value of variable <name>
        self.symbols[name] = value
        #print(self.symbols)


class MemoryStack:
                                                                             
    def __init__(self, memory=None): # initialize memory stack with memory <memory>
        self.stack = []

        if (memory is not None):
            self.stack.append(memory)
        else:
            self.stack.append(Memory("global"))

    def get(self, name):             # gets from memory stack current value of variable <name>
        i = len(self.stack) - 1

        while i >= 0:
            if self.stack[i].has_key(name):
                # print("jest")
                # print(self.stack[i].get(name))
                return self.stack[i].get(name)
            i -=1
        return None

    def insert(self, name, value): # inserts into memory stack variable <name> with value <value>
        self.stack[-1].put(name, value)

    def set(self, name, value): # sets variable <name> to value <value>
        i = len(self.stack) - 1
        while i >= 0:
            if self.stack[i].has_key(name):
                self.stack[i].put(name, value)
                break
            i -= 1

    def push(self, memory): # pushes memory <memory> onto the stack
        self.stack.append(memory)

    def pop(self):          # pops the top memory from the stack
        self.stack.pop()

