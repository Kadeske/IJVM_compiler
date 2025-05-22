import ast
from clean_code import clean

def genera_albero(espressione):
    return ast.parse(str(espressione), mode='eval').body
def traduci_in_ijvm(nodo, output=None):
    if output is None:
        output = []
    
    if isinstance(nodo, ast.Constant):
        output.append(f"BIPUSH {nodo.value}")
    elif isinstance(nodo, ast.Name):
        output.append(f"ILOAD {nodo.id}")
    elif isinstance(nodo, ast.BinOp):
        # Carica OBJREF prima di ogni operazione burda 
        if isinstance(nodo.op, (ast.Mult, ast.Div, ast.Mod)):
            output.append("LDC_W OBJREF")
        
        traduci_in_ijvm(nodo.left, output)
        traduci_in_ijvm(nodo.right, output)
        
        if isinstance(nodo.op, ast.Add):
            output.append("IADD")
        elif isinstance(nodo.op, ast.Sub):
            output.append("ISUB")
        elif isinstance(nodo.op, ast.Mult):
            output.append("INVOKEVIRTUAL mul")
        elif isinstance(nodo.op, ast.Div):
            output.append("INVOKEVIRTUAL div")
        elif isinstance(nodo.op, ast.Mod):
            output.append("INVOKEVIRTUAL mod")
    elif isinstance(nodo, ast.UnaryOp):
        traduci_in_ijvm(nodo.operand, output)
        if isinstance(nodo.op, ast.USub):
            output.append("INEG")
    
    return output

def compila_ijvm(espressione):
    albero = genera_albero(espressione)
    codice = traduci_in_ijvm(albero)
    return codice


def getStruct(s):
    if "while" in s:
        return "while"
    elif "for" in s:
        return "for"
    elif "if" in s:
        return "if"
    elif "else" in s:
        return "else"
    else:
        return ""
    
def getArithmetic(s):

    # a = b * (a+b)
    # a = b * 4 / 2 

    
    if "+=" in s:
        tmp = s.split("+=")
        s = f"{tmp[0].strip()} = {tmp[0].strip()} + {tmp[1].strip()}"
    elif "-=" in s:
        tmp = s.split("-=")
        s = f"{tmp[0].strip()} = {tmp[0].strip()} - {tmp[1].strip()}"
    elif "++" in s:
        tmp = s.split("++")
        s = f"{tmp[0].strip()} = {tmp[0].strip()} +1"
    elif "--" in s:
        tmp = s.split("--")
        s = f"{tmp[0].strip()} = {tmp[0].strip()} -1"


    

    s = s.split("=")

    res = compila_ijvm(s[1].strip())

    for i in s[0]:
        if i.isalnum():
            res.append(f"ISTORE {i}")
        

    return res 

def getOper(s):
    if ">=" in s:
        return ">="
    elif "<=" in s:
        return "<="
    elif "<" in s:
        return "<"
    elif ">" in s:
        return ">"
    elif "==" in s:
        return "=="
    else:
        return None
def getCondition(s, label):
    oper = getOper(s)
    res = ''
    

    s = s.split(oper)

    if "<" in oper:
        var1 = s[1].strip(")")
        var2 = s[0].strip("(")
    else:
        var1 = s[0].strip("(")
        var2 = s[1].strip(")")

    res += '\n'.join(compila_ijvm(f"{var1}-{var2}".strip())) + "\n"

    if oper == "==":
        res+= f"IFLT {label}\n"
        res+='\n'.join(compila_ijvm(f"{var2}-{var1}".strip())) + "\n"
        res+= f"IFLT {label}\n"

    else:
        if not "=" in oper:
            res+="DUP\n"
        res+= f"IFLT {label}\n"
        if not "=" in oper:
            res+= f"IFEQ {label}\n"
    return res
    

def compila(input_path):

    inp = open(input_path, "r")

    lines = [x.strip() for x in inp.readlines()]

    lines = clean(lines)


    order = []
    opened = []
    struct_opened =[]
    struct_opened_cond = []

    next_tag = 0

    code = []


    for l in lines:

        if '}' in l:
            act = opened.pop()
            st = struct_opened.pop()
            cond = struct_opened_cond.pop()
            if st == "while":
                prec = f"GOTO O{act}\n"

            elif st == "for":
                cond = cond.split(";")
                prec = f"\n{'\n'.join(getArithmetic(cond[2][:cond[2].index(")")].strip()))}\nGOTO O{act}\n"        # DA FINIRE
            elif "else" in l:
                prec = f"GOTO C{act+1}\n"

            else:
                prec = ""

            order.append(f"{prec}C{act}:")


        if '{' in l:

            if "(" in l:
                cond = l[l.index("("):l.index(")")+1]

            else:
                cond = "empty"

            if getStruct(l) == "for":
                tmp = cond.split(";")
                order.append('\n'.join(getArithmetic(tmp[0][tmp[0].index("(")+1:].strip())))


            order.append(f"O{next_tag}:")

            if getStruct(l) == "for":
                tmp = cond.split(";")
                order.append(getCondition(tmp[1],f"C{next_tag}"))

            elif cond != "empty":
                order.append(getCondition(cond,f"C{next_tag}"))



            
            opened.append(next_tag)
            struct_opened.append(getStruct(l))
            struct_opened_cond.append(cond)

            next_tag+=1

        if "return" in l:
            code = compila_ijvm(l.split("return")[1].strip())
            for code_l in code:
                order.append(code_l)
            order.append("IRETURN")

        elif ("=" in l or "++" in l or "--" in l) and getStruct(l) == "":
            code = getArithmetic(l)
            for code_l in code:
                order.append(code_l)

        elif "input" in l:
            tmp = l.split("input")
            order.append("LDC_W OBJREF")
            order.append("INVOKEVIRTUAL input")
            order.append(f"ISTORE {tmp[1].strip()}")

        

    inp.close()
    return order





def main():
    input_path = input("Inserisci il percorso del file contenente lo pseudocidice: ")
    output_path = "out.txt"

    out = open(output_path, "w+")
    for o in compila(input_path):
        print(f"{o}")
        out.write(f"{o}\n")    

    print(f"DUMP FATTO IN '{output_path}'")

    print(compila_ijvm("5"))



if __name__ == "__main__":
    main()



