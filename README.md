# Come utilizzare
1. Modificare il file "settings.sett" a piacimento: [file_impostazioni](#file-impostazioni)
2. **Spostarsi nella directory del programma**
3. Avviare il programma "IJVM_comp.py" (il nome di questo file può essere modificato senza problemi"
4. seguire le istruzioni

## Modalità anonima
Il programma funzionerà normalmente ma non mostrerà nessuna scritta, solamente:

- ">": ovvero inserisci input_path
- "<<": risultato scritto nel path di output scelto
-  "!": il file di input passato non esiste

## File impostazioni
- [start_id] --> numero da cui far partire le etichette del programma (default: 0)
- [output_path] --> persorso in cui salvare il risultato (default: "out.txt")
- [override_input_request] --> se True non chiederà l'input del percorso file, lo prenderà dalla riga successiva (default: False)
- [default_input_path]--> percorso file da utilizzare in caso di  override_input_request = True (default: "input.txt")



