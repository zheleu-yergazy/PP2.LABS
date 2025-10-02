class MyString:
    def __init__(self):
        self.s = ""        

    def getString(self):
        self.s = input("Введите строку: ")

    def printString(self):
        print(self.s.upper())



obj = MyString()     
obj.getString()      
obj.printString()    
