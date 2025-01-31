#-*- coding : utf-8-*-

import os
import time

start_time = time.time()
class Aiger:
    def __init__(self):
        self.name = ''
        self.frame = 0
        self.time = 0
        self.res = False


def get_frame_time_car(aiger, index):
    f_res = open("res_log/gen" + str(index) + ".res")
    f_log = open("res_log/gen" + str(index) + ".log")
    res_lines = f_res.readlines()
    try:
        if res_lines[0] == '0\n': aiger.res = True
        aiger.frame = len(res_lines)
        # print(aiger.frame)
        log_lines = f_log.readlines()
        str_list = log_lines[len(log_lines)-1].split()
        aiger.time = float(str_list[2])
        # print(aiger.time)
        f_res.close()
        f_log.close()
    except Exception:
        return


def get_frame_time_ic3(aiger, lines):
    if len(lines) < 14:
        aiger.frame = 0
        aiger.time = 0.0
        if lines[len(lines)-3] == '0':
            aiger.res = True
    else:
        time_str = lines[0]
        frame_str = lines[2]
        time = time_str.split(':')[1]
        frame = frame_str.split(':')[1]
        aiger.time = float(time)
        aiger.frame = int(frame)
        if lines[len(lines)-3] == '0':
            aiger.res = True
    

def get_frame_time_pdr(aiger, str_list):
    str_1 = ''
    str_2 = ''
    for i in range(len(str_list)):
        if str_list[i].startswith('Output') or str_list[i].startswith('Invariant'):
            str_1 = str_list[i]
        if str_list[i].startswith('Property'):
            str_2 = str_list[i]
    list = str_1.split()
    if str_1 == '':
        print("ERROR!") 
        return 1
    if list[0] == 'Output':
        for i in range(len(list)):
            if list[i] == 'frame':
                aiger.frame = int(list[i+1][0:-1])
            if list[i] == '=':
                aiger.time = float(list[i+1])
    elif list[0] == 'Invariant':
        aiger.res = True  # case is safe
        aiger.frame = int(list[1][2:-1])
    else:
        print("取出frame错误!")
        return 1

    if str_2 != '':
        list_2 = str_2.split()
        for i in range(len(list_2)):
            if list_2[i] == '=':
                aiger.time = float(list_2[i+1])
    
    return 0


def main():
    index = 1
    while index < 1000000:
        f = open(os.path.join('aigerfile', 'gen'+str(index)+'.aag'),'w')
        res = os.popen('./bin/aigfuzz -a')
        output = res.read()
        # print(output)
        lines = output.split("\n")
        if lines[-1].find('closure'):
            for i in range(len(lines)):
                lines[i] = lines[i] + '\n'
            # print(lines)
            f.writelines(lines[:-12])
        else:
            for i in range(len(lines)):
                lines[i] = lines[i] + '\n'
            f.writelines(lines[:-15])
        f.close()

        # aigtoaig
        res_toaig = os.popen('./bin/aigtoaig aigerfile/gen'+str(index)+'.aag aigerfile/gen'+str(index)+'.aig')
        toaig_gen = res_toaig.read()

        aiger = Aiger()
        # verify fcar
        of_fcar = open("result/record_fcar.txt",'a')
        res_fcar = os.popen('./check_fcar.sh '+str(index))
        fcar_gen = res_fcar.read()
        if fcar_gen.split('\n')[0] == '124':
            aiger.time = 7200 
        else:
            get_frame_time_car(aiger, index)
        end_time = time.time()
        of_fcar.write('generate gen'+str(index)+' '+lines[0])
        of_fcar.write(str(aiger.res) + ' frame:' + str(aiger.frame) + ' time:' + str(aiger.time) +' gen_time:' + str(end_time-start_time)+ '\n')
        of_fcar.close()

        #verify bcar
        # of_bcar = open("result/record_bcar.txt",'a')
        # res_bcar = os.popen('./check_bcar.sh '+str(index))
        # bcar_gen = res_bcar.read()
        # if bcar_gen.split('\n')[0] == '124':
        #     aiger.time = 7200
        # else:
        #     get_frame_time_car(aiger, index)
        # end_time = time.time()
        # of_bcar.write('generate gen'+str(index)+' '+lines[0])
        # of_bcar.write(str(aiger.res) + ' frame:' + str(aiger.frame) + ' time:' + str(aiger.time) +' gen_time:' + str(end_time-start_time)+ '\n')
        # of_bcar.close()

        #verify ic3
        # of_ic3 = open("result/record_ic3.txt",'a')
        # res_ic3 = os.popen('./check_ic3.sh '+str(index))
        # ic3_gen = res_ic3.read().split('\n')
        # if ic3_gen[len(ic3_gen)-2] == '124':
        #     aiger.time = 7200
        # else:
        #     get_frame_time_ic3(aiger, ic3_gen)
        # end_time = time.time()
        # of_ic3.write('generate gen'+str(index)+' '+lines[0])
        # of_ic3.write(str(aiger.res) + ' frame:' + str(aiger.frame) + ' time:' + str(aiger.time) +' gen_time:' + str(end_time-start_time)+ '\n')
        # of_ic3.close()

        #verify pdr
        # of_pdr = open("result/record_pdr.txt",'a')
        # res_pdr = os.popen('./check_pdr.sh '+str(index))
        # pdr_output = res_pdr.read()
        # pdr_gen = pdr_output.split('\n')
        # if pdr_gen[-2] == '124':
        #     aiger.time = 7200
        # elif get_frame_time_pdr(aiger, pdr_gen):
        #     print("PDR Error!")
        #     print(index)
        # end_time = time.time()
        # of_pdr.write('generate gen'+str(index)+' '+lines[0])
        # # of_bcar.write(str(aiger.res) + ' frame:' + str(aiger.frame) + ' time:' + str(aiger.time) + '\n')
        # of_pdr.write(pdr_output)
        # of_pdr.write('gen_time:' + str(end_time-start_time)+'\n')
        # of_pdr.close()

        print(index)
        index += 1



if __name__=='__main__':
    main()