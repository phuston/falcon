from __future__ import division
import numpy as np
from scipy.optimize import fsolve

def F(x):
    side_len = 5
    c0, c1, c2 = x

    node0pos = (0,0,0)
    node1pos = (0, 20, 0)
    node2pos = (16, 18, 0)
    cam_pos = (1, 19, 1)

    A = np.array([ele for ele in node0pos])
    B = np.array([ele for ele in node1pos])
    C = np.array([ele for ele in node2pos])
    D = np.array([ele for ele in cam_pos])

    D_A = np.subtract(A, D)
    D_B = np.subtract(B, D)
    D_C = np.subtract(C, D)

    eq0 = np.linalg.norm(c0*D_A - c1*D_B) - side_len
    eq1 = np.linalg.norm(c1*D_B - c2*D_C) - side_len
    eq2 = np.linalg.norm(c2*D_C - c0*D_A) - side_len

    return eq0, eq1, eq2

c0, c1, c2 = fsolve(F, (1,1,1))
print c0, c1, c2

node0pos = (0,0,0)
node1pos = (0, 20, 0)
node2pos = (16, 18, 0)
cam_pos = (10, 10, 13)

A = np.array([ele for ele in node0pos])
B = np.array([ele for ele in node1pos])
C = np.array([ele for ele in node2pos])
D = np.array([ele for ele in cam_pos])
D_A = np.subtract(A, D)
D_B = np.subtract(B, D)
D_C = np.subtract(C, D)

print np.add(c0*D_A, D), np.add(c1*D_B, D), np.add(c2*D_C, D)