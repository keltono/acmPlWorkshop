from lark.lark import Lark
parser = Lark(r'''
        ?toplevels : toplevel+
        ?toplevel  : statement | funcdef

        funcdef    : IDENT "(" [expr ("," expr)*] ")" "{" statements "}"

        ?statements: statement+
        statement  : if
                   | while
                   | for
                   | assign ";"
                   | expr ";"
                   | "return" expr? ";" -> return

        if         : "if" expr "{" statements "}" ["else" "{" statements "}"]
        while      : "while" expr "{" statements "}"
        for        : "for" "("assign ";" cmp ";" expr ")"  "{" statements "}"
        assign     : IDENT "=" expr

        ?expr      : product
                   | cmp
                   | expr "+" product -> add
                   | expr "-" product -> sub

        ?product   : atom
                   | product "*" atom -> mult
                   | product "/" atom -> div

        ?atom      : SIGNED_NUMBER
                   | "-" atom -> neg
                   | call
                   | IDENT -> ident
                   | ESCAPED_STRING -> string
                   | "(" expr ")"

        ?cmp       : bool
                   | expr ">" expr -> gt
                   | expr "<" expr -> lt
                   | expr "==" expr -> eq

        bool       : "true" | "false"
        call       : IDENT "(" [expr ("," expr)*] ")"

        IDENT      : /([a-zA-Z]|_)([a-zA-Z0-9]|-|_)*/

        %import common.ESCAPED_STRING
        %import common.SIGNED_NUMBER
        %import common.WS
        %ignore WS
        ''',start = "toplevels",parser="lalr")

def main():
    while True:
        try:
            s = input('> ')
        except EOFError:
            break
        print(parser.parse(s))
        print(parser.parse(s).pretty())
main()
