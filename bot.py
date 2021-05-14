from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests

from functools import wraps


LIST_OF_ALLOWED_USERS = [12345678]

def restricted(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in LIST_OF_ALLOWED_USERS:
            print("Unauthorized access denied for {}.".format(user_id))
            return
        return func(update, context, *args, **kwargs)
    return wrapped


@restricted
def help_command(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help: \n\t/ifconfig: get my public ip.\n\t/photo: get photo from camera.')


@restricted
def ifconfig_command(update: Update, _: CallbackContext) -> None:
    try:
        req = requests.get("https://api64.ipify.org?format=json")
        ip = req.json()['ip']
        update.message.reply_text(ip)
    except Exception as err:
        update.message.reply_text("Error: {0}".format(err))


@restricted
def photo_command(update: Update, _: CallbackContext) -> None:
    update.message.reply_text(update.effective_user.id)


def main() -> None:
    updater = Updater('')

    updater.dispatcher.add_handler(CommandHandler('help', help_command))
    updater.dispatcher.add_handler(CommandHandler('photo', photo_command))
    updater.dispatcher.add_handler(CommandHandler('ifconfig', ifconfig_command))


    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

