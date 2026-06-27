/* OEIS A089676 acute-set local search v2.
 * Right angle at apex Q between P,R iff ((P^Q)&(R^Q))==0.
 * S acute iff no triple has a right angle.
 *
 * Seeding:
 *   --seed FILE   : a set in dim M>=N. For each coordinate c<M and value v in {0,1},
 *                   take the subset with that coord == v, drop coord c -> an acute set in dim (M-1).
 *                   We iterate splits down to dim N. These projected sets are GUARANTEED acute
 *                   (a subset of an acute set, in fewer dims, is acute). They become seeds.
 *   Also: the raw set itself if M==N is a seed.
 * Search: per-thread restart loop: pick a seed (or empty), greedy-fill, plateau local search
 *   with (k)-removal + greedy refill, lateral moves, occasional big kicks. All cores.
 *
 * Build: cc -O3 -march=native -o acute2 acute2.c -lpthread
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>
#include <pthread.h>

typedef uint32_t u32;
#define MAXSET 512

static int N, TARGET, NTHREADS;
static double TLIMIT;
static u32 UNIV;

typedef struct { uint64_t s0,s1; } rng_t;
static inline uint64_t rnext(rng_t* r){ uint64_t x=r->s0,y=r->s1; r->s0=y; x^=x<<23; r->s1=x^y^(x>>17)^(y>>26); return r->s1+y; }
static inline u32 rint(rng_t* r,u32 m){ return m? (u32)(rnext(r)%m):0; }

static inline int can_add(const u32* arr,int m,u32 x){
    for(int a=0;a<m;a++){ u32 xa=arr[a]^x; for(int b=a+1;b<m;b++) if((xa&(arr[b]^x))==0) return 0; }
    for(int q=0;q<m;q++){ u32 xq=x^arr[q]; for(int a=0;a<m;a++){ if(a==q)continue; if((xq&(arr[a]^arr[q]))==0) return 0; } }
    return 1;
}
static int is_acute(const u32* arr,int m){
    for(int j=0;j<m;j++){ u32 Q=arr[j]; for(int a=0;a<m;a++){ if(a==j)continue; u32 xa=arr[a]^Q;
        for(int b=a+1;b<m;b++){ if(b==j)continue; if((xa&(arr[b]^Q))==0) return 0; }}}
    return 1;
}

/* seeds storage: list of acute sets in dim N */
#define MAXSEEDS 2048
static u32 seedbuf[MAXSEEDS][MAXSET];
static int seedlen_[MAXSEEDS];
static int nseed=0;
static pthread_mutex_t seedmu=PTHREAD_MUTEX_INITIALIZER;
static void add_seed(const u32* a,int m){
    if(m<2) return;
    pthread_mutex_lock(&seedmu);
    if(nseed<MAXSEEDS){ memcpy(seedbuf[nseed],a,m*sizeof(u32)); seedlen_[nseed]=m; nseed++; }
    pthread_mutex_unlock(&seedmu);
}

static volatile int g_found=0;
static u32 g_best_set[MAXSET];
static int g_best_size=0;
static pthread_mutex_t g_mu=PTHREAD_MUTEX_INITIALIZER;
static void report(const u32* arr,int m){
    if(m<=g_best_size) return;
    pthread_mutex_lock(&g_mu);
    if(m>g_best_size){ g_best_size=m; memcpy(g_best_set,arr,m*sizeof(u32));
        fprintf(stderr,"  [+] new best %d\n",m); }
    pthread_mutex_unlock(&g_mu);
}
static double now(){ struct timespec ts; clock_gettime(CLOCK_MONOTONIC,&ts); return ts.tv_sec+ts.tv_nsec*1e-9; }

static int greedy_fill(u32* arr,int m,rng_t* rng){
    u32 size=UNIV+1;
    u32 start=rint(rng,size);
    u32 stride=(rint(rng,size/2)*2+1)&UNIV; if(stride==0)stride=1;
    u32 v=start;
    for(u32 cnt=0;cnt<size && m<TARGET;cnt++){
        u32 x=v; v=(v+stride)&UNIV;
        int in=0; for(int i=0;i<m;i++) if(arr[i]==x){in=1;break;}
        if(in) continue;
        if(can_add(arr,m,x)) arr[m++]=x;
    }
    return m;
}

typedef struct { int tid; rng_t rng; } targ_t;

static void* worker(void* p){
    targ_t* t=(targ_t*)p; rng_t* rng=&t->rng;
    u32 cur[MAXSET], best[MAXSET];
    double t0=now();
    while(!g_found && now()-t0<TLIMIT){
        int m=0;
        int r=rint(rng,10);
        if(nseed>0 && r<7){
            int si=rint(rng,nseed);
            int sl=seedlen_[si];
            memcpy(cur,seedbuf[si],sl*sizeof(u32));
            m=sl;
            /* perturb: drop a random fraction so we explore around the seed */
            if(r<4){ int drop=rint(rng, sl/4+1); for(int d=0;d<drop && m>2;d++){ int idx=rint(rng,m); cur[idx]=cur[--m]; } }
        }
        m=greedy_fill(cur,m,rng);
        if(m>=TARGET){ report(cur,m); g_found=1; break; }
        int bl=m; memcpy(best,cur,m*sizeof(u32));
        report(best,bl);
        int noimp=0;
        while(!g_found && noimp<5000){
            if((noimp&1023)==1023 && now()-t0>=TLIMIT) break;
            memcpy(cur,best,bl*sizeof(u32)); m=bl;
            int rem=1+rint(rng,4); if(rem>=m)rem=1;
            for(int k=0;k<rem && m>0;k++){ int idx=rint(rng,m); cur[idx]=cur[--m]; }
            m=greedy_fill(cur,m,rng);
            if(m>bl){ bl=m; memcpy(best,cur,m*sizeof(u32)); noimp=0;
                report(best,bl);
                if(bl>=TARGET){ g_found=1; break; } }
            else if(m==bl){ if(rint(rng,3)==0){ memcpy(best,cur,m*sizeof(u32)); } noimp++; }
            else noimp++;
        }
        report(best,bl);
        /* feed strong local optima back as seeds occasionally */
        if(bl>=TARGET-2 && rint(rng,4)==0) add_seed(best,bl);
    }
    return NULL;
}

/* read a 0/1 set file -> vectors in dim M (M = #bits in first row) */
static int read_set(const char* path,u32* out,int* outM){
    FILE* f=fopen(path,"r"); if(!f) return 0;
    char line[512]; int nv=0,M=-1;
    while(fgets(line,sizeof line,f)){
        int bit=0; u32 v=0; int any=0;
        for(char*c=line;*c;c++) if(*c=='0'||*c=='1'){ if(*c=='1')v|=(1u<<bit); bit++; any=1; }
        if(any){ if(M<0)M=bit; if(bit!=M){fclose(f);return 0;} out[nv++]=v; }
    }
    fclose(f); *outM=M; return nv;
}

/* recursively split a dim-M set down to dim N, adding all dim-N acute subsets as seeds */
static void split_down(const u32* set,int cnt,int M,int n){
    if(M==n){ add_seed(set,cnt); return; }
    /* for each coordinate c, restrict to coord==0 and coord==1, drop coord c */
    for(int c=0;c<M;c++){
        for(int v=0;v<2;v++){
            u32 sub[MAXSET]; int sc=0;
            u32 lowmask=(c?((1u<<c)-1):0);
            for(int i=0;i<cnt;i++){
                if(((set[i]>>c)&1)!=(u32)v) continue;
                u32 low=set[i]&lowmask;
                u32 high=(set[i]>>(c+1))<<c;
                sub[sc++]=low|high;
            }
            if(sc>=2) split_down(sub,sc,M-1,n);
        }
    }
}

int main(int argc,char**argv){
    if(argc<4){ fprintf(stderr,"usage: %s N TARGET TLIMIT [NTHREADS] [--seed FILE]...\n",argv[0]); return 2; }
    N=atoi(argv[1]); TARGET=atoi(argv[2]); TLIMIT=atof(argv[3]);
    NTHREADS=8;
    UNIV=(N>=32)?0xFFFFFFFFu:((1u<<N)-1);
    int ai=4;
    if(ai<argc && argv[ai][0]!='-'){ NTHREADS=atoi(argv[ai]); ai++; }
    while(ai<argc){
        if(!strcmp(argv[ai],"--seed") && ai+1<argc){
            u32 set[MAXSET]; int M=0; int cnt=read_set(argv[ai+1],set,&M);
            if(cnt>0){
                if(M<N){ fprintf(stderr,"seed %s dim %d < N %d, skip\n",argv[ai+1],M,N); }
                else if(M==N){ if(is_acute(set,cnt)) add_seed(set,cnt); fprintf(stderr,"seed %s: %d vecs dim %d (direct)\n",argv[ai+1],cnt,M); }
                else { int before=nseed; split_down(set,cnt,M,N); fprintf(stderr,"seed %s: %d vecs dim %d -> %d split-seeds\n",argv[ai+1],cnt,M,nseed-before); }
            }
            ai+=2;
        } else ai++;
    }
    /* dedup-ish: report best seed size */
    int maxss=0; for(int i=0;i<nseed;i++) if(seedlen_[i]>maxss)maxss=seedlen_[i];
    fprintf(stderr,"N=%d TARGET=%d threads=%d seeds=%d (max seed size=%d) tlimit=%.0f\n",N,TARGET,NTHREADS,nseed,maxss,TLIMIT);

    pthread_t th[64]; targ_t ta[64];
    for(int i=0;i<NTHREADS;i++){
        ta[i].tid=i; ta[i].rng.s0=0x9E3779B97F4A7C15ull*(i*2+1)+0x1234567; ta[i].rng.s1=0xD1B54A32D192ED03ull*(i*3+7)+987;
        for(int w=0;w<7;w++) rnext(&ta[i].rng);
        pthread_create(&th[i],NULL,worker,&ta[i]);
    }
    for(int i=0;i<NTHREADS;i++) pthread_join(th[i],NULL);

    fprintf(stderr,"BEST size=%d (target %d) N=%d\n",g_best_size,TARGET,N);
    if(!is_acute(g_best_set,g_best_size)){ fprintf(stderr,"INTERNAL ERROR not acute!\n"); return 1; }
    for(int i=0;i<g_best_size;i++){ for(int b=0;b<N;b++) printf("%d%s",(g_best_set[i]>>b)&1,b+1<N?" ":""); printf("\n"); }
    return 0;
}
