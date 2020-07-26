class Waterfall:
    pass

class Cascade(Exception):
    def _errormessage(self, error):
        return "A Cascade has occured while executing this Waterfall\n{}".format(error)

class EconomyHandler:
    class Success(Waterfall):
        def __str__(self):
            return "Operation was a success"
    class Errors:
        class ShopAlreadyExists(Cascade):
            def __str__(self):
                return self._errormessage("This shop already exists")
        class ShopItemLimitReached(Cascade):
            def __str__(self):
                return self._errormessage("The maximum amount of items has been reached for this shop")
