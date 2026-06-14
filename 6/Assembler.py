import sys
class Code:

    def __init__(self) -> None:
        self.dest_dict = {
            'M': 2,
            'D': 1,
            'A': 0,
        }
        self.comp_dict = {
            '0': '0101010',
            '1': '0111111',
            '-1': '0111010',
            'D': '0001100',
            'A': '0110000',
            'M': '1110000',
            '!D': '0001101',
            '!A': '0110001',
            '!M': '1110001',
            '-D': '0001111',
            '-A': '0110011',
            '-M': '1110011',
            'D+1': '0011111',
            'A+1': '0110111',
            'M+1': '1110111',
            'D-1': '0001110',
            'A-1': '0110010',
            'M-1': '1110010',
            'D+A': '0000010',
            'D+M': '1000010',
            'D-A': '0010011',
            'D-M': '1010011',
            'A-D': '0000111',
            'M-D': '1000111',
            'D&A': '0000000',
            'D&M': '1000000',
            'D|A': '0010101',
            'D|M': '1010101',
        }
        self.jump_dict = {
            'null': '000',
            'JGT': '001',
            'JEQ': '010',
            'JGE': '011',
            'JLT': '100',
            'JNE': '101',
            'JLE': '110',
            'JMP': '111',
        }


    def comp(self, symbol):
        return self.comp_dict[symbol]


    def dest(self, symbol):
        code = ['0', '0', '0']
        if symbol == 'null':
            return ''.join(code)
        for d, i in self.dest_dict.items():
            if d in symbol:
                code[i] = '1'
        return ''.join(code)


    def jump(self, symbol):
        return self.jump_dict[symbol]


class Parser:

    def __init__(self, inputfile) -> None:
        self.file = open(inputfile, 'r')
        self.curr_line = ''
        self.curr_instruction = ''
        self.curr_instructionType = ''


    def hasMoreLines(self):

        self.curr_line = self.file.readline()
        return True if self.curr_line else False


    def advance(self):

        self.curr_instruction = self.curr_line.strip()

        dash = self.curr_instruction.find('//')
        self.curr_instruction = self.curr_instruction[:dash] if dash > 0 else self.curr_instruction


    def instructionType(self):
        if self.curr_instruction.startswith('//'):
            self.curr_instructionType = 'COMMENT'
        elif self.curr_instruction == '':
            self.curr_instructionType = 'BLANK'
        elif self.curr_instruction.startswith('@'):
            self.curr_instructionType = 'A_INSTRUCTION'
        elif '=' in self.curr_instruction or ';' in self.curr_instruction:
            self.curr_instructionType = 'C_INSTRUCTION'

        elif self.curr_instruction.startswith(
                '(') and self.curr_instruction.endswith(')'):
            self.curr_instructionType = 'L_INSTRUCTION'
        else:
            self.curr_instructionType = ''

    def symbol(self):
        if self.curr_instructionType == 'A_INSTRUCTION':
            return self.curr_instruction[1:]
        elif self.curr_instructionType == 'L_INSTRUCTION':
            return self.curr_instruction[1:-1]
        else:
            pass


    def comp(self):
        equal = self.curr_instruction.find('=')
        colon = self.curr_instruction.find(';')
        return self.curr_instruction[
            equal + 1:] if colon == -1 else self.curr_instruction[equal+1:colon]


    def dest(self):
        if '=' not in self.curr_instruction:
            return 'null'
        return self.curr_instruction[:self.curr_instruction.find('=')]


    def jump(self):
        if ';' not in self.curr_instruction:
            return 'null'
        return self.curr_instruction[self.curr_instruction.find(';') + 1:]


class Assembler:

    def __init__(self, inputfile) -> None:
        self.inputfile = inputfile
        self.outputfile = self.inputfile.replace('asm', 'hack')
        self.symbol_table = {
            'R0': 0,
            'R1': 1,
            'R2': 2,
            'R3': 3,
            'R4': 4,
            'R5': 5,
            'R6': 6,
            'R7': 7,
            'R8': 8,
            'R9': 9,
            'R10': 10,
            'R11': 11,
            'R12': 12,
            'R13': 13,
            'R14': 14,
            'R15': 15,
            'SP': 0,
            'LCL': 1,
            'ARG': 2,
            'THIS': 3,
            'THAT': 4,
            'SCREEN': 16384,
            'KBD': 24576,
        }

        self.rom_addr = 0
        self.ram_addr = 16


    def assemble(self):
        self.file = open(self.outputfile, 'w')
        self.first_pass()
        self.second_pass()
        self.file.close()
        print('binary code saved to: ', self.outputfile)

    def L_pass(self):
        P = Parser(self.inputfile)
        while P.hasMoreLines():
            P.advance()
            P.instructionType()
            symbol = P.symbol()
            if P.curr_instructionType == 'L_INSTRUCTION':
                self.addEntry(symbol, self.rom_addr)
            elif P.curr_instructionType == 'A_INSTRUCTION' or P.curr_instructionType == 'C_INSTRUCTION':
                self.rom_addr += 1

    def A_pass(self):
        P = Parser(self.inputfile)
        while P.hasMoreLines():
            P.advance()
            P.instructionType()
            symbol = P.symbol()
            if P.curr_instructionType == 'A_INSTRUCTION':
                if not symbol.isdigit() and not self.contains(symbol):
                    self.addEntry(symbol, self.ram_addr)
                    self.ram_addr += 1

    def first_pass(self):
        self.L_pass()
        self.A_pass()
        self.symbolfile = self.inputfile.replace('asm', 'sym')
        with open(self.symbolfile, 'w') as f:
            for i in self.symbol_table.items():
                f.write(str(i) + '\n')

    def second_pass(self):
        P = Parser(self.inputfile)
        while P.hasMoreLines():
            P.advance()
            P.instructionType()
            if P.curr_instructionType == 'A_INSTRUCTION':
                symbol = P.symbol()
                if not symbol.isdigit():
                    number = self.getAddress(symbol)
                else:
                    number = int(symbol)
                code = bin(number)[2:].rjust(16, '0') + '\n'
                self.file.write(code)
            elif P.curr_instructionType == 'C_INSTRUCTION':
                code = '111'
                C = Code()
                code += C.comp(P.comp())
                code += C.dest(P.dest())
                code += C.jump(P.jump())
                code += '\n'
                self.file.write(code)
            else:
                assert P.curr_instructionType, 'not valid instruction type'

    def addEntry(self, symbol, address):
        self.symbol_table.update({symbol: address})

    def contains(self, symbol):
        return symbol in self.symbol_table.keys()

    def getAddress(self, symbol):
        return self.symbol_table[symbol]


if __name__ == '__main__':
    assert sys.argv[1].endswith(
        '.asm')
    A = Assembler(sys.argv[1])
    A.assemble()
