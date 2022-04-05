from lark.lark import Lark
#issues: f(x,y); is not treated as an acceptable top level, because it tries to parse it as the first part of a func def.
parser = Lark('''
              ?toplevels : toplevel+
              ?toplevel : statement | funcdef

              idwithtype : IDENT ":" type -> idwithtype

              funcbody : "{" statement+ "}" -> funcbody
              funcargs : "(" [idwithtype ("," idwithtype)*] ")" -> funcargs
              funcdef : "def" IDENT funcargs "->" type funcbody -> funcdef

              type : "Int" -> tyint
                   | "Bool" -> tybool

              ?statement : if
                        | while
                        | assign ";"
                        | expr ";"
                        | "return" expr ";" -> return

              if : "if" expr "{" statement+ "}" ["else" "{" statement+ "}"] -> if
              while : "while" expr "{" statement+ "}" -> while
              assign : IDENT "=" expr -> assign

              ?expr : product
                   | cmp
                   | expr "+" product -> add
                   | expr "-" product -> sub

              ?product : atom
                      | product "*" atom -> mul
                      | product "/" atom -> div

              ?atom : SIGNED_NUMBER
                   | "-" atom -> neg
                   | call
                   | IDENT
                   | "(" expr ")"

              ?cmp  : bool
                   | expr ">" expr -> gt
                   | expr "<" expr -> lt
                   | expr "==" expr -> eq

              bool : "true" -> true
                   | "false" -> false
              call : IDENT "(" [expr ("," expr)*] ")" -> call

              IDENT : /[a-zA-Z]([a-zA-Z0-9]|_|-)*/

              %import common.SIGNED_NUMBER
              %import common.WS
              %ignore WS
              ''', start="toplevels",parser="lalr")
# while True:
#     try:
#         s = input("> ")

#     except EOFError:
#         break
#     print(parser.parse(s))
#     print(parser.parse(s).pretty())
