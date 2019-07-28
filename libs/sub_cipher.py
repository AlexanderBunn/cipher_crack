import random
from pycipher import SimpleSubstitution

class SubCipher():
    def gen_key(self, loop=None):
        if loop == None:
            loop = random.randint(0, 10)
        k = list('abcdefghijklmnopqrstuvwxyz')
        for swap in range(loop):
            i = random.randint(0, 25)
            j = random.randint(0, 25)
            t = k[i]
            k[i] = k[j]
            k[j] = t
        key = ''.join(k)
        return key

    def encipher(self, key, text):
        return SimpleSubstitution(key).encipher(text, True)

    def decipher(self, key, text):
        return SimpleSubstitution(key).decipher(text, True)
