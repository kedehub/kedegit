import logging

CODE_BASE_ERROR = 1
CODE_ALREADY_EXISTS_ERROR = 2
CODE_BAD_FILE_FORMAT_ERROR = 3
CODE_DATABASE_ERROR = 4
CODE_INVALID_DATE_ERROR = 5
CODE_INVALID_FORMAT_ERROR = 6
CODE_LOAD_ERROR = 7
CODE_MATCHER_NOT_SUPPORTED_ERROR = 8
CODE_NOT_FOUND_ERROR = 9
CODE_VALUE_ERROR = 10
CODE_DATABASE_EXISTS = 11


logger = logging.getLogger(__name__)


class BaseError(Exception):
    """Base class error.
    Derived classes can overwrite error message declaring 'message' property.
    """
    message = "Unknown error"
    code = CODE_BASE_ERROR

    def __init__(self, **kwargs):
        super(BaseError, self).__init__(kwargs)
        self.msg = self.message % kwargs

    def __str__(self):
        return self.msg

    def __int__(self):
        return self.code


class AlreadyExistsError(BaseError):
    """Exception raised when an entity already exists in the registry"""

    message = "%(entity)s '%(eid)s' already exists in the registry"
    code = CODE_ALREADY_EXISTS_ERROR

    def __init__(self, **kwargs):
        self.entity = kwargs['entity']
        self.eid = kwargs['eid']
        super(AlreadyExistsError, self).__init__(**kwargs)


class BadFileFormatError(BaseError):
    """Exception raised when an input file does not have the expected format"""

    message = "%(cause)s"
    code = CODE_BAD_FILE_FORMAT_ERROR


class DatabaseError(BaseError):
    """Exception raised when a database error occurs"""

    message = "%(error)s (err: %(code)s)"
    code = CODE_DATABASE_EXISTS


class DatabaseExists(BaseError):
    """Exception raised when trying to create a database and it already exists"""

    message = "%(error)s (err: %(code)s)"
    code = CODE_DATABASE_EXISTS


class InvalidDateError(BaseError):
    """Exception raised when a date is invalid"""

    message = "%(date)s is not a valid date"
    code = CODE_INVALID_DATE_ERROR


class InvalidFormatError(BaseError):
    """Exception raised when a format is invalid"""

    message = "%(cause)s"
    code = CODE_INVALID_FORMAT_ERROR


class LoadError(BaseError):
    """Exception raised when an error occurs loading data"""

    message = "%(cause)s"
    code = CODE_LOAD_ERROR


class MatcherNotSupportedError(BaseError):
    """Exception raised when an identity matcher is not supported"""

    message = "%(matcher)s identity matcher is not supported"
    code = CODE_MATCHER_NOT_SUPPORTED_ERROR


class NotFoundError(BaseError):
    """Exception raised when an entity is not found in the registry"""

    message = "%(entity)s not found in the registry"
    code = CODE_NOT_FOUND_ERROR


class InvalidValueError(ValueError):
    """Exception InvalidValueError is a normal ValueError with code support"""

    code = CODE_VALUE_ERROR