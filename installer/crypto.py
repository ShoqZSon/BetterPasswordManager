from cryptography.fernet import Fernet

class Crypto:
    def __init__(self, password):
        self.__rawPassword = password
        self.__key = None
        self.__cipherSuite = None

    def encrypt(self):
        if self.__cipherSuite:
            return self.__cipherSuite.encrypt(self.__rawPassword.encode('utf-8'))
        else:
            print("cipher suite not found")

    def decrypt(self,password):
        if self.__cipherSuite:
            return self.__cipherSuite.decrypt(password)
        else:
            print("cipher suite not found")

    def generateKey(self):
        self.__key = Fernet.generate_key()

    def createCipherSuite(self):
        self.__cipherSuite = Fernet(self.__key)

    def getKey(self):
        return self.__key

    def setKey(self,key:bytes):
        self.__key = key