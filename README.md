# groc

## to run, try something like 

python3 run.py
./run.py

### FYI

- The full syntax of groc.py includes optional positional parameters
- One of these lines will work best for you
  - python3 run.py number-of-grocs number-of-iterations mode log-level 
  - ./run.py number-of-grocs number-of-iterations mode log-level 

- mode 
  - is either "LIFE" or "MOTION"
  - groc will keep running as long as there is "<mode>"
  - default is LIFE

- log-level
  - 00 = NOTSET
  - 10 = DEBUG
  - 20 = INFO
  - 30 = WARNING
  - 40 = ERROR
  - 50 = CRITICAL

### Sample Syntax
- ./groc.py 100 0 
  - 100 grocs 
  - 0 means unlimited iterations
- ./groc.py 10 10 
  - 10 grocs
  - limit to 10 iterations
- ./groc.py 
  - omit groc count, use default of 2
  - omit iteration limit, use default of 1000


### Renderer grr\_pipe
- if prompted by the renderer you are using
- run one of the world renderers next:
   - pr\_pygame.py
   - pr\_text.py

### Supporting Files

The files present in this project are:
- groc.py - the core classes World, Groc
- grocfile.dat - saves the grocs when the world isn't running
- food.py - the food class
- run.py - main loop to invoke the world
- settings.py - user-configurable settings
- world.dat - stores the number of iterations since the world began
- world.py - the world class, plus any helper functions

#### the Renderers
- grr\_pygame.py 
  - the groc renderer using pygame
  - direct write requires no pipe reader
- grr\_pipe.py 
  - the groc renderer using a pipe
  - requires the use of a pipe reader

#### the Pipe Readers
- only required when using pipe-based renderer grr\_pipe
- pr\_pygame.py - pygame-based render engine 
- pr\_text.py - text based "render" engine for debugging

  
### See Also

- RELEASES.md - a compilation of features in each release
- TODO.md - a list of planned enhancements
