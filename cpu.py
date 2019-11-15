"""
    CPU functionality.
"""
import sys


class CPU:
    """
    Main CPU class.
    """

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
        self.sp = 7

    def ram_read(self, index):
        return(self.ram[index])

    def ram_write(self, value, index):
        self.ram[index] = value
        return(self.ram[index])

    def load(self):
        """Load a program into memory."""
        address = 0

        program = []
        try:
            with open(sys.argv[1]) as document:
                for line in document:
                    if line[0].startswith("0") or line[0].startswith("1"):
                        # split before and after any comment symbol '#'
                        comment_split = line.split("#")[0]
                        # convert the pre-comment portion (to the left) from binary to a value
                        # extract the first part of the split to a number variable
                        # and trim whitespace
                        num = comment_split.strip()

                        # ignore blank lines / comment only lines
                        if len(num) == 0:
                            continue

                        # set the number to an integer of base 2
                        value = int(num, 2)
                        program.append(value)
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            sys.exit(2)

        for instructions in program:
            self.ram[address] = instructions
            address += 1
