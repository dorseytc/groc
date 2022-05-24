print("This is fun")
import random
def main():
  i = 0
  perc = 0
  bina = 0
  for i in range(100):
    random.seed(i + perc + bina)
    perc = random.randint(1,100)
    bina = random.randint(1,2)
    #print("Percentile ", perc)
    print(" Binary ", bina)
if __name__ == '__main__':
    main()
