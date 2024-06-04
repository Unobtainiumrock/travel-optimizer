import numpy as np
import googlemaps
import json
import os

from dotenv import load_dotenv
from matplotlib import pyplot as plt
from itertools import permutations
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

# Load env variables from .env file. If you don't have one, add one
# and plance your own Google Maps API Key to there and be sure to add .env
# to your .gitignore!
load_dotenv()

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

x1 = (int(41.39284705069476), int(2.161692869209467))
x2 = (int(41.40375862907466), int(2.1744308998960746))
x3 = (int(41.39183008893432), int(2.1648817729104777))
x4 = (int(41.38501226483898), int(2.1836645409642723))
x5 = (int(41.41451086334113), int(2.1525872096880185))
x6 = (int(41.38014671090589), int(2.1753770606418326))
x7 = (int(41.38518643836521), int(2.180019853878209))

y1 = (41.39284705069476, 2.161692869209467)
y2 = (41.40375862907466, 2.1744308998960746)
y3 = (41.39183008893432, 2.1648817729104777)
y4 = (41.38501226483898, 2.1836645409642723)
y5 = (41.41451086334113, 2.1525872096880185)
y6 = (41.38014671090589, 2.1753770606418326)
y7 = (41.38518643836521, 2.180019853878209)

# each data point represents a location
# each location needs to be visited exactly once
# it must end from where it initally started
integer_locations = [x1, x2, x3, x4, x5, x6, x7]
locations = [y1, y2, y3, y4, y5, y6, y7]

integer_start_loc = x1
float_start_loc = y1

integer_permutations = permutations(integer_locations[1:])
float_permutations = permutations(locations[1:])


def path_builder(start_loc, permutations):
    paths = []

    for perm in permutations:
        path = [start_loc] + list(perm) + [start_loc]
        paths.append(path)

    return paths

integer_paths = path_builder(integer_start_loc, integer_permutations)
float_paths = path_builder(float_start_loc, float_permutations)

json_file = "distance_matrix.json"

def load_or_query_distance_matrix(locations, mode="driving"):
    """
    Loads distance matrix from JSON file if it exists, otherwise queries the API.

    Args:
        locations: List of tuples (latitude, longitude) for the distance matrix.
        mode: Travel mode (driving, walking, etc.). Defaults to "driving".

    Returns:
        The distance matrix as a NumPy array.
    """
    try:
        # Try loading from JSON file
        with open(json_file, "r") as f:
            response = json.load(f)
            print("Loaded distance matrix from existing JSON file.")
    except FileNotFoundError:
        # File doesn't exist, query the API
        try:
            response = gmaps.distance_matrix(locations, locations, mode=mode)
            print("Queried Google Maps API for distance matrix.")

            # Save the response to the JSON file for future use
            with open(json_file, "w") as f:
                json.dump(response, f)
        except googlemaps.exceptions.ApiError as e:
            print(f"Error querying Google Maps API: {e}")
            distance_matrix = None

    num_locations = len(locations)
    distance_matrix = np.zeros((num_locations, num_locations), dtype=int)

    for i in range(num_locations):
        for j in range(num_locations):
            distance_matrix[i][j] = response['rows'][i]['elements'][j]['distance']['value']
    
    if distance_matrix is not None:
        print("Distance Matrix (in meters):")
        print(distance_matrix)

    return distance_matrix

def create_data_model(distance_matrix):
    """Stores data for the problem"""
    data = {}
    data['distance_matrix'] = distance_matrix
    data['num_vehicles'] = 1
    data['depot'] = 0

    return data

# Print solution with coordinates
def print_solution(manager, routing, solution, locations):
    print("Objective: {} meters".format(solution.ObjectiveValue()))
    index = routing.Start(0)
    plan_output = "Route:\n"
    route_distance = 0
    route = []
    
    while not routing.IsEnd(index):
        node_index = manager.IndexToNode(index)
        route.append(node_index)
        plan_output += "{} ({}, {}) -> ".format(
            node_index, locations[node_index][0], locations[node_index][1]) + "\n"
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    
    node_index = manager.IndexToNode(index)
    route.append(node_index)
    plan_output += "{} ({}, {})\n".format(
        node_index, locations[node_index][0], locations[node_index][1])
    
    print(plan_output)
    print("Route distance: {} meters\n".format(route_distance))

# Update the main function to pass locations to print_solution
def main():
    distance_matrix = load_or_query_distance_matrix(locations)

    if distance_matrix is None:
        print("Error: Distance matrix is None")
        return

    # Create the data model
    data = create_data_model(distance_matrix)

    # Create the routing index manager
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']), data['num_vehicles'], data['depot'])
    
    # Create Routing Model
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Set parameters for the search
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console
    if solution:
        print_solution(manager, routing, solution, locations)
    else:
        print("No solution found!")

if __name__ == "__main__":
    main()