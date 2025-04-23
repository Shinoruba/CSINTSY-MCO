from utility import *
from algos import *

import subprocess # for runMeasure
def runMeasure(locations, graph):
    subprocess.run(["python", "measurement.py"])

# ui prompt
def welcome():
    #inital
    locations, graph = setupDatabase()
    printLocations(locations)
   
    # db of locations in lowercase that maps to actual case
    locations_lc = {key.lower() : key for key in locations.keys()}
    
    exit = False
    while not exit:
        print(f"{GREEN}Options:{OFF}")
        print("[1]: Add Location (needs Longitude, Latitude, and Distance from any existing location)")
        print("[2]: Remove Location (close down an existing location and cannot use it as destination)")
        print("[3]: Update Location")
        print("[4]: Run UCS and GBFS")
        print("[5]: Run Time Complexity Measurement (start and destination are hardcoded, to change please see README)")
        print("[6]: Display Location Info")  # New option for display
        print("[0]: Exit")

        choice = input(f"{GREEN}Enter choice: {OFF}")

        match choice:
            case '1':
                addLocation(locations, locations_lc, graph)
            case '2':
                removeLocation(locations, locations_lc, graph)
            case '3':
                updateLocation(locations, locations_lc, graph)
            case '4':
                runAlgos(locations, graph, locations_lc)
            case '5':
                runMeasure(locations_lc, graph)
            case '6':
                loc_name = input("Enter the name of the location to display: ").lower()
                if loc_name in locations_lc:
                    displayLocationInfo(locations_lc[loc_name], locations, graph)  # Call the display function
                else:
                    print(f"{WARN}Location not found. Please try again.{OFF}")
            case '0':
                # Exit case
                exit = True
            case '_':
                print(f"{WARN}Invalid choice. Please try again.{OFF}")
        
        print(f"{GREEN}Goodbye!{OFF}\n")

# so that this file is treated as main
if __name__ == "__main__":
    welcome()