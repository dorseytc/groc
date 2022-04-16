city.txt
 class City

public class City {



private static int size;

private static int rows;

private static int columns;

private static int[][] census;



public static final int STOP = -1;

public static final int NORTH = 0;

public static final int SOUTH = 1;

public static final int EAST = 2;

public static final int WEST = 3;



public City (int startSize)

{

double sroot;

sroot = Math.sqrt(startSize);

rows = (int)sroot;

columns = (int)sroot;

size = rows * columns;

census = new int[startSize][startSize];

for (int i=0; i[startSize; i++) {

census[i][0] = 0; // the 0th element of the second dimension is #Occupants

}

System.out.println("City: Requested city size was " + Integer.toString(startSize));

System.out.println("Actual city size is " + Integer.toString(size));

}



public static int getRows() {

return rows;

}



public static String getDirectionName(int direction) {

String directionName = null;

if (direction == NORTH) {

directionName = "North";

} else if (direction == SOUTH) {

directionName = "South";

} else if (direction == EAST) {

directionName = "East";

} else if (direction == WEST) {

directionName = "West";

}

return directionName;

}



public static int getNeighboringAddress(int parcel, int direction) {

int neighbor = -1;

int remainder = -1;

if (direction == NORTH) {

neighbor = parcel - rows;

if (neighbor [ 0) {

neighbor = -1;

}

}

else if (direction == SOUTH) {

neighbor = parcel + rows;

if (neighbor ] size) {

neighbor = -1;

}

}

else if (direction == WEST) {

remainder = parcel % rows;

neighbor = parcel - 1;

if (remainder == 0) {

neighbor = -1;

}

}

else if (direction == EAST) {

neighbor = parcel + 1;

remainder = neighbor % rows;

if (remainder == 0) {

neighbor = -1;

}

}

System.out.println("City: The neighboring address of " + Integer.toString(parcel));

System.out.println("to the " + getDirectionName(direction) + " is " + Integer.toString(neighbor));

return neighbor;

}



public void expand (int additionalAddresses) {

double sroot;

int origSize = size;

int requestedSize = origSize + additionalAddresses;

sroot = Math.sqrt(requestedSize);

rows = (int)sroot;

columns = (int)sroot;

size = rows * columns;

System.out.println("City: Original city size was " + Integer.toString(origSize));

System.out.println("Requested expansion was " + Integer.toString(additionalAddresses) + " addresses");

System.out.println("Resulting city size is " + Integer.toString(size));





}



public static int getSize () {

return size;

}



public static int getNextStep (int currentLocation, int targetLocation) {

int nextStep;

int currCol = currentLocation % rows;

int targCol = targetLocation % rows;

if (currentLocation == targetLocation) {

nextStep = STOP;

} else {



if (targCol < currCol) {

nextStep = WEST;

} else if (targCol > currCol) {

nextStep = EAST;

} else // (targCol == currCol)

{

if (currentLocation > targetLocation) {

nextStep = NORTH;

} else

{ nextStep = SOUTH;

}

}

}

System.out.println("City: Current Location: " + Integer.toString(currentLocation));

System.out.println(" Target Location: " + Integer.toString(targetLocation));

System.out.println(" Current Column: " + Integer.toString(currCol));

System.out.println(" Target Column: " + Integer.toString(targCol));

return nextStep;

}



public static void registerOccupant(int grocId, int grocAddress) {

System.out.println("City: register " + Integer.toString(grocId) +

" at " + Integer.toString(grocAddress));



int numOccupants = census[grocAddress][0];

System.out.println("City: At " + Integer.toString(grocAddress) + " there were " + Integer.toString(numOccupants) + " Occupants");

census[grocAddress][++numOccupants] = grocId;

census[grocAddress][0] = numOccupants;

System.out.println("Now there are " + Integer.toString(numOccupants) + " Occupants");

}



public static void listOccupants(int grocAddress) {

int numOccupants = census[grocAddress][0];

System.out.println("City: Address " + Integer.toString(grocAddress) +

" has " + Integer.toString(numOccupants) + " occupants");

for (int i = 1; i
System.out.println("City: Occupant " + Integer.toString(i) +

" is " + Integer.toString(census[grocAddress][i]));

}



}



public static int[] getOccupantList(int grocAddress) {

return census[grocAddress];

}



public static int getOccupancy(int grocAddress) {

int numOccupants = census[grocAddress][0];

return numOccupants;

}



public static void deregisterOccupant(int grocId, int grocAddress) {

System.out.println("City: deregister " + Integer.toString(grocId) +

" from " + Integer.toString(grocAddress));



int numOccupants = census[grocAddress][0];

System.out.println("City: At " + Integer.toString(grocAddress)

+ " there were " + Integer.toString(numOccupants)

+ " Occupants");

boolean found = false;

int foundAt = 0;

if (numOccupants == 0 ) {

found = false;

} else {

for (int i = 1; i
if (census[grocAddress][i] == grocId) {

found = true;

foundAt = i;

}

}

if (found) {

for (int j = foundAt; j
census[grocAddress][j] = census[grocAddress][j+1];

}

census[grocAddress][0] = --numOccupants;

System.out.println("Found Occupant " + Integer.toString(grocId));

} else {

System.out.println(Integer.toString(grocId) + " not found at "

+ Integer.toString(grocAddress));

}

}

System.out.println("Now there are " + Integer.toString(census[grocAddress][0]) + " Occupants");



}



}
main.txt
 class Main
package grox;
public class Main {

public static void main(String[] args) {
// TODO code application logic here


System.out.println("Hello World");
City metropolis = new City(100);

Groc alphaGroc[] = new Groc[10];
for (int i = 0; i<10; i++) {
alphaGroc[i] = new Groc("Alpha " + Integer.toString(i), "Blue", "Happy", i, i);
alphaGroc[i].introduce();
alphaGroc[i].sendMessage(alphaGroc[i].findNeighbor(), "Hi Neighbor!");
//alphaGroc[i].relocate(alphaGroc[i].getAddress() + 75);
// alphaGroc[i].visit(alphaGroc[i].getAddress() + 1);
System.out.println("Total Population Is " + Groc.getTotalPopulation());
}

/*
for (int k = 0; k<20; k++) {
alphaGroc[1].doSomething();
}

for (int j = 0; j<12; j++) {
City.listOccupants(j);
}

alphaGroc[1].examine();
alphaGroc[1].introduce();
alphaGroc[1].kill();
alphaGroc[1].examine();


int neighbor;
neighbor = Address.getNeighbor(18, Address.NORTH);
neighbor = Address.getNeighbor(8, Address.NORTH);
neighbor = Address.getNeighbor(8, Address.EAST);
neighbor = Address.getNeighbor(8, Address.WEST);
neighbor = Address.getNeighbor(9, Address.SOUTH);
neighbor = Address.getNeighbor(11, Address.EAST);
neighbor = Address.getNeighbor(10, Address.WEST);
*/

}




} stub.txt
'stash of groc frags for main: 

oc1 = Groc("George", "happy", "red")
groc2 = Groc("Phillip", "sad", "orange")
groc1.introduce()
groc1.identify()
groc2.introduce()
groc2.identify()
groc1.census()
groc2.census()


/usr/lib/python2.7/dist-packages/pygame/examples/stub.txt
