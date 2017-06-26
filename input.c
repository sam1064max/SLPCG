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

#pragma scop

for(i=0;i<6;i++){
	for(j=0;j<6;j++){  
		g[2*i+3*j+1][2*i+3*j+1] = c[3];
		c[4] = b[3*i-2*j-2];
		b[2*i+j+3] = c[5];
		c[6] = g[i+4*j+4][i+4*j+4];
	}
}

#pragma endscop

printf("After : \n");
for(i=0;i<50;i++){
	for(j=0;j<50;j++){  
		printf("%3d ", g[i*50+j]);
	}
	printf("\n");
}

}

