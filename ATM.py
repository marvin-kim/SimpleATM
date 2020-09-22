class ATM:
  def __init__(self, cash_bin, bank_server):
    self.__cash_bin = cash_bin
    self.__bank_server = bank_server
    self.__occupied = False
    self.__verifiedCard = False
    self.__verifiedCardAndPIN = False
    self.__accountSelected = False
    self.__wrong_pin_count = 0
    self.__current_card_number = 0
    self.__accounts = []
    self.__account = None


  def insertCard(self, card):
    if not self.__occupied:
      self.__occupied = True
      valid, error_msg = self.__bank_server.verifyCard(card.unique_number)
      if valid:
        self.__current_card_number = card.unique_number
        self.__verifiedCard = True
        return True, "Card accepted. Submit PIN:"
      else:
        self.ejectAndReset()
        return False, error_msg
    else:
      self.ejectAndReset()
      return False, "[ERROR] ATM is already occupied."


  def submitPIN(self, PIN):
    if self.__verifiedCard and not self.__verifiedCardAndPIN:
      validPIN = self.__bank_server.verifyPIN(self.__current_card_number, PIN)
      if validPIN:
        self.__accounts = self.__bank_server.getAccounts(self.__current_card_number)
        self.__verifiedCardAndPIN = True
        return True, "Select Account:"
      else:
        self.__wrong_pin_count += 1
        if self.__wrong_pin_count == 3:
          self.__bank_server.lockCard(self.__current_card_number)
          self.ejectAndReset()
          return False, "[ERROR] Wrong PIN 3 times. Card is locked for an hour."
        else:
          return False, "[warning] Wrong pin number: Try again."
    else:
      self.ejectAndReset()
      return False, "[ERROR] submitPIN() should not be called now."


  def ejectAndReset(self):
    hasCard = self.__occupied
    self.__occupied = False
    self.__verifiedCard = False
    self.__verifiedCardAndPIN = False
    self.__accountSelected = False
    self.__wrong_pin_count = 0
    self.__current_card_number = 0
    self.__accounts = []
    self.__account = None
    self.ejectCard()
    if hasCard:
      return True, "Card ejected and ATM reset."
    else:
      return False, "No card. ATM reset."


  def displayAccounts(self):
    if self.__verifiedCardAndPIN:
      return True, "".join(["-" + account.name+"\n" for account in self.__bank_server.getAccounts(self.__current_card_number)])
    else:
      self.ejectAndReset()
      return False, "[ERROR] displayAccounts() should not be called if card and PIN are not verified."


  def selectAccount(self, account_index):
    if self.__verifiedCardAndPIN:
      if 0 <= account_index < len(self.__accounts):
        self.__account = self.__accounts[account_index]
        self.__accountSelected = True
        return True, "{} account selected".format(self.__account.name)
      else:
        self.ejectAndReset()
        return False, "[ERROR] Account index is invalid."
    else:
      self.ejectAndReset()
      return False, "[ERROR] Cannot select account unless card and PIN are verified."


  def seeBalance(self):
    if self.__account is not None:
      balance = self.__account.balance
      return True, "Current balance: " + str(balance)
    else:
      self.ejectAndReset()
      return False, "[ERROR] seeBalance() should not be called if account is not selected."


  def deposit(self, amount):
    if self.__accountSelected:
      self.__cash_bin.deposit(amount)
      balance = self.__account.deposit(amount)
      return True, "New balance after deposit: " + str(balance)
    else:
      self.ejectAndReset()
      return False, "[ERROR] deposit() should not be called if account is not selected."


  def withdraw(self, amount):
    if self.__accountSelected:
      balance = self.__account.withdraw(amount)
      if balance >= 0:
        self.__cash_bin.withdraw(amount)
        return True, "New balance after withdrawal: " + str(balance)
      else:
        self.ejectAndReset()
        return False, "[ERROR] Not enough money in your account."
    else:
      self.ejectAndReset()
      return False, "[ERROR] deposit() should not be called if account is not selected."

  # Physical API that is mentioned but not implemented.
  def ejectCard(self):
    # Some code to physically eject the card.
    return

