#!/usr/bin/env python
# -*- coding: utf-8 -*-

f = open('acronimos.txt', 'r')
linhas = f.readlines()
f.close()


#'''
posmaior = 0
maior = ''
# Pegaer o mais comprido
for ln in linhas:
    if len(ln.split()) > 0:
        if ':' in ln:
            if (ln.find(':') > posmaior) and (ln[0] != '#'):
                posmaior = ln.find(':')
                maior = ln
                print maior
                


'''

# funcao que cria alguma coisa

f = open('novabase2.txt', 'w')
ID = ' \x09'
ID_BASE = ''
for ln in linhas:
    if len(ln.split()) > 0:
        if ID in ln:
            if ln.find(' ') < ln.find(ID):
                continue
            ID_BASE = ln[:ln.find(ID)].upper() + ': '
            resto = ln[ln.find(ID)+len(ID):-1].split(ID)
            for x in resto:
                f.write(ID_BASE + x + '\n')
        else:
            f.write(ID_BASE + ln)
    else:
        f.write('\n')
f.close()

# Repetidos

repetidos = []

i = 0
while i < len(linhas):
    if len(linhas[i]) == 1:
        i+=1
        continue
    x = 0
    while x < len(linhas):
        if len(linhas[x]) == 0:
            x += 1
            continue
        #if (x!=i) and (linhas[x].split()[0] == linhas[i].split()[0]):
        if (x!=i) and (linhas[x].lower().strip() == linhas[i].lower().strip()):
            repetidos += [linhas[i].split()[0]]
        x += 1
    i+=1
    
print len(repetidos)
print ', '.join(repetidos)
   
#'''

#for ln in linhas:
#    if len(ln.split()) > 0:
#        f.write(ln.split()[0] + ': ' + ' '.join(ln.split()[1:]) + '\n')
#    else:
#        f.write('\n')
#f.close()
print 'do'
