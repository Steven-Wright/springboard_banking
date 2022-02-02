import argparse
import logging
from bank import Account, Employee, Service, Customer, Service, Storage

def list_employees(_):
    """ print list of employees """
    with Storage() as storage:
        print("Listing {0} employees".format(len(storage.employees)))
        for i, emp in enumerate(storage.employees):
            print("{0}: {1}, {2}".format(i, emp.f_name, emp.l_name))

def add_employee(args):
    """ add new employee """
    with Storage() as storage:
        emp = Employee(args.first_name, args.last_name)
        storage.employees.append(emp)

def remove_employee(args):
    """ remove an employee """
    with Storage() as storage:
        try:
            del storage.employees[args.index]
        except IndexError:
            logging.critical("Could not find an employee with index %s", args.index)

def list_customers(_):
    """ list customers """
    with Storage() as storage:
        print("Listing {0} customers".format(len(storage.customers)))
        for i, cust in enumerate(storage.customers):
            print("{0}: {1}, {2}, {3}, ${4:.2f}".format(i, cust.f_name, cust.l_name, cust.address, cust.total_balance))

def add_customer(args):
    """ add a new customer """
    with Storage() as storage:
        cust = Customer(args.first_name, args.last_name, args.address)
        storage.customers.append(cust)

def remove_customer(args):
    """ remove a customer """
    with Storage() as storage:
        try:
            total_balance = storage.customers[args.index].total_balance
        except IndexError:
            logging.critical("Could not find a customer with index %s", args.index)

        if total_balance != 0:
            logging.error("Could not remove customer {0}, total balance is ${1:.2f}, not $0.00".format(args.index, total_balance))
        else:
            del(storage.customers[args.index])


parser = argparse.ArgumentParser(description="simulate a bank, demonstrate OOP design practices")
command_subparsers = parser.add_subparsers()

# EMPLOYEE SUB COMMAND
employee_parser = command_subparsers.add_parser('employee')
employee_subparser = employee_parser.add_subparsers()

employee_list = employee_subparser.add_parser('list')
employee_list.set_defaults(func=list_employees)

employee_add = employee_subparser.add_parser('add')
employee_add.add_argument('first_name', type=str)
employee_add.add_argument('last_name', type=str)
employee_add.set_defaults(func=add_employee)

employee_remove = employee_subparser.add_parser('remove')
employee_remove.add_argument("index", type=int)
employee_remove.set_defaults(func=remove_employee)

# CUSTOMER SUB COMMAND
customer_parser = command_subparsers.add_parser('customer')
customer_subparser = customer_parser.add_subparsers()

customer_add = customer_subparser.add_parser("list")
customer_add.set_defaults(func=list_customers)

customer_add = customer_subparser.add_parser("add")
customer_add.add_argument("first_name", type=str)
customer_add.add_argument("last_name", type=str)
customer_add.add_argument("address", type=str)
customer_add.set_defaults(func=add_customer)

customer_remove = customer_subparser.add_parser('remove')
customer_remove.add_argument("index", type=int)
customer_remove.set_defaults(func=remove_customer)

arguments = parser.parse_args()

arguments.func(arguments)
