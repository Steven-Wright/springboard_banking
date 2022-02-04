# banking - simulate a bank, demonstrate OOP design practices

## Usage
### Application
Run the module using the following syntax:
```
python -m bank <command> <sub_command> [<arg> ...]
```

For example:
```
bank employee list
bank employee add <first_name> <second_name>
bank employee remove <index>
bank employee service list
bank employee service approve <customer_index> <service_index>
bank employee service deny <customer_index> <service_index>

bank customer list
bank customer add <first_name> <last_name> <address>
bank customer remove <index>

bank customer account list <customer_index>
bank customer account add <customer_index>
bank customer account remove <customer_index> <account_index>
bank customer account deposit <customer_index> <account_index> <amount>
bank customer account withdraw <customer_index> <account_index> <amount>
bank customer account transfer <customer_index> <source_account_index> <destination_account_index> <amount>

bank customer service list <customer_index>
bank customer service apply <customer_index> <limit>
bank customer service borrow <customer_index> <service_index> <account_index> <amount>
bank customer service pay <customer_index> <service_index> <account_index> <amount>
```

### Testing
Run unit tests with the following command:
```
python -m unittest discover
```

## Structure
Tests are located within tests subdirectory, code for the module is within bank subdirectory. 
- `bank/__init__.py` defines the exported attributes (important for importing from outside module - i.e. for testing)
- `bank/__main__.py` contains the code for the command line interface (arg_parse) and acts as the entrypoint
- `bank/main.py` contains the business logic called by `__main__.py`

### Class Structure
See `Class and Code Path Diagrams.pdf`


## Possible Improvements
1. `bank/__main__.py` and `bank/main.py` could be decoupled, currently functions within the latter file depend on taking args as a parameter
2. `bank.Storage` could be refactored to handle storage in an atomic fashion implementing methods like `get_customer` rather than providing a `customers` attribute

## Generate documentation
```
mkdir doc
python -m pydoc -w bank bank.{storage,storage.storage,storage.file_utils,account,customer,employee,main,service}
mv *.html doc/
```