from parser import parser
#checks if the arguement is well-types, raising an error if there is a type error
# returning None if the arguement is not itself typed,
# or returning the type it checks out as if there it is typed.
def parsedTypeToType(t):
    if t == "tyint":
        return "INT"
    if t == "tybool":
        return "BOOL"
    return None
def typeCheck(tree, tys):
    #because life is suffering, tokens have tree.type, while nodes have tree.data
    try:
        tree.data
    except:
        if tree.type == "SIGNED_NUMBER":
            return ("INT",{})
        #idenifiers
        if tree.type == "IDENT":
            return (tys[tree.value], {})
        else:
            raise Exception(f"how did this happen?, tree.type is {tree.type}")
    if tree.data == "funcdef":
        #name
        name = tree.children[0].value
        #arguements
        # -3 to deal with the return type and body
        argTypes = []
        if tree.children[1].children[0] != None:
            for i in tree.children[1].children:
                argTy = parsedTypeToType(i.children[1].data)
                argTypes.append(argTy)
                tys[i.children[0].value] = argTy
        #return type
        #bit of a hacky way to deal with returns
        #starts with a 1 so no parsed value could be this
        retType = parsedTypeToType(tree.children[2].data)
        funcType = (argTypes,retType)
        tys["1currentFunc"] = funcType
        tys[name] = funcType
        for i in tree.children[3].children:
            tys = tys | typeCheck(i,tys)[1]
        return (None,{name : funcType})
    #TODO
    if tree.data == "assignment":
        name = tree.children[0].value
        #needs to be an expression, so there won't be bindings
        ty = typeCheck(tree.children[1],tys)[0]
        return (None,{name : ty})
    if tree.data == "return":
        ty = typeCheck(tree.children[0],tys)[0]
        if tys["1currentFunc"][1] == ty:
            return (None,{})
        funcRetType = tys["1currentFunc"][1]
        raise Exception(f"invalid return type, expected {funcRetType}, saw {ty}")
    #statements
    if  tree.data == "while" or tree.data == "if":
        #yields no value, only need to check for type errors in children
        #in case of the creation of new bindings, we update the type bindings.
        for i in tree.children:
             typeCheck(i,tys)[1]
        return (None,{})
    if tree.data == "toplevels":
        #yields no value, only need to check for type errors in children
        #in case of the creation of new bindings, we update the type bindings.
        newTys = {}
        for i in tree.children:
            newTys = newTys | typeCheck(i,tys)[1]
        return (None,newTys)
    #binary/unary integer operations
    if (tree.data == "add" or tree.data == "sub" or tree.data == "mul" or tree.data == "div"
            or tree.data == "neg" or tree.data == "gt" or tree.data == "lt"):
        for i in tree.children:
            ty = typeCheck(i,tys)
            #If we were making a non-trivial interpreter, we would want to keep track of locations and report a line number here
            if ty[0] != "INT":
                raise Exception(f"expected INT in {tree.data}, saw {ty}")
        #gt and lt take ints as arguments, but return bools
        if tree.data == "gt" or tree.data == "lt":
            return ("BOOL",{})
        return ("INT",{})
    #equality
    if tree.data == "eq":
        #check that the types are the same
        firstTy = typeCheck(tree.children[0],tys)
        secondTy = typeCheck(tree.children[1],tys)
        if firstTy == secondTy:
            return ("BOOL",{})
        raise Exception(f"expected types to be equal in eq, saw {firstTy} and {secondTy}")
    if tree.data == "call":
        ty = tys[tree.children[0].value]
        #no arguements
        if ty[0] == [] and tree.children[1] == None:
            return (ty[1],{})
        for (i,j) in (ty[0],tree.children[1:]):
            argTy = typeCheck(j,tys)[0]
            if i != j:
                raise Exception(f"mismatch in {tree.children[0].value} function call, expected {i}, saw {argTy}")
        return (ty[1],{})
    if tree.data == "true" or tree.data == "false":
        return ("BOOL",{})
    raise Exception(f"did not recognize {tree.data}")

# while True:
#     try:
#         s = input("> ")
#     except EOFError:
#         break
#     print(parser.parse(s))
#     print(parser.parse(s).pretty())
#     print("type checking:")
#     print(typeCheck(parser.parse(s),{}))
