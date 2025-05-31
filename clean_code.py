def clean(code):

    banned = [ "float", "double"]

    #spazi, virgola(tranne nel for), numeri iniziali
    new_code = []
    for c in code:
        tmp = c.strip()

        if not "for" in tmp:
            tmp = tmp.strip(";")
        
        while tmp != "" and tmp[0].isnumeric():
            tmp = tmp[1:]    
        
        tmp = tmp.replace(" ", "")

        for b in banned:
            tmp = tmp.replace(b, "")
    
        new_code.append(tmp)
    

    return new_code
    
