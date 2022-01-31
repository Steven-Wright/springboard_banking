import logging
import json
from customer import Customer
from employee import Employee

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
