from config import CALL_FRAME_OFFSET

next_heap_address = CALL_FRAME_OFFSET


class Run_Frame:
    def __init__(self):
        self.regs = []

    def push_reg(self, reg):
        global next_heap_address
        self.regs.append((reg, next_heap_address))
        next_heap_address -= 4
        return next_heap_address + 4

    def free(self):
        global next_heap_address
        next_heap_address += len(self.regs) * 4
