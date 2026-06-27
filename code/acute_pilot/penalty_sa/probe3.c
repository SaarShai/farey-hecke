/* Fast bounded multi-change repair from a low-energy seed.
 * Restrict changed positions to the INVOLVED set; restrict candidate values to a
 * structurally-plausible pool: all Hamming-<=2 neighbours of current vertices.
 * Do an exhaustive 2-change AND a greedy-deepening 3-change over that pool.
 * If energy 0 is reached, write witness (then verify externally).
 * Build: cc -O3 -o probe3 probe3.c
 * Run:   ./probe3 n seedfile [ham]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
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
static int contains_x(u32 v,int e1,int e2){ for(int i=0;i<k;i++){ if(i==e1||i==e2)continue; if(S[i]==v)return 1;} return 0; }

u32 *pool; int npool;
static void build_pool(int ham){
  /* all vertices within Hamming<=ham of any current vertex */
  char *seen=calloc((size_t)1<<n,1); npool=0;
  for(int i=0;i<k;i++){ u32 c=S[i];
    /* ham 0 */
    if(!seen[c]){seen[c]=1;}
    if(ham>=1) for(int a=0;a<n;a++){ u32 v=c^(1u<<a); if(!seen[v])seen[v]=1; }
    if(ham>=2) for(int a=0;a<n;a++)for(int b=a+1;b<n;b++){ u32 v=c^(1u<<a)^(1u<<b); if(!seen[v])seen[v]=1; }
    if(ham>=3) for(int a=0;a<n;a++)for(int b=a+1;b<n;b++)for(int d=b+1;d<n;d++){ u32 v=c^(1u<<a)^(1u<<b)^(1u<<d); if(!seen[v])seen[v]=1; }
  }
  for(u32 v=0; v<(u32)(1u<<n); v++) if(seen[v]) npool++;
  pool=malloc(npool*sizeof(u32)); int t=0;
  for(u32 v=0; v<(u32)(1u<<n); v++) if(seen[v]) pool[t++]=v;
  free(seen);
}

int main(int ac,char**av){ n=atoi(av[1]); mask_full=(1u<<n)-1;
  FILE*f=fopen(av[2],"r"); char l[256]; S=malloc(300*sizeof(u32)); k=0;
  while(fgets(l,256,f)){char*p=l;while(*p==' ')p++; if(*p<'0'||*p>'9')continue; S[k++]=(u32)strtoul(p,0,10);} fclose(f);
  int ham=(ac>3)?atoi(av[3]):2;
  long E0=energy(); printf("base E=%ld (n=%d k=%d)\n",E0,n,k); fflush(stdout);
  char inv[300]={0};
  for(int j=0;j<k;j++){u32 q=S[j]; for(int a=0;a<k;a++){if(a==j)continue;u32 xa=S[a]^q;
    for(int b=a+1;b<k;b++){if(b==j)continue; if((xa&(S[b]^q))==0){inv[j]=inv[a]=inv[b]=1;}}}}
  int invidx[300],ninv=0; for(int i=0;i<k;i++) if(inv[i]) invidx[ninv++]=i;
  build_pool(ham);
  printf("involved=%d  pool(ham<=%d)=%d\n",ninv,ham,npool); fflush(stdout);

  /* ---- exhaustive 2-change: i,j BOTH involved, values from pool ---- */
  long best=E0; int bp=-1,bq=-1; u32 bv=0,bw=0; int zero=0;
  for(int oi=0; oi<ninv && !zero; oi++){ int i=invidx[oi]; u32 OI=S[i];
    for(int pa=0; pa<npool && !zero; pa++){ u32 vi=pool[pa]; if(vi!=OI && contains_x(vi,i,-1))continue;
      long di=contrib(i,vi)-contrib(i,OI); S[i]=vi; long Ei=E0+di;
      for(int oj=0; oj<ninv && !zero; oj++){ int j=invidx[oj]; if(j==i)continue; u32 OJ=S[j];
        long cjold=contrib(j,OJ);
        for(int pb=0; pb<npool; pb++){ u32 vj=pool[pb]; if(vj==OJ)continue; if(contains_x(vj,i,j))continue;
          long e=Ei + (contrib(j,vj)-cjold);
          if(e<best){best=e;bp=i;bv=vi;bq=j;bw=vj; if(e==0){zero=1; break;}}
        }
        S[j]=OJ;
      }
      S[i]=OI;
    }
  }
  printf("2-change best=%ld\n",best); fflush(stdout);
  if(best==0){ S[bp]=bv;S[bq]=bw; FILE*o=fopen("probe_zero2.txt","w");
    for(int i=0;i<k;i++){for(int b=0;b<n;b++)fputc(((S[i]>>b)&1)?'1':'0',o);fputc('\n',o);} fclose(o);
    printf("ZERO 2-change -> probe_zero2.txt\n"); return 0; }

  /* ---- 3-change: i,j,m involved, values from pool, exhaustive ---- */
  best=E0; int z3=0; int a1=-1,a2=-1,a3=-1; u32 c1=0,c2=0,c3=0;
  for(int oi=0; oi<ninv && !z3; oi++){ int i=invidx[oi]; u32 OI=S[i];
    for(int pa=0; pa<npool && !z3; pa++){ u32 vi=pool[pa]; if(vi!=OI && contains_x(vi,i,-1))continue;
      long di=contrib(i,vi)-contrib(i,OI); S[i]=vi; long Ei=E0+di;
      for(int oj=oi+1; oj<ninv && !z3; oj++){ int j=invidx[oj]; if(j==i)continue; u32 OJ=S[j];
        long cjold=contrib(j,OJ);
        for(int pb=0; pb<npool && !z3; pb++){ u32 vj=pool[pb]; if(vj==OJ)continue; if(contains_x(vj,i,j))continue;
          long dj=contrib(j,vj)-cjold; S[j]=vj; long Eij=Ei+dj;
          if(Eij<=best+6){
            for(int om=oj+1; om<ninv && !z3; om++){ int mm=invidx[om]; if(mm==i||mm==j)continue; u32 OM=S[mm];
              long cmold=contrib(mm,OM);
              for(int pc=0; pc<npool; pc++){ u32 vm=pool[pc]; if(vm==OM)continue; if(contains_x(vm,mm,mm))continue;
                int dupp=0; for(int z=0;z<k;z++){ if(z!=i&&z!=j&&z!=mm&&S[z]==vm){dupp=1;break;} } if(dupp)continue;
                long e=Eij+(contrib(mm,vm)-cmold);
                if(e<best){best=e;a1=i;c1=vi;a2=j;c2=vj;a3=mm;c3=vm; if(e==0){z3=1;break;}}
              }
              S[mm]=OM;
            }
          }
          S[j]=OJ;
        }
      }
      S[i]=OI;
    }
  }
  printf("3-change best=%ld\n",best); fflush(stdout);
  if(best==0){ S[a1]=c1;S[a2]=c2;S[a3]=c3; FILE*o=fopen("probe_zero3.txt","w");
    for(int i=0;i<k;i++){for(int b=0;b<n;b++)fputc(((S[i]>>b)&1)?'1':'0',o);fputc('\n',o);} fclose(o);
    printf("ZERO 3-change -> probe_zero3.txt\n"); }
  return 0; }
