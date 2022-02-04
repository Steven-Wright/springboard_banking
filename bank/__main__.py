import argparse
from bank import Storage, FileUtils
from bank.main import list_employees, add_employee, remove_employee
from bank.main import list_applicaitons, approve_application, remove_application
from bank.main import list_customers, add_customer, remove_customer
from bank.main import list_accounts, add_account, remove_account, deposit, withdraw, transfer
from bank.main import list_services, apply_for_service, borrow_from_service, pay_to_service

parser = argparse.ArgumentParser()
parser.description = "simulate a bank, demonstrate OOP design practices"
parser.add_argument("-f", "--file", default="bank.json", required=False)
command_subparsers = parser.add_subparsers()
command_subparsers.required = True

# EMPLOYEE SUB COMMAND
employee_parser = command_subparsers.add_parser('employee')
employee_subparser = employee_parser.add_subparsers()
employee_subparser.required = True

# bank employee list
employee_list = employee_subparser.add_parser('list')
employee_list.set_defaults(func=list_employees)

# bank employee add <first_name> <second_name>
employee_add = employee_subparser.add_parser('add')
employee_add.add_argument('first_name', type=str)
employee_add.add_argument('last_name', type=str)
employee_add.set_defaults(func=add_employee)

# bank employee remove <index>
employee_remove = employee_subparser.add_parser('remove')
employee_remove.add_argument("employee_index", type=int)
employee_remove.set_defaults(func=remove_employee)

# EMPLOYEE APPLICATION SUB COMMAND
employee_application_parser = employee_subparser.add_parser('application')
employee_application_subparser = employee_application_parser.add_subparsers()
employee_application_subparser.required = True

# bank employee service list
employee_service_list = employee_application_subparser.add_parser('list')
employee_service_list.set_defaults(func=list_applicaitons)

# bank employee service approve <customer_index> <service_index>
employee_service_approve = employee_application_subparser.add_parser('approve')
employee_service_approve.add_argument('customer_index', type=int)
employee_service_approve.add_argument('service_index', type=int)
employee_service_approve.set_defaults(func=approve_application)

# bank employee service deny <customer_index> <service_index>
employee_service_deny = employee_application_subparser.add_parser('deny')
employee_service_deny.add_argument('customer_index', type=int)
employee_service_deny.add_argument('service_index', type=int)
employee_service_deny.set_defaults(func=remove_application)

# CUSTOMER SUB COMMAND
customer_parser = command_subparsers.add_parser('customer')
customer_subparser = customer_parser.add_subparsers()
customer_subparser.required = True

# bank customer list
customer_add = customer_subparser.add_parser("list")
customer_add.set_defaults(func=list_customers)

# bank customer add <first_name> <last_name> <address>
customer_add = customer_subparser.add_parser('add')
customer_add.add_argument("first_name", type=str)
customer_add.add_argument("last_name", type=str)
customer_add.add_argument("address", type=str)
customer_add.set_defaults(func=add_customer)

# bank customer remove <index>
customer_remove = customer_subparser.add_parser('remove')
customer_remove.add_argument("customer_index", type=int)
customer_remove.set_defaults(func=remove_customer)

# CUSTOMER ACCOUNT SUB COMMAND
customer_account_parser = customer_subparser.add_parser('account')
customer_account_subparser = customer_account_parser.add_subparsers()
customer_account_subparser.required = True

# bank customer account list <customer_index>
customer_account_list = customer_account_subparser.add_parser('list')
customer_account_list.add_argument("customer_index", type=int)
customer_account_list.set_defaults(func=list_accounts)

# bank customer account add <customer_index>
customer_account_add = customer_account_subparser.add_parser('add')
customer_account_add.add_argument("customer_index", type=int)
customer_account_add.add_argument("type", type=str)
customer_account_add.set_defaults(func=add_account)

# bank customer account remove <customer_index> <account_index>
customer_remove = customer_account_subparser.add_parser('remove')
customer_remove.add_argument("customer_index", type=int)
customer_remove.add_argument("account_index", type=int)
customer_remove.set_defaults(func=remove_account)

# bank customer account deposit <customer_index> <account_index> <amount>
customer_account_deposit = customer_account_subparser.add_parser('deposit')
customer_account_deposit.add_argument("customer_index", type=int)
customer_account_deposit.add_argument("account_index", type=int)
customer_account_deposit.add_argument("amount", type=float)
customer_account_deposit.set_defaults(func=deposit)

# bank customer account withdraw <customer_index> <account_index> <amount>
customer_account_withdraw = customer_account_subparser.add_parser('withdraw')
customer_account_withdraw.add_argument("customer_index", type=int)
customer_account_withdraw.add_argument("account_index", type=int)
customer_account_withdraw.add_argument("amount", type=float)
customer_account_withdraw.set_defaults(func=withdraw)

# bank customer account transfer <customer_index> <source_account_index> <destination_account_index> <amount>
customer_account_transfer = customer_account_subparser.add_parser('transfer')
customer_account_transfer.add_argument("customer_index", type=int)
customer_account_transfer.add_argument("source_account_index", type=int)
customer_account_transfer.add_argument("destination_account_index", type=int)
customer_account_transfer.add_argument("amount", type=float)
customer_account_transfer.set_defaults(func=transfer)

# # CUSTOMER SERVICE SUB COMMAND
customer_service_parser = customer_subparser.add_parser('service')
customer_service_subparser = customer_service_parser.add_subparsers()
customer_service_subparser.required = True

# bank customer service list <customer_index>
customer_service_list = customer_service_subparser.add_parser('list')
customer_service_list.add_argument("customer_index", type=int)
customer_service_list.set_defaults(func=list_services)

# bank customer service apply <customer_index> <limit>
customer_service_apply = customer_service_subparser.add_parser('apply')
customer_service_apply.add_argument("customer_index", type=int)
customer_service_apply.add_argument("limit", type=float)
customer_service_apply.set_defaults(func=apply_for_service)

# bank customer service borrow <customer_index> <service_index> <account_index> <amount>
customer_service_borrow = customer_service_subparser.add_parser('borrow')
customer_service_borrow.add_argument("customer_index", type=int)
customer_service_borrow.add_argument("service_index", type=int)
customer_service_borrow.add_argument("account_index", type=int)
customer_service_borrow.add_argument("amount", type=float)
customer_service_borrow.set_defaults(func=borrow_from_service)

# bank customer service pay <customer_index> <service_index> <account_index> <amount>
customer_service_pay = customer_service_subparser.add_parser('pay')
customer_service_pay.add_argument("customer_index", type=int)
customer_service_pay.add_argument("service_index", type=int)
customer_service_pay.add_argument("account_index", type=int)
customer_service_pay.add_argument("amount", type=float)
customer_service_pay.set_defaults(func=pay_to_service)

arguments = parser.parse_args()
with Storage(FileUtils, arguments.file) as storage:
    arguments.func(storage, arguments)
