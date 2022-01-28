"""Module containing all classes for bank.py"""
import logging
import json

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

class Employee:
    """
    class representing an employee
    """
    def __init__(self, f_name, l_name):
        self.f_name = f_name
        self.l_name = l_name

    def to_dict(self):
        """ Serializes class instance to dictionary """
        return {
            "f_name": self.f_name,
            "l_name": self.l_name
        }

    @classmethod
    def from_dict(cls, source):
        """ Creates class instance from dict """
        return cls(source["f_name"], source["l_name"])

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

class Customer:
    """ Encapsulates customer information, accounts and services """
    def __init__(self, f_name, l_name, address, accounts=None, services=None):
        self.f_name = f_name
        self.l_name = l_name
        self.address = address
        self.accounts = accounts if accounts is not None else []
        self.services = services if services is not None else []

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

class Storage:
    """ Class responsible for managing persisent storage """
    def __init__(self, path='bank.json'):
        self.path = path
        self.customers = []
        self.employees = []
        self.globals = {}

    def read_in(self):
        """read in data"""
        try:
            with open(self.path, 'r') as file:
                data = json.load(file)
        except FileNotFoundError as err:
            logging.warning("File not found at %s", self.path)
            raise err

        if 'customers' in data.keys():
            self.customers = [Customer.from_dict(entry) for entry in data['customers']]

        if 'employees' in data.keys():
            self.employees = [Employee.from_dict(entry) for entry in data['employees']]

        self.globals = data['globals'] if 'gobals' in data.keys() else {}

    def write_out(self):
        """ writes out data"""
        try:
            with open(self.path, 'w') as file:
                json.dump(
                    {'customers': [customer.to_dict() for customer in self.customers],
                    'employees': [employee.to_dict() for employee in self.employees],
                    'globals': self.globals},
                    file)
        except OSError as err:
            logging.critical("Unable to write to disk:%s", err)
            raise err

    def __enter__(self):
        """ trivial magic function for context manager ??? """
        self.read_in()
        return self

    def __exit__(self, *args):
        """ magic function for context manager - writes out to disk """
        self.write_out()
