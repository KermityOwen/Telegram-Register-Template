import os
import telebot
import register
import re
from enums import statesEnums

API_KEY = os.getenv("TELEGRAM_API_KEY")
HOST_IP = os.getenv("HOST_IP")

bot = telebot.TeleBot(API_KEY)

with open("helptxt.txt", "r") as t:
    help_text = t.read()
    t.close()

chat_states = {}
cached_names = {}


@bot.message_handler(commands=['help'])
def help_command(message):
    try:
        bot.reply_to(message, help_text)
    except:
        print("Error has occurred. Command: %s" % message.text)


@bot.message_handler(commands=["self"])
def test_self_id(message):
    try:
        bot.send_message(message.chat.id, message.chat.id)
    except:
        print("Error has occurred. Command: %s" % message.text)


def find_state(chat_id):
    try:
        return chat_states[chat_id]
    except KeyError:
        return statesEnums.empty


@bot.message_handler(commands=["register"])
def register_user(message):
    try:
        chat_states[message.chat.id] = statesEnums.registering
        bot.send_message(message.chat.id, "Are you a Helper or a Seeker?")
    except:
        print("Error has occurred. Command: %s" % message.text)


def validate_state(chat_id, state_enum):
    if find_state(chat_id) is state_enum:
        return True
        print("debug true")
    else:
        return False
        print("debug false")


@bot.message_handler(content_types=["text"])
def ask_status(message):
    print(chat_states[message.chat.id])
    if validate_state(message.chat.id, statesEnums.registering):
        try:
            if message.text.lower() == "helper":
                bot.reply_to(message, "Registered as helper! \n\nIf you would like, please enter your name. (Type "
                                      "'SKIP' in all caps to skip)")
                chat_states[message.chat.id] = statesEnums.registeringHelperName
                return

            elif message.text.lower() == "seeker":
                bot.reply_to(message, "Registered as seeker!")
                print("nothing") # ------------------------------------------------------------------------------------- PLACEHOLDER -------------------------------------------------------------------------------------

            elif message.text.lower() == "quit":
                chat_states[message.chat.id] = statesEnums.empty
                bot.reply_to(message, "Ok, no problem.")

            else:
                bot.reply_to(message, "Sorry that is an invalid response. \n\nPlease type either 'helper' or 'seeker' or "
                                      "'quit' to return to the commands menu.")
        except:
            print("An error has occurred")


    if validate_state(message.chat.id, statesEnums.registeringHelperName):
        print("valid")
        try:
            if message.text == "SKIP":
                cached_names[message.chat.id] = "*nameless*"
                bot.reply_to(message, "Name skipped. \n\nPlease enter your coordinates (Format: '*Latitude* (empty space) *Longitude*').")
                chat_states[message.chat.id] = statesEnums.registeringCoord
                return
            else:
                cached_names[message.chat.id] = message.text
                bot.reply_to(message, "Name set as %s. \n\nPlease enter your coordinates." % message.text)
                chat_states[message.chat.id] = statesEnums.registeringCoord
                return
        except:
            print("An error has occured")


    if validate_state(message.chat.id, statesEnums.registeringCoord):
        print("valid")
        try:
            coord = re.split(" +", message.text)
            for i in range(len(coord)):
                coord[i] = float(coord[i])
            reg_name = cached_names[message.chat.id]
            register.create_helper(reg_name, coord[0], coord[1], message.from_user.id)
            bot.reply_to(message, "Registered as Helper. \n\nName: %s, Latitude: %s, Longitude: %s, UID: %s." % (reg_name, coord[0], coord[1], message.from_user.id))
            chat_states[message.chat.id] = statesEnums.empty
            return
        except ValueError:
            print("An error has occured")
        except IndexError:
            print("An error has occured")

bot.polling()

float("sss")
# print(API_KEY)
