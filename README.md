# groc

## to run, try something like 

python3 run.py \
python3 render.py

### FYI

- The full syntax of run.py includes optional positional parameters
  - python3 run.py number-of-grocs number-of-iterations filename \

- start the world first with run.py
- run one of the world renderers next:
   - render.py
   - render-d.py

### Supporting Files

The files present in this project are:
- grocfile.dat - saves the grocs when the world isn't running
- groc.py - the core classes World, Groc
- render.py - pygame-based render engine
- render-d.py - text based "render" engine for debugging
- run.py - launches the world, spawns grocs, and loops N iterations
- .world.dat - stores the number of iterations since the world began

  
### See Also

- README.md - this document
- RELEASES.md - a compilation of features in each release
- TODO.md - a list of planned enhancements
