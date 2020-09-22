from ATM import ATM

class testATM(ATM):
  def __init__(self, cash_bin, bank_server):
    super().__init__(cash_bin, bank_server)

  def occupied(self):
    return self._ATM__occupied

  def verifiedCard(self):
    return self._ATM__verifiedCard

  def verifiedCardAndPIN(self):
    return self._ATM__verifiedCardAndPIN

  def accountSelected(self):
    return self._ATM__accountSelected

  def wrong_pin_count(self):
    return self._ATM__wrong_pin_count

  def current_card_number(self):
    return self._ATM__current_card_number

  def accounts(self):
    return self._ATM__accounts

  def account(self):
    return self._ATM__account