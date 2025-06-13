import re 
import hashlib
from datetime import *
import subprocess
import platform



def clear_terminal():
    if platform.system() == "Windows":
        subprocess.run("cls", shell=True)
    else:
        subprocess.run("clear", shell=True)


def get_file_hash(filename):
    with open(filename, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()
    
def addError(error_log_path, error_message):

    err = open(error_log_path, "a+")

    err.write(f"\n{datetime.now().strftime("%H:%M:%S")}: {error_message}")

    err.close()



def getStruct(s):
    if "while" in s:
        return "while"
    elif "for" in s:
        return "for"
    elif "if" in s:
        if "else" in s:
            return "else_if"
        else:
            return "if"
    elif "else" in s:
        return "else"
    elif "do" in s:
        return "do"
    else:
        return ""
    

    #moficca gli else if, li separa in if con all'interno degli else annidati
def modifica_else_if(code):
    n_elif = 0
    isElse_if = False
    new_code = []
    for c in code:

        if getStruct(c) == "else_if":
            n_elif += 1
            isElse_if = True
            tmp_else = c[0:c.index("if")]
            tmp_if = c[c.index("if"):]

            tmp_else += "{"

            new_code.append(tmp_else)
            new_code.append(tmp_if)

        elif isElse_if and "}" in c and getStruct(c) == "":
            for _ in range(n_elif+1):
                new_code.append("}")

        else:
            new_code.append(c)

    
    return new_code

def modifica_graffe_struct(code):

    do_trovato = False
    new_code = []
    for c in code:
        tmp = c
        if getStruct(tmp) == "" and "{" in tmp:
            tmp = tmp.replace("{", "")

        elif getStruct(tmp) in ["if", "for", "else", "else_if", "do"] and not "{" in tmp or getStruct(tmp) == "while" and not "}" in tmp:
            tmp = tmp + "{"

        elif getStruct(tmp) == "" and  "}" in tmp and len(tmp) > 1:
            tmp = tmp.replace("}", "")
            new_code.append(tmp)
            tmp = "}"

        new_code.append(tmp)


    return new_code

def clean(code, isCode = True):
    pattern_int = r'\bint\b\s+\w+'
    pattern_void = r'\bvoid\b\s+\w+'


    #spazi, virgola(tranne nel for), numeri iniziali
    new_code = []
    for c in code:
        tmp = c.strip()

        if isCode:
            #toglie eventuali commenti
            if "//" in tmp:
                tmp = tmp[0:tmp.index("//")]

            if not "for" in tmp:    #toglie le virgole, a meno che non sia un for, in quel caso servono
                tmp = tmp.replace(";", "")
            
            while tmp != "" and tmp[0].isnumeric(): #toglie i numeri all'inizio di ogni riga
                tmp = tmp[1:]    
            
            if re.search(pattern_int, tmp):     #individua "int" come assegnazione di una variabile e lo rimuove
                tmp = tmp.replace("int","")
            
            if re.search(pattern_void, tmp):     #individua "int" come assegnazione di una variabile e lo rimuove
                tmp = tmp.replace("void","")


        tmp = tmp.replace(" ", "")      #toglie ogni spazio

        new_code.append(tmp)
    
    return new_code
    

def controlla_errore_sintassi(line, anonim):

    if "else" in line:
        if "if" in line:
            print("ERRORE-> else e if non devono stare nella stessa riga" if not anonim else "!!else if")
            addError(global_data['error_log_path'], f"Attenzione! -> else e if non devono stare nella stessa riga")
        if not "{" in line:
            print("ERRORE --> { mancante in else" if not anonim else "!!{else")
            addError(global_data['error_log_path'], "Attenzione! -> { mancante in else")
        if not "}" in line:
            print ("ERRORE --> } mancante in else" if not anonim else "!!}else")
            addError(global_data['error_log_path'], "Attenzione! -> } mancante in else")
    if "if" in line:
        if not "{" in line:
            print("ERRORE --> { mancante in if" if not anonim else "!!{if")
            addError(global_data['error_log_path'], "Attenzione! -> { mancante in if")

    if "for" in line:
        if not "{" in line:
            print("ERRORE --> { mancante in for" if not anonim else "!!{for")
            addError(global_data['error_log_path'], "Attenzione! -> { mancante in for")

    if "while" in line:
        if not "{" in line and not "}" in line:
            print("ERRORE --> { mancante in while" if not anonim else "!!{while")
            addError(global_data['error_log_path'], "Attenzione! -> { mancante in while")

    if "&&" in line: 
            print("ERRORE --> && non è gestito, per && usa if annidati"if not anonim else "!!&&")
            addError(global_data['error_log_path'], "Attenzione! -> && non è gestito, per && usa if annidati")

    if "||" in line: 
            print("ERRORE -->  || non è gestito, per || dividi in 2 condizioni separate"if not anonim else "!!||")
            addError(global_data['error_log_path'], "Attenzione! -> || non è gestito, per || dividi in 2 condizioni separate")




def carica_impostazioni():
    start_id = 0 
    output_path = "out.txt" 
    override_input_request = False
    default_input_path = "input.txt" 
    always_on = True
    seconds_between_checks = 1
    error_log_path = "error.txt"
    load_template = True
    template_path = "template.txt"
    template_symbol_insertion = "<-->"

    instr = {
        'start_id': start_id,
        'output_path' : output_path,
        'override_input_request': override_input_request,
        'default_input_path' : default_input_path,
        'always_on' : always_on,
        'seconds_between_checks': seconds_between_checks,
        'error_log_path' : error_log_path,
        'load_template': load_template,
        'template_path': template_path,
        'template_symbol_insertion': template_symbol_insertion
    }

    inp = open("settings.sett")

    sett = [x.strip() for x in inp.readlines()]

    sett = clean(sett, False)

    for s in sett:
        if s.strip() != "":
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





    inp.close()
    return instr


def indent_code(code_lines):
    indented_lines = []
    indent_level = 1
   

    for line in code_lines:
        tmp = None 
        if "LDC_W" in line:
            tmp = f"{'\t'*indent_level}{line}"
            indent_level += 1
        if "INVOKEVIRTUAL" in line:
            indent_level -= 1
            tmp = f"{'\t'*indent_level}{line}"
        if "O" in line and ":" in line:
            tmp = f"{'\t'*indent_level}{line}"
            indent_level += 1
        if  "C" in line and ":" in line:
            indent_level -= 1
            tmp = f"{'\t'*indent_level}{line}"
            
        if tmp == None:
            tmp = f"{'\t'*indent_level}{line}"


        indented_lines.append(tmp)
            
    return indented_lines


def converti_all_lista(lista):

    new_lista = []

    for l in lista:

        if "\n" in l:
            tmp = l.split("\n")

            new_lista.extend(tmp)
        else:
            new_lista.append(l)

    return new_lista
        



#carica impostazioni globali
global_data = carica_impostazioni()



