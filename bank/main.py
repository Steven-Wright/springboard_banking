import logging
import sys
from bank import Employee, Customer, Account, Service


def _get_customer(storage, index):
    """ helper function to retrieve customer from storage """
    try:
        customer = storage.customers[index]
    except IndexError:
        logging.critical("Could not find customer %s", index)
        sys.exit(1)

    return customer


def _get_customer_account(storage, customer_index, account_index):
    """ helper function to retrieve account from storage """
    customer = _get_customer(storage, customer_index)
    try:
        account = customer.accounts[account_index]
    except IndexError:
        logging.critical(
            "Could not find account %s belonging to customer %s", account_index, customer_index)
        sys.exit(1)

    return (customer, account)


def _get_customer_service(storage, customer_index, service_index):
    """ helper function to retrieve service from storage """
    customer = _get_customer(storage, customer_index)
    try:
        service = customer.services[service_index]
    except IndexError:
        logging.critical(
            "Could not find service %s belonging to customer %s", service_index, customer_index)
        sys.exit(1)

    return (customer, service)


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


def list_accounts(storage, args):
    cust = _get_customer(storage, args.customer_index)
    print("Listing {0} accounts".format(len(cust.accounts)))
    for i, account in enumerate(cust.accounts):
        print("{0}: {1}, ${2:.2f}".format(i, account.type, account.balance))


def add_account(storage, args):
    """ add an account to a customer """
    cust = _get_customer(storage, args.customer_index)
    cust.accounts.append(Account(args.type, 0))


def remove_account(storage, args):
    """ remove an account from a customer """
    cust, acct = _get_customer_account(
        storage, args.customer_index, args.account_index)
    if acct.balance != 0:
        logging.error("Could not remove customer %s account %s, account balance is $%s not $0.00",
                      args.customer_index, args.account_index, acct.balance)
    else:
        del cust.accounts[args.account_index]


def deposit(storage, args):
    """ deposit into a customer's account """
    _, account = _get_customer_account(
        storage, args.customer_index, args.account_index)
    account.deposit(args.amount)


def withdraw(storage, args):
    """ withdrawl from a customer's account """
    _, account = _get_customer_account(
        storage, args.customer_index, args.account_index)
    account.withdrawl(args.amount)


def transfer(storage, args):
    """ transfer money between a customer's accounts """
    _, source_account = _get_customer_account(
        storage, args.customer_index, args.source_account_index)
    _, destination_account = _get_customer_account(
        storage, args.customer_index, args.destination_account_index)

    source_account.withdrawl(args.amount)
    destination_account.deposit(args.amount)


def list_services(storage, args):
    """ list a customer's services """
    cust = _get_customer(storage, args.customer_index)
    print("Listing {0} services".format(len(cust.services)))
    if len(cust.services) > 0:
        print("index: status, limit, balance")
    for i, service in enumerate(cust.services):
        print("{0}: {1} ${2} ${3}".format(
            i, service.status, service.limit, service.balance))


def apply_for_service(storage, args):
    """ apply for a new service """
    cust = _get_customer(storage, args.customer_index)
    service = Service(args.limit)
    cust.services.append(service)


def borrow_from_service(storage, args):
    """ borrow funds from a service """
    _, service = _get_customer_service(
        storage, args.customer_index, args.service_index)
    _, account = _get_customer_account(
        storage, args.customer_index, args.account_index)
    service.lend(args.amount, account)


def pay_to_service(storage, args):
    """ pay funds to a service """
    _, service = _get_customer_service(
        storage, args.customer_index, args.service_index)
    _, account = _get_customer_account(
        storage, args.customer_index, args.account_index)
    service.collect(args.amount, account)


def list_applicaitons(storage, _):
    """ list all pending applications """
    applications = []
    for customer_index, customer in enumerate(storage.customers):
        for service_index, service in enumerate(customer.services):
            if service.status == "application":
                applications.append((
                    customer_index,
                    customer.f_name,
                    customer.l_name,
                    customer.total_balance,
                    customer.total_limit,
                    service_index,
                    service.limit))

    print("Listing {0} applications".format(len(applications)))
    if len(applications) > 0:
        print("customer_index, first_name, last_name, total_balance, total_limit, service_index, limit")
        for application in applications:
            print("#{0}, {1}, {2}, {3}, ${4}, #{5}, ${6}".format(*application))


def approve_application(storage, args):
    """ approve an application """
    cust, service = _get_customer_service(
        storage, args.customer_index, args.service_index)
    if cust.total_balance < (cust.total_limit + service.limit):
        logging.warning("Customer %s's total balance %s is less than total limit after approval %s",
                        args.customer_index,
                        cust.total_balance,
                        cust.total_limit + service.limit
                        )
    else:
        service.approve()


def remove_application(storage, args):
    """ remove an application """
    cust, service = _get_customer_service(
        storage, args.customer_index, args.service_index)
    print(service.status)
    if service.status != "application":
        logging.warning(
            "cannot remove customer %s's service %s as it is not an application")
    else:
        del cust.services[args.service_index]
