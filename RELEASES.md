## Release Notes

### death (v0.13.0) -- not started
- hitpoints are calculated
- starvation can occur, but slowly
- grocs can carry food to grocs 
- burial ritual?

### dance (v0.12.0) -- completed
- groc, food, world on-screen inspection gauge
- sundown ritual
- better survival of dark and cold
- global settings.py file for behavior configuration

### order (v0.11.0) -- completed
- world, groc, and food class get their own files 
- pipe renderer gets feature parity 
- cold, sleeping and eating moods
- Air and Ground Temperature
- groc highlight on-screen groc details
- groc highlight with target painting for clarity

### light (v0.10.0) -- completed
- food shall spawn in the day
- grocs shall huddle for warmth at night
- vision is limited at night
- starvation shall take longer
- food shall sustain grocs longer

### tick (v0.9.0) -- complete

- the World shall tick, and all things shall proceed from there
- the main() loop shall be simplified further
- Food shall have tick
- World shall have tick
- Groc shall have observe/decide/act
- Genetic metabolism factors - randomized
- Genetic eating factors - randomized
- Variable food value - randomized

### hunger (v0.8.0) -- complete
 
- HUNGRY as a state of being
- Food as a class of item in the World
- Food Points and Calories
- Genetic metabolism factors (constant for now but easily randomizable)
- Genetic eating factors (constant for now but easily randomizable)
- Variable food value (constant for now but easily randomizable)

### uno (v0.7.0) -- complete

- no more pipe; all in one file? 

### shakers (v0.6.0) -- complete

- mood indicators in render ui
- demographic stats by mood
- click to id a groc

### movers (v0.5.0) -- complete

- randomize direction
- add overcrowding motivator
- gender based decision ai 

### auto (v0.4.0) -- complete

- behavior/motion/motivation moved to Groc class
- fix Groc/World interaction regarding movement
- add birthTick (groc world time)
- remove birthdatetime (gregorian)
- add gender
- augment groc.dat file format

### world (v0.3.0) -- complete

- separate Groc class and World class
- import Groc (into World)
- environment/movement/location moved to World class

### brown (v0.2.0) -- complete

- replace brownian movement with groc-seeking-groc behavior
- parameterize 


---


### future features
- variable speed
- gender-based companionship preference
- reproduction
