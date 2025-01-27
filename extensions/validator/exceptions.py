class DataValidationError(Exception):
    pass

class TypeValidationError(DataValidationError):
    pass

class ValueValidationError(DataValidationError):
    pass