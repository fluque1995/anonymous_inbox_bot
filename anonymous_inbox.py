import logging
import telegram
import os

from telegram.ext import (
    Updater,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    Filters
)


ANON, ANON_MSG, IDENT_MSG = 1, 2, 3


def start(update, context):
    update.message.reply_text(
        text=("Bienvenid@! Yo seré tu canal de comunicación secreto con el "
              "profesor. Si tienes alguna sugerencia anónima que hacerle, "
              "puedes hacerlo a través de mi. Para mandar una nueva sugerencia "
              "utiliza el commando /suggest"))


def start_suggestion(update, context):
    reply_markup = telegram.ReplyKeyboardMarkup(
        [['Anónima'], ['Identificable']])

    update.message.reply_text(
        text=("Vamos a registrar tu sugerencia."
              " Quieres que sea anónima o identificable? "
              "PD: Si te arrepientes, usa el comando /cancel para cancelar"
              " el envío"),
        reply_markup=reply_markup)

    return ANON


def record_suggestion(update, context):
    suggestion_type = update.message.text
    if suggestion_type == 'Anónima':
        msg = ("Tu sugerencia es anónima, no mandaré tu nombre al profesor. "
               "Por favor, mándame tu mensaje para el profesor")
        next_step = ANON_MSG

    elif suggestion_type == 'Identificable':
        msg = ("De acuerdo, mandaré tu nombre al profesor junto con la sugerencia. "
               "Por favor, mándame tu mensaje para el profesor")
        next_step = IDENT_MSG

    update.message.reply_text(msg, reply_markup=telegram.ReplyKeyboardRemove())
    return next_step


def anonymous_suggestion(update, context):
    msg = update.message.text
    update.message.reply_text(
        ("Genial, mandaré este mensaje al profesor de forma anónima. "
         "Muchas gracias por tus comentarios! Recuerda que puedes volver "
         "a utilizar el comando /suggest para hacer nuevas sugerencias")
    )

    msg = "Sugerencia enviada anónimamente:\n" + msg
    context.bot.send_message(chat_id=os.environ['TEACHER_CHAT_ID'], text=msg)

    return ConversationHandler.END


def identifiable_suggestion(update, context):
    msg = update.message.text
    update.message.reply_text(
        ("Genial, mandaré este mensaje al profesor en tu nombre. "
         "Muchas gracias por tus comentarios! Recuerda que puedes volver "
         "a utilizar el comando /suggest para hacer nuevas sugerencias")
    )
    user = update.message.from_user
    attendant = f"{user.first_name} {user.last_name} (@{user.username})"
    msg = f"Sugerencia enviada por {attendant}:\n" + msg
    context.bot.send_message(chat_id=os.environ['TEACHER_CHAT_ID'], text=msg)

    return ConversationHandler.END


def cancel(update, context):
    update.message.reply_text(
        ("De acuerdo! No mandaré nada al profesor. Espero que vuelvas a "
         "utilizarme en otro momento!")
    )

    return ConversationHandler.END


def main():
    updater = Updater(token=os.environ['BOT_API_TOKEN'],
                      use_context=True)

    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('suggest', start_suggestion)],
        states={
            ANON: [MessageHandler(Filters.regex('^(Anónima|Identificable)$'),
                                  record_suggestion
                                  )],
            IDENT_MSG: [MessageHandler(Filters.text, identifiable_suggestion)],
            ANON_MSG: [MessageHandler(Filters.text, anonymous_suggestion)],
        },
        fallbacks=[CommandHandler('cancel', cancel)])

    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(CommandHandler('start', start))
    updater.start_polling()


if __name__ == '__main__':
    main()
