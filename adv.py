from room import Room
from player import Player
from world import World
from util import Queue
import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

reverse_direction = {
    'n': 's',
    's': 'n',
    'e': 'w',
    'w': 'e',
}

# initialize a graph object to hold our traversed maze
graph = {}

def bfs(graph, starting_room):
    # create an empty queue to hold rooms
    q = Queue()
    # create an empty set to store visited rooms
    visited_set = set()
    # enqueue a path to the starting room
    q.enqueue([starting_room])
    # while the queue is not empty
    while q.size():
        # dequeue the first path from the front of the list
        path = q.dequeue()
        # get the last room in the path
        room_to_check = path[-1]
        # if room to check is not in visited set:
        if room_to_check not in visited_set:
            # add the room to visited
            visited_set.add(room_to_check)
            # check if room to check has any unexplored exits
            for room in graph[room_to_check]:
                # if unexplored
                if graph[room_to_check][room] == '?':
                    # return the path taken to get here
                    return path
            # append paths
            for each_exit in graph[room_to_check]:
                # set the exit to be tracked to a variable
                neighboring_room = graph[room_to_check][each_exit]
                # make a copy of the path
                new_path = list(path)
                # add the neighboring room to the copied path
                new_path.append(neighboring_room)
                # enqueue the path taken
                q.enqueue(new_path)


# while graph is smaller than the given 500
while len(graph) < len(room_graph):
    # save the current room id into a variable
    current_room_id = player.current_room.id
    # if the current_room_id is not in the graph yet
    if current_room_id not in graph:
        # place the room in the graph with no exits yet
        graph[current_room_id] = {}
        # for each available exit in the room
        for available_exit in player.current_room.get_exits():
            # set all exit values to '?' the first time visiting the room
            graph[current_room_id][available_exit] = "?"
    # at this point room exists in graph or has been created, if new
    # for each available exit in the room
    for direction in graph[current_room_id]:
        # if direction is not permissible from the room
        if direction not in graph[current_room_id]:
            break
        # if direction is permissible but still "?"
        if graph[current_room_id][direction] == '?':
            # set the room's exit to the direction
            room_exit = direction
            # if there is an exit in the dictionary
            if room_exit is not None:
                # append the travel direction to traversal_path
                traversal_path.append(room_exit)
                # move in that direction
                player.travel(room_exit)
                # set new room id to the current room
                new_room_id = player.current_room.id
                # if the new_room_id is not in the graph yet
                if new_room_id not in graph:
                    # add the room into graph
                    graph[new_room_id] = {}
                    # for each available exit in the room
                    for available_exit in player.current_room.get_exits():
                        # set all exit values to '?' the first time visiting the room
                        graph[new_room_id][available_exit] = '?'
            # update previous room's direction/exit
            graph[current_room_id][room_exit] = new_room_id
            # update current room's direction/exit to be opposite
            graph[new_room_id][reverse_direction[room_exit]] = current_room_id
            # Sst the current_room_id to the new room id
            current_room_id = new_room_id

    # utilize BFS, passing in graph and current room
    path_of_rooms = bfs(graph, player.current_room.id)
    # convert rooms to directions by traversing all rooms in the path_of_rooms and recording which direction was traveled
    if path_of_rooms is not None:
        # for each room in the path_of_rooms
        for room in path_of_rooms:
            # for each {n, s, e, w} of each room in path_of_rooms
            for available_exit in graph[current_room_id]:
                # if the available_exit's value is the room in path_of_rooms
                if graph[current_room_id][available_exit] == room:
                    # add this available_exit to traversal list
                    traversal_path.append(available_exit)
                    # move in that direction
                    player.travel(available_exit)
    # reset the current_room_id to be the room just moved into
    current_room_id = player.current_room.id


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
