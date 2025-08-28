from Lexer import Lexer
from parser import Parser
from AST import Program
import json
from compiler import Compiler
from llvmlite import ir
import llvmlite.binding as llvm
from ctypes import CFUNCTYPE, c_int, c_float


Lexer_Bug=False
Parse_Bug=False
Compiler_Bug = True


if __name__=='__main__':
    with open("Test/compiler.Pneuma", 'r') as f:
        code=f.read()



    #lexer debug
    if Lexer_Bug:
        debug=Lexer(source=code)
        while debug.current_character is not None:
            print(debug.next_token())

    l=Lexer(source=code)
    p = Parser(lexer=l)

    program = p.parse_program()
    if len(p.errors)>0:
         for err in p.errors:
             print(err)
         exit(1)

    #parser debug
    if Parse_Bug:
        print("parser debug")
        #program = p.parse_program()
        with open("debug/ast.json", "w") as f:
            json.dump(program.json(), f, indent=4)
        print("wrote AST to debug/ast.json sucessfully")


    #compiler debug
    c=Compiler()
    c.compile(node=program)
    module=c.module
    module.triple = llvm.get_default_triple()
    if Compiler_Bug:
        with open("debug/ir.ll", "w") as f:
            f.write(str(module))