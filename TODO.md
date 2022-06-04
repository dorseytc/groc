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
  - done (tick)
- Food restores food points
  - done (tick)
- Genetic factors affect metabolism
  - done (tick)
- Genetic factors affect eating
  - done (tick)
- Random food value (calories)
  - done (tick)
- starvation should be more rare
- metabolism and hunger should be adjusted to support day/night cycle

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

### light
- food might spawn during the day
- grocs might have limited vision at night
- grocs would need to have enough stamina to withstand a nightly fast

### render
- pygame and debug scripts
  - done (world)
- leverage World constants
  - done (world)
- encapsulate pipe complexity 
  - done (movers)
