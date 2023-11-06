#!/bin/python3

# reads and parses an instruction

import re


class Parser:
    A_COMMAND = 0
    C_COMMAND = 1
    L_COMMAND = 2
    
    def __init__(self, file_name) -> None:
        file = open(file_name, 'r')
        self._lines = file.read()
        self._commands = self._commands_list(self._lines.split('\n'))
        self.current_command = ''
        
        self._init_command_info()
    
    def _init_command_info(self):
        self._cmd_type = -1
        self._symbol = ''
        self._dest = ''
        self._comp = ''
        self._jump = ''
    
    def __str__(self) -> str:
        pass
    
    # Gibt es mehr Lines? -> BOOL
    def hasMoreLines(self):
        return self._commands != []
    
    # Überspringt Whitespace / comments.
    # Liest nächste Instruction und macht sie zur aktuellen
    # Nur wenn hasMoreLines() = true
    def advance(self):
        self._init_command_info()
        self.current_command = self._commands.pop(0)
        
        self._cmd_type = self.getInstructionType(self.current_command)
        
        if (self._cmd_type is Parser.A_COMMAND or self._cmd_type is Parser.L_COMMAND):
            self._symbol = self.getSymbol(self.current_command)
        if (self._cmd_type is Parser.C_COMMAND):
            self._dest = self.getDest(self.current_command)
            self._comp = self.getComp(self.current_command)
            self._jump = self.getJump(self.current_command)
    
    def _commands_list(self, lines):
        return [c for c in [self._single_command(l) for l in lines] if c != '']
    
    def _single_command(self, line):
        return self._remove_comments(line)
    
    _comment = re.compile('//.*$')
    def _remove_comments(self, line):
        return self._comment.sub('', line).strip()
    
    
    
    # Gibt den Typ der Instruction zurück:
    # A_INSTRUCTION für @xxx, wo xxx dezimal zahl oder symbol ist
    # C_INSTRUCTION für dest=comp;jump
    # L_INSTRUCTION für (xxx), wo xxx symbol ist
    def getInstructionType(self, instString):

        if (instString[0] == '@'):                                              # Check ob erstes Zeichen '@' ist
            #txt = instString.lstrip("@")                                        # Speichert String ohne @ in Variable txt
            #if (txt.isidentifier() or txt.isalnum()):                                                 # Check ob txt dezimal Zahl oder Symbol ist
            return Parser.A_COMMAND

        if (instString[0] == "("):                                              # Check ob erstes Zeichen '(' ist
            #txt = instString.strip("()")                                        # Speichert String ohne '()' in Variable txt
            #if (txt.isidentifier() or txt.isalpha()):                                                 # Check ob txt Symbol ist
            return Parser.L_COMMAND

        else:
            return Parser.C_COMMAND

    # Wenn aktive Instruction (xxx) ist, symbol xxx zurückgeben.
    # Wenn aktive Instruction @xxx ist, symbol oder dez. Zahl xxx zurückgeben (string).
    # Sollte nur aufgerufen werden wenn instructionType == A_INST || L_INST
    def getSymbol(self, instString):

        if (instString[0] == "("):
            Lstring = instString.strip("()")
            return Lstring

        if (instString[0] == "@"):
            Astring = instString.lstrip("@")
            return Astring


    # Gibt symbolischen "dest"-Part der aktiven C-Inst zurück (8 Möglichkeiten)
    # Sollte nur aufgerufen werden wenn instructionType == C_INST
    def getDest(self, instString):
        if (instString.count("=") != 0):
            destString = instString.split("=")
            return destString[0]
        else:
            return "null"


    # Gibt symbolischen "jump"-Part der aktiven C-Inst zurück (8 Möglichkeiten)
    # Sollte nur aufgerufen werden wenn instructionType == C_INST
    def getJump(self, instString):
        if (instString.count(";") != 0):
            jumpString = instString.rsplit(";")
            return jumpString[-1]
        else:
            return "null"


    # Gibt symbolischen "comp"-Part der aktiven C-Inst zurück (28 Möglichkeiten)
    # Sollte nur aufgerufen werden wenn instructionType == C_INST
    def getComp(self, instString):
        txt = instString.split("=")
        txt = txt[-1].split(";")
        return txt[0]

    def command_type(self):
        return self._cmd_type
    
    def symbol(self):
        return self._symbol
    
    def dest(self):
        return self._dest
    
    def comp(self):
        return self._comp
    
    def jump(self):
        return self._jump



