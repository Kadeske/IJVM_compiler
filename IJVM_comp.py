import ast
import re
from clean_code import clean
import subprocess
import platform

#non è per nienete ordinato nè ottimizzato, è già troppo se l'ho fatto
#Tutto per l'agguato alla spigola
"""
          /"*._         _
      .-*'`    `*-.._.-'/
    < * ))     ,       ( 
      `*-._`._(__.--*"`.\
"""

def controlla_errore_sintassi(line, anonim):

    if "else" in line:
        if not "{" in line:
            print("ERRORE --> { mancante in else" if not anonim else "!!{else")
        if not "}" in line:
            print ("ERRORE --> } mancante in else" if not anonim else "!!}else")
    if "if" in line:
        if not "{" in line:
            print("ERRORE --> { mancante in if" if not anonim else "!!{if")
    if "for" in line:
        if not "{" in line:
            print("ERRORE --> { mancante in for" if not anonim else "!!{for")
    if "while" in line:
        if not "{" in line:
            print("ERRORE --> { mancante in while" if not anonim else "!!{while")
    

    if "int" in line and not "print" in line:
        print("ERRORE -->  'int' non accettato, rimuovilo" if not anonim else "!! -> int")


def genera_albero(espressione):
    return ast.parse(str(espressione), mode='eval').body

def traduci_in_ijvm(nodo, output=None):
    if output is None:
        output = []
    
    if isinstance(nodo, ast.Constant):
        output.append(f"BIPUSH {nodo.value}")
    elif isinstance(nodo, ast.Name):
        output.append(f"ILOAD {nodo.id}")
    
    # Chiamate a funzione (ast.Call fa da solo e lo riconosce, godo)
    elif isinstance(nodo, ast.Call):
        # Carica OBJREF
        output.append("LDC_W OBJREF")
        
        # Carica tutti gli argomenti sullo stack
        for a in nodo.args:
            traduci_in_ijvm(a, output)
        
        # Determina il numero di argomenti
        num_args = len(nodo.args)
        
        # Genera la chiamata 
        output.append(f"INVOKEVIRTUAL {nodo.func.id}")
    
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

    res += '\n'.join(compila_ijvm(f"({var1})-({var2})".strip())) + "\n"

    if oper == "==":
        res+= f"IFLT {label}\n"
        res+='\n'.join(compila_ijvm(f"({var2})-({var1})".strip())) + "\n"
        res+= f"IFLT {label}\n"

    else:
        if not "=" in oper:
            res+="DUP\n"
        res+= f"IFLT {label}\n"
        if not "=" in oper:
            res+= f"IFEQ {label}\n"
    return res
    
def compila_corpo(lines, next_tag, anonim):

    order = []
    opened = []
    struct_opened =[]
    struct_opened_cond = []

    elenco_etichette = {}


    code = []

    for l in lines:

        controlla_errore_sintassi(l, anonim)

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
                prec = f"GOTO C{next_tag}\n"

            else:
                prec = ""

            order.append(f"{prec}C{act}:")

        if '{' in l:

            elenco_etichette[next_tag] = getStruct(l)

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
        elif "print" in l:
            order.append("LDC_W OBJREF")
            tmp = l.replace("print", "")
            order.extend(compila_ijvm(tmp.strip()))
            order.append("INVOKEVIRTUAL print")



    cp_order = order.copy()
    order = []

    #scorre e cambia nomi alle etichette 
    key_etichette = elenco_etichette.keys()

    for o in cp_order:
        for k in key_etichette: 
            o = o.replace(f"O{k}", f"{elenco_etichette[k]}{k}")
            o = o.replace(f"C{k}", f"fine_{elenco_etichette[k]}{k}")
        order.append(o)

    return order

def elenca_variabili(lines):

    words = ["for","while", "if", "else", "print", "input", "return", "fun"]

    elenco_lett = []

    for w in words:
        lines = [l.replace(w,"") for l in lines]

    for l in lines:
        for lett in l:
            if lett.isalpha():
                elenco_lett.append(lett)

    elenco_lett = list(set(elenco_lett))

    return elenco_lett


    
def clear_terminal():
    if platform.system() == "Windows":
        subprocess.run("cls", shell=True)
    else:
        subprocess.run("clear", shell=True)

def carica_impostazioni():
    start_id = 0 
    output_path = "out.txt" 
    override_input_request = False
    default_input_path = "input.txt" 
    instr = {
        'start_id': start_id,
        'output_path' : output_path,
        'override_input_request': override_input_request,
        'default_input_path' : default_input_path
    }

    inp = open("settings.sett")

    sett = [x.strip() for x in inp.readlines()]

    sett = clean(sett)

    for s in sett:
        tmp = s.split("=")
        tmp[0] = tmp[0].strip().replace("[","").replace("]", "")
        tmp[1] = tmp[1].strip().replace('"', "").replace("'", '')

        if isinstance(instr[tmp[0]], bool):
            value = tmp[1].lower() in ('true', '1', 'yes', 'y', 't')
        elif isinstance(instr[tmp[0]], int):
            value = int(tmp[1])
        elif isinstance(instr[tmp[0]], str):
            value = str(tmp[1])

        instr[tmp[0]] = value


    #riassegno i valori
    start_id = instr['start_id']
    output_path = instr['output_path']
    override_input_request = instr['override_input_request']
    default_input_path = instr['default_input_path']



    inp.close()
    return start_id, output_path, override_input_request, default_input_path



'''
inp = open("comp_py/test.txt", "r")

lines = [x.strip() for x in inp.readlines()]

lines = clean(lines)

inp.close()

print(compila_corpo(lines, 0))
'''