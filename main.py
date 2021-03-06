import os
import http

from flask import Flask, request
from werkzeug.wrappers import Response

import telegram
from telegram import Bot, Update
from telegram.ext import Dispatcher, Filters, MessageHandler, CallbackContext, CommandHandler, ConversationHandler

app = Flask(__name__)
ANON, ANON_MSG, IDENT_MSG = 1, 2, 3


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        text=("Bienvenid@! Yo seré tu canal de comunicación secreto con el "
              "profesor. Si tienes alguna sugerencia anónima que hacerle, "
              "puedes hacerlo a través de mi. Para mandar una nueva sugerencia "
              "utiliza el commando /suggest"))


def start_suggestion(update: Update, context: CallbackContext) -> int:
    reply_markup = telegram.ReplyKeyboardMarkup(
        [['Anónima'], ['Identificable']])

    update.message.reply_text(
        text=("Vamos a registrar tu sugerencia."
              " Quieres que sea anónima o identificable? "
              "PD: Si te arrepientes, usa el comando /cancel para cancelar"
              " el envío"),
        reply_markup=reply_markup)

    return ANON


def record_suggestion(update: Update, context: CallbackContext) -> int:
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


def anonymous_suggestion(update: Update, context: CallbackContext) -> int:
    msg = update.message.text
    update.message.reply_text(
        ("Genial, mandaré este mensaje al profesor de forma anónima. "
         "Muchas gracias por tus comentarios! Recuerda que puedes volver "
         "a utilizar el comando /suggest para hacer nuevas sugerencias")
    )

    msg = "Sugerencia enviada anónimamente:\n" + msg
    context.bot.send_message(chat_id=os.environ['TEACHER_CHAT_ID'], text=msg)

    return ConversationHandler.END


def identifiable_suggestion(update: Update, context: CallbackContext) -> int:
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


def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        ("De acuerdo! No mandaré nada al profesor. Espero que vuelvas a "
         "utilizarme en otro momento!")
    )

    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('suggest', start_suggestion)],
    states={
        ANON: [MessageHandler(Filters.regex('^(Anónima|Identificable)$'),
                              record_suggestion
                              )],
        IDENT_MSG: [MessageHandler(Filters.text & ~Filters.command,
                                   identifiable_suggestion)],
        ANON_MSG: [MessageHandler(Filters.text & ~Filters.command,
                                  anonymous_suggestion)],
    },
    fallbacks=[CommandHandler('cancel', cancel)])


bot = Bot(token=os.environ["TOKEN"])

dispatcher = Dispatcher(bot=bot, update_queue=None, workers=0)
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(conv_handler)


@app.route("/", methods=["POST"])
def index() -> Response:
    dispatcher.process_update(
        Update.de_json(request.get_json(force=True), bot))

    return "", http.HTTPStatus.NO_CONTENT


if __name__ == '__main__':
    app.run()
