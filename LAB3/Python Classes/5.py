class Account:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
        else:
            print("Not enough funds!")

acc = Account("Ergazy", 100)

print(acc.owner, acc.balance)  
acc.deposit(50)
print(acc.balance)           
acc.withdraw(70)
print(acc.balance)             
acc.withdraw(200)              
print(acc.balance)             
