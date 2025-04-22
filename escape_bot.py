import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ParseMode
from threading import Timer

# 🔐 Token da variabili d'ambiente (Railway)
TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_CHAT_ID = -1002510694303  # Sostituisci con il tuo chat_id del canale log

# 🔍 Enigma
ENIGMA = "È una sequenza ma non qualsiasi. Se la componi, la linea non cade mai."
RISPOSTE_CORRETTE = [
    "il numero", "numero", "numero di telefono", "il numero di telefono", "numero telefonico"
]
NUMERO_TELEFONO = "+39 3471652752"

#VITE
MAX_VITE = 3
vite_utenti = {}  # dizionario per tracciare vite per ogni utente

#INDIZI PROGRAMMATI
def invia_primo_indizio(context, chat_id):
    context.bot.send_message(chat_id=chat_id, text="🕯️ Primo indizio: ogni simbolo è una cifra, trova il punto di partenza. Non è lo zero e fa la fiamma.")

def invia_secondo_indizio(context, chat_id):
    context.bot.send_message(chat_id=chat_id, text="📜 Secondo indizio: ogni cifra si ricava dall’associazione lettera-numero (es. A=1, B=2 ecc.)")


# 🧩 Indizi
INDIZI = [
    "Zi Nick bisbiglia: «Non cercare lettere… ma cifre. Quelle che danno voce ai vivi.»",
    "Un nastro si riavvolge da solo: «Il pubblico componeva questa sequenza per parlare con la cabina…»",
    #"Un vecchio telefono squilla nel vuoto: «Chi vuole uscire, deve comporre. Ma non qualsiasi numero… quello giusto.»",
    #"Un altoparlante gracchia: «Ciò che collega due mondi… sta tra le tue dita. Ma solo se premi i tasti giusti.»",
    "La luce tremola sulla pellicola rotta: «La risposta non è una parola. È qualcosa che… si può digitare.»"
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
        "Benvenuto nel Cinema Abbandonato...\n\n"
        "Io sono Zi Nick, proiezionista di spiriti e custode dell’ultimo enigma.\n"
        "Risolvi questo, e potresti trovare la via d’uscita... o cadere nel buio:\n\n"
        f"{ENIGMA}\n\n"
        "Scrivi la tua risposta, o chiedi un /indizio."
    )
    context.bot.send_message(chat_id=chat_id, text=messaggio)
    log(update, context, risposta_bot="Ha avviato il bot con /start")

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
        log(update, context, risposta_bot="Nessun indizio disponibile")

# ✅ Verifica risposte
def risposta(update, context):
    chat_id = update.effective_chat.id
    text = update.message.text.lower().strip()

    # Inizializza vite se non presenti
    if chat_id not in vite_utenti:
        vite_utenti[chat_id] = MAX_VITE

    # Se ha finito le vite
    if vite_utenti[chat_id] <= 0:
        messaggio = (
            "🎞️ Il proiettore si ferma.\n"
            "Non puoi più tentare...\n"
            "Zi Nick ti osserva nell’ombra. È finita per te."
        )
        context.bot.send_message(chat_id=chat_id, text=messaggio)
        log(update, context, risposta_bot=messaggio)
        return

    # Risposta corretta
    if text in RISPOSTE_CORRETTE:
        messaggio = (
            "🔓 La pellicola si muove...\n"
            "Hai trovato la risposta giusta.\n\n"
            "Zi Nick svanisce tra le tende rosse."
        )
        context.bot.send_message(chat_id=chat_id, text=messaggio)
        
        with open("immagine_ricompensa.png", "rb") as img:
            context.bot.send_photo(chat_id=chat_id, photo=img)
        log(update, context, risposta_bot=messaggio)

        Timer(60.0, invia_primo_indizio, args=(context, chat_id)).start()
        Timer(120.0, invia_secondo_indizio, args=(context, chat_id)).start()

    else:
        vite_utenti[chat_id] -= 1
        tentativi_rimasti = vite_utenti[chat_id]
        if tentativi_rimasti > 0:
            errore = (
                f"❌ Non è la risposta giusta.\n"
                f"Hai ancora {tentativi_rimasti} tentativo{'i' if tentativi_rimasti > 1 else ''}..."
            )
        else:
            errore = (
                "☠️ L’ultima speranza è svanita.\n"
                "La risposta non verrà più accettata.\n"
                "Zi Nick ti lascia al buio..."
            )
        context.bot.send_message(chat_id=chat_id, text=errore)
        log(update, context, risposta_bot=errore)

# ▶️ Avvio bot
def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("indizio", indizio))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, risposta))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
