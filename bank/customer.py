from service import Service
from account import Account

class Customer:
    """ Encapsulates customer information, accounts and services """
    def __init__(self, f_name, l_name, address, accounts=None, services=None):
        self.f_name = f_name
        self.l_name = l_name
        self.address = address
        self.accounts = accounts if accounts is not None else []
        self.services = services if services is not None else []

    @property
    def total_balance(self):
        """ Return total worth of all accounts and services """
        if len(self.accounts) > 0 or len(self.services) > 0:
            accounts_total = sum([acct.balance for acct in self.accounts])
            services_total = sum([service.balance for service in self.services])
            return accounts_total + services_total
        else:
            return 0

    def to_dict(self):
        """ Serialize class instance to dictionary """
        return {
            "f_name": self.f_name,
            "l_name": self.l_name,
            "address": self.address,
            "accounts": [account.to_dict() for account in self.accounts],
            "services": [service.to_dict() for service in self.services]
        }

    @classmethod
    def from_dict(cls, source):
        """ Create instance of class from dictionary """
        return cls(
            source["f_name"],
            source["l_name"],
            source["address"],
            [Account.from_dict(account) for account in source["accounts"]],
            [Service.from_dict(service) for service in source["services"]]
        )


