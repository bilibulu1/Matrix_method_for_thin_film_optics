import numpy as np

import film


def hl(num, nl, nh, ng, na, wavelength,input_angle):
    n = [na]
    d = []
    for i in range(num):
        n.append(nh)
        n.append(nl)
    n.append(nh)
    n.append(ng)
    theta=film.compute_theta(n,input_angle)
    for i in range(num):
        d.append(wavelength/(4*nh*np.cos(theta[2*i+1]*np.pi/180)))
        d.append(wavelength/(4*nl*np.cos(theta[2*i+2]*np.pi/180)))
    d.append(wavelength/(4*nh*np.cos(theta[2*i+3]*np.pi/180)))
    return n, d

def all_set( nl, nm,nh, ng, na, wavelength,input_angle):
    n=[ng,nm,nh,nl,nh,nl,nh,nl,na]
    n.reverse()
    d=[1.043,0.244,0.167,2.333,0.2,0.356,1.043]
    d.reverse()
    temp=list(4*np.array(n))
    temp.pop(0)
    temp.pop(len(temp)-1)
    temp=np.array(temp)/np.array(d)
    theta=list(film.compute_theta(n,input_angle))
    theta.pop(0)
    theta.pop(len(theta)-1)
    theta=np.array(theta)
    temp=list(wavelength/(temp*np.cos(theta*np.pi/180)))
    return n,temp
def lh(num, nl, nh, ng, na, wavelength,input_angle):
    n = [na]
    d = []
    for i in range(num):
        n.append(nl)
        n.append(nh)
    n.append(nl)
    n.append(ng)
    theta=film.compute_theta(n,input_angle)
    for i in range(num):
        d.append(wavelength/(4*nl*np.cos(theta[2*i+1]*np.pi/180)))
        d.append(wavelength/(4*nh*np.cos(theta[2*i+2]*np.pi/180)))
    d.append(wavelength/(4*nl*np.cos(theta[2*i+3]*np.pi/180)))
    return n, d

def m2hl(nl, nm,nh, ng, na, wavelength,input_angle):
    n = [na,nh,nl,nm,ng]
    theta=film.compute_theta(n,input_angle)
    temp=list(np.cos(theta*np.pi/180))
    temp.pop(0)
    temp.pop(len(temp)-1)
    d = list(np.array([wavelength/(4*nl),wavelength/(2*nh),wavelength/(4*nm)])/temp)
    return n, d
    
def single_halfwave(num, nl, nh, ng, na, wavelength,input_angle):
    n = [na]
    d = []
    for i in zip([nh for i in range(num) ],[nl for i in range(num)]):
        n+=list(i)
    n.append(nh)
    n.append(nl)
    for i in zip([nh for i in range(num) ],[nl for i in range(num)]):
        n+=list(i)
    n.append(nh)
    n.append(ng)    
    temp=list(4*np.array(n))
    temp[len(temp)//2]=temp[len(temp)//2]/2
    temp=np.array(temp)
    theta=film.compute_theta(n,input_angle)
    temp=list(wavelength/(temp*np.cos(theta*np.pi/180)))
    temp.pop(0)
    temp.pop(len(temp)-1)
    return n,temp
