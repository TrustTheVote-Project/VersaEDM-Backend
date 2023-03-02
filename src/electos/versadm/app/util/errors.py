import abc


class CustomException(abc.ABC, Exception):
    """
    Abstract base class for custom exceptions for this application.
    """
    # noinspection PyPropertyDefinition
    @classmethod
    @property
    @abc.abstractmethod
    def error_code(cls):
        raise NotImplementedError()


class ReferentialIntegrityError(CustomException):
    """
    Raised when an attempt is made to store an object with invalid references to other objects.
    """
    error_code = 'ref-integrity'


class DuplicateObjectError(CustomException):
    """
    Raised when an attempt is made to store an object with an id that is already in use by another object.
    """
    error_code = 'duplicate-obj'
