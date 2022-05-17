# reference

## reference implementations of various elements


### class file implementation reference

- a.py
   - a imports, instantiates b 
- b.py
   - defines class b, designed to be imported


### pipes
 
- getpipe.py
   - reads characters from a pipe
   - parses messages separated by newline
- putpipe.py
   - writes messages to a pipe

  
### charts

- plot.py
   - uses matplotlib pyplot to display a static graph
   - nice looking graph but static
- gauge.py
   - uses pygame to display a clunky line chart comprised of dots
   - ugly; the other options are more elegant
- live.py
   - uses matplotlib.pyplot and matplotlib.animation
   - creates dynamic graphs 
   - will be used to render STAT gauges in groc
