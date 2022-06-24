## planned features
 
### movement
[x] - movement should be part of the Groc class - done (brown)
[x] - movement should be based on motivation - done (movers)
[x] - movement - approach direction could be randomized - done (movers)
[ ] - movement - variable speed could be introduced - started (movers)

### motivation
[x] - motivation should include companionship - LONELY done (shakers)
[x] - motivation should include space - CROWDED done (shakers)
[x] - motivation should include food - HUNGRY done (hunger, tick)
[x] - motivation - "nearest Groc" told to Groc by World - done (world)
[ ] - need for companionship/space should be randomized - not started

### food
[x] - Food appears randomly
[x] - Food - HUNGRY might override CROWDED - 
[x] - Food - HUNGRY grocs might ignoring CROWDED conditions 
[x] - Food - once sated, grocs might flee crowds - done (tick)
[x] - Food restores food points - done (tick)
[x] - Food - hunger should be based on food points - done (hunger, tick)
[x] - Food - Genetic factors affect metabolism - done (tick)
[x] - Food - Genetic factors affect eating - done (tick)
[x] - Food - Random food value (calories) - done (tick)
[x] - Food - starvation should be more rare - done (light)
[x] - Food - metabolism/hunger support day/night cycle - done (light)

### predators
[ ] - predators could be expressed as "species"
[ ] - predators might eat prey
[ ] - predators prey might band together to fight predators

### mood
[x] - mood - eye color indicates mood or health - done (shakers)

### health
[x] - health - age should be determined by ticks - done (auto)
[ ] - health - color might indicate age - not started
[ ] - health might be affected by food - not started
[ ] - health might be affected by companionship - not started
[ ] - health might be affected by mating - not started

### death
[ ] - death might occur of old age - not started
[x] - death might occur of starvation - completed (hunger)
[ ] - death might occur of predation - not started

### light
[x] - light - food might spawn during the day - done (light)
[x] - light - grocs might have limited vision at night - done (light)
[x] - light - grocs have enough stamina for a nightly fast - done (light)

### render
[x] - pygame and debug scripts - done (world)
[x] - leverage World constants - done (world)
[x] - encapsulate pipe complexity - done (movers)
[ ] - 

### cold
[x] - Specific behaviors for cold
[x] - Light affects ground and air temperature

### spotlight
[x] - Click on groc to highlight, see stats (order)
[x] - Highlighted groc's target is displayed (order)

### rituals
[ ] - Sunset ritual to gather food and provide warmth
[ ] - Funeral ritual to bury the dead

