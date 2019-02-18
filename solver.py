from collections import deque
import sys


def bfs_search(initial_state):
    """BFS search"""

    frontier = deque()
    frontier.append(initial_state)

    explored = set()

    max_depth = 0
    nodes = 0
    while frontier:
        state = frontier.popleft()
        explored.add(state.config)

        if max_depth < state.cost:
            max_depth = state.cost
        if test_goal(state):
            print("SUCCESS")
            return state, nodes, max_depth

        "expand the node"

        children = state.expand()
        nodes = nodes + 1

        for child in children:
            "check for duplicates in frontier and explored"

            if child not in frontier and child.config not in explored:
                frontier.append(child)
    print('FAILURE')
    exit()


def dfs_search(initial_state):

    """DFS search"""

    ### STUDENT CODE GOES HERE ###


def A_star_search(initial_state):

    """A * search"""

    ### STUDENT CODE GOES HERE ###


def calculate_manhattan_dist(idx, value, n):

    """calculate the manhattan distance of a tile"""

    ### STUDENT CODE GOES HERE ###


def calculate_path_to_goal(state):
    """calculate the path to goal"""
    moves = list()

    while state.parent is not None:
        moves.append(state.action)
        state = state.parent

    moves = moves[::-1]

    return str(moves)


def test_goal(puzzle_state):

    """test the state is the goal state or not"""
    goal_config = (0, 1, 2, 3, 4, 5, 6, 7, 8)
    if puzzle_state.config == goal_config:
        return True
    return False


def write_in_file(goal_state, nodes, running_time , max_depth):

    f = open('output.txt', 'w+')
    f.write("path_to_goal: " + calculate_path_to_goal(goal_state) + "\n")
    f.write("cost_of_path: " + str(goal_state.cost) + "\n")
    f.write("nodes_expanded: " + str(nodes) + "\n")
    f.write("search_depth: " + str(goal_state.cost) + "\n")
    f.write("max_search_depth: " + str(max_depth) + "\n")
    f.write("running_time: " + str(running_time) + "\n")
    f.write("max_ram_usage: " + str(calculate_max_ram_usage()) + "\n")


def calculate_max_ram_usage():
    if sys.platform == "win32":
        import psutil
        return psutil.Process().memory_info().rss
    else:
        # Note: if you execute Python from cygwin,
        # the sys.platform is "cygwin"
        # the grading system's sys.platform is "linux2"
        import resource
        return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss