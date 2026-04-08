'''Converts an INT rule to a History rule.'''
import os
import sys
try:
    from .findgenera import getgenera
    from .hensel import RuleHandler
except ImportError:
    from findgenera import getgenera
    from hensel import RuleHandler
rh = RuleHandler()
def getline(condition):
    '''Returns the line in a ruletable needed for a condition.'''
    if condition == 'B1e':
        return '0,1,0,0,0,0,0,0,0,1'
    if condition == 'B1c':
        return '0,0,1,0,0,0,0,0,0,1'
    if condition == 'B2a':
        return '0,1,1,0,0,0,0,0,0,1'
    if condition == 'B2c':
        return '0,0,1,0,1,0,0,0,0,1'
    if condition == 'B2e':
        return '0,1,0,1,0,0,0,0,0,1'
    if condition == 'B2i':
        return '0,1,0,0,0,1,0,0,0,1'
    if condition == 'B2k':
        return '0,1,0,0,1,0,0,0,0,1'
    if condition == 'B2n':
        return '0,0,1,0,0,0,1,0,0,1'
    if condition == 'B3a':
        return '0,1,1,1,0,0,0,0,0,1'
    if condition == 'B3c':
        return '0,0,1,0,1,0,1,0,0,1'
    if condition == 'B3e':
        return '0,1,0,1,0,1,0,0,0,1'
    if condition == 'B3i':
        return '0,0,1,1,1,0,0,0,0,1'
    if condition == 'B3j':
        return '0,1,0,1,1,0,0,0,0,1'
    if condition == 'B3k':
        return '0,1,0,1,0,0,1,0,0,1'
    if condition == 'B3n':
        return '0,1,1,0,1,0,0,0,0,1'
    if condition == 'B3q':
        return '0,1,1,0,0,0,1,0,0,1'
    if condition == 'B3r':
        return '0,1,1,0,0,1,0,0,0,1'
    if condition == 'B3y':
        return '0,1,0,0,1,0,1,0,0,1'
    if condition == 'B4a':
        return '0,1,1,1,1,0,0,0,0,1'
    if condition == 'B4c':
        return '0,0,1,0,1,0,1,0,1,1'
    if condition == 'B4e':
        return '0,1,0,1,0,1,0,1,0,1'
    if condition == 'B4i':
        return '0,1,1,0,1,1,0,0,0,1'
    if condition == 'B4j':
        return '0,1,1,0,0,1,0,1,0,1'
    if condition == 'B4k':
        return '0,1,1,0,1,0,0,1,0,1'
    if condition == 'B4n':
        return '0,0,1,1,1,0,1,0,0,1'
    if condition == 'B4q':
        return '0,1,1,1,0,0,1,0,0,1'
    if condition == 'B4r':
        return '0,1,1,1,0,1,0,0,0,1'
    if condition == 'B4t':
        return '0,0,1,1,1,0,0,1,0,1'
    if condition == 'B4w':
        return '0,0,1,1,0,1,1,0,0,1'
    if condition == 'B4z':
        return '0,1,1,0,0,1,1,0,0,1'
    if condition == 'B5a':
        return '0,0,1,1,1,1,1,0,0,1'
    if condition == 'B5c':
        return '0,1,0,1,1,1,0,1,0,1'
    if condition == 'B5e':
        return '0,0,1,0,1,1,1,0,1,1'
    if condition == 'B5i':
        return '0,1,1,1,1,1,0,0,0,1'
    if condition == 'B5j':
        return '0,1,1,1,1,0,1,0,0,1'
    if condition == 'B5k':
        return '0,0,1,1,0,1,1,0,1,1'
    if condition == 'B5n':
        return '0,1,0,1,1,1,1,0,0,1'
    if condition == 'B5q':
        return '0,1,1,1,0,1,1,0,0,1'
    if condition == 'B5r':
        return '0,0,0,1,1,0,1,1,1,1'
    if condition == 'B5y':
        return '0,1,0,1,1,0,1,1,0,1'
    if condition == 'B6a':
        return '0,0,1,1,1,1,1,1,0,1'
    if condition == 'B6c':
        return '0,1,0,1,1,1,1,1,0,1'
    if condition == 'B6e':
        return '0,0,1,1,1,1,1,0,1,1'
    if condition == 'B6i':
        return '0,0,1,1,1,0,1,1,1,1'
    if condition == 'B6k':
        return '0,0,1,1,0,1,1,1,1,1'
    if condition == 'B6n':
        return '0,1,1,1,0,1,1,1,0,1'
    if condition == 'B7c':
        return '0,1,0,1,1,1,1,1,1,1'
    if condition == 'B7e':
        return '0,0,1,1,1,1,1,1,1,1'
    if condition == 'B8':
        return '0,1,1,1,1,1,1,1,1,1'
    if condition == 'S0':
        return '1,0,0,0,0,0,0,0,0,1'
    condition = condition.replace('S', 'B')
    transition = getline(condition)
    return '1' + transition[1:]
def comjoin(alist):
    '''Joins a list into a comma separated string.'''
    string = ''
    for x in alist:
        string += str(x) + ','
    return string[:-1]
def makehistory(rule):
    '''Returns a ruletable for <rule>History.'''
    genera = getgenera(rule)
    if genera not in ['b3s23life', 'lifelike', 'isotropic']:
        raise ValueError('Only INT rules and their subsets can be converted to History rules.''')
    conditions = rh.parserule(rule)
    rule = rh.canoniserule(rule).replace('b', 'B').replace('s', '/S')
    #Generate the start of the ruletable:
    ruletable = '@RULE '+rule+'History'
    ruletable += '''
Automatically generated ruletable for simulating '''+rule+'''History.

@TABLE

n_states:7
neighborhood:Moore
symmetries:rotate4reflect
'''
    #Variables:
    ruletable += '''
var a = {0,2,4,6}
var b = {0,2,4,6}
var c = {0,2,4,6}
var d = {0,2,4,6}
var e = {0,2,4,6}
var f = {0,2,4,6}
var g = {0,2,4,6}
var h = {0,2,4,6}
var i = {0,2,4,6}

var A = {1,3,5}
var B = {1,3,5}
var C = {1,3,5}
var D = {1,3,5}
var E = {1,3,5}
var F = {1,3,5}
var G = {1,3,5}
var H = {1,3,5}
var I = {1,3,5}
var J = {3,5}
var K = {0,2}

var m = {0,1,2,3,4,5,6}
var n = {0,1,2,3,4,5,6}
var o = {0,1,2,3,4,5,6}
var p = {0,1,2,3,4,5,6}
var q = {0,1,2,3,4,5,6}
var r = {0,1,2,3,4,5,6}
var s = {0,1,2,3,4,5,6}
var t = {0,1,2,3,4,5,6}
var u = {0,1,2,3,4,5,6}
'''
    #Conditions for boundary cells:
    ruletable += '''
6,m,n,o,p,q,r,s,t,6
J,6,m,n,o,p,q,r,s,4
J,m,6,n,o,p,q,r,s,4
1,6,m,n,o,p,q,r,s,2
1,m,6,n,o,p,q,r,s,2
'''
    birthconditions = [x for x in conditions if x.startswith('B')]
    survivalconditions = [x for x in conditions if x.startswith('S')]
    #Conditions for marked birth:
    for x in birthconditions:
        splitcon = getline(x).split(',')
        splitcon[0] = '4'
        splitcon[9] = '3'
        alive = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        dead = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
        while splitcon.count('1') > 0:
            splitcon[splitcon.index('1')] = alive.pop(0)
        while splitcon.count('0') > 0:
            splitcon[splitcon.index('0')] = dead.pop(0)
        ruletable += comjoin(splitcon) + '\n'
    ruletable += '\n\n'
    #Conditions for survival:
    for x in survivalconditions:
        splitcon = getline(x).split(',')
        splitcon[0] = 'A'
        splitcon[9] = 'A'
        alive = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        dead = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
        while splitcon.count('1') > 0:
            splitcon[splitcon.index('1')] = alive.pop(0)
        while splitcon.count('0') > 0:
            splitcon[splitcon.index('0')] = dead.pop(0)
        ruletable += comjoin(splitcon) + '\n'
    ruletable += '\n\n'
    #Conditions for normal birth:
    for x in birthconditions:
        splitcon = getline(x).split(',')
        splitcon[0] = 'K'
        splitcon[9] = 'K'
        alive = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        dead = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
        while splitcon.count('1') > 0:
            splitcon[splitcon.index('1')] = alive.pop(0)
        while splitcon.count('0') > 0:
            splitcon[splitcon.index('0')] = dead.pop(0)
        splitcon[9] = '1'
        ruletable += comjoin(splitcon) + '\n'
    #Conditions for death:
    ruletable += '''
J,m,n,o,p,q,r,s,t,4
1,m,n,o,p,q,r,s,t,2
'''
    #Colours (mainly useful when testing with Golly):
    ruletable += '''@COLORS

1    0  255    0
2    0    0  128
3  216  255  216
4  255    0    0
5  255  255    0
6   96   96   96'''
    return ruletable
