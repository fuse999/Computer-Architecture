"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = self.reg[0]
        self.commands = {
            0b00000001: self.hlt,
            0b10000010: self.ldi,
            0b01000111: self.prn,
            0b10100010: self.mul,
            0b01000101: self.push,
            0b01000110: self.pop
        }


    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def hlt(self, operand_a, operand_b):
        return (0, False)

    def ldi(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b
        return (3, True)

    def prn(self, operand_a, operand_b):
        print(self.reg[operand_a])
        return (2, True)

    def mul(self, operand_a, operand_b):
        self.alu("MUL", operand_a, operand_b)
        return (3, True)

    def push (self, operand_a, operand_b):
        self.reg[7] -= 1
        sp = self.reg[7]
        value = self.reg[operand_a]
        self.ram[sp] = value
        return (2, True)

    def pop (self, operand_a, operand_b):
        sp = self.reg[7]
        value = self.ram[sp]
        self.reg[operand_a] = value
        self.reg[7] += 1
        return (2, True)

    def load(self, program=None):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:
        if program == None:
            program = [
                # From print8.ls8
                0b10000010, # LDI R0,8
                0b00000000,
                0b00001000,
                0b01000111, # PRN R0
                0b00000000,
                0b00000001, # HLT
            ]

            for instruction in program:
                self.ram[address] = instruction
                address += 1

        elif program == "test":
            program = [
                # From print8.ls8
                0b10000010, # LDI R0,8
                0b00000000,
                0b00001000,
                0b10000010, # LDI R1,9
                0b00000001,
                0b00001001,
                0b10100010, # MUL R0,R1
                0b00000000,
                0b00000001,
                0b01000111, # PRN R0
                0b00000000,
                0b00000001, # HLT
            ]

            for instruction in program:
                self.ram[address] = instruction
                address += 1

        elif program != None:
            try:
                with open(program) as f:
                    for line in f:
                        #parse out comments
                        comment_split = line.strip().split("#")
                        # Cast number string to int
                        value = comment_split[0].strip()
                        #ignore blank lines
                        if value == "":
                            continue
                        #populate memory array
                        self.ram[address] = int(value, 2)
                        address += 1   
            except FileNotFoundError:
                print("File not found")
                sys.exit(2)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
                self.reg[reg_a] = (self.reg[reg_a] * self.reg[reg_b])
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True

        while running:
            ir = self.ram[self.pc]
            # print(ir)

            operand_a = self.ram_read(self.pc + 1)
            # print(operand_a)
            operand_b = self.ram_read(self.pc + 2)
            # print(operand_b)

            try:
                operation_output = self.commands[ir](operand_a, operand_b)
                running = operation_output[1]
                self.pc += operation_output[0]

            except:
                print(f"command: {ir}")
                sys.exit()
