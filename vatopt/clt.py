import numpy as np

def Q_ortho(E1, E2, nu12, G12):
    nu21 = nu12*E2/E1
    denom = 1 - nu12*nu21
    Q11 = E1/denom
    Q22 = E2/denom
    Q12 = nu12*E2/denom
    Q66 = G12
    return np.array([[Q11, Q12, 0.0],[Q12, Q22, 0.0],[0.0, 0.0, Q66]])

def T_sigma(theta):
    c = np.cos(np.deg2rad(theta)); s = np.sin(np.deg2rad(theta))
    return np.array([[c*c, s*s, 2*s*c],[s*s, c*c, -2*s*c],[-s*c, s*c, c*c - s*s]])

def Qbar(Q, theta):
    T = T_sigma(theta)
    Tinv = np.linalg.inv(T)
    return Tinv @ Q @ Tinv.T

def ABD_stack(plies, h_total=0.002):
    # plies: list of (theta_deg, t_frac) where sum(t_frac)=1
    h = [-h_total/2.0]
    for _,tf in plies:
        h.append(h[-1] + tf*h_total)
    baseQ = Q_ortho(130e9, 10e9, 0.3, 5e9)
    Qlam = [Qbar(baseQ, theta) for theta,_ in plies]
    A = np.zeros((3,3)); B = np.zeros((3,3)); D = np.zeros((3,3))
    for k,Qk in enumerate(Qlam):
        zk = h[k+1]; zk1 = h[k]
        A += Qk*(zk - zk1)
        B += 0.5*Qk*(zk**2 - zk1**2)
        D += (1/3)*Qk*(zk**3 - zk1**3)
    return A,B,D
