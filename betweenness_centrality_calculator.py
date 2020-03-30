#!/usr/bin/env python3

"""
This class is defined to return the top K nodes, their Standard Betweenness Centrality and the value of k
It takes as input, a list containing the vertices of the graph and a list having its elements as the edges, 
in the form of 2-tuples.
"""


import re
import itertools
import copy

ROLLNUM_REGEX = "201[0-9]{4}"

class Graph(object):
    name = "Ruhma Mehek Khan"
    email = "ruhma18362@iiitd.ac.in"
    roll_num = "2018362"

    def __init__ (self, vertices, edges):
        """
        Initializes object for the class Graph

        Args:
            vertices: List of integers specifying vertices in graph
            edges: List of 2-tuples specifying edges in graph
        """
        unvisited=copy.deepcopy(vertices)
        Distances=[]
        level1={}
        for i in vertices:
            level1[i]=[]
        for i in unvisited:
                #visited.append(i)
                for j in range(0, len(edges)):
                    if i in edges[j]:
                                for k in edges[j]:
                                        if k!=i:
                                                level1[i].append(k)
        Distances.append(level1)

        #Level1 is a dictionary storing all nodes at distance one from the node. i.e. the immediate neighbours.

        for i in Distances[-1]:
            if len(Distances[-1][i])!=len(vertices)-1:
                level2={}
                for i in Distances[-1]:
                    level2[i]=[]
                    for j in Distances[-1][i]:
                        for k in Distances[0][j]:
                            if k not in level2[i] and k!=i:
                                level2[i].append(k)
                                for i in level2:
                                    level2[i].sort()
            else:
                continue
            Distances.append(level2)

            #Here, Distances is a list, whose elements are dictionaries storing the vertices at various distances from the 'key' vertex.

        self.vertices = vertices
        
        ordered_edges = list(map(lambda x: (min(x), max(x)), edges))
        
        self.edges    = ordered_edges

        self.Distances=Distances
        self.unvisited=unvisited
        
        self.validate()


    def __str__(self):
    	"""
    	This function helps print the output of the class Graph in the required format.

    	"""

    	return self.top_k_betweenness_centrality()

    def validate(self):
        """
        Validates if Graph if valid or not

        Raises:
            Exception if:
                - Name is empty or not a string
                - Email is empty or not a string
                - Roll Number is not in correct format
                - vertices contains duplicates
                - edges contain duplicates
                - any endpoint of an edge is not in vertices
        """

        if (not isinstance(self.name, str)) or self.name == "":
            raise Exception("Name can't be empty")

        if (not isinstance(self.email, str)) or self.email == "":
            raise Exception("Email can't be empty")

        if (not isinstance(self.roll_num, str)) or (not re.match(ROLLNUM_REGEX, self.roll_num)):
            raise Exception("Invalid roll number, roll number must be a string of form 201XXXX. Provided roll number: {}".format(self.roll_num))

        if not all([isinstance(node, int) for node in self.vertices]):
            raise Exception("All vertices should be integers")

        elif len(self.vertices) != len(set(self.vertices)):
            duplicate_vertices = set([node for node in self.vertices if self.vertices.count(node) > 1])

            raise Exception("Vertices contain duplicates.\nVertices: {}\nDuplicate vertices: {}".format(vertices, duplicate_vertices))

        edge_vertices = list(set(itertools.chain(*self.edges)))

        if not all([node in self.vertices for node in edge_vertices]):
            raise Exception("All endpoints of edges must belong in vertices")

        if len(self.edges) != len(set(self.edges)):
            duplicate_edges = set([edge for edge in self.edges if self.edges.count(edge) > 1])

            raise Exception("Edges contain duplicates.\nEdges: {}\nDuplicate vertices: {}".format(edges, duplicate_edges))


    def flatten(self,S):

        """
        A recursive function that flattens out the inputted nested lists and returns a single list.

        Args:
        The nested list that needs to be flattened out.

        Output:
        A single list containing all the elements of the nested list.
        
        """

        if S == []:
            a= S
            return a
        if isinstance(S[0], list):
            b= self.flatten(S[0]) + self.flatten(S[1:])
            return b
        c= S[:1] + self.flatten(S[1:])
        return c

    def min_dist(self, start_node, end_node):
        '''
        Finds minimum distance between start_node and end_node

        Args:
            start_node: Vertex to find distance from
            end_node: Vertex to find distance to

        Returns:
            An integer denoting minimum distance between start_node
            and end_node
        '''

        flag=0
        for i in range(len(self.Distances)):
                if end_node in self.Distances[i][start_node]:
                    minimum_distance=i+1
                    flag=1
                    return minimum_distance

    def all_paths(self, node, destination, dist, path):

        """
        Finds all paths from node to destination with length = dist

        Args:
            node: Node to find path from
            destination: Node to reach
            dist: Allowed distance of path
            path: path already traversed

        Returns:
            List of path, where each path is list ending on destination

            Returns None if there no paths
        """

        path=path+[node]
        if (len(path)-1) == dist:
                if node == destination:
                        return path
                else:
                        return None

        my_paths = []

        for next_node in self.Distances[0][node]:
                if next_node not in path:
                        returned_paths = self.all_paths(next_node, destination, dist, path)
                        if returned_paths is not None:
                                my_paths=my_paths+[returned_paths]

        if len(my_paths) != 0:
                return my_paths
        else:
                return None

        #Finds all shortest paths between start_node and end_node
    def all_shortest_paths(self, start_node, end_node):
        """
        Finds all shortest paths between start_node and end_node

        Args:
            start_node: Starting node for paths
            end_node: Destination node for paths

        Returns:
            A list of path, where each path is a list of integers.
        """
        dist = self.min_dist(start_node, end_node)
        paths = self.all_paths(start_node, end_node, dist, [])
        return paths
    def betweenness_centrality(self, node):

        """
        Find betweenness centrality of the given node

        Args:
            node: Node to find betweenness centrality of.

        Returns:
            Single floating point number, denoting betweenness centrality
            of the given node
        """

        vertices_required=copy.deepcopy(self.vertices)
        vertices_required.remove(node)
        k=[]
        for i in vertices_required:
            for j in vertices_required:
                if i != j and self.vertices.index(i)<self.vertices.index(j):
                    if (self.all_shortest_paths(i,j)) not in k:
                        k.append((self.all_shortest_paths(i,j)))

        bcs=0
        for i in k:
            if i==None:
                k.remove(None)
                
        for i in range ((len(k))):
            if k[i]!=None:
                count=0
                Y=len(k[i])
                for j in k[i]:

                    j=self.flatten(j)
                    if node in j:
                        count+=1
                        bcs=bcs+(count/Y)
        return bcs

    def top_k_betweenness_centrality(self):
        """
        Find top k nodes based on highest equal betweenness centrality.

        
        Returns:
            A string stating the Highest standard betweenness centrality
            for the graph, the top K nodes and their values.

        """
        n=len(vertices)
        division=(((n-1)*(n-2))/2)

        ListOfBetweennessCentralities={}
        Final_list=[]
        for v in vertices:
                StandardizedBCS=(self.betweenness_centrality(v)/division)
                Final_list.append([StandardizedBCS,v])
                Final_list.sort(reverse=True)

        for v in vertices:
                ListOfBetweennessCentralities[v]=[]
                StandardizedBCS=(self.betweenness_centrality(v))/division

                ListOfBetweennessCentralities[v]=(StandardizedBCS)


        ListOfBetweennessCentralities = {r: ListOfBetweennessCentralities[r] for r in sorted(ListOfBetweennessCentralities, key=ListOfBetweennessCentralities.get, reverse=True)}

        HighestBCS=Final_list[0][0]
        topKBCS=[]
        for i in ListOfBetweennessCentralities:
                if ListOfBetweennessCentralities[i]==HighestBCS:
                        topKBCS.append(i)
        Final_Printing="Highest betweenness Centrality is: "+str(HighestBCS) + ", No. of top K nodes is: " + str (len(topKBCS)) + ", Top K nodes are: "+ str(topKBCS)

        return Final_Printing


if __name__ == "__main__":
    vertices = [1, 2, 3, 4, 5, 6]
    edges    = [(1, 2), (1, 5), (2, 3), (2, 5), (3, 4), (4, 5), (4, 6)]

    

    graph = Graph(vertices, edges)
    print(graph)


