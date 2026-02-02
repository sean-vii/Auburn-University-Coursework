"""
circular16_student.py

Starter code for the Circular 16 Puzzle search assignment.

Students:
- DO NOT change function names or signatures.
- You may add helper functions if needed.
- Fill in all TODO sections.
"""

from collections import deque
import heapq
from typing import List, Tuple, Dict, Callable, Any

State = Tuple[int, ...]  # a tuple of length 16 containing 0..15
Action = str
SearchResult = Dict[str, Any]

# ---------------------------------------------------------------------------
# Puzzle representation (provided)
# ---------------------------------------------------------------------------

def parse_state(s: str) -> State:
    """
    Parse a string like "1 2 3 4 ... 15 0" or "1,2,3,...,15,0" into a State tuple.

    You may use this for your own testing. You do NOT need to modify this.
    """
    parts = s.replace(",", " ").split()
    nums = [int(p) for p in parts]
    if len(nums) != 16:
        raise ValueError(f"State must have exactly 16 numbers, got {len(nums)}")
    if sorted(nums) != list(range(16)):
        raise ValueError("State must contain exactly the numbers 0..15")
    return tuple(nums)


def pretty_print_state(state: State) -> str:
    """
    Return a string representation of the circular state.

    You do NOT need to modify this.
    """
    return " ".join(f"{x:2d}" for x in state)


class Circular16Puzzle:
    """
    Circular 16 Puzzle:
    - State: 16 tiles (0..15) arranged in a circle.
    - Goal: (1, 2, ..., 15, 0)
    - Move: choose a block of 4 consecutive positions on the circle and
      rotate it clockwise or counterclockwise by 1.
    - Step cost: 1 for every move.

    This class is fully implemented for you.
    """

    GOAL: State = tuple(range(1, 16)) + (0,)

    def __init__(self, initial_state: State):
        if len(initial_state) != 16:
            raise ValueError("Initial state must have length 16")
        if sorted(initial_state) != list(range(16)):
            raise ValueError("Initial state must contain exactly 0..15")
        self.initial_state: State = tuple(initial_state)

    def is_goal(self, state: State) -> bool:
        return state == self.GOAL

    def successors(self, state: State) -> List[Tuple[State, Action, int]]:
        """
        Generate all successor states from the given state.
        Returns a list of (next_state, action_label, step_cost) triples.

        You do NOT need to modify this.
        """
        N = 16
        BLOCK = 4
        succs: List[Tuple[State, Action, int]] = []

        for start in range(N):
            idxs = [(start + i) % N for i in range(BLOCK)]

            # Clockwise rotation
            s = list(state)
            last = s[idxs[-1]]
            for i in range(BLOCK - 1, 0, -1):
                s[idxs[i]] = s[idxs[i - 1]]
            s[idxs[0]] = last
            succs.append((tuple(s), f"cw({start})", 1))

            # Counterclockwise rotation (inverse 4-cycle)
            s = list(state)
            first = s[idxs[0]]
            for i in range(BLOCK - 1):
                s[idxs[i]] = s[idxs[i + 1]]
            s[idxs[-1]] = first
            succs.append((tuple(s), f"ccw({start})", 1))

        return succs


# Precompute goal positions for heuristics (you may use this in your heuristics)
GOAL_STATE: State = Circular16Puzzle.GOAL
GOAL_POS: Dict[int, int] = {tile: idx for idx, tile in enumerate(GOAL_STATE)}

# ---------------------------------------------------------------------------
# Heuristics (TODO)
# ---------------------------------------------------------------------------

def heuristic_misplaced(state: State) -> int:
    """
    h1: count of tiles that are not in their goal position (excluding the blank 0).

    TODO:
    - Implement this heuristic.
    - Do NOT modify the function name or signature.

    Hint:
    - Iterate over positions and tiles using: for i, tile in enumerate(state):
    - Skip tile 0 (the blank).
    - Compare tile with GOAL_STATE[i].
    """
    count = 0

    # Count tiles that are out of place, ignoring the blank (0)
    for i, tile in enumerate(state):
        if tile == 0:
            continue
        if tile != GOAL_STATE[i]:
            count += 1

    return count


def heuristic_circular_distance(state: State) -> int:
    """
    h2: sum of minimal circular distances for each tile from its goal index.
    Distance is measured around the 16-position circle.

    TODO:
    - Implement this heuristic using GOAL_POS and the circular distance.
    - Do NOT modify the function name or signature.

    Hint:
    - For each tile (except 0), find its goal index: g = GOAL_POS[tile]
    - The circular distance between i and g on a 16-position circle is:
        d = abs(i - g)
        contribution = min(d, 16 - d)
    """
    N = 16
    total = 0

    # Sum minimal circular distance for each non-blank tile
    for i, tile in enumerate(state):
        if tile == 0:
            continue
        g = GOAL_POS[tile]
        d = abs(i - g)
        total += min(d, N - d)

    return total


# ---------------------------------------------------------------------------
# Search utilities (provided)
# ---------------------------------------------------------------------------

def reconstruct_path(
    parent: Dict[State, Tuple[State, Action]],
    start: State,
    goal: State,
) -> List[Action]:
    """
    Reconstruct the sequence of actions from start to goal using a parent dict:
    parent[state] = (parent_state, action_used_to_reach_state)

    You do NOT need to modify this.
    """
    actions: List[Action] = []
    s = goal
    while s != start:
        prev, action = parent[s]
        actions.append(action)
        s = prev
    actions.reverse()
    return actions


def make_result(
    actions: List[Action],
    goal_state: State,
    nodes_expanded: int,
    max_frontier_size: int,
) -> SearchResult:
    """
    Package search result statistics into a dictionary.

    You do NOT need to modify this.
    """
    return {
        "actions": actions,
        "goal_state": goal_state,
        "nodes_expanded": nodes_expanded,
        "solution_cost": len(actions),
        "max_frontier_size": max_frontier_size,
    }


# ---------------------------------------------------------------------------
# Uninformed search algorithms (TODO)
# ---------------------------------------------------------------------------

def breadth_first_search(problem: Circular16Puzzle) -> SearchResult | None:
    """
    Breadth-First Search (BFS) with unit step costs.

    TODO:
    - Implement BFS using a queue (collections.deque).
    - Track:
        nodes_expanded: number of states you REMOVE from the frontier and expand
        max_frontier_size: maximum size of the frontier at any time
    - Use reconstruct_path and make_result to build the final answer.

    Skeleton:
    1. Initialize:
        start = problem.initial_state
        if start is goal: return a trivial result
        frontier = deque([start])
        visited = {start}
        parent = {start: (start, "")}
        nodes_expanded = 0
        max_frontier_size = 1
    2. While frontier not empty:
        - Update max_frontier_size
        - Pop a state from the frontier (popleft)
        - Increment nodes_expanded
        - For each successor (next_state, action, cost):
            * If not visited:
                - Set parent[next_state] = (state, action)
                - If next_state is goal: reconstruct and return result
                - Mark next_state visited and add to frontier
    3. If loop ends with no solution, return None.
    """
    start = problem.initial_state

    # Base case: already at goal
    if problem.is_goal(start):
        return make_result([], start, nodes_expanded=0, max_frontier_size=1)

    frontier: deque[State] = deque()
    frontier.append(start)

    visited: set[State] = set()
    visited.add(start)

    parent: Dict[State, Tuple[State, Action]] = {start: (start, "")}

    nodes_expanded = 0
    max_frontier_size = 1

    while frontier:
        # Update max frontier size
        max_frontier_size = max(max_frontier_size, len(frontier))

        # Pop from frontier and expand
        state = frontier.popleft()
        nodes_expanded += 1

        # Generate successors
        for next_state, action, cost in problem.successors(state):
            # Skip already visited states
            if next_state in visited:
                continue

            # Record how we reached next_state
            parent[next_state] = (state, action)

            # If this successor is the goal, reconstruct and return
            if problem.is_goal(next_state):
                actions = reconstruct_path(parent, start, next_state)
                return make_result(actions, next_state, nodes_expanded, max_frontier_size)

            # Mark visited and add to frontier
            visited.add(next_state)
            frontier.append(next_state)

    # If no solution is found
    return None


def uniform_cost_search(problem: Circular16Puzzle) -> SearchResult | None:
    """
    Uniform Cost Search (UCS).

    TODO:
    - Implement UCS using a priority queue (heapq).
    - The priority should be the current path cost g(s).
    - Track:
        nodes_expanded
        max_frontier_size
    - Use reconstruct_path and make_result to build the final answer.

    Skeleton:
    1. Initialize:
        start = problem.initial_state
        if start is goal: return trivial result
        frontier = priority queue of (g, state), starting with (0, start)
        best_cost = {start: 0}
        parent = {start: (start, "")}
        nodes_expanded = 0
        max_frontier_size = 1
    2. While frontier not empty:
        - Pop (g, state) with smallest g
        - If this g is worse than best_cost[state], skip (stale entry)
        - If state is goal: reconstruct and return result
        - Increment nodes_expanded
        - For each successor (next_state, action, cost):
            new_g = g + cost
            if new_g < best_cost.get(next_state, inf):
                update best_cost and parent, push (new_g, next_state) to frontier
    3. If loop ends with no solution, return None.
    """
    start = problem.initial_state

    if problem.is_goal(start):
        return make_result([], start, nodes_expanded=0, max_frontier_size=1)

    frontier: List[Tuple[int, State]] = []
    heapq.heappush(frontier, (0, start))

    best_cost: Dict[State, int] = {start: 0}
    parent: Dict[State, Tuple[State, Action]] = {start: (start, "")}

    nodes_expanded = 0
    max_frontier_size = 1

    while frontier:
        max_frontier_size = max(max_frontier_size, len(frontier))

        # Pop the lowest-cost state from the priority queue
        g, state = heapq.heappop(frontier)

        # Skip stale entries if g > best_cost[state]
        if g > best_cost.get(state, float("inf")):
            continue

        # Goal test
        if problem.is_goal(state):
            actions = reconstruct_path(parent, start, state)
            return make_result(actions, state, nodes_expanded, max_frontier_size)

        nodes_expanded += 1

        # Expand successors
        for next_state, action, cost in problem.successors(state):
            new_g = g + cost
            if new_g < best_cost.get(next_state, float("inf")):
                best_cost[next_state] = new_g
                parent[next_state] = (state, action)
                heapq.heappush(frontier, (new_g, next_state))

    return None


# ---------------------------------------------------------------------------
# Informed search algorithms (TODO)
# ---------------------------------------------------------------------------

def greedy_best_first_search(
    problem: Circular16Puzzle,
    heuristic: Callable[[State], int],
) -> SearchResult | None:
    """
    Greedy Best-First Search using the given heuristic h(s).

    TODO:
    - Implement Greedy Best-First Search using a priority queue (heapq).
    - The priority should be h(s) only (ignore path cost g).
    - Track:
        nodes_expanded
        max_frontier_size
    - Use reconstruct_path and make_result to build the final answer.

    Skeleton:
    1. Initialize:
        start = problem.initial_state
        if start is goal: return trivial result
        frontier = priority queue of (h(start), start)
        parent = {start: (start, "")}
        visited = empty set (or you can treat closed set)
        nodes_expanded = 0
        max_frontier_size = 1
    2. While frontier not empty:
        - Pop (h, state) with smallest h
        - If state already visited: continue
        - Mark state visited
        - If state is goal: reconstruct and return result
        - Increment nodes_expanded
        - For each successor:
            * If not visited, set parent and push (h(next_state), next_state) on frontier
    3. If loop ends with no solution, return None.
    """
    start = problem.initial_state

    if problem.is_goal(start):
        return make_result([], start, nodes_expanded=0, max_frontier_size=1)

    frontier: List[Tuple[int, State]] = []
    heapq.heappush(frontier, (heuristic(start), start))

    parent: Dict[State, Tuple[State, Action]] = {start: (start, "")}
    visited: set[State] = set()

    nodes_expanded = 0
    max_frontier_size = 1

    while frontier:
        max_frontier_size = max(max_frontier_size, len(frontier))

        # Pop the state with smallest heuristic value
        h_val, state = heapq.heappop(frontier)

        # Skip if already visited
        if state in visited:
            continue

        # Mark state as visited
        visited.add(state)

        # Goal test
        if problem.is_goal(state):
            actions = reconstruct_path(parent, start, state)
            return make_result(actions, state, nodes_expanded, max_frontier_size)

        nodes_expanded += 1

        # Expand successors
        for next_state, action, cost in problem.successors(state):
            if next_state not in visited:
                parent[next_state] = (state, action)
                heapq.heappush(frontier, (heuristic(next_state), next_state))

    return None


def a_star_search(
    problem: Circular16Puzzle,
    heuristic: Callable[[State], int],
) -> SearchResult | None:
    """
    A* search with f(s) = g(s) + h(s).

    TODO:
    - Implement A* search using a priority queue (heapq).
    - You must maintain g(s) = path cost so far for each state.
    - The priority should be f(s) = g(s) + h(s).
    - Track:
        nodes_expanded
        max_frontier_size
    - Use reconstruct_path and make_result to build the final answer.

    Skeleton:
    1. Initialize:
        start = problem.initial_state
        if start is goal: return trivial result
        frontier = priority queue of (f0, g0, start) where g0 = 0 and f0 = h(start)
        g_cost = {start: 0}
        parent = {start: (start, "")}
        closed = empty set
        nodes_expanded = 0
        max_frontier_size = 1
    2. While frontier not empty:
        - Pop (f, g, state) with smallest f
        - If state in closed: continue
        - Add state to closed
        - If state is goal: reconstruct and return result
        - Increment nodes_expanded
        - For each successor:
            * Compute new_g = g + cost
            * If new_g < g_cost.get(next_state, inf):
                - Update g_cost[next_state] = new_g
                - Update parent[next_state]
                - Compute new_f = new_g + heuristic(next_state)
                - Push (new_f, new_g, next_state) to frontier
    3. If loop ends with no solution, return None.
    """
    start = problem.initial_state

    if problem.is_goal(start):
        return make_result([], start, nodes_expanded=0, max_frontier_size=1)

    frontier: List[Tuple[int, int, State]] = []
    g_cost: Dict[State, int] = {start: 0}
    parent: Dict[State, Tuple[State, Action]] = {start: (start, "")}

    f0 = heuristic(start)
    heapq.heappush(frontier, (f0, 0, start))

    closed: set[State] = set()

    nodes_expanded = 0
    max_frontier_size = 1

    while frontier:
        max_frontier_size = max(max_frontier_size, len(frontier))

        # Pop state with smallest f
        f, g, state = heapq.heappop(frontier)

        # Skip if state already in closed
        if state in closed:
            continue

        # Add state to closed
        closed.add(state)

        # Goal test
        if problem.is_goal(state):
            actions = reconstruct_path(parent, start, state)
            return make_result(actions, state, nodes_expanded, max_frontier_size)

        nodes_expanded += 1

        # Expand successors
        for next_state, action, cost in problem.successors(state):
            new_g = g + cost
            if new_g < g_cost.get(next_state, float("inf")):
                g_cost[next_state] = new_g
                parent[next_state] = (state, action)
                new_f = new_g + heuristic(next_state)
                heapq.heappush(frontier, (new_f, new_g, next_state))

    return None


# ---------------------------------------------------------------------------
# Simple demo (optional for students)
# ---------------------------------------------------------------------------

def run_demo() -> None:
    """
    Simple demo for your own testing.
    You may modify this for debugging, but it will not be graded directly.
    """
    initial = (5, 1, 3, 4, 2, 6, 7, 8, 9, 11, 12, 10, 15, 13, 14, 0)
    problem = Circular16Puzzle(initial)

    print("Initial state:")
    print(pretty_print_state(initial))
    print()

    print("Running BFS...")
    bfs_res = breadth_first_search(problem)
    print("BFS result:", bfs_res)
    print()

    print("Running UCS...")
    ucs_res = uniform_cost_search(problem)
    print("UCS result:", ucs_res)
    print()

    print("Running Greedy (misplaced)...")
    greedy_mis = greedy_best_first_search(problem, heuristic_misplaced)
    print("Greedy (misplaced) result:", greedy_mis)
    print()

    print("Running Greedy (circular distance)...")
    greedy_circ = greedy_best_first_search(problem, heuristic_circular_distance)
    print("Greedy (circular) result:", greedy_circ)
    print()

    print("Running A* (misplaced)...")
    astar_mis = a_star_search(problem, heuristic_misplaced)
    print("A* (misplaced) result:", astar_mis)
    print()

    print("Running A* (circular distance)...")
    astar_circ = a_star_search(problem, heuristic_circular_distance)
    print("A* (circular) result:", astar_circ)
    print()


if __name__ == "__main__":
    run_demo()
