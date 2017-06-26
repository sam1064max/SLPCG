#include <omp.h>
#include <stdio.h>
#include <stdlib.h>

//run perf
int main (int argc, char *argv[]){

int i,j,b[1000]={0},g[1000][1000],c[50];

for(i=0;i<50;i++){
	for(j=0;j<50;j++){  
		g[i*50+j] = i*50+j;
	}
	b[i] = i;
}

printf("Before : \n");

for(i=0;i<50;i++){
	for(j=0;j<50;j++){  
		printf("%3d ", g[i*50+j]);
	}
	printf("\n");
}

int C[3][73][3] = {{{2}}
,{{72},{0,4,2},{0,8,2},{0,12,2},{0,18,1},{1,9,1},{0,11,2},{0,15,2},{0,19,2},{1,0,1},{0,16,2},{0,20,2},{1,0,2},{1,7,1},{0,4,3},{0,5,0},{0,21,0},{1,3,3},{0,3,3},{0,9,0},{1,1,0},{1,2,3},{0,5,3},{0,17,0},{1,4,3},{1,9,0},{0,1,2},{0,12,1},{1,3,1},{0,0,2},{0,20,1},{1,11,1},{0,3,0},{0,14,3},{0,19,0},{0,2,0},{0,18,0},{0,19,3},{0,2,3},{0,13,0},{1,1,3},{0,7,3},{0,12,0},{1,6,3},{0,11,3},{1,4,0},{1,10,3},{0,0,0},{0,6,3},{0,17,3},{0,23,0},{0,22,0},{0,22,3},{0,0,1},{0,0,3},{0,1,1},{0,4,1},{0,5,1},{0,8,1},{0,9,1},{0,12,3},{0,13,1},{0,16,1},{0,17,1},{0,21,2},{0,22,1},{1,1,2},{1,3,2},{1,5,1},{1,5,2},{1,9,2},{1,10,2},{1,11,3}}
,{{72},{0,2,2},{0,6,2},{0,19,1},{1,10,1},{0,5,2},{0,9,2},{0,13,2},{1,1,1},{0,10,2},{0,14,2},{0,18,2},{1,8,1},{0,22,2},{1,2,2},{1,6,1},{1,6,2},{0,4,0},{0,9,3},{0,20,0},{1,8,3},{0,8,0},{0,8,3},{1,0,0},{1,7,3},{0,10,3},{0,16,0},{1,8,0},{1,9,3},{0,3,2},{0,7,2},{1,2,1},{0,1,0},{0,1,3},{1,0,3},{0,11,0},{0,16,3},{1,3,0},{0,10,0},{0,21,3},{1,2,0},{0,15,0},{0,15,3},{1,7,0},{0,14,0},{0,20,3},{1,6,0},{0,7,0},{0,13,3},{0,6,0},{0,18,3},{1,5,0},{1,5,3},{0,23,3},{1,10,0},{0,2,1},{0,3,1},{0,6,1},{0,7,1},{0,10,1},{0,11,1},{0,14,1},{0,15,1},{0,17,2},{0,21,1},{0,23,1},{0,23,2},{1,4,1},{1,4,2},{1,7,2},{1,8,2},{1,11,0},{1,11,2}}};
int nesting = 2;
int index[2];


#pragma omp parallel for
for(int x = 1 ; x <= C[0][0][0] ; x++)
	for(int y = 1 ; y <= C[x][0][0] ; y++){
		for(int i = 0; i<nesting; i++)
			index[i] = C[x][y][i];
		switch(C[x][y][nesting]){
		case 0 : g[2*index[0]+3*index[1]+1][2*index[0]+3*index[1]+1] = c[3];
			break;
		case 1 : c[4] = b[3*index[0]-2*index[1]-2];
			break;
		case 2 : b[2*index[0]+index[1]+3] = c[5];
			break;
		case 3 : c[6] = g[index[0]+4*index[1]+4][index[0]+4*index[1]+4];
			break;
		}
	}
printf("After : \n");
for(i=0;i<50;i++){
	for(j=0;j<50;j++){  
		printf("%3d ", g[i*50+j]);
	}
	printf("\n");
}

}
