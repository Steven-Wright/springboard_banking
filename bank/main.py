import logging
import sys
from bank import Employee, Customer


def _get_customer(storage, index):
    """ helper function to retrieve customer from storage """
    try:
        customer = storage.customers[index]
    except IndexError:
        logging.critical("Could not find customer %s", index)
        sys.exit(1)

    return customer


def _get_account(storage, customer_index, account_index):
    """ helper function to retrieve account from storage """
    customer = _get_customer(storage, customer_index)
    try:
        account = customer[account_index]
    except IndexError:
        logging.critical(
            "Could not find account %s belonging to customer %s", account_index, customer_index)
        sys.exit(1)

    return account


def list_employees(storage, _):
    """ print list of employees """
    print("Listing {0} employees".format(len(storage.employees)))
    for i, emp in enumerate(storage.employees):
        print("{0}:, {1}, {2}".format(i, emp.f_name, emp.l_name))


def add_employee(storage, args):
    """ add new employee """
    emp = Employee(args.first_name, args.last_name)
    storage.employees.append(emp)


def remove_employee(storage, args):
    """ remove an employee """
    try:
        del storage.employees[args.employee_index]
    except IndexError:
        logging.critical(
            "Could not find an employee with index %s", args.employee_index)


def list_customers(storage, _):
    """ list customers """
    print("Listing {0} customers".format(len(storage.customers)))
    for i, cust in enumerate(storage.customers):
        print("{0}: {1}, {2}, {3}, ${4:.2f}".format(
            i, cust.f_name, cust.l_name, cust.address, cust.total_balance))


def add_customer(storage, args):
    """ add a new customer """
    cust = Customer(args.first_name, args.last_name, args.address)
    storage.customers.append(cust)


def remove_customer(storage, args):
    """ remove a customer, checks that total balance is 0 """
    cust = _get_customer(storage, args.customer_index)
    if cust.total_balance != 0:
        logging.error("Could not remove customer %s, total balance is $%s, not $0.00",
                      args.customer_index, cust.total_balance)
    else:
        del storage.customers[args.customer_index]

# def open_account(args):
#     """ add account for customer """
#     with Storage(FileUtils, "bank.json")

#     with Storage(FileUtils, "bank.json") as storage:
#         try:
#             customer = storage.customers[args.customer_index]
#         except IndexError:
#             logging.critical(

#             )
# def deposit(args):
#     """ deposit into a customer's account """
#     with Storage(FileUtils, "bank.json") as storage:

#         try:
#             account = customer.accounts[args.account_index]
#         except IndexError:
#             logging.critical(
#                 "Could not find account %s for customer %s",
#                     args.account_index,
#                     args.customer_index
#             )

#         account.deposit(args.amount)
