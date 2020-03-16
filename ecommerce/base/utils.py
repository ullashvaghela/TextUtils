from rest_framework.views import exception_handler
from bson.int64 import long

def base36encode(number, alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
    """
    Converts an integer to a base36 string.
    """

    if not isinstance(number, (int, long)):
        raise TypeError('number must be an integer')

    base36 = ''
    sign = ''

    if number < 0:
        sign = '-'
        number = -number

    if 0 <= number < len(alphabet):
        return sign + alphabet[number]

    while number != 0:
        number, i = divmod(number, len(alphabet))
        base36 = alphabet[i] + base36

    return sign + base36


def base36decode(number):
    """
    Converts a base36 string to integer.
    """

    return int(number, 36)



# def custom_exception_handler(exc, context):
#     # Call REST framework's default exception handler first,
#     # to get the standard error response.
#     response = exception_handler(exc, context)

#     if response is not None:
#         # check if exception has dict items
#         if hasattr(exc.detail, 'items'):
#             # remove the initial value
#             response.data = {}
#             errors = []
#             for key, value in exc.detail.items():
#                 # append errors into the list
#                 errors.append("{} : {}".format(key, " ".join(value)))
            
#             # add property errors to the response
#             response.data['errors'] = errors

#         # serve status code in the response
#         response.data['status_code'] = response.status_code

#     return response
