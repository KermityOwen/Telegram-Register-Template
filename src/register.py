import mysql.connector
import os
import telebot
import re
from enums import statesEnums

HOST = os.getenv("HOST")
USER = os.getenv("USER")
PW = os.getenv("PASSWORD")

mydb = mysql.connector.connect(
    host=HOST,
    user=USER,
    password=PW,
    database="d_morgentaler"
)

mycursor = mydb.cursor()

"""
class registerThread():
    def __init__(self, API_KEY):
        self.reg_bot = telebot.TeleBot(API_KEY)
        self.chat_states = {}
        self.cached_names = {}

        @self.reg_bot.message_handler(content_types=["text"])
        def ask_status(message):
            #print(self.chat_states[message.chat.id])
            if self.validate_state(message.chat.id, statesEnums.registering):
                try:
                    if message.text.lower() == "helper":
                        self.reg_bot.reply_to(message,
                                     "Registered as helper! \n\nIf you would like, please enter your name. (Type "
                                     "'SKIP' in all caps to skip)")
                        self.chat_states[message.chat.id] = statesEnums.registeringHelperName
                        return

                    elif message.text.lower() == "seeker":
                        self.reg_bot.reply_to(message, "Registered as seeker!")
                        print(
                            "nothing")  # ------------------------------------------------------------------------------------- PLACEHOLDER -------------------------------------------------------------------------------------

                    elif message.text.lower() == "quit":
                        self.chat_states[message.chat.id] = statesEnums.empty
                        self.reg_bot.reply_to(message, "Ok, no problem.")

                    else:
                        self.reg_bot.reply_to(message,
                                     "Sorry that is an invalid response. \n\nPlease type either 'helper' or 'seeker' or "
                                     "'quit' to return to the commands menu.")
                except:
                    print("An error has occurred")

            if self.validate_state(message.chat.id, statesEnums.registeringHelperName):
                print("valid")
                try:
                    if message.text == "SKIP":
                        self.cached_names[message.chat.id] = "*nameless*"
                        self.reg_bot.reply_to(message,
                                     "Name skipped. \n\nPlease enter your coordinates (Format: '*Latitude* (empty space) *Longitude*').")
                        self.chat_states[message.chat.id] = statesEnums.registeringCoord
                        return
                    else:
                        self.cached_names[message.chat.id] = message.text
                        self.reg_bot.reply_to(message, "Name set as %s. \n\nPlease enter your coordinates." % message.text)
                        self.chat_states[message.chat.id] = statesEnums.registeringCoord
                        return
                except:
                    print("An error has occured")

            if self.validate_state(message.chat.id, statesEnums.registeringCoord):
                print("valid")
                try:
                    coord = re.split(" +", message.text)
                    for i in range(len(coord)):
                        coord[i] = float(coord[i])
                    reg_name = self.cached_names[message.chat.id]
                    create_helper(reg_name, coord[0], coord[1], message.from_user.id)
                    self.reg_bot.reply_to(message,
                                 "Registered as Helper. \n\nName: %s, Latitude: %s, Longitude: %s, UID: %s." % (
                                 reg_name, coord[0], coord[1], message.from_user.id))
                    self.chat_states[message.chat.id] = statesEnums.empty
                    return
                except ValueError:
                    print("An error has occured")
                except IndexError:
                    print("An error has occured")

    def find_state(self, chat_id):
        try:
            return self.chat_states[chat_id]
        except KeyError:
            return statesEnums.empty

    def validate_state(self, chat_id, state_enum):
        if self.find_state(chat_id) is state_enum:
            return True
            print("debug true")
        else:
            return False
            print("debug false")

    def runRegThread(self):
        self.reg_bot.polling()
"""

def create_helper(username, name, zip_code, id):
    sql = "INSERT INTO helpers (username, name, zipcode, uid) VALUES (%s, %s, %s, %s)"
    values = (username, name, zip_code, id)
    mycursor.execute(sql, values)
    mydb.commit()
    print("done")

def create_seeker(username, name, zip_code, id):
    sql = "INSERT INTO seekers (username, name, zipcode, uid) VALUES (%s, %s, %s, %s)"
    values = (username, name, zip_code, id)
    mycursor.execute(sql, values)
    mydb.commit()
    print("done")

# mycursor.execute("CREATE TABLE helpers (name VARCHAR(255), latitude FLOAT(7, 5), longitude FLOAT(8, 5))")

