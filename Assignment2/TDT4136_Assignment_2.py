from Map import Map_Obj
from queue import PriorityQueue

def search(task):
  # Initialize the map, fills inn start and goal, gets the start and goal position
  # Performs an A* search
  # Then export the map as png
  samfundet = Map_Obj(task)
  samfundet.fill_critical_positions(task)
  startpos = samfundet.get_start_pos()
  goalpos = samfundet.get_goal_pos()
  a_star(startpos, goalpos, samfundet)
  samfundet.show_map()

def heuristic(a, b):
   # Manhattan distance on a square grid
   return abs(a[0] - b[0]) + abs(a[1] - b[1])

def neighbors(pos):
   # Returns the four neighbours of a position
   # (x, y) = pos
   # return [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
   return [(pos[0]+1, pos[1]), (pos[0]-1, pos[1]), (pos[0], pos[1]+1), (pos[0], pos[1]-1)]

def a_star(start, goal, map):
  # Implementation of the A* algorithm
  frontier = PriorityQueue()
  frontier.put((0, start))
  came_from = dict()
  cost_so_far = dict()
  came_from[tuple(start)] = None
  cost_so_far[tuple(start)] = 0

  while not frontier.empty():
    current = tuple(frontier.get()[1])

    #when the goal is reached, backtrack and color the path
    if current == tuple(goal):
      print("Path Cost:", cost_so_far[tuple(goal)])
      backtracker = came_from[tuple(goal)]
      while backtracker != tuple(start):
        map.set_cell_value(backtracker, 2)
        if backtracker is not None:
            backtracker = came_from[backtracker]
      break
    # for each neighbor of the current position, check if it is a valid position and find the cost, putting it in the prioritized frontier
    for neighbor in neighbors(current):

      if map.get_cell_value(neighbor) != -1:
        new_cost = cost_so_far[current] + map.get_cell_value(current)
        if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
          cost_so_far[neighbor] = new_cost
          priority = new_cost + heuristic(neighbor, goal)
          frontier.put((priority,neighbor))
          came_from[neighbor] = current

def run(task):
  match task:
      case 1:
        search(1)
      case 2:
        search(2)
      case 3:
        search(3)
      case 4:
        search(4)

if __name__ == "__main__":
  task = int(input("Enter task number: "))
  run(task)