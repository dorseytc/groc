print("This is fun")
import b

class Aaa ():
    'Base class for Aaa'
     
    def __init__(self, pa, pb):
        
        super(Aaa, self).__init__()
        
        self.a = pa
        self.b = pb

    def tell(self):
        return (self.a, self.b)

def main():
  print("Hello main")
  aaa = Aaa(4,5)
  print(aaa.tell())
  bbb = b.Bbb(7,8)
  print(bbb.tell())

if __name__ == '__main__':
    main()
