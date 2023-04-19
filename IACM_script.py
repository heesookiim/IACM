# -*- coding: utf-8 -*-
"""
EPICS IACM project
android branch

@author: emmad, mrajago
"""

file = open('./ParsedBuildings.txt', 'r')
output = open('./output.txt', 'w')
data = file.readlines()
final = []
flag = 0
blank = " "
buildingArray = []
polygonArray = [] 
methodStarted = False
#the flag will be 1 when adding coordinates to an entrance
#the flag will be 2 when adding coordinates to a bathroom
#the flag will be 3 when adding coordinates to an elevator

for i in range(len(data)):

   if data[i].find('initWithShortName') == 29:
       if (methodStarted):
           methodStarted = False
           z = shortName + ".setFloorToZero();"
           final.append(z)
           z = "return " + shortName + ";"
           final.append(z)
           z = "}"
           final.append(z)
           final.append(blank)
       x = data[i].replace('building = [[Building alloc] initWithShortName:@', '')
       names = x.split('@')
       shortName = names[0].strip('" fullName:')
       shortName = shortName.strip()
       longName = names[1].replace("];","")
       longName = longName.replace('"',"")
       longName = longName.replace("(", "")
       longName = longName.replace(")", "")
       longName = longName.replace(".", "")
       longName = longName.strip()
       z = "Building add" + shortName + "Building() {"
       final.append(z)
       methodStarted = True 
       test = "//Creating new building "+ shortName
       final.append(test)
       z = "ArrayList<LatLng> "+ shortName +"coordinates = new ArrayList<>();"
       final.append(blank)
       final.append(z)
       final.append(blank)
     
   if data[i].find("building setPathWithPaths") == 1:
       new = data[i].strip('[building setPathWithPaths:@[@[@')
       new = new.strip('@')
       new = new.strip(" ")
       new = new.replace("@", "")
       new = new.replace("],", "")
       new = new.strip()
       z = shortName + "coordinates.add(new LatLng(" +new+ "));"
       z = z.replace("\r\n", "")
       z = z.strip()
       final.append(z)


   if data[i].find('@[@') == 30:
       new = data[i].replace('@[@', "")
       new = new.strip(" ")
       new = new.replace("@", "")
       new = new.replace("],", "")
       new = new.replace("]]];", "")
       new = new.strip()
       z = shortName + "coordinates.add(new LatLng(" + new + "));"
       final.append(z)
       
   if data[i].find('building createPolygonForMapView:mapView') == 1:
       z = 'Building ' + shortName + ' = new Building("'+ longName +'", "'+ shortName +'", '+ shortName +'coordinates);'
       longName = longName.replace(" ", "")
       #z = 'Building ' + shortName + ' = new Building("'+ longName +'", "'+ shortName +'", '+ shortName +'coordinates);'
       
       final.append(blank)
       final.append(z) 
       buildingArray.append(shortName)

       y = 'Polygon '+ longName +' = mMap.addPolygon('+ shortName +'.getBuildingPolygonOptions());'
       final.append(y)
       polygonArray.append(longName)
       y = shortName + '.setBuildingPolygon(' + longName + ');'
       final.append(y)
       y = longName + '.setClickable(true);'
       final.append(y)
       final.append(blank)
       
        #Code to add entrances
   if data[i].find('// Creating entrance with Identifier') == 0:
       entranceID = data[i][37:38]
       #entranceID = data[i].strip('// Creating entrance with Identifier ')
       #entranceID = entranceID.strip(); #this gets rid of the newline at the end
       listName = shortName + 'Entrance' + entranceID + '_Coordinates'
       codeLine = 'ArrayList<LatLng> ' + listName + ' = new ArrayList<>();'
       final.append(blank)
       final.append(codeLine)
       flag = 1

   if data[i].find('building addEntranceWithPaths:') == 1:
       coordinates = data[i].strip('[building addEntranceWithPaths:@[@[@')
       coordinates = coordinates.strip(); #this gets rid of the newline at the end
       coordinates = coordinates.split(', @')
       coordinates[1] = coordinates[1].strip('],')
       codeLine = listName + '.add(new LatLng(' + coordinates[0] + ', ' + coordinates[1] + '));'
       final.append(codeLine)
    
   if (data[i].find('@[@') == 0) and (flag == 1):
       coordinates = data[i].strip('@[@')
       coordinates = coordinates.strip() #this gets rid of the newline at the end
       coordinates = coordinates.split(', @')
       if coordinates[1].find('accessible') == -1:
           coordinates[1] = coordinates[1].strip('],')
           codeLine = listName + '.add(new LatLng(' + coordinates[0] + ', ' + coordinates[1] + '));'
           final.append(codeLine)
       else:
           part2 = coordinates[1].split(']] ')
           codeLine = listName + '.add(new LatLng(' + coordinates[0] + ', ' + part2[0] + '));'
           final.append(codeLine)
           entranceName = shortName + 'Entrance' + entranceID
           if part2[1].find('NO') != -1:
               codeLine = 'Entrance ' + entranceName + ' = new Entrance("' + entranceID + '", ' + listName + ', false);'
           elif part2[1].find('YES') != -1:
               codeLine = 'Entrance ' + entranceName + ' = new Entrance("' + entranceID + '", ' + listName + ', true);'
           final.append(codeLine)
           codeLine = shortName + '.addEntrance(' + entranceName + ');'
           final.append(codeLine)
           codeLine = entranceName + '.setEntrancePolygon(mMap.addPolygon(' + entranceName + '.getEntrancePolygonOptions()));'
           final.append(codeLine)
           final.append(blank)
           flag = 0
     #End of code to add entrances   
     
     #Code to add Bathrooms 
   if data[i].find("// Creating bathroom with Identifier") == 0:
       flag = 2
       ID = data[i].replace("// Creating bathroom with Identifier", "")
       ID = ID.strip()
       z = "ArrayList<LatLng> " + shortName + "bathroom" + ID + "coordinates = new ArrayList<>();"
       final.append(z)
       final.append(blank)
   if data[i].find('[building addRestroomWithPaths:') == 0:
       new = data[i].strip("[building addRestroomWithPaths:@[@[@")
       new = new.replace('@', "")
       new = new.replace("],", "")
       new = new.strip()
       z = shortName + "bathroom"+ID+"coordinates.add(new LatLng(" + new + "));"
       final.append(z)
   if data[i].find("@[@") == 0 and flag == 2:
       new = data[i].replace('@[@', "")
       new = new.strip(" ")
       new = new.replace("@", "")
       new = new.replace("],", "")
       new = new.strip()
       
       if new.rfind("];") != -1:
           END = True
           test2 = new.split("]]")
           new = test2[0]
           test2[1] = test2[1].strip()
           level = test2[1][6:8]
           level = level.strip()
           acces = test2[1][20:22]
           acces = acces.strip()
           if acces == "NO":
               isAcces = "false"
           else: 
               isAcces = "true"
            
           z = shortName + "bathroom"+ID+"coordinates.add(new LatLng(" + new + "));"
           final.append(z) 
           final.append(blank)
           caller = "Bathroom "+ shortName + "Bathroom" + ID +' = new Bathroom("'+ID+'", '+ level + ', "'+ shortName + '", ' + shortName + "bathroom" + ID + "coordinates, "+ isAcces + ");"
           final.append(caller) 
           z = shortName + '.addBathroom(' + shortName + 'Bathroom' + ID +');'
           final.append(z) 
           #caller = "mMap.addPolygon(" + shortName + "Bathroom" + ID + ".getBathroomPolygon());"
           caller = shortName + 'Bathroom' + ID + '.setBathroomPolygon(mMap.addPolygon(' + shortName + 'Bathroom' + ID + '.getBathroomPolygonOptions()));'
           final.append(caller)
           final.append(blank)
           flag = 0
               
       else:
           z = shortName + "bathroom"+ID+"coordinates.add(new LatLng(" + new + "));"
           final.append(z)
       #End Code for Bathrooms

       #Code to add Elevators
   """ if data[i].find('// Creating elevator with Identifier') == 0:
        flag = 3

   if data[i].find('[building addElevatorWithPaths:') == 0:
        new = data[i].strip("[building addElevatorWithPaths]")
        new = new.replace('@',"") """


x = shortName + ".setFloorToZero();"
final.append(x)
x = "return " + shortName + ";"
final.append(x)
x = "}"
final.append(x)
final.append(blank) 
    

x = "@Override"
final.append(x)
x = "protected void onCreate(Bundle savedInstanceState) {"
final.append(x)
x = "super.onCreate(savedInstanceState);"
final.append(x)
x = "setContentView(R.layout.activity_maps);"
final.append(x)
x = "// Obtain the SupportMapFragment and get notified when the map is ready to be used."
final.append(x)
x = "SupportMapFragment mapFragment = (SupportMapFragment) getSupportFragmentManager()"
final.append(x)
x = ".findFragmentById(R.id.map);"
final.append(x)
x = "mapFragment.getMapAsync(this);"
final.append(x)
x = "}"
final.append(x)

x = "/**"
final.append(x)
x = "* Manipulates the map once available."
final.append(x)
x = "* This callback is triggered when the map is ready to be used."
final.append(x)
x = "* This is where we can add markers or lines, add listeners or move the camera. In this case,"
final.append(x)
x = "* we just add a marker near Sydney, Australia."
final.append(x)
x = "* If Google Play services is not installed on the device, the user will be prompted to install"
final.append(x)
x = "* it inside the SupportMapFragment. This method will only be triggered once the user has"
final.append(x)
x = "* installed Google Play services and returned to the app."
final.append(x)
x = "*/"
final.append(x)

x = "@Override"
final.append(x)
x = "public void onMapReady(GoogleMap googleMap) {"
final.append(x)
x = "int width = 1;"
final.append(x)
x = "mMap = googleMap;"
final.append(x)

for i in range(len(buildingArray)):
    x = "Building " + buildingArray[i] + " = add" + buildingArray[i] + "Building();"
    final.append(x)


x = "LatLng PurdueArch = new LatLng(40.431625, -86.916490);"
final.append(x)
x = "mMap.moveCamera(CameraUpdateFactory.newLatLng(PurdueArch));"
final.append(x)
x = "mMap.setMinZoomPreference(14);"
final.append(x)

x = "mMap.setOnPolygonClickListener(new GoogleMap.OnPolygonClickListener() {"
final.append(x)
x = "public void onPolygonClick(Polygon polygon) {"
final.append(x)
x = "PrettyDialog dialog = new PrettyDialog(MapsActivity.this)"
final.append(x)
x = ".setIcon(R.drawable.baseline_apartment_purple_500_48dp);"
final.append(x)

for i in range(len(polygonArray)):       
    x = "if (polygon.equals(" + buildingArray[i] + ".getBuildingPolygon())) {"
    final.append(x)
    x = "clickedBuilding(" + buildingArray[i] + ", dialog);"
    final.append(x)
    x = "}"
    final.append(x)

x = "Log.d(\"LOG\", \"Dialog made\");"
final.append(x)
x = "}"
final.append(x)
x = "});"
final.append(x)
x = "}"
final.append(x)

           
       
for i in range(len(final)):
    output.write(final[i])
    output.write('\r')
    
       
file.close()



