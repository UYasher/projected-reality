from math import atan2, pi
from random import randint

# Import dictionaries
def pull_tables(filenames):
    dicts = [{} for i in range(len(filenames))]
    for i in range(len(filenames)):
        f = open(filenames[i])
        line = f.readline()
        # print(line)
        line = line[3:]
        # print(line)
        line=line.split(',')
        while line[0]:
            line = [int(x) for x in line[:2]]+[float(x) for x in line[2:]]
            dicts[i][tuple(line[:2])] = tuple(line[2:])
            line = f.readline()
            line = line.split(',')
    return dicts

#0 is using top vertices
#1 is using left vertices
#2 is using bottom vertices
#3 is using right vertices
dirs = ((0,1,1,1,pi/2),(1,2,0,1,0),(2,3,1,-1,-pi/2),(3,0,0,-1,pi))

# Placeholder
def get_angles(indices):
    t = (randint(170,210),randint(170,210))
    print(t)
    return t

#Outputs error and an exception code
#0 = everything fine
#1 = need to reselect angles
#2 = angles not found in lookup table
#Does no interpolation atm, just taking the "closest" value
def check_table(dir):
    angles = get_angles(dir[:2])
    error = [0,0]

    if angles in table[dir[2]]:
        error = table[dir[2]][angles]
    else:
        a2 = tuple([int(2*round(angles[i]/2)) for i in range(len(angles))])
        if a2 in table[dir[2]]:
            print(a2)
            error = table[dir[2]][a2]
        else:
            a4 = tuple([int(6*round(a2[i]/6)) for i in range(len(a2))])
            print(a4)
            if a4 in table[dir[2]]:
                error = table[dir[2]][a4]
            else:
                print(a4,"was not in the lookup table!")
                return error,2
    error = [error[i]*dir[3] for i in range(len(error))]
    print(atan2(error[1],error[0])*180/pi)
    if abs(atan2(error[1],error[0]) - dir[4]) > pi/4 and abs(2*pi - abs(atan2(error[1],error[0])-dir[4])) > pi/4:
        print("Need to reselect angles")
        return error,1
    return error,0

# table = pull_tables(('horizontal.csv','vertical.csv'))
table = pull_tables(('horizontal.csv','vertical.csv'))
# print(table)
print(check_table(dirs[3]))