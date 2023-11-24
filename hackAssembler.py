#!/usr/bin/env python3

# Drives the translation process

import hackParser as Parser
import hackCode as Code
import hackSymboltable as SymbolTable
import sys

class Assembler:
    def __init__(self) -> None:
        self.symbols = SymbolTable.SymbolTable()
        self.symbol_addr = 16

    def pass0(self, file):
        parser = Parser.Parser(file)
        current_addr = 0
        while (parser.hasMoreLines()):
            parser.advance()
            cmdt = parser.command_type()
            if (cmdt == parser.A_COMMAND or cmdt == parser.C_COMMAND):
                current_addr += 1
            elif (cmdt == parser.L_COMMAND):
                self.symbols.addEntry(parser.symbol(), current_addr)


    def pass1(self, infile, outfile):
        parser = Parser.Parser(infile)
        outf = open(outfile, 'w')
        code = Code.Code()

        while (parser.hasMoreLines()):
            parser.advance()
            cmdt = parser.command_type()

            if (cmdt == parser.A_COMMAND):
                outf.write(code.gen_a(self._getAddress(parser.symbol())) + '\n')
            elif (cmdt == parser.C_COMMAND):
                outf.write(code.gen_c(parser.dest(), parser.comp(), parser.jump()) + '\n')
            elif (cmdt == parser.L_COMMAND):
                pass

        outf.close()


    def assemble(self, file):
        self.pass0(file)
        self.pass1(file, self._outfile(file))



    def _getAddress(self, symbol):
        if symbol.isdigit():
            return symbol
        else:
            if (not self.symbols.contains(symbol)):
                self.symbols.addEntry(symbol, self.symbol_addr)
                self.symbol_addr += 1
            return self.symbols.getAddress(symbol)

    def _outfile(self, infile):
        if (infile.endswith('.asm')):
            return infile.replace('.asm', '.hack')
        else:
            return infile + '.hack'






def main():
    if len(sys.argv) != 2:
        print("Usage: Assembler file.asm")
    else:
        infile = sys.argv[1]

    asm = Assembler()
    asm.assemble(infile)

main()