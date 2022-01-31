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
