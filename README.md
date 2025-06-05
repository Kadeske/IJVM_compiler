
# ATTENZIONE
Non ho nessuna responsabilità sull'utilizzo del programma, decidete  voi cosa farci, a me è sembrato 'divertente'.
Infatti è tutto vibe code, molto disordinato e poco leggibile. Non è un progetto serio.

# Come utilizzare

1. Modificare il file "settings.sett" a piacimento: [file_impostazioni](#file-impostazioni)

2.  **Spostarsi nella directory del programma**

3. Avviare il programma "main.py" (il nome di questo file può essere modificato senza problemi"

4. seguire le istruzioni

  
  

## Input file

Nel file di input vanno inserite le funzioni per intero, comprese i firme, anche il main è accettato.
In pratica basta fare copia e incolla dell'intero pseudocidice, raramente va sistemato qualcosa.

Caratteri come ';' e spazi vuoti sono ignorati.
Contano solamente le andate a capo.
I numeri ad inizio riga vengono **eliminati**, così da poter copiare da un pdf.

NON devono essere presenti tipi di nessun genere: "int i" darà problemi, cancella "int"

### Costrutti
	Le posizione e la presenza delle parentesi graffe è ESSENZIALE.
	Quando un costrutto viene aperto le parentesi graffe sono necessarie, in particolare vanno aperte nella stessa riga dell'inizio del costrutto:
	es:
		if(a < b) {  <-- va bene
		
		if (a < b)
		{		<--- questo NO

1. Firma delle funzioni: nome_fun(par1, par2, ...) {
2. for(init ; condizione ; passo){  
3. while(condizione){
4. }else{			<--- attenzione, sia la chiusa che l'aperta parentesi serve


  

esempio di input valido:<br>

fun1(a, b){
2 i=b+2;
3 while(a+3<i){
4 while(a*2<b){
5 a = a%b;
6 }
7 i++;
8 }
9 return a*i;
10 }
11
12 fun2(x, y){
13 for(i=6;i>1;i++){
14 x = y*x/4;
15 i-=2;
16 }
17
18 if (x>y){
19 y = y*3;
20 }else{
22 y = y*2;
23 }
24 return x%y;
25 }
26
27 main() {
28 input a;
29 input b;
30 input c;
31
32 print(fun1(a,b) % fun2(a,b+c));
33 }


  

## Modalità anonima

Il programma funzionerà normalmente ma non mostrerà nessuna scritta, solamente:

  

- ">": ovvero inserisci input_path

- "<<": risultato scritto nel path di output scelto

- "!": il file di input passato non esiste
- "!!{-costrutto-" mancata aperta parentesi nel costrutto specificato 
- "!!}else" mancata chiusa parentesi nel costrutto else 



  

## File impostazioni

- [start_id] --> numero da cui far partire le etichette del programma (default: 0)

- [output_path] --> persorso in cui salvare il risultato (default: "out.txt")

- [override_input_request] --> se True non chiederà l'input del percorso file, lo prenderà dalla riga successiva (default: False)

- [default_input_path]--> percorso file da utilizzare in caso di override_input_request = True (default: "input.txt")
