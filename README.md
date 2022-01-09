# Ex4_oop
![alt text](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRUC7G6cLvCjY5-Sq4vRcieUJc_O4KjwMl8NQEKDTrAElDHc2178puykOjpVgY8XRASD_M&usqp=CAU)
![Pokemon_icon](https://user-images.githubusercontent.com/79272744/148688292-072e42a1-86b1-471b-a2f9-1a20844f9e48.png)

# Ex4
>Made by Yehonatan Barel and Nadav Moyal.
>
>GitHub pages: 
>
>https://github.com/nadavmoyal
>
>https://github.com/yehonatanbarel    

## Introduction:
This project is an assignment in an object-oriented course at Ariel University. We build the project with MVC design pattern and it's consists of two main parts: The first part is to find a way to get the agent to the pokemon as fast as possible and the second part
The second part of the project is to bulid a resizable GUI visualization,so that we can see in real time the movement of the agent towards the Pokemon according to the algorithm we have built.

## Operating Instructions:
1. Download the jar file.
2. Put the data file in the same folder.
3. In the command line, write the following command:
"java -jar Ex4.jar "game_level_input"
4. run the Ex4.py file

# Description of the classes:


## Class Node implements NodeData:
##### This class represents the set of operations applicable on a node (vertex) in a (directional) weighted graph.

|          Methods                | Details                             | 
| --------------------------------|:--------------------------------------:| 
|`get_key()`|Returns the key (id) associated with this node.|
|`get_dist()`| get the dist of a given node.|
|`get_dist()`| allow to set the dist of a given node.|
|`get_visited`| tell us if the node have been visited or not.|
|`set_visited`| allow us to the node visited mode (True \ False).|
|`get_pos()`|Returns the location of this node, if none return None.| 
|`set_pos(x,y,z)`|Allows changing this node's location.|
|`get_x`| get the X location of the node.|
|`get_y`| get the Y location of the node.|


## Class DiGraph implements GraphInterface:
##### This class represents the set of operations applicable on a directional edge (src,dest) in a (directional) weighted graph.
                                 
|          Methods                | Details                             | 
| --------------------------------|:--------------------------------------:| 
|`v_size()`| Returns the number of vertices in this graph.| 
|`e_size()`| Returns the number of edges in this graph|
|`get_all_v()`|return a dictionary of all the nodes in the Graph, each node is represented using a pair (node_id, node_data).| 
|`all_in_edges_of_node()`| return a dictionary of all the nodes connected to (into) node_id ,each node is represented using a pair (other_node_id, weight)| 
|`all_out_edges_of_node()`|return a dictionary of all the nodes connected from node_id , each node is represented using a pair (other_node_id, weight).| 
|`get_mc()`| Returns the current version of this graph, on every change in the graph state - the MC should be increased .|   
|`add_node()`| Adds a node to the graph.|
|`remove_node()`| Removes a node from the graph.|
|`remove_edge()`| Removes an edge from the graph.|

## Class  GraphAlgo implements GraphAlgoInterface:
##### This class represents a Directional Weighted Graph.
 
|          Methods                | Details                             | 
| --------------------------------|:--------------------------------------:| 
|`get_graph()`| return the directed graph on which the algorithm works on.| 
|`load_from_json()`|Loads a graph from a json file.|
|`save_to_json()`|Saves the graph in JSON format to a file.| 
|`shortest_path()`|Returns the shortest path from node id1 to node id2 using Dijkstra's Algorithm.| 
|`TSP()`|Finds the shortest path that visits all the nodes in the list.| 
|`centerPoint()`|Finds the node that has the shortest distance to it's farthest node.|   
|`plot_graph()`| Plots the graph.|

explanation about the algorithms we use in order to find the best agent to each pokemon you can see on our [wiki page](https://github.com/nadavmoyal/oop-Ex3/wiki).
## We did tests to check them


## We did resizable GUI visualization
![git_gif](https://user-images.githubusercontent.com/79272744/148691324-07f33235-04aa-4d5b-abd7-450a9e710c4e.gif)



