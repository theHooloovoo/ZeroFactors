
from math import cos, sin, pi

class ZeroFactor:
    """ Generates & stores all of the data pertinent to the topic of
        Zero-Factor Analysis for some arbitrary integer.
    """
    def __init__(self, n):
        self.n = n
        self.verts = range(0, n)
        self.edges = [(a,b) for a in self.verts for b in self.verts[a+1:] if a*b % n == 0]
        self.non_trivial_edges = list(filter(lambda pair: 0 not in pair, self.edges))
        self.cardinality = len(self.edges) # Of the set of edges.
        self.degrees = [sum(1 for pair in self.edges if x in pair) for x in range(0,n)]
        self.non_trivial_degrees = [sum(1 for pair in self.non_trivial_edges if x in pair) for x in range(0,n)]
        self.factors = [a for a in range(0,n) for b in range(0,n) if a*b == n]
        # Used to easily write on the screen.
        self.factors_pos = list(map(lambda x: x if x in self.factors else None, self.verts))
        # Only relevant to drawing fancily on a screen. Projects to the unit circle.
        self.coords = [(cos(o*pi*2/n-pi/2),sin(o*pi*2/n-pi/2)) for o in range(0, n)]
        # Coloring algorithm currently broken. Incorrect results.

    def get_colors(vert_set, edge_set):
        """ Given data on a graph, returns a list of colors coresponding to
            each vertex.
            ---
            Currently broken, returns list of all the same color.
            ---
        """
        colors = [None for _ in vert_set]
        # Begin coloring the graph.
        if len(edge_set) == 0:
            return
        for vert in vert_set:
            colors_seen = []
            for edge in edge_set:
                if vert in edge and colors[vert] != None:
                    colors_seen.append(colors[vert])
            for n in range(1, len(vert_set)):
                if n not in colors_seen:
                    colors[vert] = n
                    break
        return colors

