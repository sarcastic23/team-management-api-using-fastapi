class BankAccount:
    
    accnums=["123456789","24681012"]  #sample data for program checking..
    
    
    def __init__(self):
        self.__accnum=None   #initialiazing assuming only acc num and amt is necessary
        self.__amt=0
        
        
        
    @property
    def accnum(self):
        if self.__accnum is None:
            return 0                                #not letting user access the accnum by converting mdl str to x
        s=self.__accnum
        masked = s[:2] + "x" * (len(s) - 4) + s[-2:]
        return masked

    @accnum.setter
    def accnum(self,accnum):
        if accnum in self.accnums:
            raise ValueError("already exists")       #setting accnum, checking if it exist in sample data ie accnums
        else:
            
            self.accnums.append(accnum)
            self.__accnum=accnum
            
    @property
    def amt(self):
        if self.__amt is None:
            return 0
        return self.__amt
    @amt.setter
    def amt(self,amt):
        if amt<0 or amt>999999:
            raise ValueError("not expected value")
        else:
            self.__amt=amt
    def withdraw(self,amt):
        if self.__amt<=amt:
            print(f"this much amt is deducted which was total in bank acc {self.amt} and unable to load {amt-self.amt}")
            self.__amt=0
            return self.__amt
        else:
            print(f"this much amt is loaded {amt}")
            self.__amt-=amt
            return self.__amt
            
            
            
x=BankAccount()
x.accnum="1234567"
print(x.accnum)
x.accnum="24681012"
print(x.accnum)

        
    
    
    
    
    
    
        
        
