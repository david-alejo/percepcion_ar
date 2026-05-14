#Tutorial de G2o para hacer un SLAM 2D basico en Python
# Instalar la libreria g2opy
# pip install g2opy (en Linux, sera necesario hacer un entorno virtual (venv))

import numpy as np
import g2opy as g2o 
import matplotlib.pyplot as plt
import math 

# We generate a trajectory consisting of 6 steps (2 are repeated)
def genTraj():
    init = (0, 0)

    # Forward I
    num = 20; xSt = -5; ySt = -8; leng = 9.0; step = float(leng)/num
    X1 = np.zeros(num); Y1 = np.zeros(num); X1[0] = xSt; Y1[0] = ySt
    for i in range(1, num):
        X1[i] = X1[i-1] + step
        Y1[i] = ySt

    # UTurn I
    rad = 2.5; num = 20
    xCen = X1[-1]; yCen = Y1[-1] + rad
    thetas = np.linspace(-math.pi/2, math.pi/2, num)
    X2 = np.zeros(num); Y2 = np.zeros(num)
    for i, theta in enumerate(thetas):
        X2[i] = (xCen + rad*math.cos(theta))
        Y2[i] = (yCen + rad*math.sin(theta))

    # Backward I
    num = 20; leng = 10.0; step = float(leng)/num
    xSt = X2[-1]; ySt = Y2[-1]
    X3 = np.zeros(num); Y3 = np.zeros(num); X3[0] = xSt; Y3[0] = ySt 
    for i in range(1, num):
        X3[i] = X3[i-1] - step
        Y3[i] = ySt

    # UTurn II
    rad = 2.6; num = 20
    xCen = X3[-1]; yCen = Y3[-1] - rad
    thetas = np.linspace(math.pi/2, 3*math.pi/2, num)
    X4 = np.zeros(num); Y4 = np.zeros(num)
    for i, theta in enumerate(thetas):
        X4[i] = (xCen + rad*math.cos(theta))
        Y4[i] = (yCen + rad*math.sin(theta))

    # Forward II
    num = 20; leng = 11.0; step = float(leng)/num
    xSt = X4[-1]; ySt = Y4[-1]
    X5 = np.zeros(num); Y5 = np.zeros(num); X5[0] = xSt; Y5[0] = ySt
    for i in range(1, num):
        X5[i] = X5[i-1] + step
        Y5[i] = ySt

    # UTurn III
    rad = 2.7; num = 20
    xCen = X5[-1]; yCen = Y5[-1] + rad
    thetas = np.linspace(-math.pi/2, math.pi/2, num)
    X6 = np.zeros(num); Y6 = np.zeros(num)
    for i, theta in enumerate(thetas):
        X6[i] = (xCen + rad*math.cos(theta))
        Y6[i] = (yCen + rad*math.sin(theta))	

    # Assemble
    X = np.concatenate([X1, X2, X3, X4, X5, X6]); Y = np.concatenate([Y1, Y2, Y3, Y4, Y5, Y6])
    THETA = np.array(getTheta(X, Y))

    return (X, Y, THETA)

def getTheta(X ,Y):
    THETA = [None]*len(X)
    for i in range(1, len(X)-1):
        if(X[i+1] == X[i-1]):
            if (Y[i+1]>Y[i-1]):
                THETA[i] = math.pi/2
            else:
                THETA[i] = 3*math.pi/2
            continue

        THETA[i] = math.atan((Y[i+1]-Y[i-1])/(X[i+1]-X[i-1]))

        if(X[i+1]-X[i-1] < 0):
            THETA[i] += math.pi 

    if X[1]==X[0]:
        if Y[1] > Y[0]:
            THETA[0] = math.pi/2
        else:
            THETA[0] = 3*math.pi/2
    else:
        THETA[0] = math.atan((Y[1]-Y[0])/(X[1]-X[0]))

    if X[-1] == X[len(Y)-2]:
        if Y[1] > Y[0]:
            THETA[-1] = math.pi/2
        else:
            THETA[-1] = 3*math.pi/2
    else:
        THETA[-1] = math.atan((Y[-1]-Y[len(Y)-2])/(X[-1]-X[len(Y)-2]))

    return THETA
 
# We add noise to the trajectories
def addNoise(X, Y, THETA):
    xN = np.zeros(len(X)); yN = np.zeros(len(Y)); tN = np.zeros(len(THETA))
    xN[0] = X[0]; yN[0] = Y[0]; tN[0] = THETA[0]

    for i in range(1, len(X)):
        # Get T2_1
        p1 = (X[i-1], Y[i-1], THETA[i-1])
        p2 = (X[i], Y[i], THETA[i])
        T1_w = np.array([[math.cos(p1[2]), -math.sin(p1[2]), p1[0]], [math.sin(p1[2]), math.cos(p1[2]), p1[1]], [0, 0, 1]])
        T2_w = np.array([[math.cos(p2[2]), -math.sin(p2[2]), p2[0]], [math.sin(p2[2]), math.cos(p2[2]), p2[1]], [0, 0, 1]])
        T2_1 = np.dot(np.linalg.inv(T1_w), T2_w)
        del_x = T2_1[0][2]
        del_y = T2_1[1][2]
        del_theta = math.atan2(T2_1[1, 0], T2_1[0, 0])

        # Add noise
        if(i<5):
            xNoise = 0; yNoise = 0; tNoise = 0
        else:
            xNoise = np.random.normal(0, 0.03); yNoise = np.random.normal(0, 0.03); tNoise = np.random.normal(0, 0.03)
        del_xN = del_x + xNoise; del_yN = del_y + yNoise; del_thetaN = del_theta + tNoise

        # Convert to T2_1'
        T2_1N = np.array([[math.cos(del_thetaN), -math.sin(del_thetaN), del_xN], [math.sin(del_thetaN), math.cos(del_thetaN), del_yN], [0, 0, 1]])

        # Get T2_w' = T1_w' . T2_1'
        p1 = (xN[i-1], yN[i-1], tN[i-1])
        T1_wN = np.array([[math.cos(p1[2]), -math.sin(p1[2]), p1[0]], [math.sin(p1[2]), math.cos(p1[2]), p1[1]], [0, 0, 1]])
        T2_wN = np.dot(T1_wN, T2_1N)

        # Get x2', y2', theta2'
        x2N = T2_wN[0][2]
        y2N = T2_wN[1][2]
        theta2N = math.atan2(T2_wN[1, 0], T2_wN[0, 0])

        xN[i] = x2N; yN[i] = y2N; tN[i] = theta2N  

    # tN = getTheta(xN, yN)

    return (xN, yN, tN)


 
def quat_mult(q1, q2):
    """Quaternion multiplication."""
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
    x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
    y = w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2
    z = w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2
    return np.array([w, x, y, z])
 
def quat_inv(q):
    """Quaternion inverse."""
    w, x, y, z = q
    return np.array([w, -x, -y, -z])
 
def quat_to_rot(q):
    """Quaternion to rotation matrix."""
    w, x, y, z = q
    R = np.array([[1 - 2*(y**2 + z**2), 2*(x*y - w*z), 2*(x*z + w*y)],
                  [2*(x*y + w*z), 1 - 2*(x**2 + z**2), 2*(y*z - w*x)],
                  [2*(x*z - w*y), 2*(y*z + w*x), 1 - 2*(x**2 + y**2)]])
    return R
 
def quat_diff(q1, q2):
    """Quaternion difference."""
    return quat_mult(q2, quat_inv(q1))
 
 
 

 
class PoseGraphOptimization(g2o.SparseOptimizer):
    def __init__(self):
        super().__init__()
        # solver = g2o.BlockSolverX(g2o.LinearSolverCholmodX())
        solver = g2o.BlockSolverX(g2o.g2opy.LinearSolverEigenX())
 
        # solver = g2o.BlockSolverSE3(g2o.LinearSolverCholmodSE3())
        solver = g2o.OptimizationAlgorithmLevenberg(solver)
        super().set_algorithm(solver)
        super().set_verbose(True)
 
    def optimize(self, max_iterations=20):
        print('num vertices:', len(super().vertices()))
        print('num edges:', len(super().edges()), end='\n\n')
        super().initialize_optimization()
        super().optimize(max_iterations)
        super().save("out.g2o")
 
 
    def add_vertex3(self, id, pose, fixed=False):
        v_se3 = g2o.VertexSE3()
        v_se3.set_id(id)
        v_se3.set_estimate(pose)
        v_se3.set_fixed(fixed)
        super().add_vertex(v_se3)
 
    def add_edge3(self, vertices, measurement,
                      information=np.identity(6),
                      robust_kernel=None):
 
        edge = g2o.EdgeSE3()
        for i, v in enumerate(vertices):
            if isinstance(v, int):
                v = self.vertex(v)
            edge.set_vertex(i, v)
 
        edge.set_measurement(measurement)  # relative pose
        edge.set_information(information)
        if robust_kernel is not None:
            edge.set_robust_kernel(robust_kernel)
        super().add_edge(edge)
 
    def get_pose3(self, id):
        return self.vertex(id).estimate()
 
    def add_vertex2(self, id, pose, fixed=False):
        v_se2 = g2o.VertexSE2()
        v_se2.set_id(id)
        # v_se2.set_estimate(pose)
        v_se2.set_estimate_data(pose)
        v_se2.set_fixed(fixed)
        super().add_vertex(v_se2)
 
    def add_edge2(self, vertices, measurement,
                 information=np.identity(3),
                 robust_kernel=None):
 
        edge = g2o.EdgeSE2()
        for i, v in enumerate(vertices):
            if isinstance(v, int):
                v = self.vertex(v)
            edge.set_vertex(i, v)
 
        # edge.set_measurement(measurement)  # relative pose
        edge.set_measurement(g2o.SE2(measurement))
        edge.set_information(information)
        if robust_kernel is not None:
            edge.set_robust_kernel(robust_kernel)
        super().add_edge(edge)
 
    def add_edge_from_state2(self, vertices,
                            information=np.identity(3),
                            robust_kernel=None):
 
        edge = g2o.EdgeSE2()
        for i, v in enumerate(vertices):
            if isinstance(v, int):
                v = self.vertex(v)
            edge.set_vertex(i, v)
 
        edge.set_measurement_from_state()  # relative pose
        edge.set_information(information)
        if robust_kernel is not None:
            edge.set_robust_kernel(robust_kernel)
        super().add_edge(edge)
 
    def get_pose2(self, id):
        return self.vertex(id).estimate()
 
 
 
#Implementacion del pose graph 
PGO = PoseGraphOptimization()
 
[X,Y,Theta]=genTraj()

[XN,YN,ThetaN]=addNoise(X,Y,Theta)
print(len(XN))

# Escribimos la odometria: para cada nodo con ruido ponemos el incremento
info_odom = 5
for i, (x, y, theta) in enumerate(zip(XN,YN,ThetaN)):
    PGO.add_vertex2(i, [x, y, theta], fixed=(i==0)) # The first vertex is fixed!
print (PGO.vertices())
for i in range(1, len(X)):
    p1 = (XN[i-1], YN[i-1], ThetaN[i-1])
    p2 = (XN[i], YN[i], ThetaN[i])
    T1_w = np.array([[math.cos(p1[2]), -math.sin(p1[2]), p1[0]], [math.sin(p1[2]), math.cos(p1[2]), p1[1]], [0, 0, 1]])
    T2_w = np.array([[math.cos(p2[2]), -math.sin(p2[2]), p2[0]], [math.sin(p2[2]), math.cos(p2[2]), p2[1]], [0, 0, 1]])
    T2_1 = np.dot(np.linalg.inv(T1_w), T2_w)
    del_x = str(T2_1[0][2])
    del_y = str(T2_1[1][2])
    del_theta = str(math.atan2(T2_1[1, 0], T2_1[0, 0]))

    PGO.add_edge2([i-1,i], [del_x, del_y, del_theta], information=info_odom * np.identity(3))


# Añadimos loop closure entre nodos similares
pairs = []
for i in range(0, 40, 2):
        pairs.append((i, i+80))
    # for i in range(len(X)):
    # 	pairs.append((0, i))

info_loop = 0.3

for p in pairs:
        p1 = (X[p[0]], Y[p[0]], Theta[p[0]])
        p2 = (X[p[1]], Y[p[1]], Theta[p[1]])
        T1_w = np.array([[math.cos(p1[2]), -math.sin(p1[2]), p1[0]], [math.sin(p1[2]), math.cos(p1[2]), p1[1]], [0, 0, 1]])
        T2_w = np.array([[math.cos(p2[2]), -math.sin(p2[2]), p2[0]], [math.sin(p2[2]), math.cos(p2[2]), p2[1]], [0, 0, 1]])
        T2_1 = np.dot(np.linalg.inv(T1_w), T2_w)
        del_x = str(T2_1[0][2])
        del_y = str(T2_1[1][2])
        del_theta = str(math.atan2(T2_1[1, 0], T2_1[0, 0]))

        # TODO: añadir ruido al loop closure

        PGO.add_edge2([p[0],p[1]], [del_x, del_y, del_theta], information=info_loop * np.identity(3))
 
PGO.optimize()
 
oposes = []
for i in range(len(X)):
    oposes.append(PGO.get_pose2(i).vector())
 
print(oposes)
  
# plot the trajectory

#ground truth
init = False
for i, (x, y, theta) in enumerate(zip(X,Y,Theta)):
    if init:
        plt.plot([x_a, x], [y_a, y], 'r-o', label='gt')
    else:
        init = True
    x_a = x
    y_a = y
    theta_a = theta

init = False
for i, (x, y, theta) in enumerate(zip(XN,YN,ThetaN)):
     if init:
         plt.plot([x_a, x], [y_a, y], 'g-x', label='odom')
     else:
         init = True
     x_a = x
     y_a = y
     theta_a = theta
 
for i, ref_pose in enumerate(oposes):
     if i + 1 >= len(oposes):
         break
     next_pose = oposes[i + 1]
     plt.plot([ref_pose[0], next_pose[0]], [ref_pose[1], next_pose[1]], 'b-o', label='op-aft')
 
 
plt.show()