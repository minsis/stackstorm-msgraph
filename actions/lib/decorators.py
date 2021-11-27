def requires_account(func):
    """
    Validates that an account has been defined. If not,
        then attempt to define one from 'default' account
    """
    def wrapper(self, *args, **kwargs):
        if not self.account:
            self.account = self.get_account()
        return func(*args, **kwargs)
    return wrapper
