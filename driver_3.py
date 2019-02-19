import heapq
import time
import sys
import math
from puzze_state import PuzzleState
from custom_classes import Frontier, Explored


def bfs_search(initial_state, method):
    """BFS search"""

    frontier = Frontier(method)
    frontier.queue.append(initial_state)

    explored = Explored()

    max_depth = 0
    nodes = 0
    while frontier.queue:
        state = frontier.queue.popleft()
        explored.set.add(state.config)
        if test_goal(state):
            print("SUCCESS")
            return state, nodes, max_depth

        "expand the node"

        children = state.expand()
        nodes = nodes + 1

        for child in children:
            "check for duplicates in frontier and explored"
            if max_depth < child.cost:
                max_depth += 1
            if child.config not in explored.set and child not in frontier:
                frontier.queue.append(child)
    print('FAILURE')
    exit()


def dfs_search(initial_state, method):

    """DFS search"""

    frontier = Frontier(method)
    frontier.stack.append(initial_state)

    explored = Explored()

    max_depth = 0
    nodes = 0
    while frontier.stack:
        state = frontier.stack.pop()
        explored.set.add(state.config)

        if max_depth < state.cost:
            max_depth += 1
        if test_goal(state):
            print("SUCCESS")
            return state, nodes, max_depth

        "expand the node"

        children = state.expand()
        children = children[::-1]
        nodes = nodes + 1

        for child in children:
            "check for duplicates in frontier and explored"
            if max_depth < child.cost:
                max_depth += 1
            if child.config not in explored.set and child not in frontier:
                frontier.stack.append(child)
    print('FAILURE')
    exit()


def A_star_search(initial_state, method):

    """A * search"""

    frontier = Frontier(method) #  list of entries arranged in a heap
    entry_finder = {}  #  mapping of states to entries

    initial_state.key = calculate_manhattan_score(initial_state)
    entry = (initial_state.key, initial_state)
    entry_finder[initial_state.config] = entry
    heapq.heappush(frontier.heap, entry)

    explored = Explored()

    max_depth = 0
    nodes = 0

    while frontier.heap:

        state = heapq.heappop(frontier.heap)
        del entry_finder[state[1].config]
        explored.set.add(state[1].config)


        if test_goal(state[1]):
            print("SUCCESS")
            return state[1], nodes, max_depth

        "expand the node"

        children = state[1].expand()

        nodes = nodes + 1

        for child in children:
            "check for duplicates in frontier and explored"
            child.key = child.cost + calculate_manhattan_score(child)
            if max_depth < child.cost:
                max_depth += 1

            entry = (child.key, child)
            if child.config not in explored.set and child not in frontier:

                entry_finder[child.config] = entry
                heapq.heappush(frontier.heap, entry)

            elif child.config in entry_finder and child.key < entry_finder[child.config][0]:

                index = frontier.heap.index((entry_finder[child.config][1].key, entry_finder[child.config][1]))

                frontier.heap[int(index)] = entry

                entry_finder[child.config] = entry

                heapq.heapify(frontier.heap)
    print('FAILURE')
    exit()


def calculate_manhattan_dist(idx, value, n):

    """calculate the manhattan distance of a tile"""

    row, col = idx // n, idx % n

    goal_row, goal_col = value // n, value % n

    return abs(row-goal_row) + abs(col-goal_col)


def calculate_manhattan_score(state):
    """calculate the manhattan distance of a state"""
    score = 0
    for i, item in enumerate(state.config):
        score += calculate_manhattan_dist(i, item, state.dimension)
    return score


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


def main():

    sm = sys.argv[1].lower()

    begin_state = sys.argv[2].split(",")

    begin_state = tuple(map(int, begin_state))

    size = int(math.sqrt(len(begin_state)))

    hard_state = PuzzleState(begin_state, size)

    start_time = time.time()
    if sm == "bfs":

        goal_state, nodes, max_depth = bfs_search(hard_state, sm)
        write_in_file(goal_state, nodes, time.time() - start_time, max_depth)

    elif sm == "dfs":

        goal_state, nodes, max_depth = dfs_search(hard_state, sm)
        write_in_file(goal_state, nodes, time.time() - start_time, max_depth)

    elif sm == "ast":

        goal_state, nodes, max_depth = A_star_search(hard_state, sm)
        write_in_file(goal_state, nodes, time.time() - start_time, max_depth)
    else:

        print("Enter valid command arguments !")

if __name__ == '__main__':

    main()