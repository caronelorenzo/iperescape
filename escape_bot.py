import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from telegram import ParseMode

# Config
TOKEN = os.environ.get("BOT_TOKEN")

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

# Comandi
def start(update, context):
    chat_id = update.effective_chat.id
    indizi_usati[chat_id] = 0

    messaggio = (
        "🕯️ *Benvenuto nel Cinema Abbandonato...*\n\n"
        "Io sono *Zi Nick*, proiezionista di spiriti e custode dell'enigma che ti permetterà di procedere.\n"
        "Risolvi questo, e potresti trovare la via... o cadere nel buio:\n\n"
        f"🎭 *{ENIGMA}*\n\n"
        "Scrivi la tua risposta, o chiedi un /indizio."
    )
    context.bot.send_message(chat_id=chat_id, text=messaggio, parse_mode=ParseMode.MARKDOWN)

def indizio(update, context):
    chat_id = update.effective_chat.id
    count = indizi_usati.get(chat_id, 0)

    if count < len(INDIZI):
        context.bot.send_message(chat_id=chat_id, text=INDIZI[count], parse_mode=ParseMode.MARKDOWN)
        indizi_usati[chat_id] += 1
    else:
        context.bot.send_message(chat_id=chat_id, text="😶 Zi Nick tace. Non ci sono più indizi da dare.")

def risposta(update, context):
    chat_id = update.effective_chat.id
    text = update.message.text.lower().strip()

    if text in RISPOSTE_CORRETTE:
        context.bot.send_message(
            chat_id=chat_id,
            text=(
                "🔓 *La pellicola si muove...*\n"
                "Hai trovato la risposta giusta.\n\n"
                f"📞 Chiama *{NUMERO_TELEFONO}*\n"
                "…forse qualcuno risponderà.\n\n"
                "_Zi Nick svanisce tra le tende rosse._"
            ),
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        context.bot.send_message(
            chat_id=chat_id,
            text="❌ Le tue parole scivolano giù dal palcoscenico... e si perdono nel buio.",
            parse_mode=ParseMode.MARKDOWN
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