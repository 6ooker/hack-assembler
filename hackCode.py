#!/bin/python3

# generates binary codes


class Code:
    def __init__(self) -> None:
        pass
    
    def gen_a(self, addr):
        return '0' + self._bits(addr).zfill(15);
    
    
    def gen_c(self, dest, comp, jump):
        return '111' + self.comp(comp) + self.dest(dest) + self.jump(jump)
    
    _dest_fields = ['null', 'M', 'D', 'MD', 'A', 'AM', 'AD', 'AMD']
    def dest(self, destString):
        return self._bits(self._dest_fields.index(destString)).zfill(3)
    
    _jump_fields = ['null', 'JGT', 'JEQ', 'JGE', 'JLT', 'JNE', 'JLE', 'JMP']
    def jump(self, jumpString):
        return self._bits(self._jump_fields.index(jumpString)).zfill(3)
    
    _comp_fields = {'0': '0101010', '1': '0111111', '-1': '0111010',
                    'D': '0001100', 'A': '0110000', '!D': '0001101',
                    '!A': '0110001', '-D': '0001111', '-A': '0110011',
                    'D+1': '0011111', 'A+1': '0110111', 'D-1': '0001110',
                    'A-1': '0110010', 'D+A': '0000010', 'D-A': '0010011',
                    'A-D': '0000111', 'D&A': '0000000', 'D|A': '0010101',
                    'M': '1110000', '!M': '1110001', '-M': '1110011',
                    'M+1': '1110111', 'M-1': '1110010', 'D+M': '1000010',
                    'D-M': '1010011', 'M-D': '1000111', 'D&M': '1000000',
                    'D|M': '1010101'}
    
    def comp(self, compString):
        return self._comp_fields[compString]
    
    
    def _bits(self, n):
        return bin(int(n))[2:]