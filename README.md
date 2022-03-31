# BarilePatrunoRipoli

1. [Introduzione](#introduzione)
2. [Come Giocare](#come-giocare)
3. [Descrizione del progetto](#descrizione-del-progetto)
4. [Salvataggio di Dati](#salvataggio-di-dati)
5. [Concetti Matematici](#concetti-matematici)
6. [Spiegazione Codice](#spiegazione-codice)
7. [Requisiti](#requisiti)
8. [Problemi Noti](#problemi-noti)
9. [Feature da aggiungere](#feature-da-aggiungere)
10. [Gestione dei ruoli](#gestione-dei-ruoli)

## Introduzione

Questo gioco è stato realizzato durante le ore di compresenza tra Coding e Matematica nell'istituto GB Vico con la supervisione del professore Diomede Mazzone ed ha come obbiettivo quello di creare un gioco con delle classi e delle coniche.

## Come Giocare

Per muoversi è possibile utilizzare i tasti <kbd>WASD</kbd> o le freccette direzionali. Per lanciare gli shuriken è possibile premere i tasti <kbd>z</kbd> e <kbd>k</kbd>. Per lanciare i kunai invece è possibile utilizzare i tasti <kbd>x</kbd> e <kbd>l</kbd>. Per uscire dal gioco in qualsiasi momento basta premere il tasto <kbd>q</kbd>. Per entrare nel menù di pausa basta premere il tasto <kbd>p</kbd> durante il gioco.

## Descrizione del progetto

Avviato il gioco vi è un menù iniziale con uno sfondo il miglior risultato mai avuto nel gioco ed un bottone con scritto: "gioca", premendo il bottone si può iniziare una nuova partita. Una volta entrati nella partita, il gioco consisterà nel difendere la pagoda e sconfiggere i nemici che arriveranno dal basso l obbiettivo è quello di non farli uscire dal lato opposto dello schermo. Il personaggio scelto per il gioco è un Ninja che avrà a disposizione degli shuriken e dei Kunai, gli shuriken verranno lanciati verso il basso, mentre i kunai verranno lanciati lateralmente, si avranno 3 vite e la partita finirà quando o si finiscono le vite oppure quando troppi nemici stanno attaccando la pagoda, a fine partita verrà calcolato il punteggio totale

## Salvataggio di dati

Il gioco avrà bisogno di salvare dei dati localmente, essi saranno:
- gli oggetti acquistati nello shop
- le monete di gioco
- il miglior punteggio
- il nickname del giocatore

Quando verrà realizzato un nuovo miglior punteggio verrà inoltre salvato su un database online per potere creare una classifica globale del gioco. 

## Concetti Matematici

Nel nostro progetto la retta è usata per il movimento dei proiettili mentre la parabola è utilizzata per il movimento di un nemico. La retta è il secondo ente geometrico fondamentale della Geometria Euclidea ed è quindi un'entità per cui non esiste una vera e propria definizione; tuttavia possiamo pensare a una linea retta come a un insieme formato da infiniti punti che corrono lungo la stessa direzione, senza un principio né una fine, mentre la parabola è il luogo geometrico dei punti equidistanti da una retta (direttrice) e da un punto (fuoco). La retta passante per il fuoco e perpendicolare alla direttrice si chiama asse della parabola. L'asse della parabola è un asse di simmetria e interseca la parabola nel vertice.

## Spiegazione Codice

Per come è stato organizzato il gioco esso è composto da una classe base, chiamata "Game", e da tante sottoclassi che corrispondono ognuna ad un sottoelemento del gioco. Nella classe base è presente una funzione "main" in cui viene gestito il loop del gioco, ogni volta il gioco controlla la variabile di classe "phase" per capire in quale fase di gioco esso si trovi e viene utilizzata la funzione corrispondente. Infatti sono presenti 3 diagrammi di flusso:
- [uno relativo alla funzione main](Main_Flowchart.png)
- [uno relativo alla parte di gioco](Game_Flowchart.png)
- [uno relativo ai menù dato che condividono tutti lo stesso scheletro](Menu_Flowchart.png)

## Requisiti

- Python 3.10
- Pygame

## Problemi noti

- Su Linux lo scaling della risoluzione non funziona correttamente

## Feature da aggiungere

- Logo per i nemici uccisi

- Migliorare schermata di Game Over

- Schermata di introduzione

- Power Up

- Salvare il punteggio su file

- Shop per comprare armi
## Gestione dei ruoli

| Membro         | Cosa ha fatto                               |
| -------------- | --------------------------------------------|
| Patruno Luca   | *Codice* e supervisione del progetto                                      |
| *Ripoli Luca*  | *Diagramma di flusso e sprite di gioco*     |
| *Barile Luigi* | *README.md e CHANGELOG.md*                  |
