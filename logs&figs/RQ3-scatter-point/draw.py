import matplotlib.pyplot as plt
import numpy as np


def get_record(file_path):
    d = {}
    with open(file_path,'r') as of:
        line = of.readline()
        while line:
            line_list = line.split(' ')
            if 'log' not in line:
                pass
            elif len(line_list) == 1:
                d[line_list[0][:-1]] = 7200.0
            else:    
                d[line_list[0]] = float(line_list[1])   
            
            line = of.readline()
    
    return d

def main():
    
    bcar_bm = get_record('record/bcar-record.txt')
    fcar_bm = get_record('record/fcar-record.txt')
    ic3_bm = get_record('record/ic3-record.txt')
    pdr_bm = get_record('record/pdr-record.txt')
    
    # Fig.5(a)
    bcar_bm_p = set(); fcar_bm_p = set()
    for e in bcar_bm.keys():
        if 'bcar' in e:
            bcar_bm_p.add(e)
        if 'fcar' in e:
            fcar_bm_p.add(e)
    for e in fcar_bm.keys():
        if 'bcar' in e:
            bcar_bm_p.add(e)    
        if 'fcar' in e:
            fcar_bm_p.add(e)

    bcar_x = []; bcar_y = []
    for e in bcar_bm_p:
        bcar_x.append(bcar_bm[e])
        bcar_y.append(fcar_bm[e])
        

    fcar_x = []; fcar_y = []
    for e in fcar_bm_p:
        fcar_x.append(bcar_bm[e])
        fcar_y.append(fcar_bm[e])

    plt.scatter(bcar_x, bcar_y, c='#F9CB80', marker = 'o', edgecolor = 'grey', label='B.CAR')
    plt.scatter(fcar_x, fcar_y, c='#F89588', marker = 'D', edgecolor = 'grey', label='F.CAR')
    plt.xlabel('Backward CAR solving time')
    plt.ylabel('Forward CAR solving time')
    plt.title('Forward and Backward CAR')
    plt.savefig("Fig.5(a).pdf")


    # Fig.5(b)  
    ic3_bm_p = set(); pdr_bm_p = set()
    for e in ic3_bm.keys():
        if 'ic3' in e:
            ic3_bm_p.add(e)
        if 'pdr' in e:
            pdr_bm_p.add(e)
    for e in pdr_bm.keys():
        if 'ic3' in e:
            ic3_bm_p.add(e)
        if 'pdr' in e:
            pdr_bm_p.add(e)

    ic3_x = []; ic3_y = []
    for e in ic3_bm_p:
        print(e, ic3_bm[e], pdr_bm[e])
        ic3_x.append(ic3_bm[e])
        ic3_y.append(pdr_bm[e])
        

    pdr_x = []; pdr_y = []
    for e in pdr_bm_p:
        pdr_x.append(ic3_bm[e])
        pdr_y.append(pdr_bm[e])
    plt.clf()
    plt.scatter(pdr_x, pdr_y, c='#9192C2', marker = 'D', edgecolor = 'grey', label='PDR')
    plt.scatter(ic3_x, ic3_y, c='#63B2EF', marker = 'o', edgecolor = 'grey', label='IC3')
    plt.xlabel('IC3ref solving time')
    plt.ylabel('PDR solving time')
    plt.title('PDR and ic3ref')
    plt.savefig("Fig.5(b).pdf")


main()