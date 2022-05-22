# groc

## to run, try something like 

python3 run.py 

### FYI

- The full syntax of run.py includes optional positional parameters
  - python3 run.py number-of-grocs number-of-iterations filename \

- start the world first with run.py


### Renderer grr\_pipe
- if prompted by the renderer you are using
- run one of the world renderers next:
   - pr\_pygame.py
   - pr\_text.py

### Supporting Files

The files present in this project are:
- grocfile.dat - saves the grocs when the world isn't running
- groc.py - the core classes World, Groc
- .world.dat - stores the number of iterations since the world began

#### the Renderers
- grr\_pyg.py 
  - the groc renderer using pygame
  - direct write requires no pipe reader
- grr\_pipe.py 
  - the groc renderer using a pipe
  - requires the use of a pipe reader

#### the Pipe Readers
- pr\_pygame.py - pygame-based render engine using grr\_pipe renderer
- pr\_text.py - text based "render" engine for debugging

  
### See Also

- README.md - this document
- RELEASES.md - a compilation of features in each release
- TODO.md - a list of planned enhancements
