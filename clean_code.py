import re 
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


        tmp = tmp.replace(" ", "")      #toglie ogni spazio

    
        new_code.append(tmp)
    
    print (new_code)
    return new_code
    
