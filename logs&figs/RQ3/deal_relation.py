from math import floor
import os
import sys
import networkx as nx

f_relation = open(os.path.join(sys.argv[1], 'record.txt'))
f_info = open(os.path.join(sys.argv[1], 'top.txt'))
f_table = open(os.path.join(sys.argv[1], 'table.txt'))

info_top = []
line = f_info.readline()
while line:
    str_list = line.split(' ')
    info_top.append(str_list)
    line = f_info.readline() 

info_table = ['']
line = f_table.readline()
while line:
    str_list = line.split(' ')
    info_table.append(str_list)
    line = f_table.readline() 

G_all = nx.DiGraph()
G_all.add_node(0)

line = f_relation.readline()

while line:
    str_list = line.split()
    if 'reGenerate' in str_list:
        G_all.add_node(str_list[0])
        G_all.add_edge(str_list[0], str_list[5].split('/')[1])
    elif 'generate' in str_list:
        G_all.add_node(str_list[0])
        G_all.add_edge(str_list[0], 0)
    line = f_relation.readline()


G = nx.DiGraph()
for top in info_top:
    time = float(top[3])
    fill_color = '#63b2ee%02x'%floor(time/7200*255) 
    top_name = top[0]
    G.add_node(top_name, style='filled', fillcolor=fill_color, color='#34495e')
    
    while(list(G_all[top_name])[0]):
        pre = list(G_all[top_name])[0]
        time = float(info_table[int(pre.split('.')[0][3:])][3])
        
        fill_color = '#63b2ee%02x'%floor(time/7200*255) 
        G.add_node(pre, style='filled', fillcolor=fill_color, color='#34495e')
        G.add_edge(pre, top_name, color='#34495e')
        top_name = pre

nx.draw_networkx(G, node_color='red')
nx.nx_agraph.write_dot(G, os.path.join(sys.argv[1], 'relation.dot'))

