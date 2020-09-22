class ExampleBin:
  def __init__(self, initial_cash):
    self.balance = initial_cash

  def deposit(self, amount):
    self.balance += amount

  def withdraw(self, amount):
    self.balance -= amount