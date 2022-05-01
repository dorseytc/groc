# groc

## to run, try something like 

python3 groc.py \
python3 w-flat.py

### FYI

- start the grocs first with groc.py
- run one of the world generators next:
   - w-debug.py 
   - w-flat.py
  

## Releases

### brown (v0.2.0) -- complete

- replace brownian movement with groc-seeking-groc behavior
- parameterize 

### world (v0.3.0) -- in progress

- separate Groc class and World class
- import Groc (into World)
- behavior/motion/motivation moved to Groc class
- environment/movement/location moved to World class


## wish list
 
### movement

- "movement" should be part of the Groc class
- "movement" should be based on motivation
- "nearest Groc" should be told to the Groc by the World
- variable speed could be introduced
- approach direction could be randomized

### motivation
- "motivation" should include companionship, food, space (overcrowding)
- age should be determined by ticks
- hunger should be based on ticks since food
- need for companionship vs need for space should be randomized

### predators
- could be expressed as "species"
- predators might eat prey
- prey might band together to fight predators

### mood
- color might indicate mood or health
- color might indicate age
- health might be affected by food, companionship, mating

### death
- death might occur of old age, starvation, predation
