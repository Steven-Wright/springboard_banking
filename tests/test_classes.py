import unittest
import json
from bank import Account, Employee, Service, Customer, Storage

class TestAccount(unittest.TestCase):
    def test_init_properties(self):
        acct = Account("savings", 0.)
        self.assertEqual(acct.type, "savings")
        self.assertEqual(acct.balance, 0.)

        acct = Account("checking", 100.)
        self.assertEqual(acct.type, "checking")
        self.assertEqual(acct.balance, 100.)

        with self.assertRaises(ValueError):
            Account("savings", -100)

        acct = Account("service", -50.)
        self.assertEqual(acct.type, "service")
        self.assertEqual(acct.balance, -50.)

    def test_deposit(self):
        acct = Account("savings", 0.)
        acct.deposit(100.)
        self.assertEqual(acct.balance, 100.)

    def test_withdrawl(self):
        acct = Account("savings", 100.0)
        self.assertEqual(acct.balance, 100.)
        acct.withdrawl(100.)
        self.assertEqual(acct.balance, 0.)
        with self.assertRaises(ValueError):
            acct.withdrawl(100.)

        acct = Account("service", 100.)
        self.assertEqual(acct.balance, 100.)
        acct.withdrawl(100.)
        acct.withdrawl(100.)
        self.assertEqual(acct.balance, -100.)

    def test_to_dict(self):
        acct = Account("savings", 100.0)
        self.assertDictEqual({
            "type": "savings",
            "balance": 100.0
        }, acct.to_dict())

    def test_from_dict(self):
        acct = Account.from_dict({
            "type": "savings",
            "balance": 100.0
        })
        self.assertEqual(acct.type, "savings")
        self.assertEqual(acct.balance, 100.0)


class TestEmployee(unittest.TestCase):
    def test_init(self):
        emp = Employee("Bill", "Gates")
        self.assertEqual(emp.f_name, "Bill")
        self.assertEqual(emp.l_name, "Gates")

        emp = Employee("Steve", "Jobs")
        self.assertEqual(emp.f_name, "Steve")
        self.assertEqual(emp.l_name, "Jobs")

    def test_to_dict(self):
        emp = Employee("Steve", "Wozniak")
        self.assertDictEqual(emp.to_dict(), {
            "f_name": "Steve",
            "l_name": "Wozniak"
        })

    def test_from_dict(self):
        emp = Employee.from_dict({
            "f_name": "Linus",
            "l_name": "Torvald"})
        self.assertEqual(emp.f_name, "Linus")
        self.assertEqual(emp.l_name, "Torvald")


class TestService(unittest.TestCase):
    def test_init(self):
        service = Service(100.)
        self.assertEqual(service.limit, 100.)
        self.assertEqual(service.balance, 0.)
        self.assertEqual(service.status, "application")

        service = Service(50., status="approved")
        self.assertEqual(service.limit, 50.)
        self.assertEqual(service.status, "approved")

        service = Service(25., account=Account("service", -250.))
        self.assertEqual(service.limit, 25.)
        self.assertEqual(service.balance, -250.)

        with self.assertRaises(ValueError):
            Service(-100.)

    def test_approve(self):
        service = Service(150.)
        service.approve()
        self.assertEqual(service.status, "approved")

    def test_collect(self):
        acct = Account("checking", 200.)
        service_account = Account("service", -150)
        service = Service(100., service_account, "approved")
        service.collect(100., acct)

        self.assertEqual(acct.balance, 100.)
        self.assertEqual(service.balance, -50.)

        with self.assertRaises(RuntimeError):
            service.collect(101., acct)
        self.assertEqual(acct.balance, 100.)
        self.assertEqual(service.balance, -50.)

        with self.assertRaises(RuntimeError):
            service = Service(100, status="application")
            service.collect(1, acct)
        self.assertEqual(acct.balance, 100.)

    def test_lend(self):
        acct = Account("checking", 10.)
        service_account = Account("service", 0.)
        service = Service(100., service_account, "approved")

        service.lend(50., acct)
        self.assertEqual(acct.balance, 60.)
        self.assertEqual(service.balance, -50.)

        service.lend(50., acct)
        self.assertEqual(acct.balance, 110.)
        self.assertEqual(service.balance, -100.)

        with self.assertRaises(ValueError):
            service.lend(50., acct)
        self.assertEqual(acct.balance, 110.)
        self.assertEqual(service.balance, -100.)

        with self.assertRaises(RuntimeError):
            service = Service(50., status="application")
            service.lend(25., acct)
        self.assertEqual(acct.balance, 110.)

    def test_to_dict(self):
        acct = Account("service", -20)
        service = Service(20, acct, "approved")
        self.assertDictEqual(service.to_dict(), {
            "account": acct.to_dict(),
            "limit": 20,
            "status": "approved"
        })

    def test_from_dict(self):
        acct = Account("service", -20)
        service = Service.from_dict({
            "account": acct.to_dict(),
            "limit": 20,
            "status": "approved"
        })
        self.assertEqual(service.limit, 20)
        self.assertEqual(service.balance, -20)
        self.assertEqual(service.status, "approved")

        acct = Account("service", 0)
        service = Service.from_dict({
            "account": acct.to_dict(),
            "limit": 100,
            "status": "application"
        })
        self.assertEqual(service.limit, 100)
        self.assertEqual(service.balance, 0)
        self.assertEqual(service.status, "application")


class TestCustomer(unittest.TestCase):
    def test_init(self):
        cust0 = Customer("Albert", "Einstien", "1 Zurich Place")
        self.assertEqual(cust0.f_name, "Albert")
        self.assertEqual(cust0.l_name, "Einstien")
        self.assertEqual(cust0.address, "1 Zurich Place")
        self.assertEqual(cust0.accounts, [])
        self.assertEqual(cust0.services, [])

        acct = Account("checking", 1.)
        cust1 = Customer("Stephen", "Hawking",
                         "1 Prince Mews", accounts=[acct])
        self.assertEqual(cust1.f_name, "Stephen")
        self.assertEqual(cust1.l_name, "Hawking")
        self.assertEqual(cust1.address, "1 Prince Mews")
        self.assertEqual(len(cust1.accounts), 1)
        self.assertEqual(cust1.accounts[0].type, "checking")
        self.assertEqual(cust1.accounts[0].balance, 1.)
        self.assertEqual(cust1.services, [])

        service = Service(100., Account("service", 0), "approved")
        cust2 = Customer("Carl", "Sagan", "1 Main Street", services=[service])
        self.assertEqual(cust2.f_name, "Carl")
        self.assertEqual(cust2.l_name, "Sagan")
        self.assertEqual(cust2.address, "1 Main Street")
        self.assertEqual(cust2.accounts, [])
        self.assertEqual(len(cust2.services), 1)
        self.assertEqual(cust2.services[0].limit, 100)
        self.assertEqual(cust2.services[0].balance, 0)
        self.assertEqual(cust2.services[0].status, "approved")

    def test_total_balance(self):
        acct = Account("checking", 0)
        service = Service(100)
        cust = Customer("Alex", "Trebek", "1 Jeopardy! Ave", [acct], [service])
        self.assertEqual(cust.total_balance, 0)

        acct = Account("checking", 100)
        service = Service(100)
        cust = Customer("Steve", "Harvey", "1 Family Affiars Highway", [acct], [service])
        self.assertEqual(cust.total_balance, 100)

        acct = Account("checking", 0)
        service_account = Account("service", -100)
        service = Service(100, service_account, status="approved")
        cust = Customer("Pat", "Sajak", "1 Wheel Way", [acct], [service])
        self.assertEqual(cust.total_balance, -100)


    def test_to_dict(self):
        acct = Account("checking", 0)
        service = Service(100)
        cust = Customer("Jeremy", "Clarkson",
                        "1 Diddly Squat Road", [acct], [service])
        self.assertDictEqual(cust.to_dict(),
                             {
            "f_name": "Jeremy",
            "l_name": "Clarkson",
            "address": "1 Diddly Squat Road",
            "accounts": [acct.to_dict()],
            "services": [service.to_dict()]
        })

    def test_from_dict(self):
        acct = Account("checking", 1.)
        service = Service(100., Account("service", 0), "approved")
        cust = Customer.from_dict({
            "f_name": "Richard",
            "l_name": "Hammond",
            "address": "1 Trekking Way",
            "accounts": [acct.to_dict()],
            "services": [service.to_dict()]
        })

        self.assertEqual(cust.f_name, "Richard")
        self.assertEqual(cust.l_name, "Hammond")
        self.assertEqual(cust.address, "1 Trekking Way")
        self.assertEqual(len(cust.accounts), 1.)
        self.assertEqual(cust.accounts[0].type, "checking")
        self.assertEqual(cust.accounts[0].balance, 1.)
        self.assertEqual(len(cust.services), 1.)
        self.assertEqual(cust.services[0].limit, 100.)
        self.assertEqual(cust.services[0].balance, 0.)
        self.assertEqual(cust.services[0].status, "approved")


class TestStorage(unittest.TestCase):
    def test_init(self):
        storage = Storage("test.json")
        self.assertEqual(storage.path, "test.json")

    def test_read_in(self):
        with open("tests/test_read.json", "w") as file:
            json.dump({
                "customers": [{
                    "f_name": "James",
                    "l_name": "May",
                    "address": "1 Downing Street",
                    "accounts": [{
                        "type": "checking",
                        "balance": 10.
                    }],
                    "services": [{
                        "limit": 100,
                        "account": {
                            "type": "service",
                            "balance": 0
                        },
                        "status": "approved"
                    }]
                }],
                "employees": [{
                    "f_name": "Richard",
                    "l_name": "Feynman"
                }],
                "globals": {"test": True}
            },
                file)

        storage = Storage("tests/test_read.json")
        storage.read_in()
        self.assertEqual(len(storage.customers), 1)
        self.assertEqual(storage.customers[0].f_name, "James")
        self.assertEqual(storage.customers[0].l_name, "May")
        self.assertEqual(storage.customers[0].address, "1 Downing Street")
        self.assertEqual(len(storage.customers[0].accounts), 1)
        self.assertEqual(storage.customers[0].accounts[0].type, "checking")
        self.assertEqual(storage.customers[0].accounts[0].balance, 10)
        self.assertEqual(len(storage.customers[0].services), 1)
        self.assertEqual(storage.customers[0].services[0].limit, 100)
        self.assertEqual(storage.customers[0].services[0].balance, 0)
        self.assertEqual(storage.customers[0].services[0].status, "approved")

        with self.assertRaises(FileNotFoundError):
            Storage("tests/test_missing_file.json").read_in()

    def test_write_out(self):
        storage = Storage("tests/test_write.json")
        acct = Account("checking", 10.)
        service = Service(100, Account("service", 0), "approved")
        cust = Customer("James", "May", "1 Downing Street", [acct], [service])
        emp = Employee("Richard", "Feynman")
        storage.customers = [cust]
        storage.employees = [emp]
        storage.globals = {"test": True}
        storage.write_out()

        with open("tests/test_write.json", "r") as file:
            self.assertDictEqual(json.load(file), {
                "customers": [{
                                 "f_name": "James",
                                 "l_name": "May",
                                 "address": "1 Downing Street",
                                 "accounts": [{
                                     "type": "checking",
                                     "balance": 10.
                                 }],
                                 "services": [{
                                     "limit": 100,
                                     "account": {
                                         "type": "service",
                                         "balance": 0
                                     },
                                     "status": "approved"
                                 }]
                                 }],
                "employees": [{
                    "f_name": "Richard",
                    "l_name": "Feynman"
                }],
                "globals": {"test": True}
            }
            )

        with self.assertRaises(OSError):
            Storage("/root/test.json").write_out()
