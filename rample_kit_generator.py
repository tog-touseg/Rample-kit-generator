from tkinter import *
from tkinter import ttk
import os
import tkinter as tk
import simpleaudio as sa
from natsort import natsorted
import string
from tkinter import filedialog
import shutil
import pickle

# from urlparse import urlparse
# path = urlparse(url_string).path
# ext = os.path.splitext(path)[1]
# if ext in extensionsToCheck:
#   print(url_string)

# check extension (wav mp3 flac)
# autofocus on last selected on sp_tree 

idx = 0
selected_kit = 'A0'
selected_sample = ''
orig_path = ''
orig_file = ''
selected_layer = ''

def edit(event):
    tree = event.widget
    if (tree == kits_tree and tree.identify_column(event.x) == '#2') or (tree in sp_trees and tree.identify_column(event.x) == '#3') :
        # the user clicked on a cell

        def ok(event):
            """Change item value."""
            tree.set(item, column, entry.get())
            entry.destroy()
            if tree == sp1_tree:
                offset = 12
            elif tree == sp2_tree:
                offset = 36
            elif tree == sp3_tree:
                offset = 60
            elif tree == sp4_tree:
                offset = 84

            data[selected_kit][int(layer)-1+offset] = tree.set(item, column)
            # with open(os.getcwd() + '/kit_data.pkl', 'wb') as handle:
            #     pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

        it = tree.focus()
        it = tree.item(it)
        layer = it['values'][0]

        column = tree.identify_column(event.x)  # identify column
        item = tree.identify_row(event.y)  # identify item
        x, y, width, height = tree.bbox(item, column) 
        value = tree.set(item, column)

    else:
        return
    # display the Entry   
    entry = ttk.Entry(tree)  # create edition entry
    entry.place(x=x, y=y, width=width, height=height,
                anchor='nw')  # display entry on top of cell
    entry.insert(0, value)  # put former value in entry
    # entry.bind('<FocusOut>', lambda e: entry.destroy())  
    entry.bind('<FocusOut>', ok)  
    entry.bind('<Return>', ok)  # validate with Enter
    entry.focus_set()

def explorer_select(event):
    curr_item = event.widget.focus()
    tags = event.widget.item(curr_item)['tags']

    if 'sample' in tags:
        sa.stop_all()
        wave_obj = sa.WaveObject.from_wave_file(tags[1])
        wave_obj.play()
        global orig_path
        global orig_file
        global selected_sample
        orig_path = tags[1]
        orig_file = orig_path.split("/")[-1]
        selected_sample = orig_file

def kit_select(event):
    curr_item = event.widget.focus()
    values = event.widget.item(curr_item)['values']
    global selected_kit
    selected_kit = values[0]
    for e in sp_trees:
        e.delete(*e.get_children())

    content1 = []
    content2 = []
    content3 = []
    content4 = []

    for x in range(12):
        content1.append((str(x+1), data[selected_kit][x].split('/')[-1], data[selected_kit][x+12]))
        content2.append((str(x+1), data[selected_kit][x+24].split('/')[-1], data[selected_kit][x+36]))
        content3.append((str(x+1), data[selected_kit][x+48].split('/')[-1], data[selected_kit][x+60]))
        content4.append((str(x+1), data[selected_kit][x+72].split('/')[-1], data[selected_kit][x+84]))

    for idx, x in enumerate(content1):
        sp1_tree.insert('', 'end', values=content1[idx])
        sp2_tree.insert('', 'end', values=content2[idx])
        sp3_tree.insert('', 'end', values=content3[idx])
        sp4_tree.insert('', 'end', values=content4[idx])


def update_tree(tree, offset):
    tree.delete(*tree.get_children())

    content = []
    for x in range(12):
        content.append((str(x+1), data[selected_kit][x+offset].split('/')[-1], data[selected_kit][x+12+offset]))

    for x in content:
        tree.insert('', 'end', values=x)

def generate_tree(path,parent,tree):    
    for p in reversed(sorted(os.listdir(path))):
        abspath = os.path.join(path, p)
        if ".wav" in p:
            global idx
            idx = idx + 1
            if idx % 2:
                parent_element = tree.insert(parent, '0', text=p, open=False, tags=('sample', abspath, 'even'))
            else:
                parent_element = tree.insert(parent, '0', text=p, open=False, tags=('sample', abspath, 'odd'))

        if os.path.isdir(abspath):
            parent_element = tree.insert(parent, '0', text=p, open=False, tags=('dir', abspath))
            generate_tree(abspath, parent_element, tree)


window = Tk()
window.geometry('885x660+700+200')
window.resizable(False, False)
# window.configure(bg='black')
# window.columnconfigure(0, weight=1)
# window.columnconfigure(1, weight=1)
# window.rowconfigure(2, weight=1)

explorer_tree = ttk.Treeview(window ,height=12)
explorer_tree.tag_configure('odd', background='#EEEEEE')
explorer_tree.tag_configure('even', background='#DFDFDF')

vsb1 = ttk.Scrollbar(window, orient="vertical", command=explorer_tree.yview)
explorer_tree.configure(yscrollcommand=vsb1.set)
explorer_tree.heading("#0" ,text="Explorer")

def create_explorer_tree(path):
    # tree.pack(expand=YES,fill=BOTH)
    root = explorer_tree.insert('', 'end', text=path.split('/')[-1], open=True)
    generate_tree(path,root,explorer_tree)

# init_path = '/home/morgane/Bureau/Pulsar_23_Samples'
# init_path = os.getcwd()
# create_explorer_tree(init_path)

columns = ('kit', 'tag')

kits_tree = ttk.Treeview(window, columns=columns, show='headings', height=12)

kits_tree.heading("#0", text="Kits")
kits_tree.heading('kit', text='Kit')
kits_tree.heading('tag', text='Tag')

kits_tree.column("kit", minwidth=0, width=50, stretch=NO)
kits_tree.column("tag", minwidth=0, width=100, stretch=NO)

kits = []
alpha = list(string.ascii_uppercase)
for a in alpha:
    for x in range(10):
        kits.append((a + str(x), ' '))

for i in kits:
    kits_tree.insert('', 'end', values=i) #text=str(i))

vsb2 = ttk.Scrollbar(window, orient="vertical", command=kits_tree.yview)
kits_tree.configure(yscrollcommand=vsb2.set)

data_path = os.getcwd() + '/kit_data.pkl'
if os.path.exists(data_path):
    with open(os.getcwd() + '/kit_data.pkl', 'rb') as handle:
        data = pickle.load(handle)
        init_path = data['memory'][0]
        if not os.path.exists(init_path):
            init_path = os.getcwd()
else:
    data = {}
    for e in kits:
        data[e[0]] = ['']*12*2*4
    
    data['memory'] = [os.getcwd()]
    with open(os.getcwd() + '/kit_data.pkl', 'wb') as handle:
            pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)


create_explorer_tree(init_path)

child_id = kits_tree.get_children()[0]
kits_tree.focus(child_id)
kits_tree.selection_set(child_id)


def create_sample_tree():
    columns = ('layer', 'name', 'path')

    tree = ttk.Treeview(window, columns=columns, show='headings', height=12)

    tree.heading("#0", text="Sample Track")
    tree.heading('name', text='File Name')
    tree.heading('path', text='Rename')
    tree.heading('layer', text='#')

    tree.column("name", minwidth=0, width=100, stretch=NO)
    tree.column("path", minwidth=0, width=100, stretch=NO)
    tree.column("layer", minwidth=0, width=25, stretch=NO)

    # content = []
    # for x in range(12):
    #     content.append((str(x+1), ' ', ' '))

    # for x in content:
    #     tree.insert('', 'end', values=x)

    return tree

sp1_tree = create_sample_tree()
sp2_tree = create_sample_tree()
sp3_tree = create_sample_tree()
sp4_tree = create_sample_tree()

sp_trees = [sp1_tree, sp2_tree, sp3_tree, sp4_tree]

padding = 5
kits_tree.grid(column=0, row=1, rowspan=3, sticky=tk.N+tk.S, padx=padding, pady=padding)
explorer_tree.grid(column=2, row=1, rowspan=3, sticky=tk.N+tk.S, padx=padding, pady=padding)
vsb1.grid(row=1, column=3, rowspan=3, sticky='ns')
vsb2.grid(row=1, column=1, rowspan=3, sticky='ns')

from tkinter import font
label_font = font.Font(weight="bold")

Label(window, text="SP1").grid(row=0,column=4)
sp1_tree.grid(row=1,column=4,sticky=tk.N, padx=padding,pady=padding)

Label(window, text="SP2").grid(row=0,column=5)
sp2_tree.grid(row=1,column=5,sticky=tk.N, padx=padding,pady=padding)

Label(window, text="SP3").grid(row=2,column=4, sticky='s')
sp3_tree.grid(row=3,column=4,sticky=tk.N, padx=padding,pady=padding)

Label(window, text="SP4").grid(row=2,column=5, sticky='s')
sp4_tree.grid(row=3,column=5,sticky=tk.N, padx=padding,pady=padding)

Label(window, text="RAMPLE kit generator", font=label_font).grid(row=0,column=2, sticky='s')

help_text = Label(window, text="keyboard shortcuts description", justify='left', fg='#FF0000').grid(row=5,column=0, columnspan=4, sticky='w', padx=padding, pady=padding)
save_text = Label(window, text="saved message", justify='right', fg='#00AA00').grid(row=5,column=4, columnspan=2, sticky='e', padx=padding, pady=padding)


def browse_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global init_path
    filename = filedialog.askdirectory(initialdir=init_path, title="Select directory")
    if (filename):  
        folder_path.set(filename)
        explorer_tree.delete(*explorer_tree.get_children())
        create_explorer_tree(filename)
        init_path = filename
        data['memory'][0] = init_path
        with open(os.getcwd() + '/kit_data.pkl', 'wb') as handle:
            pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

def copy_sample(layer, order, source, dest, new_name):
    if source != '':
        if new_name == '':
            name = source.split('/')[-1]
            shutil.copy(source, dest + str(layer) + " l" + str(order+1) + " " + name)
        else:
            shutil.copy(source, dest + str(layer) + " l" + str(order+1) + " " + new_name + ".wav")

def save_button():

    with open(os.getcwd() + '/kit_data.pkl', 'wb') as handle:
                pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

    save_path = os.getcwd()
    shutil.rmtree(save_path + '/kits/')

    for e in data:
        count = 0
        for s in data[e]:
            if s == '':
                count = count + 1

        if count < 12*2*4:
            
            if not os.path.exists(save_path + "/kits"):
                os.makedirs(save_path + "/kits")
            if not os.path.exists(save_path + "/kits/" + e):
                os.makedirs(save_path + "/kits/" + e)
            # clear folder before saving
            for i in range(12):
                copy_sample(1, i, data[e][i], save_path + "/kits/" + e + "/", data[e][i+12])
                copy_sample(2, i, data[e][i+24], save_path + "/kits/" + e + "/", data[e][i+36])
                copy_sample(3, i, data[e][i+46], save_path + "/kits/" + e + "/", data[e][i+60])
                copy_sample(4, i, data[e][i+72], save_path + "/kits/" + e + "/", data[e][i+84])


folder_path = StringVar()
# load_lbl = Label(master=window,textvariable=folder_path)
# load_lbl.grid(row=4, column=1)
load_btn = Button(text="Browse", command=browse_button)
load_btn.grid(row=4, column=2)

load_btn = Button(text="Save", command=save_button)
load_btn.grid(row=4, column=5, sticky=tk.E)

def select_layer(event):
    # selected_layer = n + tree
    tree = event.widget
    item = tree.identify_row(event.y)  # identify item
    x, y, width, height = tree.bbox(item, 0) 
    value = tree.set(item, 0)
    global selected_layer
    selected_layer = int(value)

    if tree == sp1_tree:
        offset = 0
    elif tree == sp2_tree:
        offset = 24
    elif tree == sp3_tree:
        offset = 48
    elif tree == sp4_tree:
        offset = 72

    sample = data[selected_kit][int(value)+offset-1]
    if sample != '':
        sa.stop_all()
        wave_obj = sa.WaveObject.from_wave_file(sample)
        wave_obj.play()

def delete_layer(event):
    tree = event.widget
    item = tree.identify_row(event.y)  # identify item
    x, y, width, height = tree.bbox(item, 0) 
    value = tree.set(item, 0)

    if tree == sp1_tree:
        offset = 0
    elif tree == sp2_tree:
        offset = 24
    elif tree == sp3_tree:
        offset = 48
    elif tree == sp4_tree:
        offset = 72

    data[selected_kit][int(value)+offset-1] = ''
    data[selected_kit][int(value)+offset-1+12] = ''
    update_tree(tree, offset)

def mouse_wheel_up(event):
    tree = event.widget
    global selected_layer

    child_id = tree.get_children()[selected_layer-1]
    tree.focus(child_id)
    tree.selection_set(child_id)

    if tree == sp1_tree:
        offset = 0
    elif tree == sp2_tree:
        offset = 24
    elif tree == sp3_tree:
        offset = 48
    elif tree == sp4_tree:
        offset = 72

    if selected_layer > 1:
        selected_layer = selected_layer-1
    

        selection = offset+selected_layer
        if selection >= offset:
            data[selected_kit][selection], data[selected_kit][selection-1] = data[selected_kit][selection-1], data[selected_kit][selection]

            data[selected_kit][selection+12],data[selected_kit][selection+12-1] = data[selected_kit][selection+12-1], data[selected_kit][selection+12]

            update_tree(tree, offset)

        child_id = tree.get_children()[selected_layer-1]
        tree.focus(child_id)
        tree.selection_set(child_id)


def mouse_wheel_down(event):
    tree = event.widget
    global selected_layer
    child_id = tree.get_children()[selected_layer-1]
    tree.focus(child_id)
    tree.selection_set(child_id)

    if tree == sp1_tree:
        offset = 0
    elif tree == sp2_tree:
        offset = 24
    elif tree == sp3_tree:
        offset = 48
    elif tree == sp4_tree:
        offset = 72

    if selected_layer < 12:
        selected_layer = selected_layer + 1

        selection = offset+selected_layer
        if selection <= offset+12 :
            data[selected_kit][selection-2], data[selected_kit][selection-1] = data[selected_kit][selection-1], data[selected_kit][selection-2]

            data[selected_kit][selection+12-2],data[selected_kit][selection+12-1] = data[selected_kit][selection+12-1], data[selected_kit][selection+12-2]

            update_tree(tree, offset)

        child_id = tree.get_children()[selected_layer-1]
        tree.focus(child_id)
        tree.selection_set(child_id)


def enter(event):
    global selected_layer
    tree = event.widget
    curr_item = tree.focus()
    n = tree.item(curr_item)['values']
    if n != '':
        selected_layer = int(n[0])
    else:
        selected_layer = 0


explorer_tree.bind('<<TreeviewSelect>>', explorer_select)
kits_tree.bind('<<TreeviewSelect>>', kit_select)
kits_tree.bind('<Double-1>', edit)
for e in sp_trees:
    e.bind('<Double-1>', edit)
    e.bind('<Button-1>', select_layer)
    e.bind('<Button-3>', delete_layer)
    e.bind('<Button-4>', mouse_wheel_up)
    e.bind('<Button-5>', mouse_wheel_down)
    e.bind('<Enter>', enter)

def insert_sample(tree):
    if tree == sp1_tree:
        offset = 0
        msg = 'SP1'
    elif tree == sp2_tree:
        offset = 24
        msg = 'SP2'
    elif tree == sp3_tree:
        offset = 48
        msg = 'SP3'
    elif tree == sp4_tree:
        offset = 72
        msg = 'SP4'

    if selected_sample != '':
        count = 0
        for i in range(12):
            if (data[selected_kit][i+offset] == ''):
                data[selected_kit][i+offset] = orig_path
                update_tree(tree, offset)
                break
            count = count + 1
        if count == 12:
            print(msg + 'FULL')

def key_pressed(event):
    match event.keysym:
        case 'a':
            insert_sample(sp1_tree)
        case 'z':
            insert_sample(sp2_tree)
        case 'e':
            insert_sample(sp3_tree)
        case 'r':
            insert_sample(sp4_tree)
                
        case '_':
            pass

window.bind('<Key>', key_pressed)

window.mainloop()