import argparse
from bank import Storage, FileUtils
from bank.main import list_employees, add_employee, remove_employee,  list_customers, add_customer, remove_customer

parser = argparse.ArgumentParser()
parser.description = "simulate a bank, demonstrate OOP design practices"
parser.add_argument("-f", "--file", default="bank.json", required=False)
command_subparsers = parser.add_subparsers()
command_subparsers.required = True

# EMPLOYEE SUB COMMAND
employee_parser = command_subparsers.add_parser('employee')
employee_subparser = employee_parser.add_subparsers()
employee_subparser.required = True

employee_list = employee_subparser.add_parser('list')
employee_list.set_defaults(func=list_employees)

employee_add = employee_subparser.add_parser('add')
employee_add.add_argument('first_name', type=str)
employee_add.add_argument('last_name', type=str)
employee_add.set_defaults(func=add_employee)

employee_remove = employee_subparser.add_parser('remove')
employee_remove.add_argument("employee_index", type=int)
employee_remove.set_defaults(func=remove_employee)

# CUSTOMER SUB COMMAND
customer_parser = command_subparsers.add_parser('customer')
customer_subparser = customer_parser.add_subparsers()
customer_subparser.required = True

customer_add = customer_subparser.add_parser("list")
customer_add.set_defaults(func=list_customers)

customer_add = customer_subparser.add_parser('add')
customer_add.add_argument("first_name", type=str)
customer_add.add_argument("last_name", type=str)
customer_add.add_argument("address", type=str)
customer_add.set_defaults(func=add_customer)

customer_remove = customer_subparser.add_parser('remove')
customer_remove.add_argument("customer_index", type=int)
customer_remove.set_defaults(func=remove_customer)

# CUSTOMER ACCOUNT SUB COMMAND
customer_account_parser = customer_subparser.add_parser('account')
customer_account_subparser = customer_account_parser.add_subparsers()
customer_account_subparser.required = True

customer_account_deposit = customer_account_subparser.add_parser('deposit')
customer_account_deposit.add_argument("customer_index", type=int)
customer_account_deposit.add_argument("account_index", type=int)
customer_account_deposit.add_argument("amount", type=float)
# customer_account_deposit.set_defaults(func=deposit)


arguments = parser.parse_args()
with Storage(FileUtils, arguments.file) as storage:
    arguments.func(storage, arguments)
