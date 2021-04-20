import networkx as nx
from parse import read_input_file, write_input_file, write_output_file, ten_in_builder
from utils import is_valid_solution, calculate_happiness
import sys
import copy
import random 


def solve(G, s, f):
    """
    Args:
        G: networkx.Graph
        s: stress_budget
    Returns:
        D: Dictionary mapping for student to breakout room r e.g. {0:2, 1:0, 2:1, 3:2}
        k: Number of breakout rooms
    """
    # setting up list of attributes according to edge. I.e attributelist[0] = [happiness of i to j, stress of i to j, i, j]
    overall = 0
    edgelist = list(G.edges)
    num_vertices = len(list(G.nodes))
    attributelist = []
    for i in range(len(edgelist)):
        attributelist.append([G.edges[edgelist[i][0], edgelist[i][1]]["happiness"], G.edges[edgelist[i][0], edgelist[i][1]]["stress"],  edgelist[i][0], edgelist[i][1]])
    attributelist.sort(reverse = True, key = helper)
    att_list_copy = copy.deepcopy(attributelist)
    
    k = 1 #number of breakout rooms, initialized to 1 to start
    i = 0 # number of vertices we've added already
    counter = 0 #what room we are on
    room_list = [] # roomlist[0] = [[<vertices in room 0>], happiness of room 0, stress of room 0]
    #print(att_list_copy)

    while (i < num_vertices):
        # print("second k:", k)
        # print("second counter:", counter)
        while (k > counter):
            # print("here")
            room_list.append([[], 0, 0]) #index 0 = list of vertices, index 1 = total room happiness, index 2 = total room stress
            while (room_list[counter][2] < s/k and i < num_vertices and len(att_list_copy) > 0):

                current_room = room_list[counter]
                stress = nx.get_edge_attributes(G,'stress')
                happiness = nx.get_edge_attributes(G,'happiness')
                stress_to_add = att_list_copy[0][1]
                happiness_to_add = att_list_copy[0][0]
                #print(current_room)
                for m in range(len(current_room[0])): #compute the stress of the newly added vertice to the room with every other vertice in the room
                    if (current_room[0][m] != att_list_copy[0][3] and att_list_copy[0][2] not in current_room[0]):
                        
                        if (current_room[0][m] < att_list_copy[0][2]):
                            #print(stress[(current_room[0][m], att_list_copy[0][2])])
                            stress_to_add  += stress[(current_room[0][m], att_list_copy[0][2])]
                            happiness_to_add += happiness[(current_room[0][m], att_list_copy[0][2])]

                        if (current_room[0][m] > att_list_copy[0][2]):
                            #print(stress[(att_list_copy[0][2], current_room[0][m])])
                            stress_to_add  += stress[(att_list_copy[0][2], current_room[0][m])]
                            happiness_to_add += happiness[(att_list_copy[0][2], current_room[0][m])]

                    if ((current_room[0][m] != att_list_copy[0][2]) and att_list_copy[0][3] not in current_room[0]):

                        if (current_room[0][m] < att_list_copy[0][3]):
                            #print(stress[(current_room[0][m], att_list_copy[0][3])])
                            stress_to_add  += stress[(current_room[0][m], att_list_copy[0][3])]
                            happiness_to_add += happiness[(current_room[0][m], att_list_copy[0][3])]

                        if (current_room[0][m] > att_list_copy[0][3]):
                            #print(stress[(att_list_copy[0][3], current_room[0][m])])
                            stress_to_add  += stress[(att_list_copy[0][3], current_room[0][m])]
                            happiness_to_add += happiness[(att_list_copy[0][3], current_room[0][m])]

                #print("TOTAL", stress_to_add)
                if (stress_to_add + current_room[2] > s/k): #if stress of new edge exceeds current room stress
                    counter += 1
                    for z in range(len(current_room[0])):#  remove all instances of this vertice from the rest of the list
                        end = len(att_list_copy)
                        q = 0
                        while (q < end):
                            if (current_room[0][z] == att_list_copy[q][2] or current_room[0][z] == att_list_copy[q][3]):
                                att_list_copy.pop(q)
                                end -= 1
                                q -= 1
                            q += 1
                    break
        
                current_room[1] += happiness_to_add # add the happiness of the new edge to the total rooms happiness
                current_room[2] += stress_to_add  #add the stress of the edge to the total room stress

                #add the new vertice without avoiding double ups of vertices in the same room

                #remove all permuations from copy
                for m in range(len(current_room[0])): #compute the stress of the newly added vertice to the room with every other vertice in the room
                    if (current_room[0][m] != att_list_copy[0][3]):
                        if (current_room[0][m] < att_list_copy[0][2]):
                            end = len(att_list_copy)
                            q = 0
                            while (q < end):
                                if (current_room[0][m] == att_list_copy[q][2] and att_list_copy[0][2] == att_list_copy[q][3]):
                                    att_list_copy.pop(q)
                                    break
                                q+=1

                        if (current_room[0][m] > att_list_copy[0][2]):
                            end = len(att_list_copy)
                            q = 0
                            while (q < end):
                                if (att_list_copy[0][2] == att_list_copy[q][2] and current_room[0][m] == att_list_copy[q][3]):
                                    att_list_copy.pop(q)
                                    break
                                q+=1
                            
                    if ((current_room[0][m] != att_list_copy[0][2])):

                        if (current_room[0][m] < att_list_copy[0][3]):
                            end = len(att_list_copy)
                            q = 0
                            while (q < end):
                                if (att_list_copy[0][3] == att_list_copy[q][2] and current_room[0][m] == att_list_copy[q][3]):
                                    att_list_copy.pop(q)
                                    break
                                q+=1

                        if (current_room[0][m] > att_list_copy[0][3]):
                            end = len(att_list_copy)
                            q = 0
                            while (q < end):
                                if (current_room[0][m] == att_list_copy[q][2] and att_list_copy[0][3] == att_list_copy[q][3]):
                                    att_list_copy.pop(q)
                                    break
                                q+=1

                if att_list_copy[0][2] not in current_room[0]: 
                    current_room[0].append(att_list_copy[0][2])
                    i += 1
                if att_list_copy[0][3] not in current_room[0]:
                    current_room[0].append(att_list_copy[0][3])
                    i += 1

                att_list_copy.pop(0)

                if (i  >= num_vertices): # if a solution has been reached, break out of loop
                    break
                        
            if (i  >= num_vertices): # if a solution has been reached, break out of loop
                break

        if (i < num_vertices):
            k += 1
            # if s/k is less than the minimum possible then have a different helper sort it
            if (k > num_vertices/2 and overall <= 25):
                attributelist.sort(reverse = False, key = helper2)
                att_list_copy = copy.deepcopy(attributelist)
                k = 1
            elif (overall > 25):
                random.shuffle(attributelist)
                att_list_copy = copy.deepcopy(attributelist)
                k = 1
            else:
                att_list_copy = copy.deepcopy(attributelist)
            room_list.clear()
            
            print(overall)
            overall+=1
            i = 0
            counter = 0

    # print(room_list)
    # print(len(room_list))
    # print("s/k:", s / len(room_list))

    c = 0
    r = {}
    while (c < num_vertices):
        for d in range(len(room_list)):
            if (c in room_list[d][0]):
                r[c] = d
        c += 1
    write_output_file(r, f + ".out", num_vertices)

def helper(list):
    if (list[1] != 0):
        return list[0]/list[1]
    else:
        return list[0]

def helper2(list):
    return list[1]/(list[2] + 1)

# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

# if __name__ == '__main__':
#     assert len(sys.argv) == 2
#     path = sys.argv[1]
#     G, s = read_input_file(path)
#     D, k = solve(G, s)
#     assert is_valid_solution(D, G, s, k)
#     print("Total Happiness: {}".format(calculate_happiness(D, G)))
#     write_output_file(D, 'out/test.out')


# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
# if __name__ == '__main__':
#     inputs = glob.glob('file_path/inputs/*')
#     for input_path in inputs:
#         output_path = 'file_path/outputs/' + basename(normpath(input_path))[:-3] + '.out'
#         G, s = read_input_file(input_path, 100)
#         D, k = solve(G, s)
#         assert is_valid_solution(D, G, s, k)
#         cost_t = calculate_happiness(T)
#         write_output_file(D, output_path)

def main():
    G = nx.Graph()
    tom = ten_in_builder(G)
    solve(tom,28, "testing")

if __name__ == "__main__":
    main()
