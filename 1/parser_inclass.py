from lark.lark import Lark
parser = Lark('''
              ?toplevels : toplevel+
              ?toplevel : statement | funcdef

              funcdef : IDENT "(" [IDENT ("," IDENT)*] ")" "{" statement+ "}"

              statement : if
                        | while
                        | assign ";"
                        | expr ";"
                        | "return" expr ";" -> return

              if : "if" expr "{" statement+ "}" ["else" "{" statement+ "}"]
              while : "while" expr "{" statement+ "}"
              assign : IDENT "=" expr

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
              call : IDENT "(" [expr ("," expr)*] ")"

              IDENT : /[a-zA-Z]([a-zA-Z0-9]|_|-)*/

              %import common.SIGNED_NUMBER
              %import common.WS
              %ignore WS
              ''', start="toplevels",parser="lalr")
while True:
    try:
        s = input("> ")

    except EOFError:
        break
    print(parser.parse(s))
    print(parser.parse(s).pretty())
