#include <stdio.h>
#include <stdlib.h>
#include <time.h>

//run perf
int main (int argc, char *argv[]){

int i,j,b[5000],g[5000];


for(i=0;i<40;i++){
	g[i] = i;
	b[i] = 4;
}

printf("Before : \n");

for(i=0;i<40;i++){
		printf("%3d ", g[i]);
}


clock_t t;
t = clock();

#pragma scop

for(i=0;i<2;i++){
	for(j=0;j<2;j++){
		g[2*i+3*j+2*k+1]= b[2];
		b[3] = g[3*i+j+5*k+6];
	}
}

#pragma endscop

t = clock() - t;
double time_taken = ((double)t)/CLOCKS_PER_SEC; // in seconds
 
printf("\n\nExecution Time = %f \n\n", time_taken);

printf("\n\nAfter : \n");

for(i=0;i<40;i++){
	printf("%3d ", g[i]);
}

printf("\n\n");

}

