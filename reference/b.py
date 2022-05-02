
print("This is b")

class Bbb ():
    'Base class for Bbb'
     
    def __init__(self, pa, pb):
        
        super(Bbb, self).__init__()
        
        self.a = pa
        self.b = pb

    def tell(self):
        return (self.a, self.b)
