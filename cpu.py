"""
    CPU functionality.
"""
import sys
PRN = 0b01000111
LDI = 0b10000010
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110


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

        # state (running)
        self.running = True

        # REPL (FETCH, DECODE, EXECUTE)
        self.op_pc = False

        self.branch_table = {}
        self.branch_table[PRN] = self.prn
        self.branch_table[LDI] = self.ldi
        self.branch_table[CMP] = self.cmp
        self.branch_table[JMP] = self.jmp
        self.branch_table[JEQ] = self.jeq
        self.branch_table[JNE] = self.jne

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

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """
        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ldi(self, op_a, op_b):
        # Set the value of a register to an integer.
        self.reg[op_a] = op_b
        self.op_pc = False

        if not self.op_pc:
            self.pc += 3

    def prn(self, op_a, op_b):
        # Print numeric value stored in the given register.
        print(self.reg[op_a])

        self.op_pc = False
        if not self.op_pc:
            self.pc += 2

    def cmp(self, op_a, op_b):
        # If they are equal, set the Equal E flag to 1
        if self.reg[op_a] == self.reg[op_b]:
            self.equal = 1
        # otherwise set it to 0.
        else:
            self.equal = 0

        self.op_pc = False

        if not self.op_pc:
            self.pc += 3

    def jmp(self, op_a, op_b):
        # Jump to the address stored in the given register.
        # Set the PC to the address stored in the given register.
        self.pc = self.reg[op_a]

        self.op_pc = True

        if not self.op_pc:
            self.pc += 2

    def jeq(self, op_a, op_b):
        # If equal flag is set(true), jump to the address stored in the given register.
        if self.equal == 1:
            self.pc = self.reg[op_a]
            self.op_pc = True

        if not self.op_pc:
            self.pc += 2

    def run(self):
        """Run the CPU."""
        command = self.ram[self.pc]

        if len(sys.argv) != 2:
            print("usage: cpy.py filename")
            sys.exit(1)

        self.program_filename = sys.argv[1]
        self.load()

        while self.running:
            command = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if command in self.branch_table:
                self.branch_table[command](operand_a, operand_b)
            else:
                sys.exit(1)


cpu = CPU()
cpu.run()
