from bank.account import Account

class Service:
    """ Class representing a lending service """
    def __init__(self, limit, account=None, status="application"):
        if limit < 0:
            raise ValueError("limit must cannot be negative")

        if account is None:
            self._account = Account("service", 0.)
        else:
            self._account = account
        self.limit = limit
        self._status = status

    @property
    def status(self):
        """Status of service - approved or application etc."""
        return self._status

    @property
    def balance(self):
        """Returns balance of """
        return self._account.balance

    def approve(self):
        """Sets status to approved"""
        self._status = "approved"

    def collect(self, amount, from_account):
        """Credit service account from from_account"""
        if self._status != 'approved':
            raise RuntimeError("Service not approved")

        try:
            from_account.withdrawl(amount)
            self._account.deposit(amount)
        except ValueError as err:
            raise RuntimeError("Unable to collect funds") from err

    def lend(self, amount, to_account):
        """Lend balance from service account to to_account"""
        if self._status != 'approved':
            raise RuntimeError("Service not approved")

        if (self._account.balance - amount) < -self.limit:
            raise ValueError("Requested amount exceeds credit limit")

        self._account.withdrawl(amount)
        to_account.deposit(amount)

    def to_dict(self):
        """ Serialize class instance to dictionary """
        return {
            "account": self._account.to_dict(),
            "limit": self.limit,
            "status": self._status
        }

    @classmethod
    def from_dict(cls, source):
        """ Create class instance from dictionary"""
        return cls(source["limit"], Account.from_dict(source["account"]), source["status"])
