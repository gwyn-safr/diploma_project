import database as postgres
import tkinter as tk
from tkinter import ttk
import csv
import os
import sys

config = []
data = []
tableptr = 0
table = ''

def connectionTest(self):

    if (len(config) == 0):
        err = 'No connection string specified.  Please configure your connection'
        self.connectionstr.set(err)
        return False

    if (postgres.connect(config)):
        success = 'Connection Successful'
        self.connectionstr.set(success)
        return True
    else:
        fail = 'Connection failed.  Try configuring env variables'
        self.connectionstr.set(fail)
        return False

def setdefaultconfig(self):

    global config

    dbname = 'postgres'
    user = 'postgres'
    pwd = '1234'
    host = 'localhost'

    config = [host, dbname, user, pwd]

    if (postgres.connect(config)):
        success = 'Connection Successful'
        self.connectionstr.set(success)
        return True

def setConfig(self):

    global config

    dbname = self.dbname.get('1.0', 'end-1c')
    user = self.user.get('1.0', 'end-1c')
    pwd = self.password.get('1.0', 'end-1c')
    host = self.host.get('1.0', 'end-1c')

    config = [host, dbname, user, pwd]
    connectionTest(self)

def getConfig():

    return config

def setData(arr):

    global data
    data = arr

def getData():

    return data

def getTable(self, textbox):

    global table

    table = textbox.get('1.0', 'end-1c')
    output = postgres.view(table)
    self.console.set(output)

def getnextTable(self):
    output = postgres.viewrange(table, tableptr)
    self.console.set(output)


def getprevTable(self):
    output = postgres.viewrange(table, tableptr)
    self.console.set(output)


def getName(textbox):

    table = textbox.get('1.0', 'end-1c')
    print(table)

def drawnewTable(self):
    tv = ttk.Treeview(self)
    tv['show'] = 'headings'
    tv['columns'] = ('1', '2', '3', '4')

    tv.heading('1', text='1', anchor='w')
    tv.column('1', anchor='w', width=100)
    tv.heading('2', text='2', anchor='w')
    tv.column('2', anchor='w', width=100)
    tv.heading('3', text='3', anchor='w')
    tv.column('3', anchor='w', width=100)
    tv.heading('4', text='4', anchor='w')
    tv.column('4', anchor='w', width=100)
    tv.pack()
    self.treeview = tv
    
    


def drawTable(self):

    tv = ttk.Treeview(self)
    tv['show'] = 'headings'
    tv['columns'] = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10')

    tv.heading('1', text='1', anchor='w')
    tv.column('1', anchor='w', width=100)
    tv.heading('2', text='2', anchor='w')
    tv.column('2', anchor='w', width=100)
    tv.heading('3', text='3', anchor='w')
    tv.column('3', anchor='w', width=100)
    tv.heading('4', text='4', anchor='w')
    tv.column('4', anchor='w', width=100)
    tv.heading('5', text='5', anchor='w')
    tv.column('5', anchor='w', width=100)
    tv.heading('6', text='6', anchor='w')
    tv.column('6', anchor='w', width=100)
    tv.heading('7', text='7', anchor='w')
    tv.column('7', anchor='w', width=100)
    tv.heading('8', text='8', anchor='w')
    tv.column('8', anchor='w', width=100)
    tv.heading('9', text='9', anchor='w')
    tv.column('9', anchor='w', width=100)
    tv.heading('10', text='10', anchor='w')
    tv.column('10', anchor='w', width=100)
    tv.pack()
    self.treeview = tv


def loadTable(self, table, textbox):

    global tableptr
    if (table.treeview is not None):
        remove_all(table)
        
    getTable(self, textbox)

    temp = data
    for entry in reversed(temp):
        if len(temp[0]) == 4:
            table.treeview.insert('', 0, values=(entry[0],entry[1], entry[2], entry[3]))
        elif len(temp[0]) == 10:
            table.treeview.insert('', 0, values=(entry[0],entry[1], entry[2], entry[3], entry[4], entry[5], entry[6],entry[7],entry[8],entry[9]))
    
    tableptr = 10
    
def loadNext(self, table, textbox):

    global tableptr
    
    if (table.treeview is not None):
        remove_all(table)

    getnextTable(self)

    temp = data
    for entry in reversed(temp):
        if len(temp[0]) == 4:
            table.treeview.insert('', 0, values=(entry[0],entry[1], entry[2], entry[3]))
        elif len(temp[0]) == 7:
            table.treeview.insert('', 0, values=(entry[0],entry[1], entry[2], entry[3], entry[4], entry[5], entry[6]))
    tableptr += 10
    
    
    
def loadPrev(self, table, textbox):
    
    global tableptr
    if (tableptr > 0):
    
        if (table.treeview is not None):
            remove_all(table)
        tableptr -= 10
        getprevTable(self)

        temp = data
        for entry in reversed(temp):
            if len(temp[0]) == 4:
                table.treeview.insert('', 0, values=(entry[0],entry[1], entry[2], entry[3]))
            elif len(temp[0]) == 7:
                table.treeview.insert('', 0, values=(entry[0],entry[1], entry[2], entry[3], entry[4], entry[5], entry[6]))
        
        

def remove_all(table):
    x = table.treeview.get_children()
    print(x)
    if x != '()':
        for child in x:
            table.treeview.delete(child)