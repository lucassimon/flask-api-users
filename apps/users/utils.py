# Third

# Apps

# Local


def check_password_in_signup(password: str, confirm_password: str):

    if not password:
        return False

    if not confirm_password:
        return False

    if not password == confirm_password:
        return False

    return True

class Cpf:
    def __init__(self, cpf):
        self.cpf = cpf

    def validate(self):
        if self.check_len():
            return False

        first_digit = self.calculate_first_digit()
        if self.cpf[9] != str(first_digit):
            return False

        second_digit = self.calculate_second_digit()
        if self.cpf[10] != str(second_digit):
            return False

        return True

    def check_len(self):
        return len(self.cpf) != 11

    def calculate_first_digit(self):
        first_digit = 0
        for i in range(10, 1, -1):
            first_digit += int(self.cpf[10 - i]) * i

        rest = first_digit % 11

        return self.cpf_rule(rest)

    def calculate_second_digit(self):
        second_digit = 0
        for i in range(11, 1, -1):
            second_digit += int(self.cpf[11 - i]) * i

        rest = second_digit % 11

        return self.cpf_rule(rest)

    def cpf_rule(self, rest):
        if rest < 2:
            return 0
        else:
            return 11 - rest
