from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Dati configurabili
TOKEN = '7940579077:AAHbaL1ZwON8gQGtPSfFt-Go2ZON5tIa3LA'
ENIGMA = "È una sequenza ma non qualsiasi. Se la componi la linea non cade mai."
RISPOSTA_CORRETTA = ["il numero", "numero", "numero di telefono", "il numero di telefono", "numero telefonico"]
NUMERO_TELEFONO = "+39 3471652752"

# Indizi che verranno dati a richiesta
INDIZI = [
    "Indizio 1",
    "Indizio 2",
    "Indizio 3"
]

indizi_usati = {}

# Comandi del bot
def start(update, context):
    user = update.effective_user
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Ciao {user.first_name}! Ecco il tuo enigma:\n\n{ENIGMA}\n\nPuoi premere qui per chiedere un /indizio o provare a rispondere direttamente.")

def indizio(update, context):
    chat_id = update.effective_chat.id
    if chat_id not in indizi_usati:
        indizi_usati[chat_id] = 0

    if indizi_usati[chat_id] < len(INDIZI):
        context.bot.send_message(chat_id=chat_id, text=f"Indizio: {INDIZI[indizi_usati[chat_id]]}")
        indizi_usati[chat_id] += 1
    else:
        context.bot.send_message(chat_id=chat_id, text="Hai già ricevuto tutti gli indizi!")

def risposta(update, context):
    chat_id = update.effective_chat.id
    text = update.message.text.lower().strip()

    if text == RISPOSTA_CORRETTA:
        context.bot.send_message(chat_id=chat_id, text=f"Corretto! Giusto, quindi quale?")
    else:
        context.bot.send_message(chat_id=chat_id, text="Mmmm no, non è la risposta giusta. Riprova o chiedi un /indizio")

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Handlers
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('indizio', indizio))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, risposta))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()