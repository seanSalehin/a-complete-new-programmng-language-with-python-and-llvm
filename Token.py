from enum import Enum
from typing import Any

class TokenType(Enum):
    #End of file token
    EOF = "EOF"

    #Lexor Error
    ILLEGAL = "ILLEGAL"
    

    #Data Types
    INT = "INT"
    FLOAT = "FLOAT"


    #Arithmatic Symbols
    PLUS = "PLUS"
    MINUS = "MINUS"
    ASTERISK = "ASTERISK"
    SLASH = "SLASH"
    POW = "POW"
    MODULUS = "MODULUS"


    #Symbols
    SEMICOLON = "SEMICOLON"
    LEFTPARENTHESES = "LEFTPARENTHESES"
    RIGHTPARENTHESES="RIGHTPARENTHESES"



class Token:
    def __init__(self, type, literal, line_number, position):
        self.type=type
        self.literal=literal
        self.line_number=line_number
        self.position=position
        
    #error
    def __str__(self):
        return f"Token[{self.type}:{self.literal}:Line{self.line_number}:Position{self.position}]"
        
    #representing
    def __repr__(self):
        return str(self)
            