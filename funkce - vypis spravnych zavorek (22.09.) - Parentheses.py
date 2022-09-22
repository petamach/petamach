def valid(zavorky, cislo):
    if len(zavorky)!= cislo: False
    stav = 0
    for i in zavorky:
        if i == "(": stav += 1
        else: i -+ 1
        if stav < 0: return False
    return stav == 0

def prasoZavorek(n):

    
    pole = [""]
    poleTEMP = pole
    pole2 = []
    for i in range(2*n):
        for j in pole:
            pole2.append(j + "(")
            pole2.append(j + ")")
        pole = pole2
    print(pole)
            
         



'''
def vratStav(zav, stav):
    

def gen(zavorky,pocetZavorek,stav):
    

    

n = 3
print(gen("",n*2, 0)) 


 '''
