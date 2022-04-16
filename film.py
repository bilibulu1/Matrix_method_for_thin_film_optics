import numpy as np


def refrect(incidence_angle, n1, n2):
    refrect_angle = np.arcsin(n1/n2*np.sin(incidence_angle*np.pi/180))
    return refrect_angle*180/np.pi

def compute_theta(n,input_angle):
    theta = []
    theta.append(input_angle)
    input_angle = input_angle
    for i in range(len(n)-1):
        output_angle = refrect(input_angle, n[i], n[i+1])
        input_angle = output_angle
        theta.append(output_angle)
    return np.array(theta)

class Film():

    def __init__(self, n, wavelength, input_angle,layers_d):
        self.n = n
        self.wavelength = wavelength
        self.layers_d = layers_d
        self.layers_number = len(layers_d)
        self.layers_n = np.array(n[1:-1])
        self.input_angle = input_angle
        self.n_s = []
        self.n_p = []

    def theta_compute(self):
        theta = []
        theta.append(self.input_angle)
        input_angle = self.input_angle
        for i in range(len(self.n)-1):
            output_angle = refrect(
                input_angle, self.n[i], self.n[i+1])
            input_angle = output_angle
            theta.append(output_angle)
        self.n_s = self.n*np.cos(np.array(theta)*np.pi/180)
        self.n_p = self.n/np.cos(np.array(theta)*np.pi/180)
        return np.array(theta)

    def delta(self, theta):
        layers_theta = theta[1:-1]
        return np.array(2*np.pi*self.layers_n*self.layers_d*np.cos(layers_theta*np.pi/180)/self.wavelength)

    def matrix(self, correction_admittance, theta0):
        theta = theta0
        delta = self.delta(theta)
        n = correction_admittance[1:-1]
        a = (np.cos(delta),
             1j/n*np.sin(delta), n*np.sin(delta)*1j, np.cos(delta))
        matrix = np.identity(2)
        for i in range(self.layers_number):
            matrix = np.dot(matrix, np.matrix(
                [[a[0][i], a[1][i]], [a[2][i], a[3][i]]]))
        base = np.matrix([[1], [correction_admittance[-1]]])
        bc = np.array(np.dot(matrix, base))
        return bc

    def Y(self):
        theta = self.theta_compute()
        bc_s = self.matrix(self.n_s, theta).squeeze()
        bc_p = self.matrix(self.n_p, theta).squeeze()
        Y_s = bc_s[1]/bc_s[0]
        Y_p = bc_p[1]/bc_p[0]
        return Y_s, Y_p

    def Opt_prop(self):
        Y_s, Y_p = self.Y()
        n0_s = self.n_s[0]
        n0_p = self.n_p[0]
        R_s = abs((n0_s-Y_s)/(n0_s+Y_s))**2
        R_p = abs((n0_p-Y_p)/(n0_p+Y_p))**2
        T_s = 1-R_s
        T_p = 1-R_p
        return R_s, R_p, T_s, T_p

def compute_feature(n, i, d, j):
    a = Film(n, i, d, j)
    prop = a.Opt_prop()
    R = (prop[0]+prop[1])/2
    R_s = prop[0]
    R_p = prop[1]
    T_s = prop[2]
    T_p = prop[3]
    T = (prop[2]+prop[3])/2
    return R_s, R_p, T_s, T_p, R, T
