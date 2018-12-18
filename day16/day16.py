## Advent of Code 2018: Day 16
## https://adventofcode.com/2018/day/16
## Jesse Williams
## Answers: [Part 1]: 570, [Part 2]: 503

import re

opcodes = ['addr', 'addi', 'mulr', 'muli', 'banr', 'bani', 'borr', 'bori', 'setr', 'seti', 'gtir', 'gtri', 'gtrr', 'eqir', 'eqri', 'eqrr']

class Instruction():
    opcode = 0
    inputA = 0
    inputB = 0
    outputC = 0
    def __init__(self, instruction):
        self.opcode, self.inputA, self.inputB, self.outputC = instruction
    def getInstruction(self):
        return self.opcode, self.inputA, self.inputB, self.outputC

class State():
    r_0, r_1, r_2, r_3 = 0, 0, 0, 0
    def __init__(self, state):
        self.r_0, self.r_1, self.r_2, self.r_3 = state
    def getState(self):
        return (self.r_0, self.r_1, self.r_2, self.r_3)
    def compareState(self, registers):
        # Compares this object's registers to another register list
        return (self.r_0, self.r_1, self.r_2, self.r_3) == registers

def handleOpcode(registers, opcode, inputA, inputB, outputC):
    registers = list(registers)
    if opcode == 'addr':
        registers[outputC] = registers[inputA] + registers[inputB]
    elif opcode == 'addi':
        registers[outputC] = registers[inputA] + inputB
    elif opcode == 'mulr':
        registers[outputC] = registers[inputA] * registers[inputB]
    elif opcode == 'muli':
        registers[outputC] = registers[inputA] * inputB
    elif opcode == 'banr':
        registers[outputC] = registers[inputA] & registers[inputB]
    elif opcode == 'bani':
        registers[outputC] = registers[inputA] & inputB
    elif opcode == 'borr':
        registers[outputC] = registers[inputA] | registers[inputB]
    elif opcode == 'bori':
        registers[outputC] = registers[inputA] | inputB
    elif opcode == 'setr':
        registers[outputC] = registers[inputA]
    elif opcode == 'seti':
        registers[outputC] = inputA
    elif opcode == 'gtir':
        registers[outputC] = 1 if inputA > registers[inputB] else 0
    elif opcode == 'gtri':
        registers[outputC] = 1 if registers[inputA] > inputB else 0
    elif opcode == 'gtrr':
        registers[outputC] = 1 if registers[inputA] > registers[inputB] else 0
    elif opcode == 'eqir':
        registers[outputC] = 1 if inputA == registers[inputB] else 0
    elif opcode == 'eqri':
        registers[outputC] = 1 if registers[inputA] == inputB else 0
    elif opcode == 'eqrr':
        registers[outputC] = 1 if registers[inputA] == registers[inputB] else 0
    else: return False
    return tuple(registers)


if __name__ == '__main__':

    ## Part 1
    tests = []  # a list of triples of instruction tests in the form [(State object, Instruction object, State object), ...]

    with open('day16_input_part1.txt') as f:
        patt_beforeState = re.compile(r"Before:\s+\[(\d), (\d), (\d), (\d)\]")
        patt_instruction = re.compile(r"(\d+)\s(\d+)\s(\d+)\s(\d+)")
        patt_afterState = re.compile(r"After:\s+\[(\d), (\d), (\d), (\d)\]")

        while True:
            test = [0, 0, 0]  # temp list for constructing tuple

            line = f.readline()  # Before: [0, 1, 2, 3]
            if not line: break  # EOF
            test[0] = State(tuple(map(int, patt_beforeState.match(line).groups())))

            line = f.readline()  # O, A, B, C
            test[1] = Instruction(tuple(map(int, patt_instruction.match(line).groups())))

            line = f.readline()  # After: [0, 1, 2, 3]
            test[2] = State(tuple(map(int, patt_afterState.match(line).groups())))

            tests.append(tuple(test))
            _ = f.readline()  # [Blank line]

    multiCodeInstructions = 0  # a count of all test samples that behave like 3 or more opcodes

    for test in tests:
        opcodesMatched = 0
        for opcode in opcodes:
            registers = test[0].getState()
            if test[2].compareState( handleOpcode(registers, opcode, test[1].inputA, test[1].inputB, test[1].outputC) ):
                # If true, states are the same
                opcodesMatched += 1

                # TEST
                #print('Before: {}\tInst: {}\tAfter: {} == {} (comparison)'.format(test[0].getState(), test[1].getInstruction(), handleOpcode(registers, opcode, test[1].inputA, test[1].inputB, test[1].outputC), test[2].getState()))
        if opcodesMatched >= 3:
            multiCodeInstructions += 1

    print('There are {} samples in the test data that behave like three or more opcodes.'.format(multiCodeInstructions))

    ## Part 2
    # First, we need to figure out the number corresponding to each opcode
    opcodeWorks = {}  # a reverse dict to map opcodes to numbers that succeed
    opcodeFails = {}  # a reverse dict to map opcodes to numbers that fail
    for opcode in opcodes:
        opcodeWorks[opcode] = []  # initialize dicts with empty lists
        opcodeFails[opcode] = []  # initialize dicts with empty lists

    for test in tests:
        for opcode in opcodes:
            registers = test[0].getState()
            if test[2].compareState( handleOpcode(registers, opcode, test[1].inputA, test[1].inputB, test[1].outputC) ):
                if test[1].opcode not in opcodeWorks[opcode]:
                    opcodeWorks[opcode].append(test[1].opcode)  # if this sample behaves like this opcode, add it to the works list
            else:
                if test[1].opcode not in opcodeFails[opcode]:
                    opcodeFails[opcode].append(test[1].opcode)  # if this sample *doesn't* behave like this opcode, add it to the fail list

    # Once all tests are run and both dicts have been filled, clean the opcodeWorks list by removing any failures
    for opcode in opcodes:
        for fail in opcodeFails[opcode]:
            if fail in opcodeWorks[opcode]:
                opcodeWorks[opcode].remove(fail)  # remove any numbers in the fail list from the works list

    # Now, we need to make passes through the list of valid candidates for each opcode and narrow down each number by process of elimination
    opcodeDict = {}
    while True:
        matchedOpcodes = 0
        for opcode in opcodes:
            if len(opcodeWorks[opcode]) == 1:
                opNum = opcodeWorks[opcode][0]
                opcodeDict[opNum] = opcode  # we've found a unique match, so add entry to new reverse-lookup dict
                for otherOp in opcodes:  # remove this opcode number from every other entry
                    try:
                        opcodeWorks[otherOp].remove(opNum)
                    except ValueError:
                        pass

            elif len(opcodeWorks[opcode]) == 0:
                matchedOpcodes += 1  # if there are no entries left in this opcode, we've successfully matched it

        if matchedOpcodes == len(opcodes):
            break  # if we've narrowed down all opcodes to one in this pass, end the loop

    # Next, we load the test program
    program = []  # a list of Instruction objects describing the test program

    with open('day16_input_part2.txt') as f:
        patt_programLine = re.compile(r"(\d+) (\d+) (\d+) (\d+)")
        while True:
            line = f.readline()  # Instruction: O, A, B, C
            if not line: break  # EOF
            program.append( Instruction(tuple(map(int, patt_programLine.match(line).groups()))) )

    # Finally, we run the test program and measure the final register state
    registers = (0, 0, 0, 0)
    for prgline in program:
        registers = handleOpcode(registers, opcodeDict[prgline.opcode], prgline.inputA, prgline.inputB, prgline.outputC)
    print('\nProgram successful: (0, 0, 0, 0) -> {}'.format(registers))
    print('\n\nOpcode map:')
    for opcode in opcodeDict:
        print('{}: {}'.format(opcodeDict[opcode], opcode))
