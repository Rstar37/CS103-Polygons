# 103 Johnstone UAB Fall 2016

# Your name: Ramiz Midani


class Pol (object):
    
    """Pol is a closed polygon in 2-space."""

    def __init__ (self, vtx):
        
        """Initialize a closed polygon from a list of vertices.
        Params: vtx (list of float 2-tuples) vertices, ordered around the bdry
        """
        self.num = len(vtx) #number of sides
        # vtx.append(vtx[0]) #closing the Polygon
        # vtx.append(vtx[1])
        self.vtx = vtx

    def __str__ (self):

        """str method 
        https://www.mathsisfun.com/geometry/polygons.html
        Returns: (str) a string representation of the polygon
        """
        str = ''
        if not self.isSimple():
            str += 'complex '
        else:
            if not self.isConvex():
                str += 'concave '
            else:
                if not self.isRegular():
                    str += 'irregular '
                else:
                    str += 'regular '
        '''didn't know how you wanted it'''
        # if (self.isRegular()):
        #     str += 'regular '
        # else:
        #     str += 'irregular '
        # if (self.isConvex()):
        #     str += 'convex '
        # else:
        #     str += 'concave '
        # if (self.isSimple()):
        #     str += 'simple '
        # else:
        #     str += 'complex '
        polyNames={3:'Triangle', 4:'Quadrilateral', 5:'Pentagon', 6:'Hexagon', 7:'Heptagon', 8:'Octagon', 9:'Nonagon', 10:'Decagon'}
        str += polyNames[self.num]
        return str

    def sideLengths (self, i):
        """the length of a particular side
        params: i (int): the particular side between vertex i and i-1
        returns (float) the length of that side
        """
        X = self.vtx[i-1][0] - self.vtx[i][0]
        Y = self.vtx[i-1][1] - self.vtx[i][1]
        return (X*X + Y*Y)**.5
    
    def vectors (self, i):
        """the vector defined by 2 particular points
        params: i (int): the vector from point vtx[i-1] to vtx[i]
        returns (2-tuple) the vector
        """
        X = self.vtx[i-1][0] - self.vtx[i][0]
        Y = self.vtx[i-1][1] - self.vtx[i][1]
        return (X, Y)
    
    def crossProd (self, V, U):
        """simply the cross product
        params: V, U (2-tuple) both vectors
        returns (float) the cross product of the 2 vectors
        """
        return V[0]*U[1] - V[1]*U[0]
    
    def isParallel (self, A, B, C, D):
        """are the lines parallel
        params:
            A, B (2-tuple): first line segment
            C, D (2-tuple): second line segment
        returns (bool) are they parallel?
        """
        V = (B[0] - A[0], B[1] - A[1])
        U = (D[0] - C[0], D[1] - C[1])
        return self.crossProd(V, U) == 0
    def intersection (self, A, B, C, D):
        """intersection of two lines
        params:
            A, B (2-tuple): first line segment
            C, D (2-tuple): second line segment
        returns (2-tuple) intersection point
        """
        if self.isParallel(A, B, C, D):
            return "nun"
        elif (A[0] == B[0]) or (C[0] == D[0]): # excluding the vertical lines
            if A[0] == B[0]:
                M2 = (C[1] - D[1]) / (C[0] - D[0])
                X = A[0]
                Y = M2 * (X - C[0]) + C[1]
            else:
                M1 = (A[1] - B[1]) / (A[0] - B[0])
                X = C[0]
                Y = M1 * (X - A[0]) + A[1]
        else:
            M1 = (A[1] - B[1]) / (A[0] - B[0])
            M2 = (C[1] - D[1]) / (C[0] - D[0])
            X = (M1*A[0] - M2*C[0] + C[1] - A[1]) / (M2 - M1)
            Y = M1 * (X - A[0]) + A[1]
        P = (X, Y)
        return P
    
    def isPointOnSeg (self, P, A, B):
        """is the point on the segment or the line (in one dimention)
        params:
            P (float): point being tested
            A, B (float): the line segment
        return (bool) wither the point is on the segment
        """
        if (B >= A == P >= A) and (P >= B == A >= B):
            return True
        return False
    
    def doesIntersect(self, A, B, C, D):
        """does the two line SEGMENTS intersect
        params:
            A, B (2-tuple): first line segment
            C, D (2-tuple): second line segment
        returns (bool) does it intersect
        """
        return self.isPointOnSeg(self.intersection(A, B, C, D)[0], A[0], B[0])
    
    def perimeter (self):
        
        """Sum of the lengths of the sides of the polygon.
        Returns: (float) perimeter
        """
        perimeter = 0
        for i in range(self.num):
            perimeter += self.sideLengths(i)
        return perimeter

    def avgEdgeLength (self):
        """
        Returns: (float) average edge length
        """
        return self.perimeter() / self.num


    
    def angle (self, i):
        import math
        """
        Params: i (int): vertex index (0 = first vertex)
        Returns: (float) angle, in degrees, at vertex i
        """
        if i == (self.num - 1): # out of range fix
            i = -1
        lA = self.sideLengths(i+1)
        lB = self.sideLengths(i)
        vA = self.vectors(i+1)
        vB = self.vectors(i)
        AdotB = vA[0]*vB[0] + vA[1]*vB[1]
        return 180 - math.degrees(math.acos(AdotB/(lA*lB)))

    def isSimple (self):                                        # optional bonus

        """Test for simplicity.
        A polygon is simple if it has no self-intersections.
        That is, non-neighbouring edges do not intersect.
        Returns: (bool) is this polygon simple?
        """
        for i in range (self.num):
            for j in range (i+2, self.num-1):
                A = self.vtx[i-1]
                B = self.vtx[i]
                C = self.vtx[j-1]
                D = self.vtx[j]
                if self.doesIntersect(A, B, C, D):
                    return False
        return True

    def isConvex (self):                                        # optional bonus

        """Test for convexity.

        A set S is convex if A, B in S implies the line segment AB is in S.
        But can you make this computational?
        Hint: the cross product is your friend.

        Returns (bool) is this polygon convex?
        """
        V = self.vectors(-1)
        U = self.vectors(0)
        positive = self.crossProd(V, U) > 0
        for i in range(1, self.num):
            V = self.vectors(i-1)
            U = self.vectors(i)
            partPos = self.crossProd(V, U) > 0
            if (partPos != positive):
                return False
        return True
    
    def isRegular (self):
        """Test if it is a regular polygon.
        
        A polygon is regular if all its sides and angles are equal.
        
        Returns (bool) is it a regular polygon?
        """
        reg = True
        L = self.sideLengths(0)
        A = self.angle(0)
        for i in range(1, self.num):
            if self.sideLengths(i) != L:
                return False
            if self.angle(i) != A:
                return False
        return True

class Tri (Pol):

    """Tri is a triangle class."""

    def __init__ (self, A, B, C, rgbA, rgbB, rgbC):
        
        """
        Params:
            A,B,C (float 2-tuples): vertices of the triangle ABC
            rgbA, rgbB, rgbC (int 3-tuples): RGB colours of the vertices
                     colour range is [0,255]; e.g., 0 <= rgbA[i] <= 255
        """
        self.vtx = [A, B, C]
        self.num = 3
        self.rgbA = rgbA
        self.rgbB = rgbB
        self.rgbC = rgbC

    def __str__ (self):

        """
        https://www.mathsisfun.com/triangle.html
        Returns: (str) a string representation of the triangle
        """
        a = self.angle(0)
        b = self.angle(1)
        c = self.angle(2)
        str = ''
        if a == 90 or b == 90 or c == 90:
            str += 'Right '
        else:
            if a > 90 or b > 90 or c > 90:
                str += 'Obtuse '
            else:
                str += 'Acute '
        if a == b and b == c:
            str += 'Equilateral '
        else:
            if a == b or b == c or c == a:
                str += 'Isosceles '
            else:
                str += 'Scalene '
        
        return str + 'Triangle'

    def midPoint (self, A, B):
        """the midpoint of two points
        params: A, B (2-tuple): the two points
        returns: (2-tuple) the midpoint
        """
        return ((A[0]+B[0])/2, (A[1]+B[1])/2)

    def getColour (self, i):

        """
        Params: i (int): vertex index, 0<=i<=2
        Returns: (int 3-tuple) colour of ith vertex
        """
        color = {0:self.rgbA, 1:self.rgbB, 2:self.rgbC}
        return color[i]

    def isEquilateral (self, eps):

        """Test for equilateral triangle.
        Params: eps (float): allowable deviation in length
        Returns: (bool) is the triangle equilateral within eps?
                        (difference between min edge and max edge < eps?)
        """
        EQ = True
        if(self.sideLengths(1) - self.sideLengths(0) > eps):
            EQ = False
        if(self.sideLengths(2) - self.sideLengths(1) > eps):
            EQ = False
        if(self.sideLengths(0) - self.sideLengths(2) > eps):
            EQ = False
        return EQ

    def isCCW (self):
        
        """Counterclockwise orientation.
        ccw iff all (both) turns are left
        Returns: (bool) is the triangle oriented counterclockwise?
        """
        V = self.vectors(0)
        U = self.vectors(1)
        # based on the cross product in 2D:
        # U x V = Ux * Vy - Uy * Vx (if it's positive then it's ccw
        return self.crossProd(V, U) > 0
        
    def signedArea (self):

        """
        Returns: (float) signed area of the triangle, +ve iff counterclockwise
        """
        U = self.vectors(0)
        V = self.vectors(1)
        return abs(U[0]*V[1] - U[1]*V[0])/2

    def centroid (self):                                        # optional bonus

        """
        Returns: (float 2-tuple): centroid of the triangle
        """
        A = self.vtx[0]
        B = self.vtx[1]
        C = self.vtx[2]
        M = self.midPoint(B, C) # midpoint of B and C
        return (M[0] + (A[0]-M[0])/3, M[1] + (A[1]-M[1])/3)

    def circumCenter (self):                                    # optional bonus

        """Circumcenter, the center of the circumscribing circle.
        Returns: (float 2-tuple): circumcenter of the triangle
        """
        M1 = self.midPoint(self.vtx[0], self.vtx[2]) # the midpoint between A and C
        M2 = self.midPoint(self.vtx[0], self.vtx[1]) # the midpoint between A and B
        X1 = self.vectors(0)[0]
        Y1 = self.vectors(0)[1]
        X2 = self.vectors(1)[0]
        Y2 = self.vectors(1)[1]
        return self.intersection(M1, (M1[0] + Y1, M1[1] - X1), M2, (M2[0] + Y2, M2[1] - X2))
        #as simple as it gets B)