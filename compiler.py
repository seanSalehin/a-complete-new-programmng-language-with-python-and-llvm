from llvmlite import ir

from AST import NodeType, Statement, Expression, Program, ExpressionStatement, InfixExpression, IntegerLiteral, FloatLiteral

class Compiler:

    def __init__(self):
        self.type_map={
            'int':ir.IntType(32),
            'float':ir.FloatType(),
        }
        self.module = ir.Module('main')
        self.builder = ir.IRBuilder()
    


    def compile(self, node):
        match node.type():
            case NodeType.Program:
                self.__visit_program(node)

            case NodeType.ExpressionStatement:
                self.__visit_expression_statement(node)

            case NodeType.InfixExpression:
                self.__visit_infixExpression(node)

    
    def __visit_program(self, node):
        function_name="main"
        parameters_types=[]
        return_type=self.type_map["int"]
        functionType = ir.FunctionType(return_type, parameters_types)
        function = ir.Function(self.module, functionType, name=function_name)
        block = function.append_basic_block(f"(function_name)_entry")
        self.builder = ir.IRBuilder(block)

        for stmt in node.statements:
            self.compile(stmt)
        return_value = ir.Constant(self.type_map["int"], 444)
        self.builder.ret(return_value)


    def __visit_expression_statement(self, node):
        self.compile(node.e)

    def __visit_infixExpression(self, node):
        operator = node.operator
        left_value, left_type = self.__resolve_value(node.left_node)
        right_value, right_type=self.__resolve_value(node.right_node)
        value = None
        Type=None
        if isinstance(right_type, ir.IntType) and isinstance(left_type, ir.IntType):
            Type = self.type_map['int']
            match operator:
                case '+':
                    value = self.builder.add(left_value, right_value)
                case '-':
                    value = self.builder.sub(left_value, right_value)
                case '*':
                     value = self.builder.mul(left_value, right_value)
                case '/':
                    value = self.builder.sdiv(left_value, right_value)   
                case '%':
                    value= self.builder.srem(left_value, right_value) 
                case '^':
                    # TODO
                    pass
        elif isinstance(right_type, ir.FloatType) and isinstance(left_type, ir.FloatType):
            Type = ir.FloatType()
            match operator:
                case '+':
                    value = self.builder.fadd(left_value, right_value)
                case '-':
                    value = self.builder.fsub(left_value, right_value)
                case '*':
                    value = self.builder.fmul(left_value, right_value)
                case '/':
                    value = self.builder.fdiv(left_value, right_value)
                case '%':
                    value = self.builder.frem(left_value, right_value)
                case '^':
                    #TODO
                    pass

        return value, Type

    def __resolve_value(self, node, value_type=None):
        match node.type():
            case NodeType.IntegerLiteral:
                node=node
                value, Type = node.value, self.type_map['int' if value_type is None else value_type]
                return ir.Constant(Type, value), Type
            
            case NodeType.FloatLiteral:
                node=node
                value, Type = node.value, self.type_map['float' if value_type is None else value_type]
                return ir.Constant(Type, value), Type
            
            case NodeType.InfixExpression:
                return self.__visit_infixExpression(node)
               
