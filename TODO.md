## planned features
 
### movement

- "movement" should be part of the Groc class
  - done (brown)
- "movement" should be based on motivation
  - done (movers)
- "nearest Groc" should be told to the Groc by the World
  - done (world)
- variable speed could be introduced
  - started (movers)
- approach direction could be randomized
  - done (movers)

### motivation
- "motivation" should include companionship, food, space (overcrowding)
  - LONELY and CROWDED done (shakers)
  - HUNGRY started in (hunger)
- age should be determined by ticks
  - done (auto)
- hunger should be based on food points
  - started in (hunger)
- need for companionship vs need for space should be randomized
  - not started

### food

- Food appears randomly
- HUNGRY might override CROWDED
  - HUNGRY grocs might ignoring CROWDED conditions
  - once sated, grocs might flee crowds seeking HAPPY condition
- Food restores food points
- Genetic factors affect metabolism
- Genetic factors affect eating
- Random food value (calories)

### predators
  - not started
- could be expressed as "species"
- predators might eat prey
- prey might band together to fight predators

### mood
- eye color indicates mood or health
  - done (shakers)
- color might indicate age
  - not started
- health might be affected by food, companionship, mating
  - not started

### death
- death might occur of old age, starvation, predation
  - not started

### render
- pygame and debug scripts
  - done (world)
- leverage World constants
  - done (world)
- encapsulate pipe complexity 
  - done (movers)
