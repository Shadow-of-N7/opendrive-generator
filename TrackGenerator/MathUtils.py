# -*- coding: utf-8 -*-

"""
Provides some useful math operations
"""

import math
import numpy as np
import matplotlib.pyplot as plt


def perp(a):
    b = np.empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b


def seg_intersect(a1, a2, b1, b2):
    """
    # line segment a given by endpoints a1, a2
    # line segment b given by endpoints b1, b2
    # return
    """
    da = a2 - a1
    db = b2 - b1
    dp = a1 - b1
    dap = perp(da)
    denom = np.dot(dap, db)
    num = np.dot(dap, dp)
    return (num / denom.astype(float)) * db + b1


def on_segment(p, q, r):
    '''Given three colinear points p, q, r, the function checks if
    point q lies on line segment "pr"
    '''
    if (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and
        q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1])):
        return True
    return False


def orientation(p, q, r):
    '''Find orientation of ordered triplet (p, q, r).
    The function returns following values
    0 --> p, q and r are colinear
    1 --> Clockwise
    2 --> Counterclockwise
    '''

    val = ((q[1] - p[1]) * (r[0] - q[0]) -
            (q[0] - p[0]) * (r[1] - q[1]))
    if val == 0:
        return 0  # colinear
    elif val > 0:
        return 1   # clockwise
    else:
        return 2  # counter-clockwise


def do_intersect(p1, q1, p2, q2):
    '''Main function to check whether the closed line segments p1 - q1 and p2
       - q2 intersect'''
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    # General case
    if (o1 != o2 and o3 != o4):
        return True

    # Special Cases
    # p1, q1 and p2 are colinear and p2 lies on segment p1q1
    if (o1 == 0 and on_segment(p1, p2, q1)):
        return True

    # p1, q1 and p2 are colinear and q2 lies on segment p1q1
    if (o2 == 0 and on_segment(p1, q2, q1)):
        return True

    # p2, q2 and p1 are colinear and p1 lies on segment p2q2
    if (o3 == 0 and on_segment(p2, p1, q2)):
        return True

    # p2, q2 and q1 are colinear and q1 lies on segment p2q2
    if (o4 == 0 and on_segment(p2, q1, q2)):
        return True

    return False # Doesn't fall in any of the above cases


def isPointOnLine(lineA, lineB, PointC):
    """
    2D - Check if C is on line A-B
    """
    AB = lineB - lineA
    AC = PointC - lineA

    cr = np.cross(AB, AC)
    if (cr.ndim and cr.size) != 0:
        return False
    KAC = np.dot(AB, AC)
    if KAC < 0:
        return False
    if KAC == 0:
        return True

    KAB = np.dot(AB, AB)
    if KAC > KAB:
        return False
    if KAC == KAB:
        return True

    return True


def GetArcMiddle(Astart, aEnd, bStart, bEnd):
    A = aEnd - Astart
    B = bEnd - bStart

    Ap = perp(A) + aEnd
    Bp = perp(B) + bStart

    M = seg_intersect(Ap, aEnd, Bp, bStart)
    return M


def GetArcMiddle(straightAStart, straightAEnd, straightBStart, straightBEnd, radius, parallelDir):
    print("Radius: " + str(radius))

    # Parallele zu A
    A2D = np.array([(straightAEnd - straightAStart)[0], (straightAEnd - straightAStart)[2]])

    Aperpendicular = perp(parallelDir * A2D) + np.array([straightAStart[0], straightAStart[2]])
    Aparallel1 = VectorLerpAbs(straightAStart, np.array([Aperpendicular[0], 0, Aperpendicular[1]]), radius)

    Aperpendicular = perp(parallelDir * A2D) + np.array([straightAEnd[0], straightAEnd[2]])
    Aparallel2 = VectorLerpAbs(straightAEnd, np.array([Aperpendicular[0], 0, Aperpendicular[1]]), radius)
    print("A Normale Distanz: " + str(np.linalg.norm(Aparallel2 - straightAEnd)))

    # ----
    # Parallele zu B
    B2D = np.array([(straightBEnd - straightBStart)[0], (straightBEnd - straightBStart)[2]])

    Bperpendicular = perp(parallelDir * B2D) + np.array([straightBStart[0], straightBStart[2]])
    Bparallel1 = VectorLerpAbs(straightBStart, np.array([Bperpendicular[0], 0, Bperpendicular[1]]), radius)

    Bperpendicular = perp(parallelDir * B2D) + np.array([straightBEnd[0], straightBEnd[2]])
    Bparallel2 = VectorLerpAbs(straightBEnd, np.array([Bperpendicular[0], 0, Bperpendicular[1]]), radius)
    print("B Normale Distanz: " + str(np.linalg.norm(Bparallel2 - straightBEnd)))

    # ----
    # Schnittpunkt der beiden Parallelen
    ArcMiddle = seg_intersect(np.array([Aparallel1[0], Aparallel1[2]]),
                              np.array([Aparallel2[0], Aparallel2[2]]),
                              np.array([Bparallel1[0], Bparallel1[2]]),
                              np.array([Bparallel2[0], Bparallel2[2]]))

    curvature = AngleBetween(Aparallel2 - Aparallel1, Bparallel2 - Bparallel1)
    length = curvature * radius

    # ----
    # Startpunkt des Arcs & Endpunkt der Geraden
    ArcStart = seg_intersect(np.array([Bparallel1[0], Bparallel1[2]]),
                             np.array([Bparallel2[0], Bparallel2[2]]),
                             np.array([straightAStart[0], straightAStart[2]]),
                             np.array([straightAEnd[0], straightAEnd[2]]))

    ArcEnd = seg_intersect(np.array([Aparallel1[0], Aparallel1[2]]),
                           np.array([Aparallel2[0], Aparallel2[2]]),
                           np.array([straightBStart[0], straightBStart[2]]),
                           np.array([straightBEnd[0], straightBEnd[2]]))

    # -- Bestimmen, ob M innerhalb oder außerhalb ist
    SchnittpunktAB = seg_intersect(np.array([straightAStart[0], straightAStart[2]]),
                                   np.array([straightAEnd[0], straightAEnd[2]]),
                                   np.array([straightBStart[0], straightBStart[2]]),
                                   np.array([straightBEnd[0], straightBEnd[2]]))

    doIntersect = do_intersect(np.array([Bparallel1[0], Bparallel1[2]]),
                               np.array([Bparallel2[0], Bparallel2[2]]),
                               np.array([straightAStart[0], straightAStart[2]]),
                               np.array([straightAEnd[0], straightAEnd[2]]))
    normalIntersect = seg_intersect(np.array([Bparallel1[0], Bparallel1[2]]),
                               np.array([Bparallel2[0], Bparallel2[2]]),
                               np.array([straightAStart[0], straightAStart[2]]),
                               np.array([straightAEnd[0], straightAEnd[2]]))

    isNormalIntersectOnA = isPointOnLine(np.array([straightAStart[0], straightAStart[2]]),
                                         np.array([straightAEnd[0], straightAEnd[2]]),
                                         normalIntersect)

    if not isNormalIntersectOnA:
        print("Normales do not intersect. Reapeating. ArcMiddle: " + str(ArcMiddle))
        ArcMiddle, ArcStart, ArcEnd, curvature, length = GetArcMiddle(straightAStart, straightAEnd, straightBStart, straightBEnd, radius, -1)
    else:
        print("Found ArcMiddle at " + str(ArcMiddle))
        # ----
        # Plot
        fig, ax = plt.subplots()
        ax.plot([straightAStart[0], straightAEnd[0], straightBStart[0], straightBEnd[0]], [straightAStart[2], straightAEnd[2], straightBStart[2], straightBEnd[2]])
        print("Aparallel1: " + str(Aparallel1))
        print("Aparallel2: " + str(Aparallel2))
        ax.plot([Aparallel1[0], Aparallel2[0]], [Aparallel1[2], Aparallel2[2]])
        ax.plot([Bparallel1[0], Bparallel2[0]], [Bparallel1[2], Bparallel2[2]])

        ax.scatter(ArcMiddle[0], ArcMiddle[1])
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()
    return ArcMiddle, ArcStart, ArcEnd, curvature, length


def VectorLerpRel(A, B, amount: float):
    V = B - A

    normal = V * (np.array([1, 1, 1]) / np.linalg.norm(V))
    distance = np.linalg.norm(B - A)
    result = A + normal * (distance * amount)
    return result


def VectorLerpAbs(A, B, amount: float):
    V = B - A

    normal = V * (np.array([1, 1, 1]) / np.linalg.norm(V))
    distance = np.linalg.norm(B - A)
    result = A + normal * amount
    return result


def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)


def AngleBetween(A, B):
    v1_u = unit_vector(A)
    v2_u = unit_vector(B)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))


# ---
pol = isPointOnLine(np.array([0, 0]), np.array([0, 10]), np.array([0, 4]))

# Test M
straightAStart = np.array([10, 0, 1])
straightAEnd = np.array([13, 0, 4])

straightBStart = np.array([13, 0, 4])
straightBEnd = np.array([8, 0, 9])

Inter = seg_intersect(np.array([straightAStart[0], straightAStart[2]]),
                      np.array([straightAEnd[0], straightAEnd[2]]),
                      np.array([straightBStart[0], straightBStart[2]]),
                      np.array([straightBEnd[0], straightBEnd[2]]))
dointer = do_intersect(np.array([straightAStart[0], straightAStart[2]]),
                      np.array([straightAEnd[0], straightAEnd[2]]),
                      np.array([straightBStart[0], straightBStart[2]]),
                      np.array([straightBEnd[0], straightBEnd[2]]))

lenA = np.linalg.norm(straightAEnd - straightAStart)
lenB = np.linalg.norm(straightBEnd - straightBStart)

radius = lenA * 0.4
if lenB < lenA:
    radius = lenB * 0.4

ArcMiddle, ArcStart, ArcEnd, curvature, length = GetArcMiddle(straightAStart, straightAEnd, straightBStart, straightBEnd, radius, 1)