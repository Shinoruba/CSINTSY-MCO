import random
from algos import *
from utility import *
import big_o # pip install big-o
from memory_profiler import * # pip install matplotlib

RED = '\033[91m' # GBFS
GREEN = '\033[92m' # user prompts
CYAN = '\033[96m' # UCS
WARN = '\033[31m' # errors
OFF = '\033[0m' # needed talaga or everything will be in that color

# picks 2 random locations and tests the time complexity of UCS and GBFS
def test_random_connection(locations, graph):
    # comment this out if you want a specific test case
    start, goal = random.sample(list(locations.keys()), 2)

    # test_specific_connection(locations, graph)
    print(f"Testing random connection from {start} to {goal}")

    # Runs the UCS algorithm once
    # UNCOMMENT IF YOU WANT TO TEST UCS
    @profile
    def ucs_wrapper(n):
        ucs_noprint(graph, start, goal)

    # heuristic: calculates the distance between two locations (used by GBFS to estimate the remaining cost)
    # runs GBFS once
    # UNCOMMENT IF YOU WANT TO TEST GBFS
    @profile
    def gbfs_wrapper(n):
        def heuristic(a, b):
            return getDistance(locations[a][0], locations[a][1], locations[b][0], locations[b][1])
        gbfs_noprint(graph, start, goal, lambda a, b: heuristic(a, b))

    # Analyze UCS
    best, _ = big_o.big_o(ucs_wrapper, lambda n: n)
    print(f"{CYAN}UCS Time Complexity: {best}{OFF}")
    print("FULL REPORT:")
    print(big_o.reports.big_o_report(best, _)) # prints the report

    # Analyze GBFS
    best, _ = big_o.big_o(gbfs_wrapper, lambda n: n)
    print(f"{RED}GBFS Time Complexity: {best}{OFF}")
    print("FULL REPORT:")
    print(big_o.reports.big_o_report(best, _)) # prints the report
    
    return 0

def test_specific_connection(locations, graph):
    locations_lc = {key.lower(): key for key in locations.keys()}

    # manually type start and goal IN LOWER CASE
    start = "p. ocampo st."
    goal = "fidel a reyes st."

    # handle manually selected locations
    if goal in ["miguel", "velasco", "cads/henry sy ", "sj hall", "yuchengco"]:
        print(f"{WARN}Inputted destination is not a food place. Please try again.{OFF}")
        return None
    elif start in locations_lc and goal in locations_lc:
        print(f"Testing specific connection from {start} to {goal}")

        # Runs the UCS algorithm once
        # UNCOMMENT IF YOU WANT TO TEST UCS
        # @profile
        def ucs_wrapper(n):
            ucs_noprint(graph, locations_lc[start], locations_lc[goal])

        # UNCOMMENT IF YOU WANT TO TEST GBFS
        # @profile
        def gbfs_wrapper(n):
            def heuristic(a, b):
                return getDistance(locations[a][0], locations[a][1], locations[b][0], locations[b][1])
            gbfs_noprint(graph, locations_lc[start], locations_lc[goal], lambda a, b: heuristic(a, b))

        # Analyze UCS
        best_ucs, _ = big_o.big_o(ucs_wrapper, lambda n: n)
        print(f"{CYAN}UCS Time Complexity: {best_ucs}{OFF}")
        print("FULL REPORT:")
        print(big_o.reports.big_o_report(best_ucs, _)) # prints the report

        # Analyze GBFS
        best_gbfs, _ = big_o.big_o(gbfs_wrapper, lambda n: n)
        print(f"{RED}GBFS Time Complexity: {best_gbfs}{OFF}")
        print("FULL REPORT:")
        print(big_o.reports.big_o_report(best_gbfs, _)) # prints the report

        return best_ucs, best_gbfs
    else:
        print(f"{WARN}Invalid location(s). Please try again.{OFF}")
        return None

# MAIN
locations, graph = setupDatabase()

# UNCOMMENT THESE IF NEEDED
test_random_connection(locations, graph)
# test_specific_connection(locations, graph)


