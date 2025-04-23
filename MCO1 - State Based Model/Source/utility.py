from math import radians, sin, cos, acos # for getDistance
import algos as algos 
from algos import ucs, gbfs
import time as time

# https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
# some global UI stuff; you can replace \033 with \x1b
# sample: print(f"{RED}Goodbye!{OFF}")
RED = '\033[91m' # GBFS
GREEN = '\033[92m' # user prompts
CYAN = '\033[96m' # UCS
WARN = '\033[31m' # errors
OFF = '\033[0m' # needed talaga or everything will be in that color

# https://www.askpython.com/python/examples/find-distance-between-two-geo-locations
# this will calculate the h(n) when we're doing gbfs
def getDistance(lat1, lon1, lat2, lon2):
    mlat = radians(float(lat1))
    mlon = radians(float(lon1))
    plat = radians(float(lat2))
    plon = radians(float(lon2))

    # Calculate the cosine of the angle between the points
    # ensures that cos_angle is clamped within the range [-1, 1] before passing it to acos
    cos_angle = sin(mlat) * sin(plat) + cos(mlat) * cos(plat) * cos(mlon - plon)

    # Ensure the value is within the valid range for acos
    cos_angle = min(1, max(cos_angle, -1))

    # Calculate the distance
    dist_km = 6371.01 * acos(cos_angle)

    # Convert to meters
    dist_m = dist_km * 1000
    return dist_m

# this gives us ValueError: math domain error when inputting leon g. and razon in GBFS
def old_getDistance(lat1, lon1, lat2, lon2):
    mlat = radians(float(lat1))
    mlon = radians(float(lon1))
    plat = radians(float(lat2))
    plon = radians(float(lon2))
    dist = 6371.01 * acos(sin(mlat)*sin(plat) + cos(mlat)*cos(plat)*cos(mlon - plon))
    return round(dist * 1000, 2)  # Convert to meters and round to 2 decimal places

# database of locations to choose from and path weights, locations should have an optional h(n) value
def setupDatabase():
    locations = {
        "Agno Food Court": (14.56609562694215, 120.99249522032345),
        "Bloemen": (14.565301280227494, 120.99266359892113),
        "Br. Andrew (Kitchen City)": (14.566982831862903, 120.9924318450502),
        "Burgundy St.": (14.565248852994166, 120.9942380797893),
        "CADS/Henry Sy": (14.564985651284422, 120.99306405442523),
        "Dagonoy St.": (14.565958585672702, 120.99415159883056),
        "Dixies/Castro St.": (14.566555791517636, 120.99285161075852),
        "D'Students Place": (14.564351974914983, 120.99465777047357),
        "EGI Taft": (14.565994665124373, 120.99314239696405),
        "Estrada St.": (14.564607638127875, 120.9948040259048),
        "Fidel A Reyes St.": (14.567296862957642, 120.99209073491625),
        "Green Court": (14.56674466608153, 120.99221208053847),
        "Green Mall": (14.56725086739992, 120.9922541487042),
        "Jollibee": (14.56720326384671, 120.99334991872865),
        "Leon G.": (14.56542885867989, 120.99489144620075),
        "LS Food Court": (14.563824676132967, 120.99404025749809),
        "McDo": (14.563531963795027, 120.99439138751849),
        "Miguel": (14.56561039166978, 120.99256866635147),
        "One Archers": (14.566762172820633, 120.99277852055954),
        "P. Ocampo St.": (14.562646395559774, 120.99516948776468),
        "Razon": (14.567020764690477, 120.99208647717667),
        "Sherwood": (14.567697756009427, 120.99323652325401),
        "SJ Hall": (14.56481720664187, 120.99260445992562),
        "UMall": (14.563232686292091, 120.99440659468942),
        "Velasco": (14.565503248281326, 120.9932552271001),
        "WH Taft": (14.565757713747448, 120.99324032500704),
        "Yuchengco": (14.564425531450715, 120.99327442029133),
    }

    # graph of connections (adjacencies) from map
    graph = {location: {} for location in locations}

    connections = [
        ("LS Food Court", "McDo", 55.33),
        ("LS Food Court", "UMall", 162.42),
        ("McDo", "UMall", 20.77),
        ("UMall", "P. Ocampo St.", 20.47),
        ("P. Ocampo St.", "D'Students Place", 198.58),
        ("D'Students Place", "Estrada St.", 49.47),
        ("Estrada St.", "Burgundy St.", 63.34),
        ("Burgundy St.", "Dagonoy St.", 85.50),
        ("Dagonoy St.", "Jollibee", 154.64),
        ("Jollibee", "Sherwood", 62.88),
        ("Sherwood", "Dixies/Castro St.", 152.13),
        ("Fidel A Reyes St.", "Green Mall", 34.68),
        ("Green Mall", "Razon", 34.37),
        ("Razon", "Br. Andrew (Kitchen City)", 27.24),
        ("Br. Andrew (Kitchen City)", "Green Court", 33.68),
        ("Green Court", "One Archers", 45.77),
        ("One Archers", "Agno Food Court", 57.38),
        ("Agno Food Court", "EGI Taft", 43.2),
        ("EGI Taft", "WH Taft", 44.60),
        ("WH Taft", "Velasco", 31.17),
        ("SJ Hall", "CADS/Henry Sy", 44.20),
        ("CADS/Henry Sy", "Yuchengco", 70.44),
        ("Yuchengco", "LS Food Court", 154.61),
        ("Bloemen", "Miguel", 51.67),
        ("Dixies/Castro St.", "Agno Food Court", 61.23),
        ("Leon G.", "Dagonoy St.", 170.29),
        ("Leon G.", "Estrada St.", 161.96),
        ("Jollibee", "Dixies/Castro St.", 75.65),
        ("One Archers", "Dixies/Castro St.", 66.17),
        ("Green Mall", "Br. Andrew (Kitchen City)", 39.86),
        ("McDo", "P. Ocampo St.", 129.96), 
        ("Fidel A Reyes St.", "Razon", 39.29),
        ("Razon", "Green Court", 46.37),
        ("Green Court", "Agno Food Court", 79.93),
        ("WH Taft", "Miguel", 17.68),
        ("Miguel", "Velasco", 60.60),
        ("Velasco", "Bloemen", 60.86),
        ("Bloemen", "CADS/Henry Sy", 61.95),
        ("Bloemen", "SJ Hall", 100.95),
        ("SJ Hall", "Yuchengco", 121.66), 
        ("Br. Andrew (Kitchen City)", "One Archers", 38.41),
        ("Velasco", "CADS/Henry Sy", 64.57),
        ("Sherwood","Green Mall", 35.88),
        ("Br. Andrew (Kitchen City)","Sherwood", 81.12),
        ("Velasco","Dagonoy St.", 43.49),
        ("Velasco","Burgundy St.", 39.48),
        ("CADS/Henry Sy","Burgundy St.", 117.03),
        ("McDo","D'Students Place", 124.45),
    ]

    # make graph bidirectional 
    for start, end, distance in connections:
        graph[start][end] = distance
        graph[end][start] = distance
    
    return locations, graph 

# calls the appropriate algorithm and returns the answer
def getAnswer(start, goal, graph, locations):
    # call UCS here and print the answer
    print("\n[UCS Algorithm Results]")
    ucs_start = time.perf_counter() # start time for ucs
    ucs_path = ucs(graph, start, goal)
    ucs_end = time.perf_counter() # end time for ucs
  
    # print UCS results
    print(f"\n{CYAN}UCS Path:", ' -> '.join(ucs_path))
    print("UCS Cost:", getCost(graph, ucs_path))
    print("UCS Time:", f"{getTime(ucs_start, ucs_end)*1000} ms")
    print(f"{OFF}") # turns off the cyan
    
    # call GBFS here and print the answer
    def heuristic(a, b):
        return getDistance(locations[a][0], locations[a][1], locations[b][0], locations[b][1])
    
    print("[GBFS Algorithm Results]")
    gbfs_start = time.perf_counter() # start time for gbfs
    gbfs_path = gbfs(graph, start, goal, lambda a, b: heuristic(a, b))
    gbfs_end = time.perf_counter() # end time for gbfs

    # print GBFS results
    print(f"{RED}GBFS Path:", ' -> '.join(gbfs_path))
    print("GBFS Cost:", getCost(graph, gbfs_path))
    print("GBFS Time:", f"{getTime(gbfs_start, gbfs_end)*1000} ms")
    print(f"{OFF}") # turns off the red

    return ucs_path, gbfs_path

# returns time complexity measurement
def getTime(timeStart, timeEnd):
    return timeEnd - timeStart

# returns the cost of path rounded to 2 decimal places
def getCost(graph, path):
    cost = 0
    for i in range(len(path) - 1):
        current_node = path[i]
        next_node = path[i + 1]
        cost += graph[current_node][next_node]
    return round(cost, 2)

def runAlgos(locations, graph, locations_lc):
    non_destinations = ["sj hall", "velasco", "cads/henry sy", "yuchengco", "miguel"]
    exit = False
    while not exit:
        printLocations(locations)

        print(f"{GREEN}Please type the full name of your starting point and destination below.{OFF}")
        try:
            start = input("Enter starting point: ").lower()
            goal = input("Enter destination: ").lower()
        except EOFError:
            # for i/o redirection testing, exit when EOF reached if ever
            return 0

        # deny traversal when goal is non-food destination (halls)
        if (goal in non_destinations):
            print(f"{WARN}Inputted destination is not a food place. Please try again.{OFF}")
            
        elif start in locations_lc and goal in locations_lc:
            # print ucs and gbfs paths
            getAnswer(locations_lc[start], locations_lc[goal], graph, locations)
            
        else:
            print(f"{WARN}Invalid location(s). Please try again.{OFF}")

        # exit option when input is valid
        # move into elif valid input if preferred 
        exit = input(f"{GREEN}Do you want to exit? (y/n): {OFF}").lower() == 'y'
    #if exit
    print(f"{GREEN}Going back to main menu...{OFF}")
        
def addLocation(locations, locations_lc, graph):
    # prompt for name
    name = input("Enter the name of the new location: ")
    
    # location already in database 
    if name.lower() in locations_lc:
        print(f"{WARN}This location already exists. Please try again. {OFF}")
        
    # location name is unique
    else:
        # enter latitude and longitude values
        try:
            latitude = float(input("Enter the latitude of " + name + ": "))
            longitude = float(input("Enter the longitude of " + name + ": "))
            
            locations[name] = (latitude, longitude) # add to locations
            locations_lc[name.lower()] = name # add to lowercase locations
        except ValueError:
            print(f"{WARN}Invalid longitude/latitude value(s). {OFF}")
            return
        # enter adjacencies
        try:
            terminate = False
            num_adjacent = int(input("How many points are connected to your new location?: "))
            
            # valid number of connections
            if num_adjacent > 0 and num_adjacent < len(locations):
                for i in range(1, num_adjacent + 1):
                    adjacent = input(f"{i}. Enter location: ").lower()
                    
                    # adjacent location is an existing location
                    if adjacent.lower() in locations_lc and adjacent.lower() != name.lower():
                        distance = float(input(f"   Distance from {name} to {locations_lc[adjacent.lower()]}: "))
                        
                        # if distance is non-zero
                        if distance >= 0:
                            graph[name] = {} # create in dictionary
                            graph[name][locations_lc[adjacent]] = distance
                            graph[locations_lc[adjacent]][name] = distance
                        else:
                            print("Distance must be a positive value! Process terminated.")
                            terminate = True
                    # location does not exist
                    else:
                        # undo addition of location (avoid errors since "lone" nodes aren't accounted for in the algos)
                        print("Not an existing location! Process terminated.")
                        terminate = True
                        break
                if not terminate:
                    print(f"{GREEN}New location added successfully{OFF}")
            else:
                print("Distance must be a positive float value! Process terminated.")

        except ValueError:
            print("Invalid distance! Process terminated.")
            terminate = True
            
        if terminate:
            locations.pop(name, None)
            locations_lc.pop(name.lower(), None)

def removeLocation(locations, locations_lc, graph):
    loc = input("Enter the name of the location to remove: ").lower()
    
    # location exists 
    if loc in locations_lc:
        if input("Confirm removal of this location? (y/n): ").lower() == 'y':
            print(f"{GREEN}{locations_lc[loc]} successfully removed from the database.{OFF}")
            
            # remove all instances in all databases
            del graph[locations_lc[loc]]
            for location, connection in graph.items(): # since bidirectional
                if locations_lc[loc] in connection:
                    del connection[locations_lc[loc]]
            locations.pop(locations_lc[loc])
            locations_lc.pop(loc)
            
        else:
            print(f"{WARN}Process terminated.{OFF}")
    # location does not exist
    else:
        print(f"{WARN}Not an existing location in the database. Please try again.{OFF}")

def updateLocation(locations, locations_lc, graph):
    # Get the name of the location to update
    name = input("Enter the name of the location to update: ").lower()

    # Check if the location exists
    if name in locations_lc:
        # Display current information (latitude, longitude, and adjacencies)
        displayLocationInfo(locations_lc[name], locations, graph)

        # Ask if the user wants to update the coordinates (latitude and longitude)
        if input("Do you want to update the coordinates? (y/n): ").lower() == 'y':
            try:
                new_lat = float(input("Enter new latitude: "))
                new_lon = float(input("Enter new longitude: "))
                locations[locations_lc[name]] = (round(new_lat, 2), round(new_lon, 2))
                print(f"{GREEN}Coordinates updated successfully!{OFF}")
            except ValueError:
                print(f"{WARN}Invalid latitude/longitude values. Update failed.{OFF}")

        # Ask if the user wants to update the distances (adjacencies) to other locations
        if input("Do you want to update distances to adjacent locations? (y/n): ").lower() == 'y':
            for adjacent in graph[locations_lc[name]]:
                print(f"Current distance to {adjacent}: {graph[locations_lc[name]][adjacent]} meters")
                try:
                    new_distance = float(input(f"Enter new distance to {adjacent}: "))
                    if new_distance > 0:
                        graph[locations_lc[name]][adjacent] = new_distance
                        graph[adjacent][locations_lc[name]] = new_distance  # Update both directions
                        print(f"{GREEN}Distance to {adjacent} updated successfully!{OFF}")
                    else:
                        print(f"{WARN}Distance must be positive!{OFF}")
                except ValueError:
                    print(f"{WARN}Invalid distance entered!{OFF}")
        print(f"{GREEN}Location update completed.{OFF}")
    
    else:
        print(f"{WARN}Location not found in the database.{OFF}")


#display values/adjacencies
def displayLocationInfo(name, locations, graph):
    # Check if location exists in the database
    if name in locations:
        lat, lon = locations[name]
        print(f"Location: {name}")
        print(f"Latitude: {lat}, Longitude: {lon}")
        
        # Display connections (adjacent locations)
        if name in graph and graph[name]:
            print(f"Connections from {name}:")
            for adjacent, distance in graph[name].items():
                print(f"  -> {adjacent}: {distance} meters")
        else:
            print(f"{WARN}No connections found for {name}.{OFF}")
    else:
        print(f"{WARN}Location {name} not found in the database.{OFF}")


def printLocations(locations):
    print(f"{GREEN}Available locations:{OFF}")
    for i, location in enumerate(locations.keys(), 1):
        print(f"{i}. {location}")
    print()