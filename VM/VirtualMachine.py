class Memory:
    virtual_memory = {
        "global": [],
        "local": [],
        "temp": [],
        "quad": [],
    }

    def __init__(self, quad, functions):
        self.virtual_memory['quad'] = quad
        self.exec_quad()

    def exec_quad(self):
        for _quad in self.virtual_memory['quad']:
            func = self.switch.get(_quad[0], lambda: "Invalid action")

    def exec_goto(self):
        print("Goto action")

    switch = {
        'goto': exec_goto
    }


def start_vm(quad, functions):
    mem = Memory(quad, functions)
