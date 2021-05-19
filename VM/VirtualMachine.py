def exec_goto():
    print("Goto action")


class Memory:
    virtual_memory = {
        "global": [],
        "local": [],
        "temp": [],
        "quad": [],
    }

    def __init__(self, quad, functions):
        self.virtual_memory['quad'] = quad
        print(self.virtual_memory['quad'])
        self.exec_quad()

    def exec_quad(self):
        for _quad in self.virtual_memory['quad']:
            func = self.switch.get(_quad[0], lambda: "Invalid action")

    switch = {
        'goto': exec_goto
    }


def start_vm(quad, functions):
    print("VM")
    mem = Memory(quad, functions)
