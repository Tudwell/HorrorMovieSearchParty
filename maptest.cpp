////////////////////////////////////////////////////////////////////////////////
// Compile with g++ maptest.cpp
// Usage: ./a.out <filename>
////////////////////////////////////////////////////////////////////////////////
#include <iostream>
#include <fstream>
#include <queue>
using namespace std;

char map[256][256];
int N,M,temp;
queue< pair<int,int> > Q;
pair <int,int> P;

void addkill(int i, int j){
   P.first = i;
   P.second = j;
   Q.push(P);
   map[i][j] = '#';
}

int main(int argc, char **argv){
   ifstream in;
   in.open(argv[1]);
   in >> N >> M >> temp >> temp;

   for(int i=0;i<N;i++){
      for(int j=0;j<M;j++){
         in >> map[i][j];
         cout << map[i][j];
         if(map[i][j]=='S'){
            P.first = i;
            P.second = j;
         }
      }
      cout << endl;
   }
   
   Q.push(P);
   map[P.first][P.second] = '#';
   
   while(!Q.empty()){
      P = Q.front();
      Q.pop();
      int i = P.first, j = P.second;
      
      if(i>0 && j>0){     if(map[i-1][j-1] == '.'){ addkill(i-1,j-1); } }
      if(i>0){            if(map[i-1][j] == '.'){   addkill(i-1,j); } }
      if(i>0 && j<M-1){   if(map[i-1][j+1] == '.'){ addkill(i-1,j+1); } }
      if(j>0){            if(map[i][j-1] == '.'){   addkill(i,j-1); } }
      if(j<M-1){          if(map[i][j+1] == '.'){   addkill(i,j+1); } }
      if(i<N-1 && j>0){   if(map[i+1][j-1] == '.'){ addkill(i+1,j-1); } }
      if(i<N-1){          if(map[i+1][j] == '.'){   addkill(i+1,j); } }
      if(i<N-1 && j<M-1){ if(map[i+1][j+1] == '.'){ addkill(i+1,j+1); } }
   }
   
   cout << endl;
   for(int i=0;i<N;i++){
      for(int j=0;j<M;j++){
         cout << map[i][j];         
      }
      cout << endl;
   }  
   
   return 0;
}