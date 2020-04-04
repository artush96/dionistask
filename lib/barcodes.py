# from lib.errors import HTTPBadRequest
#
# # Python 3
# try:
#     reduce
# except NameError:
#     from functools import reduce
#
#
# def calculate_checksum(code):
#     def sum_(x, y): return int(x) + int(y)
#
#     evensum = reduce(sum_, code[-2::-2])
#     oddsum = reduce(sum_, code[-1::-2])
#     return (10 - ((evensum + oddsum * 3) % 10)) % 10
#
#
# def validate_ean13(code) -> bool:
#     code = str(code)
#     if len(code) != 13 or code.isdigit() is False:
#         return False
#     else:
#         number = code[0:12]
#         number_with_checksum = code[0:13]
#         ean13 = number + str(calculate_checksum(number))
#         if ean13 != number_with_checksum:
#             return False
#
#     return True
#
#
# def validate_ean13_or_400(code) -> None:
#     if validate_ean13(code) is False:
#         raise HTTPBadRequest(description={
#             "error_code": 300,
#             "error_message": "Ошибка валидации кода"
#         })
