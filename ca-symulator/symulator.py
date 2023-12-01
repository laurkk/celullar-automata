#!/usr/bin/env python

from random import uniform, randint
import sys


'''Przetwarza plik na listę sąsiedztw'''
def create_own_CA(file):
    try:
        f=open(file,'r')
    except IOError:
        print('Cannot open the neighbourhood file: ', file)   
    else:
        ff=f.read().splitlines()
        CA={}
        for x in ff: 
            line=x.split()
            n=[]
            for x in line[2].split(','):
                n.append(int(x))
            CA[int(line[0])]=n
        f.close()
        return CA
  
'''Generuje listę sąsiedztw Moora dla siatki 2D o wymiarach n x n '''  
def create_moore(n):
    CA={}
    
    CA[0]=[1,n,n+1]
    
    for k in range(1, n-1):
        CA[k]=[k-1, k+1, k+n, k+n-1, k+n+1]
        
    CA[n-1]=[n-2, 2*n-1, 2*n-2]
    
    CA[n**2-n]=[n**2-2*n, n**2-2*n+1, n**2-n+1]
    
    CA[n**2-1]=[n**2-1-n, n**2-2-n, n**2-2]
    
    for k in range(n**2-n+1, n**2-1):
        CA[k]=[k-n, k-n-1, k-n+1, k-1, k+1]
        
    for k in range(n, n**2-2*n+1, n):
        CA[k]=[k-n, k-n+1 ,k+1, k+n, k+n+1]
    
    for k in range(2*n-1, n**2-n, n):
        CA[k]=[k-n, k-n-1, k-1, k+n, k+n-1]

    rest=set(range(0,n**2)).difference(set(CA.keys()))  
    for k in rest:
        CA[k]=[k-n-1, k-n, k+n, k-n+1, k-1, k+1, k+n-1, k+n+1]
    
    return CA


'''Generuje listę sąsiedztw von Neumanna dla siatki 2D o wymiarach n x n '''
def create_von_neumann(n):
    CA={}
    
    CA[0]=[1,n]
    
    for k in range(1, n-1):
        CA[k]=[k-1, k+1, k+n]
        
    CA[n-1]=[n-2, 2*n-1]
    
    CA[n**2-n]=[n**2-2*n, n**2-n+1]
    
    CA[n**2-1]=[n**2-1-n, n**2-2]
    
    for k in range(n**2-n+1, n**2-1):
        CA[k]=[k-n, k-1, k+1]
        
    for k in range(n, n**2-2*n+1, n):
        CA[k]=[k-n, k+1, k+n]
    
    for k in range(2*n-1, n**2-n, n):
        CA[k]=[k-n, k+n, k-1]

    rest=set(range(0,n**2)).difference(set(CA.keys()))
    for k in rest:
        CA[k]=[k-n, k+n, k+1, k-1]
    
    return CA


'''Generuje losowe warunki początkowe rozsiewając stany od 0 do number_of_states'''    
def random(number_of_states, CA):
    CA_states=list(range(0,len(CA)))

    for x in range(0,len(CA)):
        CA_states[x]=randint(0, number_of_states-1)
        
    return CA_states


'''Przetwarza plik na zagnieżdżoną listę reguł'''   
def get_rules(file):
    try:
        f=open(file,'r')
    except IOError:
        print('Cannot open the rules file: ', file)
    else:
        ff=f.read().splitlines()
        rules=[]
        
        for x in ff: 
            line=x.split('\t')
            for i in range(len(line)-1):line[i]=int(line[i])
            rules.append(line)
        f.close()
        return rules    


'''Ewolucja automatu komórkowego na podstawie zasad dostarczonych w pliku,
 po każdym kroku czasowym stan CA jest zapisywany do listy wynikowej''' 
def evolution(CA, timesteps, list_of_states, file):
    old_states=list_of_states.copy()
    new_states=list_of_states.copy()
    rules=get_rules(file)
    results=[]
    for i in range(0,timesteps):
        for k in CA:
            neighbours=[old_states[x] for x in CA[k]]   #przygotowanie listy stanów sąsiadów komórki
            new_states[k]=transition(old_states[k], neighbours, rules)  #przypisanie nowego stanu w liście nowych stanów (t+1)
        results.append(new_states.copy())                                      # na podstawie listy starych stanów (t) i zasad przejścia
        old_states,new_states=new_states,old_states 
    return results


def P(x):
    return x


'''Przeprowadza aktualizację stanu komórki na podstawie
stanów jej i sąsiadów, zwraca nowy stan'''  
def transition(cell, neighbours, rules):  
    n=neighbours.copy()
    
    if len(rules[0])==3:
        for x in rules:
            if cell == x[0] and eval(x[2]):
                return x[1]  
        return cell       
    elif len(rules[0])==2 and rules[0][1][0] != 'P':
        for x in rules:
            if eval(x[1]):
                return x[0]
        return cell
    elif rules[0][1][0] == 'P':
        cumulate=[]
        cumulate.append(eval(rules[0][1]))
        for i in range(1,len(rules)):
                cumulate.append(eval(rules[i][1])+cumulate[i-1])                
        prob=uniform(0,cumulate[-1])
        i=0
        for x in cumulate:
            if prob < x:
                return rules[i][0]
            i+=1

if sys.argv[1]=='moore':
    CA=create_moore(int(sys.argv[2]))
elif sys.argv[1]=='von_neumann':
    CA=create_von_neumann(int(sys.argv[2]))
elif sys.argv[1]=='own':
    CA=create_own_CA(sys.argv[2])
else:
    sys.exit("Wrong neighbourhood argument")
    
if sys.argv[3][0:6]=='random':
    l=sys.argv[3].split(",")
    list_of_states=list(random(int(l[1]), CA))
else:
    try:
        with open(sys.argv[3], 'r') as file:
            states=file.read().split(";")
    except IOError:
        print('Wrong beginning-terms argument, cannot open the file: ', sys.argv[3])
    else:
        for x in range(len(states)):
            states[x]=int(states[x])
        file.close()
        list_of_states=states
    
evolved_CA=evolution(CA, int(sys.argv[5]), list_of_states, sys.argv[4])

'''Każdy element z listy wynikowej, czyli listy stanów CA w poszczególnych krokach
są konwertowane ciągi znaków oraz umieszczane w pliku tak, 
aby na każdą linijkę przypadał jeden krok czasowy'''
text=''
for x in evolved_CA:
    for y in x:
        text+=str(y)+';'
    text+='\n'

try:
    with open(sys.argv[6], 'w') as file:
        file.write(text)
except IOError:
    print('Wrong directory for saving the results: ', sys.argv[6])
    