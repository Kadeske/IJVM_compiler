from IJVM_comp import *
import time 



def main():

    #cancella vecchio log / lo crea se non esiste
    open(global_data['error_log_path'], "w+")

    #richiesta modalità anonima
    if global_data['anonim_always_on'] != True:
        anonim = input("Mod anonima? [1 = si altro = no]")
    else:
        anonim = True

    if anonim:  #cancella la domandas
        clear_terminal()


    #richiedi/recupera path input
    if global_data['override_input_request'] == False:
        input_path = input("Inserisci il percorso del file contenente lo pseudocidice: "if not anonim else ">")
    else:
        input_path = str(global_data['default_input_path'])

    #controlla esistenza file
    try:
        open(input_path, "r")
    except FileNotFoundError:
        print(f"Il file ({input_path}) non esiste" if not anonim else "!")  
        return



    if global_data['always_on']:
        #controlla nel tempo se il file nel path specificato viene modificato
        old_hash = get_file_hash(input_path)
        while True:
            #se input cambiato, compila
            if old_hash != get_file_hash(input_path):
                try:
                    compila_input(input_path, anonim)
                except:
                    addError(global_data["error_log_path"], "Errore inaspettato e sconosciuto, arriva da 'compila_input()")
                old_hash = get_file_hash(input_path)

           
            time.sleep(global_data['seconds_between_checks'])
    else:
        compila_input(input_path, anonim)



    
if __name__ == "__main__":
    main()