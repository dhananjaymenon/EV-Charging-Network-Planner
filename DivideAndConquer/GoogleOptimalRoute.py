from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

class TSP:
    def __init__(self,matrix):
        self.data = {}
        self.data['distance_matrix'] = matrix
        self.data['num_vehicles'] = 1
        self.data['depot'] = 0
        self.manager = pywrapcp.RoutingIndexManager(len(self.data['distance_matrix']),
                                               self.data['num_vehicles'], self.data['depot'])
        self.routing = pywrapcp.RoutingModel(self.manager)

    def print_solution(self,solution):
        """Prints solution on console."""
        print('Objective: {} metres'.format(solution.ObjectiveValue()))
        index = self.routing.Start(0)
        plan_output = 'Route for vehicle 0:\n'
        route_distance = 0
        while not self.routing.IsEnd(index):
            plan_output += ' {} ->'.format(self.manager.IndexToNode(index))
            previous_index = index
            index = solution.Value(self.routing.NextVar(index))
            route_distance += self.routing.GetArcCostForVehicle(previous_index, index, 0)
        plan_output += ' {}\n'.format(self.manager.IndexToNode(index))

        plan_output += 'Route distance: {}metres\n'.format(route_distance)
        print(plan_output)

    # ROUTE and DISTANCE
    def return_path_and_distance(self,solution):
        print('Objective: {} metres'.format(solution.ObjectiveValue()))
        route = []
        index = self.routing.Start(0)
        #plan_output = 'Route for vehicle 0:\n'
        route_distance = 0
        while not self.routing.IsEnd(index):
            #plan_output += ' {} ->'.format(self.manager.IndexToNode(index))
            route.append(self.manager.IndexToNode(index))
            previous_index = index
            index = solution.Value(self.routing.NextVar(index))
            route_distance += self.routing.GetArcCostForVehicle(previous_index, index, 0)

        route.append(self.manager.IndexToNode(index))
        ReturnPandD = []
        ReturnPandD.append(route)
        ReturnPandD.append(route_distance)
        return ReturnPandD

    def distance_callback(self,from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = self.manager.IndexToNode(from_index)
        to_node = self.manager.IndexToNode(to_index)
        return self.data['distance_matrix'][from_node][to_node]

    def get_solution(self):
        transit_callback_index = self.routing.RegisterTransitCallback(self.distance_callback)

        # Define cost of each arc.
        self.routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        # Setting first solution heuristic.
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

        # Solve the problem.
        solution = self.routing.SolveWithParameters(search_parameters)

        # Print solution on console.
        if solution:
            self.print_solution(solution)

    def return_solution(self):
        transit_callback_index = self.routing.RegisterTransitCallback(self.distance_callback)

        # Define cost of each arc.
        self.routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        # Setting first solution heuristic.
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

        # Solve the problem.
        solution = self.routing.SolveWithParameters(search_parameters)

        # Print solution on console.
        if solution:
            return self.return_path_and_distance(solution)