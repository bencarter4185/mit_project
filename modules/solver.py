"""
Library file to solve the Biot-Savart law.
"""

from scipy.constants import mu_0 as mu
from numpy import array, zeros, complex_, sqrt, pi, cross
from itertools import pairwise


def _magnitude(vec):
    """
    Returns the magnitude of a vector
    """
    return sqrt(vec.dot(vec))

def _solve_segment(segment, point, current):
    """
    Calculate the magnetic field for a small current element, at a given point. 
    """
    # Generate an empty variable for the magnetic field
    db = zeros(3)

    # Calculate segment vector
    ux = segment[0][1] - segment[0][0]
    uy = segment[1][1] - segment[1][0]
    uz = segment[2][1] - segment[2][0]

    dl = array([ux, uy, uz])

    # Get reference point in the middle of the segment
    ux_r = (segment[0][1] + segment[0][0])/2
    uy_r = (segment[1][1] + segment[1][0])/2
    uz_r = (segment[2][1] + segment[2][0])/2

    rp = array([ux_r, uy_r, uz_r])

    # Displacement vector
    ux_d = point[0] - rp[0]
    uy_d = point[1] - rp[1]
    uz_d = point[2] - rp[2]

    r = array([ux_d, uy_d, uz_d])

    # Perform Biot-Savart integral calculation
    db = mu/(4*pi) * current * cross(dl, r) / _magnitude(r)**3

    return db


def solve(wire, points):
    """
    Calculate the resultant magnetic field due to an arbitrary wire object, for a given set of points.
    """

    # Store an `effective current`, which is the current in the wire where the real part is multiplied
    # by the number of turns, n
    current = complex(wire.current.real * wire.n, wire.current.imag)

    # Generate an empty variable for the magnetic field
    b = zeros((len(points[0]), 3), dtype=complex_)

    # Iterate through every segment of wire
    for ((x2, x1),
         (y2, y1),
         (z2, z1)) in zip(pairwise(wire.coordinates[0]),
                          pairwise(wire.coordinates[1]),
                          pairwise(wire.coordinates[2])):
        # Generate coordinates of resultant line segment
        segment = array([array([x1, x2]), array([y1, y2]), array([z1, z2])])
        
        # Iterate through every point in question and solve
        for i in range(len(points[0])):
            # Generate coordinates of point
            point = array([points[0][i], points[1][i], points[2][i]])
            b[i] += _solve_segment(segment, point, current)

    return b

def b_abs(b):
    """
    Return the absolute value of a calculated magnetic field
    """
    b_abs = zeros(len(b))

    for i in range(len(b_abs)):
        b_abs[i] = abs(_magnitude(b[i]))

    return b_abs