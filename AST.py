#Abstract Syntax Tree =>showing only meaningful parts like expressions and statements without extra syntax details.
from abc import ABC, abstractmethod
from enum import Enum

class NodeType(Enum):
    Program="Program"
    ExpressionStatement = "ExpressionStatement"
    InfixExpression = "InfixExpression"
    IntegerLiteral = "IntegerLiteral"
    FloatLiteral = "FloatLiteral"



class Node(ABC):
    #each node represents a piece of the program's syntax.
    #each node has type and can be converted to JSON.
    @abstractmethod
    def type(self):
        pass


    @abstractmethod
    #for debuging
    def json(self):
        pass


    
class Statement(Node):
    pass

class Expression(Node):
    pass

class Program(Node):
    def __init__(self):
        self.statements=[]
    
    def type(self):
        return NodeType.Program
    
    def json(self):
        return {
            "type":self.type().value,
            "statements":[{stmt.type().value:stmt.json()}for stmt in self.statements]
        }
    

#statement
class ExpressionStatement(Statement):
    def __init__(self, e):
        self.e=e

    def type(self):
        return NodeType.ExpressionStatement

    def json(self):
        return{
            "type":self.type().value,
            "e":self.e.json()
        }
    

#expressions
class InfixExpression(Expression):
    def __init__(self, left_node, operator, right_node=None):
        self.left_node=left_node
        self.operator=operator
        self.right_node=right_node

    def type(self):
        return NodeType.InfixExpression
    
    def json(self):
        return {
            "type":self.type().value,
            "left_node":self.left_node.json(),
            "operatpr":self.operator,
            "right_node":self.right_node.json()
        }
    

#Literals
class IntegerLiteral(Expression):
    def __init__(self, value):
        self.value=value
    
    def type(self):
        return NodeType.IntegerLiteral
    
    def json(self):
        return {
            "type":self.type().value,
            "value":self.value
        }
    

class FloatLiteral(Expression):
    def __init__(self, value):
        self.value=value
    
    def type(self):
        return NodeType.FloatLiteral
    
    def json(self):
        return {
            "type":self.type().value,
            "value":self.value
        }