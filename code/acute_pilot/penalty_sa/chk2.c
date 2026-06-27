#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>
typedef uint32_t u32;
int n,k; u32 *S; u32 mask_full;
static long energy(){ long e=0; for(int j=0;j<k;j++){u32 q=S[j];
  for(int a=0;a<k;a++){if(a==j)continue;u32 xa=S[a]^q;
   for(int b=a+1;b<k;b++){if(b==j)continue; if((xa&(S[b]^q))==0)e++;}}} return e; }
static long contrib(int idx,u32 val){ long e=0;
  for(int a=0;a<k;a++){ if(a==idx)continue; u32 xa=S[a]^val;
    for(int b=a+1;b<k;b++){ if(b==idx)continue; if((xa&(S[b]^val))==0)e++; } }
  for(int j=0;j<k;j++){ if(j==idx)continue; u32 q=S[j]; u32 xi=val^q;
    for(int b=0;b<k;b++){ if(b==idx||b==j)continue; if((xi&(S[b]^q))==0)e++; } }
  return e; }
int main(int ac,char**av){ n=atoi(av[1]); mask_full=(1u<<n)-1; u32 full=mask_full+1;
  FILE*f=fopen(av[2],"r"); char l[256]; S=malloc(300*sizeof(u32)); k=0;
  while(fgets(l,256,f)){char*p=l;while(*p==' ')p++; if(*p<'0'||*p>'9')continue; S[k++]=(u32)strtoul(p,0,10);} fclose(f);
  srand(7); long E0=energy(); int bad=0;
  for(int t=0;t<20000;t++){ int i=rand()%k,j=rand()%k; if(i==j)continue;
    u32 oi=S[i],oj=S[j]; u32 vi=rand()&mask_full, vj=rand()&mask_full;
    // skip dup
    int dup=0; for(int z=0;z<k;z++){ if(z!=i&&z!=j&&(S[z]==vi||S[z]==vj))dup=1; } if(vi==vj)dup=1; if(dup)continue;
    long di=contrib(i,vi)-contrib(i,oi); S[i]=vi; long cjold=contrib(j,oj); long dj=contrib(j,vj)-cjold;
    long pred=E0+di+dj; S[i]=oi;
    S[i]=vi;S[j]=vj; long act=energy(); S[i]=oi;S[j]=oj;
    if(pred!=act){ bad++; if(bad<5) printf("MISMATCH i=%d j=%d pred=%ld act=%ld\n",i,j,pred,act); }
  }
  printf("delta check: %s (bad=%d)\n", bad?"FAIL":"ALL CORRECT", bad); return 0; }
