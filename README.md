# Implement a simple ATM controller

## Assumptions
The card holder of the ATM can only fit one card inside.

For simplicity, we assume that there is only two types of information per card: a unique number and the PIN. We disregard any other information such as card holder name, date of validity, etc.

We allow up to 3 submissions for a PIN. That is, if you are wrong for 3 PIN submissions, your card is locked out for an hour by the server. This is controlled by `__wrong_pin_count` in `ATM.py`.

If you try to withdraw more than your balance, the ATM is reset and you will have to start from the beginning. This also happens if you select an account index that is unavailable.

Physical APIs are mentioned and not implemented.

Doing more than action consecutively is not implemented in `ATM.py`. This is up to the UI designer.

## Code explanation
The main code is in `ATM.py`.

The test code is in `main.py`.
Functions are tested with `assert()` functions.

You can simply run it with `python main.py`. If all tests pass, you will see `Success!` at the end.
To see all logs while running the file, run `python main.py --log`.
(This is for seeing all ERROR messages, and even for viewing the available accounts.)

In `main.py`, we use a `testATM` instead of an `ATM` for testing purposes.
Simply put, `testATM` inherits `ATM`, but all of the class variables are available through public functions, so that we can check it easily.
For production, `ATM` should be used.

All files that start with `example_` are not a scope of this task, but a simple mock version is implemented for API users that may use this code in the future.

The security in the ATM's APIs are controlled by private flags.

The flags are turned on in this order: `__occupied`, `__verifiedCard`, `__verifiedCardAndPIN`, `__accountSelected`.
The APIs are protected by these flags. That is, if you do not properly turn these flags on with a valid card, valid PIN, valid account, the APIs will not work at all and return `False` and an error message.

An API called at the wrong time is considered a malicious attempt and will always cause the machine to eject the card and reset.

