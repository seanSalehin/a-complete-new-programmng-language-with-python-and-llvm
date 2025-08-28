from Lexer import Lexer
from Token import Token, TokenType
from typing import Callable
from enum import Enum, auto
from AST import Statement, Expression, Program, ExpressionStatement, InfixExpression, IntegerLiteral, FloatLiteral

# precedence Type => evels of operator priority from lowest to highest
class PresedanceType(Enum):
    P_LOWEST=0
    P_EQUALS=auto()
    P_LESSGREATER=auto()
    P_SUM=auto()
    P_CALL=auto()
    P_INDEX=auto()
    P_PREFIX=auto()
    P_EXPONENT=auto()
    P_PRODUCT=auto()




# precedence mapping => Maps token types (like PLUS, MINUS) to their corresponding precedence levels.
PRECEDENCES:dict[TokenType, PresedanceType]={
     TokenType.PLUS: PresedanceType.P_SUM,
     TokenType.MINUS:PresedanceType.P_SUM,
     TokenType.SLASH:PresedanceType.P_PRODUCT,
     TokenType.ASTERISK:PresedanceType.P_PRODUCT,
     TokenType.MODULUS:PresedanceType.P_PRODUCT,
     TokenType.POW:PresedanceType.P_EXPONENT,
}


class Parser:
    def __init__(self, lexer):
        self.lexer=lexer
        self.errors=[]
        self.current_token=None
        self.peek_token=None
        self.prefix_parse={
            TokenType.INT:self.__parse_int_literal,
            TokenType.FLOAT:self.__parse_float_literal,
            TokenType.LEFTPARENTHESES:self.__parse_grouped_expression,
        }
        self.infix_parse={
            TokenType.MINUS:self.__parse_infix_expression,
            TokenType.MODULUS: self.__parse_infix_expression,
            TokenType.SLASH: self.__parse_infix_expression,
            TokenType.PLUS: self.__parse_infix_expression,
            TokenType.POW: self.__parse_infix_expression,
            TokenType.ASTERISK: self.__parse_infix_expression,
        }
        #load the first two tokens (Calls twice)
        self.__next_token()
        self.__next_token()



    def __next_token(self):
        #Move current token to the peek token and get the next token from lexer
        self.current_token = self.peek_token
        self.peek_token = self.lexer.next_token()
        


    def __peek_token(self, tt):
        #check the type of the next token
        return self.peek_token.type == tt
    


    def __peek_error(self, tt):
        self.errors.append(f"Expected next token to be {tt}, not {self.peek_token.type}")



    def __expect_peek(self, tt):
        #ensure the next token matches an expected type
        if self.__peek_token(tt):
           self.__next_token()
           return True
        else:
            self.__peek_error(tt)
            return False



    def __no_prefix_parse_error(self, tt):
        #error when no parsing function exists for the current token
        self.errors.append(f"Expected next token to be {tt}, not {self.peek_token.type}")



    def __current_precedence(self):
        prec = PRECEDENCES.get(self.peek_token.type)
        if prec is None:
            #return the lowest by default if the prec in None
            return PresedanceType.P_LOWEST
        return prec
    


    def __peek_precedence(self):
        prec = PRECEDENCES.get(self.peek_token.type)
        if prec is None:
            return PresedanceType.P_LOWEST
        return prec
    

    #Main execution point of the parser
    def parse_program(self):
        program=Program()
        while self.current_token.type != TokenType.EOF:
            stmt=self.__parse_statement()
            if stmt is not None:
                program.statements.append(stmt)
            self.__next_token()
        return program
    

    #statement methods
    def __parse_statement(self):
        return self.__parse_expression_statement()
    
    
    def __parse_expression_statement(self):
        expr=self.__parse_expression(PresedanceType.P_LOWEST)
        #if we rech : it's mean the expression is done
        if self.__peek_token(TokenType.SEMICOLON):
            self.__next_token()
        # e => based on AST (ExpressionStatement)
        stmt=ExpressionStatement(e=expr)
        return stmt



    #Expression method
    def __parse_expression(self, precedence):
        prefix_function=self.prefix_parse.get(self.current_token.type)
        if prefix_function is None:
            self.__no_prefix_parse_error(self.current_token.type)
            return None
        left_expr=prefix_function()
        while not self.__peek_token(TokenType.SEMICOLON) and precedence.value < self.__peek_precedence().value:
            infix_function=self.infix_parse.get(self.peek_token.type)
            if infix_function is None:
                return left_expr
            self.__next_token()
            left_expr=infix_function(left_expr)
        return left_expr



    def __parse_infix_expression(self, left_node):
        infix_exp = InfixExpression(left_node=left_node, operator=self.current_token.literal)
        precedence = self.__current_precedence()
        self.__next_token()
        infix_exp.right_node=self.__parse_expression(precedence)
        return infix_exp
    

    def __parse_grouped_expression(self):
        self.__next_token()
        expr=self.__parse_expression(PresedanceType.P_LOWEST)
        if not self.__expect_peek(TokenType.RIGHTPARENTHESES):
            #if the last one is not a parentheses => syntax error
            return None
        return expr
    

    #prefix methods
    def __parse_int_literal(self):
        try:
            value = int(self.current_token.literal)
        except:
            self.errors.append("could not parse this as an Integer")
            return None
        int_lit = IntegerLiteral(value)
        return int_lit
    

    def __parse_float_literal(self):
        
        try:
            value=float(self.current_token.literal)
            float_lit=FloatLiteral(value)
        except:
            self.errors.append("could not parse this as an Intiger")
            return None
        return float_lit