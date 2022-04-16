import argparse
from gettext import ngettext

import numpy as np
from matplotlib import pyplot as plt

import film
import structure


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--start_wav', default=380*1e-9,type=float,
                        help='start_wav: (default: 380*1e-9)')
    parser.add_argument('--end_wav', default=800*1e-9, type=float,
                        help='end_wav: (default: 800*1e-9)')
    parser.add_argument('--center_wav', default=500*1e-9,type=float,
                        help='center wavelength')    
    parser.add_argument('--points', default=8000, type=int,
                        help='sample points')
    parser.add_argument('--nl', default=1.38,type=float,
                        help='refractive index of low refractive index material')
    parser.add_argument('--nh', default=1.88, type=float,
                        help='refractive index of high refractive index material')
    parser.add_argument('--nm', default=1.58, type=float,
                        help='refractive index of medium refractive index material')    
    parser.add_argument('--ng', default=1.58, type=float,
                        help='refractive index of glass')   
    parser.add_argument('--na', default=1, type=float,
                        help='refractive index of medium')                                                   
    parser.add_argument('--structure', default='hl',choices=['hl', 'all_set','lh','m2hl','single_halfwave'], 
                        help='structure of films')    
    parser.add_argument('--num', default=1, type=int,
                        help='number of films')   
    parser.add_argument('--input_angle', default=0, type=float,
                        help='input angle')                                                  
    config = parser.parse_args()
    return config

def feature(start,end,points,n,d,label,input_angle):
    wavelength = np.linspace(start,end, points)
    R_s = []
    R_p = []
    T_s = []
    T_p = []
    R=[]
    T=[]
    for i in wavelength:
        a = film.Film(n, i, input_angle, d)
        prop = a.Opt_prop()
        R_s.append(prop[0])
        R_p.append(prop[1])
        T_s.append(prop[2])
        T_p.append(prop[3])
        R.append((prop[0]+prop[1])/2)
        T.append((prop[2]+prop[3])/2)
    plt.plot(wavelength, R, label=label)
    plt.title('R')
    plt.xlabel('wavelength')
    plt.ylabel('R')
    plt.legend()
    plt.savefig('wavelength.jpg',)
    plt.show()  

def change_wavelength(start,end,points,num,nl,nh,ng,na,center_wav,input_angle,structure,label):
    n,d=structure(num, nl, nh, ng, na, center_wav,input_angle)
    feature(start,end,points,n,d,label,input_angle)

def main():
    config = vars(parse_args())
    nl=config['nl']
    nm=config['nm']
    nh=config['nh']
    ng=config['ng']
    na=config['na']
    num=config['num']
    start_wav=config['start_wav']
    end_wav=config['end_wav']
    sample_points=config['points']
    input_angle=config['input_angle']
    center_wav=config['center_wav']
    label=config['structure']
    if config['structure'] == 'hl':
        layer_structure = structure.hl
    elif config['structure'] == 'lh':
        layer_structure = structure.lh_
    elif config['structure'] == 'm2hl':
        layer_structure = structure.m2hl
    elif config['structure'] == 'all_set':
        layer_structure = structure.all_set
    elif config['structure'] == 'single_halfwave':
        layer_structure = structure.single_halfwave
    else:
        raise NotImplementedError
    change_wavelength(start_wav,end_wav,sample_points,num,nl,nh,ng,na,center_wav,input_angle,layer_structure,label)
    

if __name__ == '__main__':
    main()
