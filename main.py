from IJVM_comp import clear_terminal, clean, carica_impostazioni, elenca_variabili, compila_corpo

#carica impostazioni globali
start_id, output_path, override_input_request, default_input_path = carica_impostazioni()


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
            tmp_code = []
            tmp = l.split("(")
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
    

def compila_funzione(func_name, func_param, func_lines, anonim):

    code = []
    elenco_var = elenca_variabili(func_lines)
    for x in func_param:
        elenco_var.remove(x)

    #apertura metodo
    if func_name != "main":
        code.append(f".method {func_name}({','.join(func_param)})")
    else:
        code.append(".main")

    #inserimento variabili non presenti tra i parametri
    code.append(".var")
    code.extend(elenco_var)
    code.append(".end-var")

    #inserimento corpo della funzione

    code.extend(compila_corpo(func_lines,start_id, anonim))


    #chiusura metodo
    if func_name != "main":
        code.append(".end-method")
    else:
        code.append("HALT")
        code.append(".end-main")

    return code

    

        
    



def main():

    code = []
    
    #richiesta modalità anonima
    anonim = input("Mod anonima? [1 = si altro = no]")


    if anonim:  #cancella la domandas
        clear_terminal()


    #richiedi/recupera path input
    if override_input_request == False:
        input_path = input("Inserisci il percorso del file contenente lo pseudocidice: "if not anonim else ">")
    else:
        input_path = str(default_input_path)

    #controlla esistenza file
    try:
        open(input_path, "r")
    except FileNotFoundError:
        print(f"Il file ({input_path}) non esiste" if not anonim else "!")  
        return



    #prendi input dati e pulisci
    inp = open(input_path, "r")

    lines = [x.strip() for x in inp.readlines()]

    lines = clean(lines)

    inp.close()

    


    #dividi codice per metodi
    func_parameters, func_lines = separa_metodi(lines)


    #identifica main e mettilo per primo
    func_keys = list(func_lines.keys())

    if "main" in func_keys:
        code.extend(compila_funzione("main", [], func_lines["main"], anonim))
        func_keys.remove("main")
    #per ogni metodo compila corpo
    
    for k in func_keys:
        code.extend(compila_funzione(k, func_parameters[k], func_lines[k],anonim))


    #apri file output
    out = open(output_path, "w+")
    for c in code:
        if not anonim:
            print(c)
        out.write(f"{c}\n")
    out.close()

    print(f"\n\nDUMP FATTO IN {output_path}" if not anonim else "<<")

if __name__ == "__main__":
    main()