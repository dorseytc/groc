# groc

## to run, try something like 

python3 groc.py 

### FYI

- The full syntax of groc.py includes optional positional parameters
- One of these lines will work best for you
  - python3 groc.py number-of-grocs number-of-iterations filename 
  - ./groc.py number-of-grocs number-of-iterations filename 

### Sample Syntax
- ./groc.py 100 0 
  - 100 grocs 
  - 0 means unlimited iterations
  - filename is omitted which means it uses the default grocfile.dat
- ./groc.py 10 10 testfile.dat
  - 10 grocs
  - limit to 10 iterations
  - use testfile.dat instead of grocfile.dat
- ./groc.py 
  - omit groc count, use default of 2
  - omit iteration limit, use default of 1000
  - omit filename, use default of grocfile.dat


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
- only required when using pipe-based renderer grr\_pipe
- pr\_pygame.py - pygame-based render engine 
- pr\_text.py - text based "render" engine for debugging

  
### See Also

- RELEASES.md - a compilation of features in each release
- TODO.md - a list of planned enhancements
