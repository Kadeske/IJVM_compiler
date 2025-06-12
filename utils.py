import re 
import hashlib
from datetime import *



def get_file_hash(filename):
    with open(filename, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()
    
def addError(error_log_path, error_message):

    err = open(error_log_path, "a+")

    err.write(f"\n{datetime.now().strftime("%H:%M:%S")}: {error_message}")

    err.close()


def clean(code, isCode = True):
    pattern = r'\bint\b\s+\w+'


    #spazi, virgola(tranne nel for), numeri iniziali
    new_code = []
    for c in code:
        tmp = c.strip()

        if isCode:
            if not "for" in tmp:    #toglie le virgole, a meno che non sia un for, in quel caso servono
                tmp = tmp.strip(";")
            
            while tmp != "" and tmp[0].isnumeric(): #toglie i numeri all'inizio di ogni riga
                tmp = tmp[1:]    
            
            if re.search(pattern, tmp):     #individua "int" come assegnazione di una variabile e lo rimuove
                tmp = tmp.replace("int","")

            #toglie eventuali commenti
            if "//" in tmp:
                tmp = tmp[0:tmp.index("//")]


        tmp = tmp.replace(" ", "")      #toglie ogni spazio

    
        new_code.append(tmp)
    
    return new_code
    



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




#carica impostazioni globali
global_data = carica_impostazioni()

