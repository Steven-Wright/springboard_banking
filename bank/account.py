class Account:
    """
    class representing an account.
    """
    def __init__(self, type_str, balance):
        if type_str != 'service' and balance < 0:
            raise ValueError("Only service accounts can have negative balance")
        self._type = type_str
        self._balance = balance

    @property
    def type(self):
        """
        the account's type
        "service" is special as it can carry a negative balance
        """
        return self._type

    @property
    def balance(self):
        """
        the account's balance
        should be modified using deposit and withdraw methods
        """
        return self._balance

    def deposit(self, amount):
        """ deposit to account balance """
        self._balance += amount

    def withdrawl(self, amount):
        """ withdraw from account balance. Raises ValueError if withdrawl amount exceeds funds. """
        if amount > self._balance and self._type != "service":
            raise ValueError("Insufficient Funds")
        self._balance -= amount

    def to_dict(self):
        """ Serializes class instance to dictionary """
        return {
            "type": self._type,
            "balance": self._balance
        }

    @classmethod
    def from_dict(cls, source):
        """ Creates class instance from dict """
        return cls(source["type"], source["balance"])
    