import os
import matplotlib.pyplot as plt

"""
    Plot the results with four different paras
"""

safe = []  # save safe case time 
unsafe = []  # save unsafe case time

case = []
name = {
    'backward_car' : 'Backward CAR',
    'forward_car' : 'Forward CAR',
    'ic3-ref' : 'IC3ref',
    'abc-pdr' : 'PDR'
}

def update_all(path):
    """do not distinguish the safe or unsafe"""
    case.clear()
    f = open(path)
    case.append(0)
    index, max = 1,0
    gen_time = 0.0

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
                        # unsafe[un_index] = un_max
                        case.append(max)
                        index += 1
                    if time > max: max = time
                elif str_list[0] == 'True' or str_list[0] == 'Timeout':
                    while gen_time > index:
                        # safe[s_index] = s_max
                        case.append(max)
                        index += 1
                    if time > max: max = time
                else:
                    print('ERROR: Undeifined word!')
                    print(line)
                    exit(0)
            line = f.readline()


def draw_all(filename, pos):
    """do not distinguish safe or unsafe"""
     # 15-70-15
    plt.subplot(pos)
    update_all(os.path.join(filename,'15-70-15.txt'))
    line1, = plt.plot(case, color='#E84446', linewidth=2.5, linestyle='solid', marker='^', markevery=15000,label='para1', markersize=10)

    # 25-50-25
    plt.subplot(pos)
    update_all(os.path.join(filename,'25-50-25.txt'))
    line2, = plt.plot(case, color='#8cc5be', linewidth=2.5, linestyle='solid', marker='.', markevery=15000, label='para2', markersize=15)
        
    # 20-40-40
    plt.subplot(pos)
    update_all(os.path.join(filename,'20-40-40.txt'))
    line3, = plt.plot(case, color='#deae8f', linewidth=2.5, linestyle='solid', marker='D', markevery=15000,label='para3', markersize=8)

    # 40-40-20
    plt.subplot(pos)
    update_all(os.path.join(filename,'40-40-20.txt'))
    line4, = plt.plot(case, color='#8583a9', linewidth=2.5, linestyle='solid', marker='v', markevery=15000,label='para4', markersize=10)

    ax1 = plt.subplot(pos)
    ax1.set_title(name[filename], fontsize=32)
    if filename.find('ic3') != -1:
        plt.legend(bbox_to_anchor=(1.05, 1.35),handles=[line1, line2, line3, line4], ncol = 2, loc=0, borderaxespad=0, fontsize=34)

    y_ticks = [0,1000, 3000, 5000, 7000]
    plt.yticks(y_ticks, fontsize=28)
    x_ticks = [0, 30000, 60000, 90000]
    plt.xticks(x_ticks, fontsize=28)
    plt.ylim((-200,7500))
    plt.axhline(y=7200, color='grey', linestyle='--', linewidth=2)


if __name__ == '__main__':
    plt.figure(figsize=(20,18))

    draw_all('backward_car', 224)
    draw_all('forward_car', 223)
    draw_all('ic3-ref', 222)
    draw_all('abc-pdr', 221)

    plt.tight_layout(pad=5)
    plt.savefig('RQ1-Fig4.pdf')