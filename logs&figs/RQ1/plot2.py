import os
import matplotlib.pyplot as plt

"""
    Compare four tool
"""

safe = []  # save safe case time
unsafe = []  # save unsafe case time
case = []

def update_all(path):
    """do not distinguish the safe or unsafe"""
    case.clear()
    f = open(path)
    case.append(0)
    index, max = 1,0
    gen_time = 0.0
    time = 0.0

    line = f.readline()
    if path.find('pdr') != -1:
        while line != '':
            if line.find('gen_time') != -1:
                gen_time = float(line.split(':')[1])
                while gen_time > index:
                    case.append(max)
                    index += 1
                if time > max: max = time
            if line.find('Output') != -1:
                time = float(line.split()[-2])  
            if line.find('Property') != -1:
                time = float(line.split()[-2])           
            if line == '124\n':
                time = 7200           
            line = f.readline()
    else:
        while line != '':
            if line.find('gen_time') != -1:
                str_list = line.split()
                time = float(str_list[2].split(':')[1])
                gen_time = float(str_list[3].split(':')[1])
                if str_list[0] == 'False':
                    while gen_time > index:
                        case.append(max)
                        index += 1
                    if time > max: 
                        max = time
                elif str_list[0] == 'True' or str_list[0] == 'Timeout':
                    while gen_time > index:
                        case.append(max)
                        index += 1
                    if time > max: 
                        max = time
                else:
                    print('ERROR: Undeifined word!')
                    print(line)
                    exit(0)
            line = f.readline()


def draw(filename, pos_up, name):  
    plt.subplot(pos_up) 
    update_all(os.path.join('compare', 'aigrow', filename))
    plt.plot(case, color='#E84446', linewidth=2.5, linestyle='solid', marker='D', markevery=15000, label='AIGROW', markersize=8)  # 深红色

    update_all(os.path.join('compare', 'aigfuzz', filename))
    plt.plot(case, color='#8cc5be', linewidth=2.5, linestyle='solid', marker='^', markevery=15000, label='AIGFUZZ', markersize=10)  # 金黄色

    update_all(os.path.join('compare', 'aigen', filename))
    plt.plot(case, color='#deae8f', linewidth=2.5, linestyle='solid', marker='.', markevery=15000, label='AIGEN', markersize=15)  # 蓝色

    update_all(os.path.join('compare', 'aigrow_no_feedback', filename))
    plt.plot(case, color='#8583a9', linewidth=2.5, linestyle='solid', marker='v', markevery=15000, label='AIGROW-nofeed', markersize=10)  # 绿色

    ax2 = plt.subplot(pos_up)
    ax2.set_title(name, fontsize=32)  
    if filename.find('ic3') != -1:
        plt.legend(bbox_to_anchor=(1.05, 1.35), ncol=2, loc=0, borderaxespad=0,prop={'size': 34})  
    y_ticks = [0, 1000, 3000, 5000, 7000]
    plt.yticks(y_ticks, fontsize=28,)  
    x_ticks = [0, 30000, 60000, 90000]
    plt.xticks(x_ticks, fontsize=28) 
    plt.ylim((-200, 7500))
    plt.axhline(y=7200, color='grey', linestyle='--', linewidth=2)



if __name__ == '__main__':
    plt.figure(figsize=(20,18))
    
    draw('record_bcar.txt', 224, 'Backward CAR')
    draw('record_fcar.txt', 223, 'Forward CAR')
    draw('record_ic3.txt', 222, 'IC3ref')
    draw('record_pdr.txt', 221, 'PDR')

    plt.tight_layout(pad=5)
    plt.savefig('RQ1-Fig3.pdf')
