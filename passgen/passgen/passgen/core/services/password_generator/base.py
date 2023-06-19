import secrets
from string import ascii_letters, digits
from passgen.core.entities import PasswordSpec
from passgen.core.services.base import PasswordGeneratorService
special = "!#$%&()*+-<=>?@^{}"


class PasswordGeneratorServiceImpl(PasswordGeneratorService):
    def __init__(self):
        pass

    @staticmethod
    def _get_charset(spec: PasswordSpec) -> str:
        charset = ""
        if spec.use_ascii:
            charset += ascii_letters
        if spec.use_digits:
            charset += digits
        if spec.use_special:
            charset += special
        return charset

    def generate(self, spec: PasswordSpec) -> str:
        charset = self._get_charset(spec)
        password = "".join(secrets.choice(charset) for _ in range(spec.length))
        return password
