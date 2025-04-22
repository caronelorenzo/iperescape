import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from telegram import ParseMode

# Config
TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_CHAT_ID = -68226596  # <-- usa il tuo chat_id qui

ENIGMA = "È una sequenza ma non qualsiasi. Se la componi, la linea non cade mai."
RISPOSTE_CORRETTE = [
    "il numero", "numero", "numero di telefono", "il numero di telefono", "numero telefonico"
]
NUMERO_TELEFONO = "+39 3471652752"

INDIZI = [
    "📽️ *Primo indizio*: Il suono del tuo respiro non è l’unico rumore qui dentro...",
    "🎞️ *Secondo indizio*: «Non cercare lettere… ma cifre. Quelle che danno voce ai vivi.»",
    "📡 *Terzo indizio*: «Ciò che collega due mondi…tra le tue dita. Ma solo se premi i tasti giusti.»"
]

indizi_usati = {}

def log(update, context, risposta_bot=None):
    user = update.effective_user.full_name
    user_msg = update.message.text

    log_text = f"🗣️ {user} ha scritto:\n{user_msg}"
    if risposta_bot:
        log_text += f"\n\n🤖 Bot ha risposto:\n{risposta_bot}"

    context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=log_text)

# Comandi
def start(update, context):
    chat_id = update.effective_chat.id
    indizi_usati[chat_id] = 0

    messaggio = (
        "🕯️ *Benvenuto nel Cinema Abbandonato...*\n\n"
        "Io sono *Zi Nick*, proiezionista di spiriti e custode dell'enigma che ti permetterà di procedere.\n"
        "Risolvi questo, e potresti trovare la via... o cadere nel buio:\n\n"
        f"🎭 *{ENIGMA}*\n\n"
        "Scrivi la tua risposta, o premi /indizio per chiedere aiuto a Zi Nick."
    )
    context.bot.send_message(chat_id=chat_id, text=messaggio, parse_mode=ParseMode.MARKDOWN)
    log(update, context, risposta_bot="Ha avviato il bot con /start")

def indizio(update, context):
    chat_id = update.effective_chat.id
    count = indizi_usati.get(chat_id, 0)

    if count < len(INDIZI):
        context.bot.send_message(chat_id=chat_id, text=INDIZI[count], parse_mode=ParseMode.MARKDOWN)
        indizi_usati[chat_id] += 1
        log(update, context, risposta_bot=f"Indizio {count + 1}: {messaggio}")
    else:
        context.bot.send_message(chat_id=chat_id, text="😶 Zi Nick tace. Non ci sono più indizi da dare.")
        log(update, context, risposta_bot="Nessun indizio disponibile")

def risposta(update, context):
    chat_id = update.effective_chat.id
    text = update.message.text.lower().strip()

    if text in RISPOSTE_CORRETTE:
        messaggio = (
            "🔓 *La pellicola si muove...*\n"
            "Hai trovato la risposta giusta.\n\n"
            f"📞 Chiama *{NUMERO_TELEFONO}*\n"
            "…forse qualcuno risponderà.\n\n"
            "_Zi Nick svanisce tra le tende rosse._"
        )
        context.bot.send_message(chat_id=chat_id, text=messaggio, parse_mode=ParseMode.MARKDOWN)
        log(update, context, risposta_bot=messaggio)
    else:
        context.bot.send_message(
            errore = "Le tue parole scivolano giù dal palcoscenico... Non è la risposta giusta."
            context.bot.send_message(chat_id=chat_id, text=errore, parse_mode=ParseMode.MARKDOWN)
            log(update, context, risposta_bot=errore)
        )

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