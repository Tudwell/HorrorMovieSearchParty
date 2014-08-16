import sys, subprocess, string
# '.' is unseen open space
# 'o' is seen open space
# '#' is an obstacle

def valid(i,j):
   if i>=0 and i<N:
      if j>=0 and j<M:
         return True
   return False

def finished():
   for y in range(0,len(map)):
      for x in range(0,len(map[y])):      
         if(map[y][x]=='.'):
            return False
   sys.stderr.write('Finished in '+str(turn-1)+' turns\n')
   numcostars = 0
   numextras = 0
   for L in costars:
      if L[0]>=0:
         numcostars += 1
   for L in extras:
      if L[0]>=0:
         numextras += 1
   sys.stderr.write(str(turn-1)+' '+str(numcostars)+' '+str(numextras)+'\n')            
   return True
   
#
#   ...   
#  .....
#  ..@..
#  .....
#   ...
#   
def d2(i,j,i2,j2):
   return (i2-i)*(i2-i)+(j2-j)*(j2-j)

def look(i,j):   
   for x in [i-2,i+2]:
      for y in [j-1,j,j+1]:
         if valid(x,y) and map[y][x]=='.':
            map[y][x] = 'o'
   for x in [i-1,i,i+1]:
      for y in range(j-2,j+3):
         if valid(x,y) and map[y][x]=='.':
            map[y][x] = 'o'
            
def seenStar(i,j):
   if d2(i,j,star[0],star[1]) < 8:
      return 1
   return 0

def seenCostars(i,j):
   num = 0
   for L in costars:
      if L[0] != -1 and d2(i,j,L[0],L[1]) < 8:
         num += 1
   return num

def seenExtras(i,j):
   num = 0
   for L in extras:
      if L[0] != -1 and d2(i,j,L[0],L[1]) < 8:
         num += 1
   return num

# Note that everyone can see himself
def kill():
   for L in costars:
      if L[0] != -1:         
         if seenStar(L[0],L[1])==0 and seenCostars(L[0],L[1])==1 and seenExtras(L[0],L[1])==0:
            L.append('dead')
   for L in extras:
      if L[0] != -1:         
         if seenStar(L[0],L[1])==0 and seenCostars(L[0],L[1])==0 and seenExtras(L[0],L[1])<3:
            L.append('dead')
   for L in costars:
      if L[0] != -1 and L[-1] == 'dead':
         L[0] = -1
   for L in extras:
      if L[0] != -1 and L[-1] == 'dead':
         L[0] = -1
         
def move(L,dir):
   if dir=='7' and valid(L[0]-1,L[1]-1) and map[L[1]-1][L[0]-1]=='o':
      L[0] -= 1
      L[1] -= 1      
   elif dir=='8' and valid(L[0],L[1]-1) and map[L[1]-1][L[0]]=='o':      
      L[1] -= 1      
   elif dir=='9' and valid(L[0]+1,L[1]-1) and map[L[1]-1][L[0]+1]=='o':
      L[0] += 1
      L[1] -= 1      
   elif dir=='4' and valid(L[0]-1,L[1]) and map[L[1]][L[0]-1]=='o':
      L[0] -= 1      
   elif dir=='6' and valid(L[0]+1,L[1]) and map[L[1]][L[0]+1]=='o':
      L[0] += 1      
   elif dir=='1' and valid(L[0]-1,L[1]+1) and map[L[1]+1][L[0]-1]=='o':
      L[0] -= 1
      L[1] += 1      
   elif dir=='2' and valid(L[0],L[1]+1) and map[L[1]+1][L[0]]=='o':
      L[1] += 1
   elif dir=='3' and valid(L[0]+1,L[1]+1) and map[L[1]+1][L[0]+1]=='o':
      L[0] += 1
      L[1] += 1
   else:
      if(dir!='5'):
         sys.stderr.write('Invalid move of '+str(L)+' in direction '+str(dir)+' onto # or off of the map\n')
         quit()
   
def printmap():
   for i in map:   
      for j in i:
         proc.stdin.write(j)
      proc.stdin.write('\n')
      
def printstate():
   #sys.stderr.write('Turn '+str(turn)+'\n')
   proc.stdin.write('Turn '+str(turn)+'\n')
   #sys.stderr.write('@:'+str(star[0])+','+str(star[1]))
   proc.stdin.write('@:'+str(star[0])+','+str(star[1]))
   for i in range(C):
      if costars[i][0]!=-1:
         proc.stdin.write(' '+chr(ord('A')+i)+':'+str(costars[i][0])+','+str(costars[i][1]))         
   for i in range(E):
      if extras[i][0]!=-1:
         proc.stdin.write(' '+chr(ord('a')+i)+':'+str(extras[i][0])+','+str(extras[i][1]))
   proc.stdin.write('.\n')
   printmap()
   proc.stdin.write('----------------------------------------\n')
   proc.stdin.flush()
   
proc = subprocess.Popen(sys.argv[2:], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
f = open(sys.argv[1], 'r')
lines = f.readlines()
# N,M,C,E = #cols, #rows, #costars, #extras
N,M,C,E = [int(i) for i in lines[0].split()]
map = lines[1:]
for i in range(0,len(map)):
   map[i] = list(map[i].strip());
for y in range(0,len(map)):
   for x in range(0,len(map[y])):      
      if(map[y][x]=='S'):
         Sx = x
         Sy = y
         map[y][x]='o'
look(Sx,Sy)
costars = [[Sx,Sy] for i in range(C)]
extras = [[Sx,Sy] for i in range(E)]
star = [Sx,Sy]
turn = 1
printstate()
if finished():
   quit()

while(True):
   turn += 1
   # Get a line from stdin
   L = proc.stdout.readline().strip()   
   L = L.strip('.')
   L = L.split()
   S = set([i[0] for i in L])
   if len(S) != len(L):
      sys.stderr.write('Invalid movelist (moving someone more than once in a turn)\n')
      quit()
   # Make the moves
   for m in L:
      if m[0]=='@':
         move(star,m[1])
      if m[0] in list(string.ascii_uppercase):
         temp = ord(m[0]) - ord('A')
         if temp>=C or costars[temp][0] == -1:
            sys.stderr.write('Invalid move of dead or nonexistent costar '+m[0]+'\n')
            quit()
         move(costars[temp],m[1])
      if m[0] in list(string.ascii_lowercase):
         temp = ord(m[0]) - ord('a')
         if temp>=E or extras[temp][0] == -1:
            sys.stderr.write('Invalid move of dead or nonexistent extra '+m[0]+'\n')
            quit()
         move(extras[temp],m[1])
   # Process the turn
   look(star[0],star[1])
   for L in costars:
      if L[0] != -1:
         look(L[0],L[1])
   for L in extras:
      if L[0] != -1:
         look(L[0],L[1])
   kill()
   if finished():
      quit()
   # Print the state of the board
   printstate()         