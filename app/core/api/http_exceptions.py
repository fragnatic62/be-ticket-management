from typing import Tuple


# This status code indicates that the server understands the content type of the request entity,
# and the syntax of the request is correct, but it was unable to process the contained instructions.
HTTP_CODE_422_EXCEPTION_LIST: Tuple = ()

# This status code means that the method could not be performed on the resource because the
# requested action depended on another action and that action failed.
HTTP_CODE_424_EXCEPTION_LIST: Tuple = ()

# This indicates that the server has encountered a situation it doesn't know how to handle
HTTP_CODE_500_EXCEPTION_LIST: Tuple = (
)
