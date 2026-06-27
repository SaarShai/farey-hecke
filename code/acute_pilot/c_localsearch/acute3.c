/* WARNING: acute3 is a REGRESSION (annealing destroys seeds, underperforms acute2). USE acute2. */
/* acute3: stronger local search for A089676. Adds: large-kick (remove K, K up to 8),
 * simulated-annealing lateral acceptance, tabu on recently-removed, and restart from seeds.
 * Right angle apex Q legs P,R iff ((P^Q)&(R^Q))==0.  Build: cc -O3 -march=native -o acute3 acute3.c -lpthread
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>
#include <math.h>
#include <pthread.h>
typedef uint32_t u32;
static int N,TARGET,NTHREADS; static double TLIMIT; static u32 UNIV;
#define MAXSET 600
#define MAXSEEDS 4096
static u32 seedbuf[MAXSEEDS][MAXSET]; static int seedlen_[MAXSEEDS]; static int nseed=0;
static pthread_mutex_t smu=PTHREAD_MUTEX_INITIALIZER;
static void add_seed(const u32* s,int c){ pthread_mutex_lock(&smu); if(nseed<MAXSEEDS && c>0 && c<=MAXSET){ memcpy(seedbuf[nseed],s,c*sizeof(u32)); seedlen_[nseed]=c; nseed++; } pthread_mutex_unlock(&smu); }
typedef struct{uint64_t s0,s1;}rng_t;
static inline uint64_t rnext(rng_t*r){uint64_t x=r->s0,y=r->s1;r->s0=y;x^=x<<23;r->s1=x^y^(x>>17)^(y>>26);return r->s1+y;}
static inline u32 rri(rng_t*r,u32 m){return (u32)(rnext(r)%m);}
static inline double rdbl(rng_t*r){return (rnext(r)>>11)*(1.0/9007199254740992.0);}
static inline int can_add(const u32*a,int m,u32 x){
    for(int i=0;i<m;i++){u32 xi=a[i]^x; if(xi==0)return 0; for(int j=i+1;j<m;j++) if((xi&(a[j]^x))==0) return 0;}
    for(int q=0;q<m;q++){u32 xq=x^a[q]; for(int i=0;i<m;i++){ if(i==q)continue; if((xq&(a[i]^a[q]))==0) return 0; }}
    return 1;
}
static int is_acute(const u32*a,int m){
    for(int j=0;j<m;j++){u32 Q=a[j]; for(int i=0;i<m;i++){if(i==j)continue;u32 xi=a[i]^Q; for(int k=i+1;k<m;k++){if(k==j)continue; if((xi&(a[k]^Q))==0)return 0;}}}
    return 1;
}
static int greedy_fill(u32*a,int m,rng_t*rng){
    u32 size=UNIV+1; u32 start=rri(rng,size); u32 stride=(rri(rng,size/2)*2+1)&UNIV; if(!stride)stride=1; u32 v=start;
    for(u32 c=0;c<size;c++){ u32 x=v; v=(v+stride)&UNIV; int in=0; for(int i=0;i<m;i++) if(a[i]==x){in=1;break;} if(in)continue; if(can_add(a,m,x)){ a[m++]=x; if(m>=TARGET) break; } }
    return m;
}
static volatile int g_found=0; static u32 g_best[MAXSET]; static int g_bsize=0; static pthread_mutex_t bmu=PTHREAD_MUTEX_INITIALIZER;
static void report(u32*a,int m){ pthread_mutex_lock(&bmu); if(m>g_bsize){g_bsize=m;memcpy(g_best,a,m*sizeof(u32)); fprintf(stderr,"  [+] best %d\n",m);} pthread_mutex_unlock(&bmu); }
static double now(){struct timespec t;clock_gettime(CLOCK_MONOTONIC,&t);return t.tv_sec+t.tv_nsec*1e-9;}
typedef struct{int tid;rng_t rng;}targ_t;
static void* worker(void*p){
    targ_t*t=(targ_t*)p; rng_t*rng=&t->rng; double t0=now();
    u32 cur[MAXSET],best[MAXSET]; 
    while(!g_found && now()-t0<TLIMIT){
        int m=0;
        if(nseed>0 && rri(rng,3)>0){ int si=rri(rng,nseed); memcpy(cur,seedbuf[si],seedlen_[si]*sizeof(u32)); m=seedlen_[si];
            /* trim to acute core just in case */ u32 tmp[MAXSET]; int mm=0; for(int i=0;i<m;i++) if(can_add(tmp,mm,cur[i])) tmp[mm++]=cur[i]; memcpy(cur,tmp,mm*sizeof(u32)); m=mm; }
        m=greedy_fill(cur,m,rng);
        int bl=m; memcpy(best,cur,m*sizeof(u32));
        if(bl>=TARGET){report(best,bl);g_found=1;break;}
        double T=2.0; int noimp=0;
        while(!g_found && now()-t0<TLIMIT && noimp< 60000){
            memcpy(cur,best,bl*sizeof(u32)); m=bl;
            int K=1+rri(rng,8); if(K>=m)K=1;
            for(int r=0;r<K&&m>0;r++){ int idx=rri(rng,m); cur[idx]=cur[--m]; }
            m=greedy_fill(cur,m,rng);
            if(m>bl){ bl=m; memcpy(best,cur,m*sizeof(u32)); noimp=0; if(bl>=TARGET){report(best,bl);g_found=1;break;} }
            else if(m==bl){ if(rdbl(rng)<0.5){memcpy(best,cur,m*sizeof(u32));} noimp++; }
            else { /* annealing accept worse */ if(rdbl(rng) < exp((m-bl)/T)){ bl=m; memcpy(best,cur,m*sizeof(u32)); } noimp++; }
            T*=0.9999; if(T<0.05)T=2.0;
        }
        report(best,bl);
        if(bl>=TARGET-1) add_seed(best,bl);
    }
    return NULL;
}
static int read_set(const char*path,u32*out,int*oM){ FILE*f=fopen(path,"r"); if(!f)return 0; char L[512];int nv=0,M=-1; while(fgets(L,sizeof L,f)){int bit=0;u32 v=0,any=0; for(char*c=L;*c;c++) if(*c=='0'||*c=='1'){if(*c=='1')v|=(1u<<bit);bit++;any=1;} if(any){if(M<0)M=bit; if(bit!=M){fclose(f);return 0;} out[nv++]=v;}} fclose(f);*oM=M;return nv; }
static void split_down(const u32*set,int cnt,int M,int n){ if(M==n){add_seed(set,cnt);return;} for(int c=0;c<M;c++) for(int v=0;v<2;v++){u32 sub[MAXSET];int sc=0;u32 lm=(c?((1u<<c)-1):0); for(int i=0;i<cnt;i++){ if(((set[i]>>c)&1)!=(u32)v)continue; u32 lo=set[i]&lm,hi=(set[i]>>(c+1))<<c; sub[sc++]=lo|hi;} if(sc>=2) split_down(sub,sc,M-1,n);} }
int main(int argc,char**argv){
    if(argc<4){fprintf(stderr,"usage:%s N TARGET TLIMIT [NTHR] [--seed F]...\n",argv[0]);return 2;}
    N=atoi(argv[1]);TARGET=atoi(argv[2]);TLIMIT=atof(argv[3]); NTHREADS=8; UNIV=(N>=32)?0xFFFFFFFFu:((1u<<N)-1);
    int ai=4; if(ai<argc&&argv[ai][0]!='-'){NTHREADS=atoi(argv[ai]);ai++;}
    while(ai<argc){ if(!strcmp(argv[ai],"--seed")&&ai+1<argc){u32 set[MAXSET];int M=0;int cnt=read_set(argv[ai+1],set,&M); if(cnt>0){ if(M==N){if(is_acute(set,cnt))add_seed(set,cnt);} else if(M>N){split_down(set,cnt,M,N);} } ai+=2;} else ai++; }
    int mss=0;for(int i=0;i<nseed;i++)if(seedlen_[i]>mss)mss=seedlen_[i];
    fprintf(stderr,"acute3 N=%d TARGET=%d thr=%d seeds=%d maxseed=%d t=%.0f\n",N,TARGET,NTHREADS,nseed,mss,TLIMIT);
    pthread_t th[64];targ_t ta[64];
    for(int i=0;i<NTHREADS;i++){ta[i].tid=i;ta[i].rng.s0=0x9E3779B97F4A7C15ull*(i*2+1)+now()*1e6;ta[i].rng.s1=0xD1B54A32D192ED03ull*(i*3+7)+12345; for(int w=0;w<9;w++)rnext(&ta[i].rng); pthread_create(&th[i],NULL,worker,&ta[i]);}
    for(int i=0;i<NTHREADS;i++)pthread_join(th[i],NULL);
    fprintf(stderr,"BEST=%d (target %d) N=%d\n",g_bsize,TARGET,N);
    if(!is_acute(g_best,g_bsize)){fprintf(stderr,"ERR not acute\n");return 1;}
    for(int i=0;i<g_bsize;i++){for(int b=0;b<N;b++)printf("%d%s",(g_best[i]>>b)&1,b+1<N?" ":"");printf("\n");}
    return 0;
}
