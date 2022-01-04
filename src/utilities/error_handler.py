"""Generic error handling module for the application."""
import traceback
import pytz
from merry import Merry
from werkzeug.exceptions import NotFound, BadRequest, MethodNotAllowed
from datetime import datetime
from flask import jsonify

ehandler = Merry()


def lookup_status_code(error):
    """Associate an exception with a status_code."""
    # default status_code
    status_code = 500

    if type(error) == MemoryError:
        status_code = 507
    elif type(error) == NotImplementedError:
        status_code = 501
    elif type(error) in [FileNotFoundError, NotFound]:
        status_code = 404
    elif type(error) == BadRequest:
        status_code = 400
    elif type(error) == MethodNotAllowed:
        status_code = 405

    return status_code


@ehandler._except(Exception)
def convert_error(err):
    """Convert all exceptions to standard error format.

    Args:
        e ([type])
    """
    if type(err) == ProxyAppError:
        # Avoid recursive error handling
        raise err

    raise ProxyAppError(
        message=f"{err}",
        status_code=lookup_status_code(err),
        error_type=err.__class__.__name__,
        tb=traceback.format_exc(-1),
    )


def generic_error_hanlder(raised_error):
    """Handle generic errors.

    Args:
        e ([type]): [description]
    """
    status_code: int = int()
    if type(raised_error) == ProxyAppError:
        response = raised_error.to_dict()
        status_code = raised_error.status_code
    else:
        response = {
            "error_type": raised_error.name,
            "message": (
                "The requested URL was not found on the server. "
                "If you entered the URL manually please check your spelling and try again."
            ),
            "status": raised_error.code,
            "timestamp": pytz.utc.localize(datetime.now()).strftime(
                "%Y-%m-%dT%H:%M:%S.%f%z"
            ),
        }
    response = jsonify(response)
    response.status_code = status_code if status_code else raised_error.code
    return response


class ProxyAppError(Exception):
    """Iitialize ProxyApp Standard Error Class for Exceptions."""

    status_code = 500
    date_format = "%Y-%m-%dT%H:%M:%S.%f%z"

    def __init__(self, message, status_code=None, error_type=None, tb=None):
        """Initialize the class."""
        super().__init__(self)
        self.error_type = error_type
        self.message = str(message)
        self.status_code = status_code if status_code else self.status_code
        self.traceback = tb if tb else traceback.format_exc(-1)

    def to_dict(self):
        """Return a dictionary representation of the error."""
        return {
            "error_type": self.error_type,
            "message": self.message,
            "status": self.status_code,
            "timestamp": pytz.utc.localize(datetime.now()).strftime(self.date_format),
            "traceback": self.traceback,
        }
