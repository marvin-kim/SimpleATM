class Account:
  def __init__(self, account_name, initial_amount=0):
    self.name = account_name
    self.balance = initial_amount

  def getBalance(self):
    return self.balance

  def deposit(self, amount):
    self.balance += amount
    return self.balance

  def withdraw(self, amount):
    if amount > self.balance:
      return -1
    else:
      self.balance -= amount
      return self.balance
