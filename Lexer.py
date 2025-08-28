from Token import Token, TokenType
from typing import Any

class Lexer:
    def __init__(self, source):
        self.source=source
        self.position=-1
        self.read_position=0
        self.line_number=1
        self.current_character=None
        #for updating lexer (add number to position and line)
        self.__read_char()



    def __read_char(self):
        #check if we are at the end of the file or not
        if self.read_position>=len(self.source):
            self.current_character=None
        else:
            self.current_character=self.source[self.read_position]
        self.position=self.read_position
        self.read_position+=1



    def __skip_whitespace(self):
        #skip ignored characters like new lines, spaces, tabs
        while self.current_character in [' ','\t', '\n','r']:
            if self.current_character =='\n':
                self.line_number+=1
            self.__read_char()




    def __new_token(self, tokens, literal):
        return Token(type=tokens, literal=literal, line_number=self.line_number, position=self.position)



    def __is_digit(self, ch):
        #if our tokens were not inside (*^%+-) then this function check that if current character is an intiger or not
        return '0' <=ch and ch <='9'



    def __read_number(self):
        start_position=self.position
        dot_count=0
        output=""
        while self.__is_digit(self.current_character) or self.current_character==".":
            #checking for decimal
            if self.current_character==".":
                dot_count +=1
            if dot_count>1:
                print("Decimal numbers should only have one dot")
                #start position to current position is illegal
                return self.__new_token(TokenType.ILLEGAL, self.source[start_position:self.position])
            output+=self.source[self.position]
            self.__read_char()
            if self.current_character is None:
                break
        if dot_count==0:
            #it is an intiger
            return self.__new_token(TokenType.INT, int(output))
        else:
            return self.__new_token(TokenType.FLOAT, float(output))


    def next_token(self):
        token=None
        self.__skip_whitespace()

        #handle intigers
        if self.current_character is not None and self.__is_digit(self.current_character):
            return self.__read_number()
        
        match self.current_character:
            case'+':
                token=self.__new_token(TokenType.PLUS, self.current_character)
            case'-':
                token=self.__new_token(TokenType.MINUS, self.current_character)
            case'*':
                token=self.__new_token(TokenType.ASTERISK, self.current_character)
            case'/':
                token=self.__new_token(TokenType.SLASH, self.current_character)                
            case'^':
                token=self.__new_token(TokenType.POW, self.current_character)
            case'%':
                token=self.__new_token(TokenType.MODULUS, self.current_character)                
            case'(':
                token=self.__new_token(TokenType.LEFTPARENTHESES, self.current_character)
            case')':
                token=self.__new_token(TokenType.RIGHTPARENTHESES, self.current_character)
            case';':
                token=self.__new_token(TokenType.SEMICOLON, self.current_character)
            case None:
                token=self.__new_token(TokenType.EOF, "")
            case _:
                # Illegal token for unmatched characters
                token = self.__new_token(TokenType.ILLEGAL, self.current_character)
        
        #read a new character and return the token
        self.__read_char()
        return token