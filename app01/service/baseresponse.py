class BaseRespose:

    def __init__(self,error = None,data=None,code = 1000):
        self.error = error
        self.data = data
        self.code = code
    @property
    def dic(self):
        return self.__dict__