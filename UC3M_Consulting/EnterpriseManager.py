"""
Enterprise Manager module.
Enterprise Management custom exception module.
Handles enterprise data operations.
"""

import json
from .EnterpriseManagementException import EnterpriseManagementException
from .EnterpriseRequest import EnterpriseRequest


class EnterpriseManager:
    def __init__(self):
        pass

    def ValidateCIF(self, CiF):
        CiF = CiF.upper()
        if len(CiF) != 9:
            return False

        letter = CiF[0]
        number_block = CiF[1:8].rjust(7, '0')
        control_char = CiF[8]

        def sum_digits(n):
            return sum(int(d) for d in str(n))

        # Sum even positions (2nd, 4th, 6th)
        even_sum = sum(int(number_block[i]) for i in [1,3,5])
        # Sum odd positions (1st, 3rd, 5th, 7th) after doubling and summing digits
        odd_sum = sum(sum_digits(int(number_block[i]) * 2) for i in [0,2,4,6])
        total_sum = even_sum + odd_sum

        unit = total_sum % 10
        base_digit = 0 if unit == 0 else 10 - unit

        # Determine expected control character
        if letter in ['A','B','E','H']:
            expected_control = str(base_digit)
        elif letter in ['K','P','Q','S']:
            mapping = {0:'J',1:'A',2:'B',3:'C',4:'D',5:'E',6:'F',7:'G',8:'H',9:'I'}
            expected_control = mapping[base_digit]
        else:
            expected_control = str(base_digit)

        return control_char == expected_control

    def ReadproductcodefromJSON(self, fi):

        try:
            with open(fi, encoding="utf-8") as f:
                DATA = json.load(f)
        except FileNotFoundError as e:
            raise EnterpriseManagementException("Wrong file or file path") from e
        except json.JSONDecodeError as e:
            raise EnterpriseManagementException("JSON Decode Error - Wrong JSON Format") from e

        try:
            T_CIF = DATA["cif"]
            T_PHONE = DATA["phone"]
            E_NAME = DATA["enterprise_name"]
            req = EnterpriseRequest(T_CIF, T_PHONE, E_NAME)
        except KeyError as e:
            raise EnterpriseManagementException("JSON Decode Error - Invalid JSON Key") from e
        if not self.ValidateCIF(T_CIF):
            raise EnterpriseManagementException("Invalid FROM IBAN")
        return req

# Optional: quick test block
if __name__ == "__main__":
    manager = EnterpriseManager()

    valid_cif = "A58818501"
    invalid_cif = "B12345678"

    print(f"Validating {valid_cif}: {manager.ValidateCIF(valid_cif)}")   # True
    print(f"Validating {invalid_cif}: {manager.ValidateCIF(invalid_cif)}") # False
