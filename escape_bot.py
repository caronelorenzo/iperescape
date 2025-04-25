import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram import ParseMode
from threading import Timer

# 🔐 Token da variabili d'ambiente (Railway)
TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_CHAT_ID = -1002510694303  # Sostituisci con il tuo chat_id del canale log

# 🔍 Enigma
ENIGMA = "\n*È una sequenza ma non qualsiasi, non ha volto nè voce ma può connetterti con chi ti occorre.*\n"
RISPOSTE_CORRETTE = [
    "il numero", "numero", "numero di telefono", "il numero di telefono", "numero telefonico", "un numero di telefono", "un numero", "un numero telefonico"
]

#VITE
#MAX_VITE = 3
#vite_utenti = {}  # dizionario per tracciare vite per ogni utente

fase_utenti = {}  # "inizio", "attesa_numero"
indizi_usati = {}

NUMERO_DECIFRATO = ["+393494521309", "3494521309"]

#INDIZI PROGRAMMATI
def invia_primo_indizio(context, chat_id, update):
    context.bot.send_message(chat_id=chat_id, text="🕯️ Primo indizio: ogni simbolo è una cifra, trova il punto di partenza. Non è lo zero e fa la fiamma.")
    log(update, context, risposta_bot="Ho inviato il primo indizio dopo la foto.")

def invia_secondo_indizio(context, chat_id, update):
    context.bot.send_message(chat_id=chat_id, text="📜 Secondo indizio: ogni cifra si ricava dall’associazione lettera-numero (es. A=1, B=2 ecc.)")
    log(update, context, risposta_bot="Ho inviato il secondo indizio dopo la foto.")


# 🧩 Indizi
INDIZI = [
    "È composto da cifre e connette i vivi fra loro.",
    "Le cifre da cui è composto sono precisamente dieci.",
    "Non ha volto nè voce ma può farti parlare con chiunque."
    #"Un nastro si riavvolge da solo: «Il pubblico componeva questa sequenza per parlare con la cabina…»",
    #"Un vecchio telefono squilla nel vuoto: «Chi vuole uscire, deve comporre. Ma non qualsiasi numero… quello giusto.»",
    #"Un altoparlante gracchia: «Ciò che collega due mondi… sta tra le tue dita. Ma solo se premi i tasti giusti.»",
    #"La luce tremola sulla pellicola rotta: «La risposta non è una parola. È qualcosa che… si può digitare.»"
]

indizi_usati = {}

# 📤 Logging su canale Telegram
def log(update, context, risposta_bot=None):
    try:
        user = update.effective_user.full_name
        user_msg = update.message.text
        log_text = f"{user} ha scritto:\n{user_msg}"
        if risposta_bot:
            log_text += f"\n\nBot ha risposto:\n{risposta_bot}"
        context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=log_text)
    except Exception:
        pass  # evita crash se il log fallisce

# 🎬 /start
def start(update, context):
    chat_id = update.effective_chat.id
    indizi_usati[chat_id] = 0

    messaggio = (
        "Se la luce vuoi riportare risolvi questo enigma utilizzando SOLO il cellulare:\n"
        f"{ENIGMA}"
        "Cos'è?\n\n"
        "Risolvilo e potresti trovare la via d’uscita... o cadere nel buio.\n\n"
        "*Scrivi la tua risposta, o premi /indizio per ricevere gli aiuti di Zi Nick. (ATTENZIONE: non sono infiniti.)*"
    )
    context.bot.send_message(chat_id=chat_id, text=messaggio, parse_mode=ParseMode.MARKDOWN)
    log(update, context, risposta_bot="Ha avviato il bot con /start")

def reset(update, context):
    chat_id = update.effective_chat.id

    # Reset variabili utente
    fase_utenti.pop(chat_id, None)
    if 'indizi_usati' in globals():
        indizi_usati.pop(chat_id, None)

    context.bot.send_message(
        chat_id=chat_id,
        text="🔄 *Bot resettato completamente.*\nRicomincio da capo...",
        parse_mode=ParseMode.MARKDOWN
    )

    log(update, context, risposta_bot="Ha richiesto il reset completo del bot.")
    
    # Riavvia automaticamente la sequenza con /start
    start(update, context)

# 🔦 /indizio
def indizio(update, context):
    chat_id = update.effective_chat.id
    count = indizi_usati.get(chat_id, 0)

    if count < len(INDIZI):
        messaggio = INDIZI[count]
        context.bot.send_message(chat_id=chat_id, text=messaggio)
        indizi_usati[chat_id] = count + 1
        log(update, context, risposta_bot=f"Indizio {count + 1}: {messaggio}")
    else:
        context.bot.send_message(chat_id=chat_id, text="Zi Nick tace. Non ci sono più indizi da dare.")
        log(update, context, risposta_bot="Ha terminato gli indizi")

# ✅ Verifica risposte
def risposta(update, context):
    chat_id = update.effective_chat.id
    text = update.message.text.lower().strip()

    # Inizializza vite se non presenti
    #if chat_id not in vite_utenti:
    #    vite_utenti[chat_id] = MAX_VITE

    # Se ha finito le vite
    #if vite_utenti[chat_id] <= 0:
    #    messaggio = (
    #        "🎞️ Il proiettore si ferma.\n"
    #        "Non puoi più tentare...\n"
    #        "Zi Nick ti osserva nell’ombra. È finita per te."
    #    )
    #    context.bot.send_message(chat_id=chat_id, text=messaggio)
    #    log(update, context, risposta_bot=messaggio)
    #    return
    
    if chat_id not in fase_utenti:
        fase_utenti[chat_id] = "inizio"

    fase = fase_utenti[chat_id]

    if fase == "inizio":
        if text in RISPOSTE_CORRETTE:
            fase_utenti[chat_id] = "attesa_numero"
            context.bot.send_message(chat_id=chat_id, text="Quale sarà quindi questo numero?")

            Timer(15.0, lambda: context.bot.send_photo(chat_id=chat_id, photo=open("immagine_ricompensa.png", "rb"))).start()
            log(update, context, risposta_bot="Ha risolto l'enigma. Inviata immagine e programmati indizi.")
            #with open("immagine_ricompensa.png", "rb") as img:
            #    context.bot.send_photo(chat_id=chat_id, photo=img)
            Timer(120.0, invia_primo_indizio, args=(context, chat_id, update)).start()
            Timer(300.0, invia_secondo_indizio, args=(context, chat_id, update)).start()

        else:
            context.bot.send_message(chat_id=chat_id, text="❌ Non è la risposta giusta. Riprova.")
            log(update, context, risposta_bot="Risposta errata.")

    elif fase == "attesa_numero": 
        log(update, context, risposta_bot=f"Attendo numero")
        numero_utente = text.replace(" ", "").replace("-", "")
        if numero_utente in [n.replace(" ", "").replace("-", "") for n in NUMERO_DECIFRATO]:
            fase_utenti[chat_id] = "completato"
            numero = numero_utente
            log(update, context, risposta_bot=f"Numero corretto ricevuto: {numero}")
            #keyboard = [[InlineKeyboardButton("📞 Chiama ora", url=f"https://t.me/share/url?url={numero}&text=Chiama questo numero:")]]
            #reply_markup = InlineKeyboardMarkup(keyboard)
            #context.bot.send_message(chat_id=chat_id, text="🔓 Hai decifrato il codice. È ora di comporlo.", reply_markup=reply_markup)

            numero_mostrato = "+393494521309"
            context.bot.send_message(chat_id=chat_id, text=f"📞 Clicca sul numero e poi su Chiamata Vocale Telegram:\n*{numero_mostrato}*", parse_mode=ParseMode.MARKDOWN)
            log(update, context, risposta_bot="Numero corretto, mostrato bottone per chiamata.")
        else:
            context.bot.send_message(chat_id=chat_id, text="❌ Questo numero non ha vita. Riprova.", parse_mode=ParseMode.MARKDOWN)
            log(update, context, risposta_bot="Numero decifrato errato.")

    elif fase == "completato":
        context.bot.send_message(chat_id=chat_id, text="Hai già completato questa parte. La chiamata ti aspetta.")

# ▶️ Avvio bot
def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("indizio", indizio))
    dispatcher.add_handler(CommandHandler("reset", reset))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, risposta))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
