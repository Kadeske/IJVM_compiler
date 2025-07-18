import ast
import re
from utils import *

#non è per nienete ordinato nè ottimizzato, è già troppo se l'ho fatto
#Tutto per l'agguato alla spigola
"""
          /"*._         _
      .-*'`    `*-.._.-'/
    < * ))     ,       ( 
      `*-._`._(__.--*"`.\
"""

pattern_variabile_valida = r'(?!\S=+-*/;,)[a-zA-Z_][a-zA-Z0-9_]*(?!\S=+-*/;,)'


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


def getArithmetic(s):
    
    #trasforma la sintassi accorciata di incrementi e decrementi in operazioni normali es a++ -> a = a + 1
    if "+=" in s:
        tmp = s.split("+=")
        s = f"{tmp[0].strip()} = {tmp[0].strip()} + ({tmp[1].strip()})"
    elif "-=" in s:
        tmp = s.split("-=")
        s = f"{tmp[0].strip()} = {tmp[0].strip()} - ({tmp[1].strip()})"
    elif "++" in s:
        tmp = s.replace("++","")
        if bool(re.fullmatch(pattern_variabile_valida, tmp.strip())):
            return [f"IINC {tmp.strip()} 1"]
        else:
            addError(global_data['error_log_path'], "Attenzione! utilizzo errato dell'operatore di inremento '++'")
    elif "--" in s:
        tmp = s.replace("--","")
        if bool(re.fullmatch(pattern_variabile_valida, tmp.strip())):
            return [f"IINC {tmp.strip()} -1"]
        else:
            addError(global_data['error_log_path'], "Attenzione! utilizzo errato dell'operatore di decremento '--'")

    
    s = s.split("=")    #divide per l'uguale in modo da capire chi riceve l'operazione

    res = compila_ijvm(s[1].strip())    #trasformo l'operazione dopo l'uguale

    #Rimetto il risultato dell'operazione nel left value, controllando che sia una variabile
    if bool(re.fullmatch(pattern_variabile_valida, s[0].strip())):
            res.append(f"ISTORE {s[0]}")

  
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
    elif "!=" in s:
        return "!="
    else:
        return None
    
def getCondition(s,label):
    return getSingleCondition(s,label)
    #mai finito, sono troppo pigro e non serve
    
    # c > 8 && a == b || b == 9 && c == 0 && t == 9
    conds_or = []
    conds_and = []
    if "||" in s:
        tmp = s.split("||")
        for t in tmp:
            if "&&" in t:
                sep = t.split("&&")
                conds_and.extend(sep[1:])
                conds_or.append(sep[0])
            else:
                conds_or.append(t)
    else :
        pass
    print( conds_or)
    print (conds_and)


def getSingleCondition(s, label, invert = False):
    oper = getOper(s)
    res = ''


    if invert:
        if "<" in oper:
            new_oper = ">"
        elif ">" in oper:
            new_oper = "<"

        if new_oper != None and "=" in oper:
            new_oper+= "="
        elif oper == "==":
            new_oper = "!="
        else:
            new_oper = "=="
        
        oper = new_oper
                



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
    elif oper == "!=":
        res+=f"IFEQ {label}\n"
    else:
        if not "=" in oper:
            res+="DUP\n"
        res+= f"IFLT {label}\n"
        if not "=" in oper:
            res+= f"IFEQ {label}\n"
    return res
    
def compila_corpo(lines, next_tag, anonim, other_func_names):

    order = []
    opened = []
    struct_opened =[]
    struct_opened_cond = []

    elenco_etichette = {}

    code = []

    lines = clean(lines, True,True, True)

    lines = modifica_graffe_struct(lines)
    lines = modifica_else_if(lines)


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
            elif st == "do":
                if "while" in l:
                    cond = l[l.index("("):l.index(")")+1]
                    prec = f"{getCondition(cond, f"C{act}")}\nGOTO O{act}\n"
                else:
                    addError(global_data['error_log_path'], f"Errore: la chiusura del do non coincide con il while associato")



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
            #any([True if l in x else False for x in other_func_names])
        elif ("=" in l or "++" in l or "--" in l ) and getStruct(l) == "":
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
        elif any([True if x in l else False for x in other_func_names]) and getStruct(l) == "":
            order.extend(compila_ijvm(l))


    order = converti_all_lista(order)
    order = indent_code(order)

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

def elenca_variabili(lines, other_func_names):
    words = ["for","while", "if", "else", "print", "printf", "input", "return", "fun", "do"]
    
    elenco_parole = []

    for f in other_func_names:
        lines = [l.replace(f,"") for l in lines]

    for w in words:
        lines = [l.replace(w,"") for l in lines]

    for l in lines:
        elenco_parole.extend(re.findall(pattern_variabile_valida, l))

    elenco_parole = list(set(elenco_parole))

    return elenco_parole

    
def separa_metodi(lines):
    func_lines = {}
    func_parameters = {}

    while lines[0] == '':
        lines = lines[1:]   #tolgo le linee vuote

    #primo posto non vuoto sarà la prima firma peffò
    opened = 0
    closed = 0
    for l in lines:
        if abs(opened - closed) == 0 and l != '':
            if len(l.replace("","").strip()) > 1:
                tmp_code = []
                tmp = l.replace(" ", "")
                tmp = tmp.split("(")
                func_name = tmp[0].replace("(","")
                tmp[1] = tmp[1].replace(")","").replace("{","")
                func_var = [v for v in tmp[1].split(",")]
        

        tmp_code.append(l)

        if "{" in l:
            opened += 1
        if "}" in l:
            closed += 1
            if abs(opened - closed) == 0:
                tmp_code = tmp_code[1:-1]
                func_lines[func_name] = tmp_code.copy()
                func_parameters[func_name] = func_var
                tmp_code = []

    return func_parameters, func_lines
    



def compila_funzione(func_name, func_param, func_lines, anonim, other_func_names):

    code = []
    elenco_var = elenca_variabili(func_lines, other_func_names)
    for x in func_param:
        if x in elenco_var:
            elenco_var.remove(x)

    #apertura metodo
    if func_name != "main":
        code.append(f".method {func_name}({','.join(func_param)})")
    else:
        code.append(".main")

    #inserimento variabili non presenti tra i parametri
    if len(elenco_var) > 0:
        code.append(".var")
        code.extend(elenco_var)
        code.append(".end-var")

    #inserimento corpo della funzione

    try:
        code.extend(compila_corpo(func_lines,global_data['start_id'], anonim, other_func_names))
    except Exception :
        addError(global_data['error_log_path'], f"Errore inaspettato durante il compilamento del corpo del metodo {func_name}")
        

    #chiusura metodo
    if func_name != "main":
        code.append(".end-method")
    else:
        code.append("HALT")
        code.append(".end-main")

    return code

    

def compila_input(input_path, anonim):

    code = []

    #prendi input dati e pulisci
    inp = open(input_path, "r")

    lines = [x.strip() for x in inp.readlines()]

    lines = clean(lines, True, True, False) #pulisce ma non toglie gli spazi

    inp.close()

    #toglie maiuscole dalle srtrutture
    lines = lowercase_target_words_regex(lines)

    


    #dividi codice per metodi
    try:
        func_parameters, func_lines = separa_metodi(lines)
       
    except Exception:
        addError(global_data['error_log_path'], "Errore inaspettato nel riconoscimento delle funzioni, prova a ricontrollare firme e chiusure delle funzioni")
        return


    #identifica main e mettilo per primo
    func_keys = list(func_lines.keys())

    if "main" in func_keys:
        code.extend(compila_funzione("main", [], func_lines["main"], anonim, func_keys))
        func_keys.remove("main")
        code.append("\n")
    #per ogni metodo compila corpo
    
    for k in func_keys:
        code.extend(compila_funzione(k, func_parameters[k], func_lines[k],anonim,func_keys))
        code.append("\n")


    #apri file output
    out = open(global_data['output_path'], "w+")
    writed = False


    #controllo se inserire il template 
    if global_data['load_template']:
        #controllo che il template esista
        try:
            open(global_data['template_path'], "r")
        except:
            addError(global_data['error_log_path'], f"Template non trovato nella path '{global_data['template_path']}'")
        else:
            #controllo che sia presente il segnaposto in cui inserire il programma
            if global_data['template_symbol_insertion'] not in open(global_data['template_path'], "r").read():
                addError(global_data['error_log_path'], f"Non trovato il punto di inserimento del programma, '{global_data['template_symbol_insertion']}'")
            else:
                #inserisco primo pezzo template (fino al simbolo scelto)
                template = open(global_data['template_path'], "r")
                template_lines = [x.replace("\n","") for x in template.readlines()]
                for tl in template_lines:
                    if global_data['template_symbol_insertion'] not in tl:
                        out.write(f"{tl}\n")
                    else:
                        for c in code:
                            if not anonim:
                                print(c)
                            out.write(f"{c}\n")
                writed = True
    
    # se per qualche motivo non è stato possibile finire la scirttura con il template
    #riscrivo ma senza il template
    if not writed:
        out.close()
        out = open(global_data['output_path'], "w+")    #così è obbligato a resettarlo
        for c in code:
            if not anonim:
                print(c)
            out.write(f"{c}\n")

    
    out.close()

    print(f"\n\nDUMP FATTO IN {global_data['output_path']}" if not anonim else "<<")

    




