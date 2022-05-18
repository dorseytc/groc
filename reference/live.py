import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

def main():
  style.use('fivethirtyeight')
  fig = plt.figure()
  ax1 = fig.add_subplot(1,3,1)
  ax1.set_title('Happy')
  ax2 = fig.add_subplot(1,3,2)
  ax2.set_title('Lonely')
  ax3 = fig.add_subplot(1,3,3)
  ax3.set_title('Crowded')

  def animate(i):
    graph_data = open('example.txt', 'r').read()
    lines = graph_data.split('\n')
    xs = []
    y1s = []
    y2s = []
    y3s = []
    for line in lines:
      if len(line) > 1:
        x, y1, y2, y3  = line.split(',')
        xs.append(float(x))
        y1s.append(float(y1))
        y2s.append(float(y2)) 
        y3s.append(float(y3))
    ax1.clear()
    ax1.set_title('Happy')
    ax1.plot(xs, y1s)
    ax2.clear()
    ax2.set_title('Lonely')
    ax2.plot(xs, y2s)
    ax3.clear()
    ax3.set_title('Crowded')
    ax3.plot(xs, y3s)
    print(i)

  ani = animation.FuncAnimation(fig, animate, interval=1000)
  plt.show()


if __name__ == '__main__':
  main()
