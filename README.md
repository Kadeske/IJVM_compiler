
  

# ATTENZIONE

Non ho nessuna responsabilità sull'utilizzo del programma, decidete voi cosa farci, a me è sembrato 'divertente'.
**Pubblico solamente dal 9 luglio 2025.**

Infatti è tutto storto, molto disordinato e poco leggibile (probabilmente una IA lo fa meglio). **Non** è un progetto serio.
Buona fortuna se vuoi guardare o modificare il codice, non ricordo nemmeno io come funziona, troppo spaghettoso.

  

# Come utilizzare

  

1. Modificare il file "settings.sett" a piacimento: [file_impostazioni](#file-impostazioni)


3.  **Spostarsi nella directory del programma**

  

4. Avviare il programma "main.py" (il nome di questo file può essere modificato senza problemi"

  

5. seguire le istruzioni

  
Ho aggiunto anche un template con le funzioni mul, div, mod, print, ma in versione iterativa, ovvero daranno meno problemi durante l'esecuzione, dato che utilizzano meno spazio in memoria, e il mic ne ha molto poco.
  
  I file .py devono stare tutti assieme, anche il file di settings, è quindi necessario avviare il programma dalla directory in cui si trova. Mentre i file di errore, input e output, posso stare ovunque, basta inserire il loro percorso nel file di impostazioni.

## Input file

  

Nel file di input vanno inserite le funzioni per intero, comprese i firme, anche il main è accettato.

In pratica basta fare copia e incolla dell'intero pseudocidice, raramente va sistemato qualcosa.

  

Caratteri come ';' e spazi vuoti sono ignorati.

Contano solamente le andate a capo.

I numeri ad inizio riga vengono **eliminati**, così da poter copiare da un pdf.

  

NON devono essere presenti tipi di nessun genere: "int i" darà problemi, cancella "int"

  

Le variabili DEVONO essere **monocarattere**, niente numeri o caratteri speciali.

  

## Costrutti

Attenzioe alla posizione e alla presenza delle parentesi graffe: la presenza è **essenziale**, e l'ordine è piuttosto rigido nel do-while, dove la graffa di chiusura ('}') deve stare nella stessa riga del while.



#### if

if(condizione){

//corpo

}

  

#### if else

if(condizione){

//corpo vero

}else{

//corpo caso falso

}


#### if else if ...
  

    
    
    if(cond){
    
	    //corpo con1
    
    }else if(cond 2){
    
	    //corpo cond2
    
     }else{
     
	    //corpo else
    
    }

#### for

Esattamente come in c ma i tipi non sono necessari, meglio evitarli (es. rimuovi int se possibile):


    for(init ; cond ; passo){
    
	    //corpo
    
    }

#### while

Ancora, esattamente come in c

  

    while(cond){
    
	    //corpo
    
    }

#### do

Ancora ancora uguale a c:

  

    do{
    
	    //corpo
    
    }while (condizione)	//Attenzione, la graffa va nella stessa riga del while, come qua



#### esempio di input valido:<br>

	Si possono tranquillamente lasciare i numeri a inizio riga, magari state compiando da un pdf, dover togliere ogni numero farebbe perdere tempo durante lo studio.  

    fun1(x,y){
    2 while(x+3<y){
    3 for(i=0;i>6;i++){
    4 x = x+x;
    5 y = y+i;
    6 }
    7 }
    8 return x%y;
    9 }
    10
    11 fun2(x,y){
    12 while (x+y<2+y){
    13 if(x > 8){
    14 x = y+x;
    15 }
    16 else{
    17 x = x-y;
    18 }
    19 }
    20 return x%y;
    21 }
    22
    23 main() {
    24 input a;
    25 input b;
    26 input c;
    27
    28 print(fun1(a*2,b) + fun2(a,b*c));
    29 }

  
  
  

  

## Modalità anonima

  

Il programma funzionerà normalmente ma non mostrerà nessuna scritta, solamente:

  

- ">": ovvero inserisci input_path

 
- "<<": risultato scritto nel path di output scelto
- "!": il file di input passato non esiste

- "!!{-costrutto-" mancata aperta parentesi nel costrutto specificato

- "!!}else" mancata chiusa parentesi nel costrutto else

Possibili errori. Attenzione: è meglio segure gli errori che vengono scritti nell'apposito file, con percorso [error_log_path].

 -   **"!!{-costrutto-"**: mancata parentesi aperta `{` nel costrutto specificato (if, else, for, while)

-   **"!!else if"**: else e if non devono stare nella stessa riga
    
-   **"!!&&"**: `&&` non è gestito (usa if annidati)
    
-   **"!!||"**: `||` non è gestito (dividi in due condizioni separate)
    
-   **Errore nel for**: manca una condizione o è stato usato un separatore diverso da `;`
  
  

  

## File impostazioni

Attenzione: il file di settings deve stare obbligatoriamente nella stessa directory da cui chiamate il programma, come gli altri file python.

  
-   **[start_id]** --> numero da cui far partire le etichette del programma (**default: 0**)
    
-   **[output_path]** --> percorso in cui salvare il risultato (**default: "out.txt"**)
    
-   **[error_log_path]** --> percorso al file dove scriverà gli eventuali errori
    
-   **[override_input_request]** --> se **True**, non chiederà l'input del percorso file, lo prenderà dalla riga successiva (**default: False**)
    
-   **[default_input_path]** --> percorso file da utilizzare in caso di **override_input_request = True** (**default: "input.txt"**)
    
-   **[always_on]** --> se **True**, il programma non si fermerà mai e continuerà ad aggiornare il codice quando il file di input verrà modificato (**default: True**)
    
-   **[seconds_between_checks]** --> numero di secondi tra il controllo della modifica del file di input (**consiglio di lasciare a 1**)
    
-   **[load_template]** --> se **True**, caricherà in automatico il template al percorso specificato, sostituendo un simbolo scelto con il codice compilato
    
-   **[template_path]** --> percorso contenente il template
    
-   **[template_symbol_insertion]** --> simbolo da sostituire con il codice generato

## Possibili problemi per cui "non va" o genera un codice errato

  

1. **Presenza di qualche tipizzazione**: sono tutti interi, scrivere int non è necessario, anzi potrebbe dare problemi anche se è gestito

2. **posizione errata parentesi graffe**: attenzione alla '}' nel do-while, ed è preferibile scrivere else ed else if con: '}/else o else if/{'
	


esempi di porzioni di codice errate o con possibili errori:


Attenzione a print, potrebbe essere scritto come 'Print' o 'printf'. Anche se è gestito, meglio evitare.
Attenzione a input, potrebbe essere scritto come 'Input' o 'INPUT'. Anche se è gestito, meglio evitare.



Float x 	//NON andrà sicurmente, è meglio evitare ogni tipizzazione, anche se int è ammesso  

if (a = b){ // è == non =   è identico al c
}

  


costrutto{
x++} // la parentesi graffa è preferibile a capo, ma non dovrebbe dare problemi in ogni caso

do{

//corpo

}
while(i == p) //compila ma da problemi, la graffa va chiusa subito prima di 'while'
