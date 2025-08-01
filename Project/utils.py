class Calculator():
    def __init__(self):
        pass

    def addition(self,a,b):
        return a + b
    
    def substraction(self,a,b):
        return a -  b
    
    def multiplication(self,a,b):
        return a * b
    
    def division(self, a, b):
        if b == 0:
            return "Error: Division by zero"
        sub = a / b
        return sub
        
    def power(self,a,b):
        return a ** b
    
