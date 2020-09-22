from exampleBin import ExampleBin
from exampleBank import ExampleBankServer
from exampleCard import ExampleCard
from testATM import testATM


def setup():
  # The cash bin has $10000 within it.
  exampleBin = ExampleBin(10000)
  exampleServer = ExampleBankServer()
  cards = []

  # User 1 has card1 and PIN 1000, with 1 account connected to card1.
  card1 = ExampleCard(1)
  exampleServer.addCard(1, 1000)
  exampleServer.addAccount(1, 'checking', 20)
  cards.append(card1)

  # User 2 has card2 and PIN 2000, with 2 accounts connected to card2.
  card2 = ExampleCard(2)
  exampleServer.addCard(2, 2000)
  exampleServer.addAccount(2, 'checking', 80)
  exampleServer.addAccount(2, 'savings', 40)
  cards.append(card2)

  return testATM(exampleBin, exampleServer), cards

def simpleEval(result, msg, expected_boolean):
  print(msg+'\n')
  assert result == expected_boolean

# User 1 does some actions.
def main1(atm, card1):
  print("********** main1() starts here **********")
  assert atm.occupied() is False
  simpleEval(*atm.insertCard(card1), True)
  assert atm.occupied() is True
  assert atm.verifiedCard() is True
  simpleEval(*atm.submitPIN(1000), True)
  assert atm.verifiedCardAndPIN() is True
  simpleEval(*atm.displayAccounts(), True)
  simpleEval(*atm.selectAccount(0), True)
  assert atm.account() is not None
  simpleEval(*atm.seeBalance(), True)
  assert atm.account().balance == 20
  simpleEval(*atm.deposit(30), True)
  assert atm.account().balance == 50
  simpleEval(*atm.seeBalance(), True)
  simpleEval(*atm.withdraw(60), False)  # Trying to withdraw more than balance
  assert atm.occupied() is False

  # 3 mistaken PIN submissions and card insert attempt.
  simpleEval(*atm.insertCard(card1), True)
  assert atm.occupied() is True
  assert atm.verifiedCard() is True
  simpleEval(*atm.submitPIN(1001), False)
  assert atm.verifiedCardAndPIN() is False
  simpleEval(*atm.submitPIN(1002), False)
  assert atm.verifiedCardAndPIN() is False
  simpleEval(*atm.submitPIN(1003), False)
  assert atm.verifiedCardAndPIN() is False
  assert atm.occupied() is False
  simpleEval(*atm.insertCard(card1), False)
  assert atm.occupied() is False


# User 2 does some actions.
def main2(atm, card2):
  print("********** main2() starts here **********")
  simpleEval(*atm.insertCard(ExampleCard(3)), False)  # Wrong card
  assert atm.occupied() is False
  simpleEval(*atm.insertCard(ExampleCard(2)), True)
  assert atm.occupied() is True
  simpleEval(*atm.submitPIN(2000), True)
  assert atm.occupied() is True
  assert atm.verifiedCard() is True
  simpleEval(*atm.displayAccounts(), True)
  simpleEval(*atm.selectAccount(3), False)  # Wrong account index
  assert atm.account() is None
  simpleEval(*atm.insertCard(ExampleCard(2)), True)
  assert atm.occupied() is True
  simpleEval(*atm.submitPIN(2000), True)
  assert atm.occupied() is True
  assert atm.verifiedCard() is True
  simpleEval(*atm.displayAccounts(), True)
  simpleEval(*atm.selectAccount(1), True)
  assert atm.account() is not None
  simpleEval(*atm.seeBalance(), True)
  assert atm.account().balance == 40
  simpleEval(*atm.deposit(10), True)
  assert atm.account().balance == 50
  simpleEval(*atm.withdraw(30), True)
  assert atm.account().balance == 20
  simpleEval(*atm.ejectAndReset(), True)  # End the transaction normally.
  assert atm.occupied() is False


if __name__=='__main__':
  atm, cards = setup()
  main1(atm, cards[0])
  main2(atm, cards[1])
  