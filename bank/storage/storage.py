from bank.customer import Customer
from bank.employee import Employee

class Storage:
    """Class responsible for managing persisent storage"""
    def __init__(self, utils_class, *args, **kwargs):
        self.utils = utils_class(*args, **kwargs)
        self.customers = []
        self.employees = []
        self.globals = {}

    def load(self):
        """Retrieves data from storage"""
        data = self.utils.read_dict()
        customers = data.get("customers", [])
        employees = data.get("employees", [])
        self.globals = data.get("globals", {})

        self.customers = [Customer.from_dict(source_dict) for source_dict in customers]
        self.employees = [Employee.from_dict(source_dict) for source_dict in employees]

    def save(self):
        """Saves data to storage"""
        data = {
            "customers": [customer.to_dict() for customer in self.customers],
            "employees": [employee.to_dict() for employee in self.employees],
            "globals": self.globals
        }

        self.utils.write_dict(data)

    def __enter__(self):
        self.load()
        return self

    def __exit__(self, *_):
        self.save()
