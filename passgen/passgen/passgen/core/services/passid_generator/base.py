import secrets
import urllib.request as urequest
from passgen.core.entities import PassIdSpec
from passgen.core.services.base import PassIdGeneratorService
word_site = "https://www.mit.edu/~ecprice/wordlist.10000"


class PassIdGeneratorServiceImpl(PassIdGeneratorService):
    def __init__(self):
        resp = urequest.urlopen(word_site)
        txt = resp.read().decode('utf-8')
        self._words = txt.splitlines()

    def generate(self, spec: PassIdSpec) -> str:
        passid = " ".join(secrets.choice(self._words)
                          for _ in range(spec.length))
        return passid
