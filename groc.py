package grox;
public class Groc {

private String myName;
private int myId;
private String myColor;
private String myMood;
private boolean isLiving;
private int myAddress;
private int currentLocation;
private int targetLocation;
private boolean inConversation;
private int conversingWith;
private boolean wanderingUp = true;

private static int totalPopulation;



public Groc(String startName, String startColor, String startMood, int startAddress, int startId) {
myName = startName;
myId = startId;
myColor = startColor;
myMood = startMood;
myAddress = startAddress;
currentLocation = startAddress;
targetLocation = startAddress;
City.registerOccupant(myId, myAddress);
totalPopulation++;
isLiving = true; // all Grocs are born alive
}


public boolean isAtHome() {
if (myAddress == currentLocation) {
return true;
} else
{ return false;
}
}

public boolean isMoving() {
if (targetLocation == currentLocation) {
return false;
} else
{ return true;
}
}

public String getColor() {
return myColor;
}

public static int getTotalPopulation() {
return totalPopulation;
}

public String getName() {
return myName;
}

public int getId() {
return myId;
}

public String getMood() {
return myMood;
}

public int getAddress() {
return myAddress;
}

public boolean getIsLiving() {
return isLiving;
}

public void setMood(String newMood) {
myMood = newMood;
}

public void kill() {
isLiving = false;
System.out.println("Groc: " + myName + " dies");
myMood = "Unknown";
}

public void introduce () {
if (isLiving) {
System.out.println("Groc: Hi! My name is " + myName);
System.out.println("I am " + myColor);
System.out.println("My address is " + Integer.toString(myAddress));
System.out.println("I am feeling " + myMood);
System.out.println("My id is " + Integer.toString(myId));
} else
{
System.out.println("Groc: No response");
}
}

public void move() {
int direction;
int startLocation = currentLocation;
int oneRow = City.getRows();
if (isMoving()) {
direction = City.getNextStep(currentLocation, targetLocation);
if (direction == City.NORTH) {
currentLocation = currentLocation - oneRow;
} else if (direction == City.SOUTH) {
currentLocation = currentLocation + oneRow;
} else if (direction == City.EAST) {
currentLocation++;
} else {
currentLocation--;
}
System.out.println("Groc: Moved from " + Integer.toString(startLocation));
System.out.println(" to " + Integer.toString(currentLocation));
} else
System.out.println("Groc: Got no place to go!");
}

public void relocate(int newAddress) {
int townSize = City.getSize();
if (townSize > newAddress) {
int oldAddress = myAddress;
System.out.println("Groc: Moving from " + Integer.toString(oldAddress)
+ " to " + Integer.toString(newAddress));
myAddress = newAddress;
targetLocation = newAddress;
City.registerOccupant(myId, newAddress);
City.deregisterOccupant(myId, oldAddress);
} else {
System.out.println("Groc: Won't move out of the city");
System.out.println("Staying at " + Integer.toString(myAddress));
}
}

public void visit(int newLocation) {
int townSize = City.getSize();
if (currentLocation == newLocation) {
System.out.println("Groc: Already at " + Integer.toString(newLocation));
} else if (townSize > newLocation) {
int oldLocation = currentLocation;
System.out.println("Groc: Leaving " + Integer.toString(oldLocation)
+ " to visit " + Integer.toString(newLocation));
targetLocation = newLocation;
} else {
System.out.println("Groc: Won't visit outside of the city");
System.out.println("Staying at " + Integer.toString(currentLocation));
}
}

public int findNeighbor() {
int neighborAddress = -1;
int neighborId = -1;
int[] occupantList;
for (int i=0; i<4; i++) {
System.out.println("Looking " + City.getDirectionName(i));
if (neighborId == -1) {
System.out.println("Haven't found a neighbor yet");
if (neighborAddress == -1) {
System.out.println("Haven't found a neighboring address yet");
neighborAddress = City.getNeighboringAddress(myAddress, i);
if ( neighborAddress > -1) {
System.out.println("Found a neighboring address of " + Integer.toString(neighborAddress));
if (City.getOccupancy(neighborAddress) > 0) {
occupantList = City.getOccupantList(neighborAddress);
neighborId = occupantList[1];
} else {
System.out.println("No one lives at " + Integer.toString(neighborAddress) + " so keep looking");
neighborAddress = -1;
}

}
}
}
}
if (neighborId == -1) {
System.out.println("Groc: No neighbor found");
} else
{
System.out.println("Groc: " + myName + " has a neighbor at " + Integer.toString(neighborId));
}
return neighborId;
}

public void doSomething() {
if (isMoving()) {
move();
} else
{
int neighbor;
neighbor = findNeighbor();
if (neighbor == -1) {
wander();
} else {
sendMessage(neighbor, "Hi, neighbor");
}
}
}

public void wander() {
int citySize = City.getSize();
if (wanderingUp) {
System.out.println("Wandering Up");
targetLocation++;
if (targetLocation > citySize) {
wanderingUp = false;
targetLocation = targetLocation - 2;
}
} else
System.out.println("Wandering Down");
targetLocation--;
if (targetLocation < 0) {
wanderingUp = true;
targetLocation = 2;
}
System.out.println("Groc: Wandering to " + Integer.toString(targetLocation));

}

public void sendMessage(int recipient, String myMessage) {
Message theMessage;
theMessage = new Message(myId, recipient, myMessage);
}

public void examine () {
if (isLiving) {
System.out.println("Groc: How rude!");
myMood = "Irritated";
} else
{
System.out.println("Groc: Subject is " + myColor);
System.out.println("Subject's address is " + Integer.toString(myAddress));
System.out.println("Subject's name was " + myName);
System.out.println("Subject's id was " + Integer.toString(myId));
}
}

} 