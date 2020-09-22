import collections
import time
from Account import Account

class ExampleBankServer:
  def __init__(self):
    # __PINdict: The key is a unique card number, and the value is the card's PIN.
    self.__PINdict = {}
    # __AccountDB: The key is a unique card number, and the value is the list of accounts
    self.__AccountDB = collections.defaultdict(list)
    # __lockedCards: The key is a unique number of a locked card, and the value is the time the lock ends.
    self.__lockedCards = {}


  def addCard(self, card_number, PIN):
    if card_number in self.__PINdict:
      print("[ERROR] The current card number already exists in the system.")
      return
    else:
      self.__PINdict[card_number] = PIN


  def addAccount(self, card_number, account_name, initialAmount=0):
    self.__AccountDB[card_number].append(Account(account_name, initialAmount))


  # For simplicity, we only use the card_number as an identification for the user.
  def verifyCard(self, card_number):
    if card_number in self.__lockedCards:
      curr_time = time.time()
      if curr_time < self.__lockedCards[card_number]:
        return False, "[ERROR] Card is locked."
      else:
        self.__lockedCards.pop(card_number)
    
    if card_number in self.__PINdict:
      return True, ""
    else:
      return False, "[ERROR] Card is unavailable."


  def verifyPIN(self, card_number, PIN):
    return PIN == self.__PINdict[card_number]


  def lockCard(self, card_number):
    curr_time = time.time()
    self.__lockedCards[card_number] = curr_time + 60*60  # Locked for an hour


  def getAccounts(self, card_number):
    return self.__AccountDB[card_number]
