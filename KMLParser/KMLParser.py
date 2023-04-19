#######################################################
#    Author:        <Matthew Bolda>
#    email:         <mbolda@purdue.edu>
#    ID:            <mbolda>
#    Date Created:  <3/24/2020>
#    Date Updated:  <12/3/2020>
#######################################################


class Building:
    def __init__(self, abbreviation, fullname, coordinates, building_num, entrances_list, bathroom_list):
        self.abbreviation = abbreviation            # the official abbreviation for the building
        self.fullname = fullname                    # the official name of the building
        self.building_num = str(building_num)       # the number the building got parsed at
        self.coordinates = coordinates[1:]          # the list of the coordinates for the building
        self.first_coord = coordinates[0]           # the first point of coordinates for the building
        self.entrance_list = entrances_list         # tuple('letter_ID', 'Accessible Y/N', list of coords)
        self.bathroom_list = bathroom_list          # List of all bathrooms
        self.floors_list = []                       # a floor is considered a floor if it has a bathroom

        # Below are not necessary used as each entrance and restroom stores this data
        # but could be used in the future and is helpful for testing.
        self.A_entrance_list = []                   # accessible entrance list
        self.NA_entrance_list = []                  # Nonaccessible entrance list
        self.A_bathroom_list = []                   # List of Accessible bathrooms
        self.NA_bathroom_list = []                  # List of NOT Accessible bathrooms
        self.MEN_bathroom_list = []                 # List of MENS bathrooms
        self.WOMEN_bathroom_list = []               # List of WOMENS bathrooms
        return

    # This is the current required output as off (12/3/2020)
    def printer(self):
        a = '// Creating Building #' + self.building_num + ' ' + self.fullname + '...\n'
        b = 'building = [[Building alloc] initWithShortName:@"' + (
            self.abbreviation).upper() + '" fullName:@"' + self.fullname + '"];\n'
        x1, y1, z1 = self.first_coord
        c = '[building setPathWithPaths:@[@[@' + y1 + ', @' + x1 + '],\n'
        d = ''
        length = len(self.coordinates)
        counter = 0
        for coord in self.coordinates:
            x, y, z = coord
            counter = counter + 1
            if counter == length:
                d += '                              @[@' + y + ', @' + x + ']]];\n\n'
            else:
                d += '                              @[@' + y + ', @' + x + '],\n'
        e = '[building createPolygonForMapView:mapView];\n\n'
        f = '[buildingsArr addObject:building];\n\n'

        return a + b + c + d + e + f

###########################################
# Start of functions for printing outputs #
###########################################


def feature_printer_helper(building):
    # Check to see if floor information has been inputted
    if building.floors_list == []:
        total_str = "// Not enough information to input floors\n\n"
    else:
        ordered_floors = reorder_floors(building.floors_list)
        total_str = print_floors(ordered_floors)
        total_str = total_str + '\n\n'

    # Check to see if entrance information has been inputted
    if building.entrance_list == []:
        total_str = total_str + "// Not enough information to input entrances\n\n"
    else:
        for entrance in building.entrance_list:
            total_str = total_str + print_entrance(entrance) + '\n'
        total_str = total_str + '\n'

    # Check to see if bathroom information has been inputted
    if building.bathroom_list == []:
        total_str = total_str + "// Not enough information to input bathrooms\n\n\n"
    else:
        for bathroom in building.bathroom_list:
            ordered_floors = reorder_floors(building.floors_list)
            total_str = total_str + print_bathroom(bathroom, ordered_floors) + '\n'
            total_str = total_str + '\n'

    return total_str


def print_bathroom(bathroom, floor_list):
    floor, identifier, accessible, coords = bathroom
    ret_str = '// Creating bathroom with Identifier ' + str(identifier) + '\n[building addRestroomWithPaths:@['
    floor_index = 0

    try:
        floor = int(floor)
    except:
        pass

    for temp_floor in floor_list:
        if temp_floor == floor:
            break
        floor_index += 1

    length = len(coords)
    for i in range(length):
        x, y, z = coords[i]
        if i == length - 1:
            add_part = '@[@' + str(y) + ', @' + str(x) + ']] level: ' + str(floor_index) + ' accessible:' + accessible + ' mapView:mapView];\n'
        else:
            add_part = '@[@' + str(y) + ', @' + str(x) + '],\n'
        ret_str = ret_str + add_part
    return ret_str


def print_floors(list_of_floors):
    final_list = list_of_floors
    ret_str = "[building setLevels:@["
    length = len(final_list)
    for i in range(length):
        if i == length - 1:
            add_part = '@"' + str(final_list[i]) + '"]];'
        else:
            add_part = '@"' + str(final_list[i]) + '", '
        ret_str = ret_str + add_part
    return ret_str


def print_entrance(entrance):
    identifier, accessible, coords = entrance
    ret_str = '// Creating entrance with Identifier ' + str(identifier) + '\n[building addEntranceWithPaths:@['
    length = len(coords)
    for i in range(length):
        x, y, z = coords[i]
        if i == length - 1:
            add_part = '@[@' + str(y) + ', @' + str(x) + ']] accessible:' + accessible + ' mapView:mapView];\n'
        else:
            add_part = '@[@' + str(y) + ', @' + str(x) + '],\n'
        ret_str = ret_str + add_part
    return ret_str


def reorder_floors(list_of_floors):
    lettered_floors = []
    numbered_floors = []
    for floor in list_of_floors:
        try:
            tester = int(floor)
            numbered_floors.append(tester)
        except:
            lettered_floors.append(floor)
    numbered_floors.sort()
    final_list = []

    for floor in lettered_floors:
        final_list.append(floor)
    for floor in numbered_floors:
        final_list.append(floor)
    return final_list


###########################################
#  End of functions for printing outputs  #
###########################################

###########################################
# Start of functions for filling building #
###########################################


def build_dictionary(KMLfile):
    building_list = []
    in_building = False
    need_name = False
    need_coords = False
    list_of_coords = []
    building_num = 1
    with open(KMLfile, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()

            if line == "<Placemark>":
                in_building = True
                need_name = True
            elif line == "</Placemark>":
                in_building = False
            elif need_name == True:
                name = line
                name = name.strip()
                name = name.strip('<name>')
                name = name.strip('</name>')
                abbreviation = name.split(' ')[0]
                abbreviation = abbreviation.lower()
                name = name.split(' ')
                name = name[1:]
                full_name = ''
                length = len(name)
                index = 0
                for word in name:
                    index += 1
                    full_name += word
                    if index != length:
                        full_name += ' '
                need_name = False
            elif line == "<coordinates>":
                need_coords = True
                list_of_coords = []
            elif line == "</coordinates>":
                need_coords = False
                new_building = Building(abbreviation, full_name, list_of_coords, building_num, [], [])
                building_num += 1
                building_list.append(new_building)
                #
                # Create the building here
                #
            elif need_coords == True:
                coords = line.strip()
                coords = coords.split(',')
                x = coords[0]
                y = coords[1]
                z = coords[2]
                coordinates = x, y, z
                list_of_coords.append(coordinates)
    return building_list


def build_bathrooms(KMLfile, building_list):
    bathroom_list = []
    in_building = False
    need_name = False
    need_coords = False
    building_num = 1

    with open(KMLfile, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()

            # Are we at the start of the information for a bathroom
            if line == "<Placemark>":
                in_building = True
                need_name = True
            # Are we at the end of the information for a bathroom
            elif line == "</Placemark>":
                in_building = False
            # Have we could which building this bathroom cooresponds to and if it is Mens/Womens and/or accessible
            elif need_name == True:
                # ABBREVIATION, Floor, Identifier, Mens, Womens, Accessible
                name = line
                name = name.strip()
                name = name.strip('<name>')
                name = name.strip('</name>')
                abbreviation = name.split(' ')[0]
                abbreviation = abbreviation.lower()
                floor = name.split(' ')[1]
                letter = name.split(' ')[2]
                mens = name.split(' ')[3]
                womens = name.split(' ')[4]
                accessible = name.split(' ')[5]
                need_name = False
            # We are past the name and now we will be looking for coordinates
            elif line == "<coordinates>":
                need_coords = True
                list_of_coords = []
            # We are past the coordinates and now we need to add them to the building
            elif line == "</coordinates>":
                need_coords = False
                for building in list_of_buildings:
                    if building.abbreviation.upper() == abbreviation.upper():
                        building.bathroom_list.append((floor, letter, accessible, list_of_coords))
                        not_new = True
                        if building.floors_list == []:
                            building.floors_list.append(floor)
                            not_new = False
                        for floor_index in building.floors_list:
                            if floor_index == floor:
                                not_new = False
                        if not_new:
                            building.floors_list.append(floor)
                        if accessible == 'YES':
                            building.A_bathroom_list.append((letter, list_of_coords))
                        if accessible == 'NO':
                            building.NA_bathroom_list.append((letter, list_of_coords))
                        if mens == 'YES':
                            building.MEN_bathroom_list.append((letter, list_of_coords))
                        if womens == 'YES':
                            building.WOMEN_bathroom_list.append((letter, list_of_coords))
                        #'''
                        if accessible != 'NO' and accessible != 'YES':
                            print("ACCESSIBLE IS", accessible)
                            print('There was an error, one of the bathroom was not specified to be accessible or not')
                            print('Please use exactly "YES" or "NO" to specify')
                            print('The building with a problem is ' + str(building.abbreviation) + ' with bathroom '+ str(letter))
                            break
                        #'''
            # This is a coordinate for a point on the polygon that outlines a bathroom
            elif need_coords == True:
                coords = line.strip()
                coords = coords.split(',')
                x = coords[0]
                y = coords[1]
                z = coords[2]
                coordinates = x, y, z
                list_of_coords.append(coordinates)
    return


def build_entrances(KMLfile, building_list):
    entrance_list = []
    in_building = False
    need_name = False
    need_coords = False
    building_num = 1
    with open(KMLfile, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()

            if line == "<Placemark>":
                in_building = True
                need_name = True
            elif line == "</Placemark>":
                in_building = False
            elif need_name == True:
                name = line
                name = name.strip()
                name = name.strip('<name>')
                name = name.strip('</name>')
                abbreviation = name.split(' ')[0]
                abbreviation = abbreviation.lower()
                letter = name.split(' ')[1]
                accessible = name.split(' ')[2]
                need_name = False
            elif line == "<coordinates>":
                need_coords = True
                list_of_coords = []
            elif line == "</coordinates>":
                need_coords = False
                for building in list_of_buildings:
                    if building.abbreviation.upper() == abbreviation.upper():
                        building.entrance_list.append((letter, accessible, list_of_coords))
                        if accessible == 'YES':
                            building.A_entrance_list.append((letter, list_of_coords))
                        if accessible == 'NO' or accessible == "NOÂ ":
                            accessible = "NO"
                            building.NA_entrance_list.append((letter, list_of_coords))
                        if accessible != 'NO' and accessible != 'YES':
                            print("ACCESSIBLE IS", accessible)
                            print('There was an erorr, one of the entrances was not specified to be accessible or not')
                            print('Please use exactly "YES" or "NO" to specify')
                            print('The building with a problem is ' + str(building.abbreviation) + 'with entrance ' + str(letter))
                        break
                #
                # Create the building here
                #
            elif need_coords == True:
                coords = line.strip()
                coords = coords.split(',')
                x = coords[0]
                y = coords[1]
                z = coords[2]
                coordinates = x, y, z
                list_of_coords.append(coordinates)
    return


###########################################
#  End of functions for filling building  #
###########################################

# Usage:
# Please have 3 txt files in folder with script
# UnParsedBuildings.txt ParsedBuildings.txt UnParsedEntrances.txt
# Your output file will be modified, or created if does not exist
# ParsedBuildings.txt
if __name__ == "__main__":

    # These are constants for inputs and output
    BuildingFileName = "UnParsedBuildings.txt"
    EntranceFileName = "UnParsedEntrances.txt"
    BathroomFileName = "UnParsedBathrooms.txt"
    OutputFileName = "ParsedBuildings.txt"

    # Parse the UnParsedBuildings.txt to build list of building classes
    list_of_buildings = build_dictionary(BuildingFileName)

    # Parse the UnParsedEntrances.txt to add entrances to buildings
    build_entrances(EntranceFileName, list_of_buildings)

    # Parse the UnParsedBathrooms.txt to add bathrooms to buildings
    build_bathrooms(BathroomFileName, list_of_buildings)

    # Open the output file for writing
    output_file = open(OutputFileName, 'w')

    # Print the required text for each building
    for building in list_of_buildings:
        build = building.printer()
        features = feature_printer_helper(building)
        text_for_building = build + features
        output_file.write(text_for_building)

    # Close the output file
    output_file.close()
