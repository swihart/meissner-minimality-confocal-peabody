#include <mpfr.h>

#include <errno.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define DEFAULT_PREC_BITS 384
#define ENDPOINT_X_PANELS 4
#define Q_SLABS 32
#define X_PANELS 10
#define DECIMAL_DIGITS 95

#define DIE(...) do { fprintf(stderr, __VA_ARGS__); fputc('\n', stderr); exit(2); } while (0)

typedef struct { mpfr_t lo, hi; mpfr_prec_t p; } I;
typedef struct { I v, d1, d2, d3; mpfr_prec_t p; } D3;
typedef struct { D3 v, x, xx; mpfr_prec_t p; } X2;
typedef struct {
    mpfr_prec_t p;
    I zero, one, two, sqrt2, kappa, K, pi, psi0;
} Ctx;

static void i_init(I *a, mpfr_prec_t p) {
    a->p = p;
    mpfr_init2(a->lo, p);
    mpfr_init2(a->hi, p);
}
static void i_clear(I *a) { mpfr_clear(a->lo); mpfr_clear(a->hi); }
static void i_copy(I *o, const I *a) {
    mpfr_set(o->lo, a->lo, MPFR_RNDD);
    mpfr_set(o->hi, a->hi, MPFR_RNDU);
}
static void i_set_si(I *o, long v) {
    mpfr_set_si(o->lo, v, MPFR_RNDD);
    mpfr_set_si(o->hi, v, MPFR_RNDU);
}
static void i_set_frac(I *o, long n, unsigned long d) {
    mpfr_t nn, dd;
    mpfr_init2(nn, o->p); mpfr_init2(dd, o->p);
    mpfr_set_si(nn, n, MPFR_RNDN);
    mpfr_set_ui(dd, d, MPFR_RNDN);
    mpfr_div(o->lo, nn, dd, MPFR_RNDD);
    mpfr_div(o->hi, nn, dd, MPFR_RNDU);
    mpfr_clear(nn); mpfr_clear(dd);
}
static void i_set_hull_frac(I *o, long nlo, unsigned long dlo, long nhi, unsigned long dhi) {
    mpfr_t n1,d1,n2,d2;
    mpfr_init2(n1,o->p); mpfr_init2(d1,o->p); mpfr_init2(n2,o->p); mpfr_init2(d2,o->p);
    mpfr_set_si(n1,nlo,MPFR_RNDN); mpfr_set_ui(d1,dlo,MPFR_RNDN);
    mpfr_set_si(n2,nhi,MPFR_RNDN); mpfr_set_ui(d2,dhi,MPFR_RNDN);
    mpfr_div(o->lo,n1,d1,MPFR_RNDD);
    mpfr_div(o->hi,n2,d2,MPFR_RNDU);
    mpfr_clear(n1);mpfr_clear(d1);mpfr_clear(n2);mpfr_clear(d2);
    if (mpfr_cmp(o->lo,o->hi)>0) DIE("invalid hull fraction");
}
static void i_set_pi(I *o) {
    mpfr_const_pi(o->lo, MPFR_RNDD);
    mpfr_const_pi(o->hi, MPFR_RNDU);
}
static void i_add(I *o, const I *a, const I *b) {
    mpfr_t lo,hi; mpfr_init2(lo,o->p); mpfr_init2(hi,o->p);
    mpfr_add(lo,a->lo,b->lo,MPFR_RNDD); mpfr_add(hi,a->hi,b->hi,MPFR_RNDU);
    mpfr_set(o->lo,lo,MPFR_RNDD); mpfr_set(o->hi,hi,MPFR_RNDU);
    mpfr_clear(lo);mpfr_clear(hi);
}
static void i_sub(I *o, const I *a, const I *b) {
    mpfr_t lo,hi; mpfr_init2(lo,o->p); mpfr_init2(hi,o->p);
    mpfr_sub(lo,a->lo,b->hi,MPFR_RNDD); mpfr_sub(hi,a->hi,b->lo,MPFR_RNDU);
    mpfr_set(o->lo,lo,MPFR_RNDD); mpfr_set(o->hi,hi,MPFR_RNDU);
    mpfr_clear(lo);mpfr_clear(hi);
}
static void i_neg(I *o, const I *a) {
    mpfr_t lo,hi; mpfr_init2(lo,o->p); mpfr_init2(hi,o->p);
    mpfr_neg(lo,a->hi,MPFR_RNDD); mpfr_neg(hi,a->lo,MPFR_RNDU);
    mpfr_set(o->lo,lo,MPFR_RNDD); mpfr_set(o->hi,hi,MPFR_RNDU);
    mpfr_clear(lo);mpfr_clear(hi);
}
static void i_mul(I *o, const I *a, const I *b) {
    mpfr_t ld[4], uu[4];
    for(int k=0;k<4;k++){mpfr_init2(ld[k],o->p);mpfr_init2(uu[k],o->p);}    
    mpfr_mul(ld[0],a->lo,b->lo,MPFR_RNDD); mpfr_mul(uu[0],a->lo,b->lo,MPFR_RNDU);
    mpfr_mul(ld[1],a->lo,b->hi,MPFR_RNDD); mpfr_mul(uu[1],a->lo,b->hi,MPFR_RNDU);
    mpfr_mul(ld[2],a->hi,b->lo,MPFR_RNDD); mpfr_mul(uu[2],a->hi,b->lo,MPFR_RNDU);
    mpfr_mul(ld[3],a->hi,b->hi,MPFR_RNDD); mpfr_mul(uu[3],a->hi,b->hi,MPFR_RNDU);
    int il=0,iu=0;
    for(int k=1;k<4;k++){if(mpfr_cmp(ld[k],ld[il])<0)il=k;if(mpfr_cmp(uu[k],uu[iu])>0)iu=k;}
    mpfr_set(o->lo,ld[il],MPFR_RNDD); mpfr_set(o->hi,uu[iu],MPFR_RNDU);
    for(int k=0;k<4;k++){mpfr_clear(ld[k]);mpfr_clear(uu[k]);}
}
static void i_inv(I *o, const I *a) {
    if(mpfr_cmp_si(a->lo,0)<=0 && mpfr_cmp_si(a->hi,0)>=0) DIE("division interval contains zero");
    mpfr_t one,lo,hi; mpfr_init2(one,o->p);mpfr_init2(lo,o->p);mpfr_init2(hi,o->p);
    mpfr_set_ui(one,1,MPFR_RNDN);
    mpfr_div(lo,one,a->hi,MPFR_RNDD); mpfr_div(hi,one,a->lo,MPFR_RNDU);
    mpfr_set(o->lo,lo,MPFR_RNDD);mpfr_set(o->hi,hi,MPFR_RNDU);
    mpfr_clear(one);mpfr_clear(lo);mpfr_clear(hi);
}
static void i_div(I *o, const I *a, const I *b) { I t; i_init(&t,o->p); i_inv(&t,b); i_mul(o,a,&t); i_clear(&t); }
static void i_sqrt(I *o, const I *a) {
    if(mpfr_cmp_si(a->lo,0)<0) DIE("negative sqrt lower endpoint");
    mpfr_t lo,hi;mpfr_init2(lo,o->p);mpfr_init2(hi,o->p);
    mpfr_sqrt(lo,a->lo,MPFR_RNDD);mpfr_sqrt(hi,a->hi,MPFR_RNDU);
    mpfr_set(o->lo,lo,MPFR_RNDD);mpfr_set(o->hi,hi,MPFR_RNDU);
    mpfr_clear(lo);mpfr_clear(hi);
}
static void i_atan(I *o, const I *a) {
    mpfr_t lo,hi;mpfr_init2(lo,o->p);mpfr_init2(hi,o->p);
    mpfr_atan(lo,a->lo,MPFR_RNDD);mpfr_atan(hi,a->hi,MPFR_RNDU);
    mpfr_set(o->lo,lo,MPFR_RNDD);mpfr_set(o->hi,hi,MPFR_RNDU);
    mpfr_clear(lo);mpfr_clear(hi);
}
static void i_pow_ui(I *o, const I *a, unsigned n) {
    I r,b,t; i_init(&r,o->p);i_init(&b,o->p);i_init(&t,o->p);i_set_si(&r,1);i_copy(&b,a);
    while(n){if(n&1){i_mul(&t,&r,&b);i_copy(&r,&t);}n>>=1;if(n){i_mul(&t,&b,&b);i_copy(&b,&t);}}
    i_copy(o,&r);i_clear(&r);i_clear(&b);i_clear(&t);
}
static void i_scale_si(I *o, const I *a, long n) { I s; i_init(&s,o->p); i_set_si(&s,n); i_mul(o,a,&s); i_clear(&s); }
static bool i_pos(const I *a){return mpfr_cmp_si(a->lo,0)>0;}
static bool i_upper_lt(const I *a,const I *b){return mpfr_cmp(a->hi,b->lo)<0;}
static bool i_lower_gt(const I *a,const I *b){return mpfr_cmp(a->lo,b->hi)>0;}
static char *mpstr(mpfr_srcptr x, int digits, mpfr_rnd_t rnd){
    char *s=NULL;
    const char *fmt = (rnd==MPFR_RNDD) ? "%.*RDe" : ((rnd==MPFR_RNDU) ? "%.*RUe" : "%.*RNe");
    if(mpfr_asprintf(&s,fmt,digits,x)<0||!s)DIE("mpfr_asprintf failed");
    return s;
}

static void d3_init(D3 *a,mpfr_prec_t p){a->p=p;i_init(&a->v,p);i_init(&a->d1,p);i_init(&a->d2,p);i_init(&a->d3,p);}
static void d3_clear(D3 *a){i_clear(&a->v);i_clear(&a->d1);i_clear(&a->d2);i_clear(&a->d3);}
static void d3_copy(D3 *o,const D3 *a){i_copy(&o->v,&a->v);i_copy(&o->d1,&a->d1);i_copy(&o->d2,&a->d2);i_copy(&o->d3,&a->d3);}
static void d3_const_i(D3 *o,const I *v){i_copy(&o->v,v);i_set_si(&o->d1,0);i_set_si(&o->d2,0);i_set_si(&o->d3,0);}
static void d3_const_si(D3 *o,long v){i_set_si(&o->v,v);i_set_si(&o->d1,0);i_set_si(&o->d2,0);i_set_si(&o->d3,0);}
static void d3_add(D3 *o,const D3*a,const D3*b){D3 t;d3_init(&t,o->p);i_add(&t.v,&a->v,&b->v);i_add(&t.d1,&a->d1,&b->d1);i_add(&t.d2,&a->d2,&b->d2);i_add(&t.d3,&a->d3,&b->d3);d3_copy(o,&t);d3_clear(&t);}
static void d3_sub(D3 *o,const D3*a,const D3*b){D3 t;d3_init(&t,o->p);i_sub(&t.v,&a->v,&b->v);i_sub(&t.d1,&a->d1,&b->d1);i_sub(&t.d2,&a->d2,&b->d2);i_sub(&t.d3,&a->d3,&b->d3);d3_copy(o,&t);d3_clear(&t);}
static void d3_neg(D3 *o,const D3*a){D3 t;d3_init(&t,o->p);i_neg(&t.v,&a->v);i_neg(&t.d1,&a->d1);i_neg(&t.d2,&a->d2);i_neg(&t.d3,&a->d3);d3_copy(o,&t);d3_clear(&t);}
static void d3_mul(D3 *o,const D3*a,const D3*b){D3 t;d3_init(&t,o->p);I u1,u2,u3,u4; i_init(&u1,o->p);i_init(&u2,o->p);i_init(&u3,o->p);i_init(&u4,o->p);
 i_mul(&t.v,&a->v,&b->v);
 i_mul(&u1,&a->d1,&b->v);i_mul(&u2,&a->v,&b->d1);i_add(&t.d1,&u1,&u2);
 i_mul(&u1,&a->d2,&b->v);i_mul(&u2,&a->d1,&b->d1);i_scale_si(&u2,&u2,2);i_mul(&u3,&a->v,&b->d2);i_add(&u4,&u1,&u2);i_add(&t.d2,&u4,&u3);
 i_mul(&u1,&a->d3,&b->v);i_mul(&u2,&a->d2,&b->d1);i_scale_si(&u2,&u2,3);i_mul(&u3,&a->d1,&b->d2);i_scale_si(&u3,&u3,3);i_mul(&u4,&a->v,&b->d3);I s; i_init(&s,o->p);i_add(&s,&u1,&u2);i_add(&s,&s,&u3);i_add(&t.d3,&s,&u4);i_clear(&s);
 d3_copy(o,&t);i_clear(&u1);i_clear(&u2);i_clear(&u3);i_clear(&u4);d3_clear(&t);}
static void d3_inv(D3 *o,const D3*a){D3 t;d3_init(&t,o->p);I v2,v3,v4,u1,u2,u3; i_init(&v2,o->p);i_init(&v3,o->p);i_init(&v4,o->p);i_init(&u1,o->p);i_init(&u2,o->p);i_init(&u3,o->p);
 i_inv(&t.v,&a->v);i_pow_ui(&v2,&a->v,2);i_pow_ui(&v3,&a->v,3);i_pow_ui(&v4,&a->v,4);
 i_div(&u1,&a->d1,&v2);i_neg(&t.d1,&u1);
 i_pow_ui(&u1,&a->d1,2);i_scale_si(&u1,&u1,2);i_div(&u1,&u1,&v3);i_div(&u2,&a->d2,&v2);i_sub(&t.d2,&u1,&u2);
 i_pow_ui(&u1,&a->d1,3);i_scale_si(&u1,&u1,-6);i_div(&u1,&u1,&v4);i_mul(&u2,&a->d1,&a->d2);i_scale_si(&u2,&u2,6);i_div(&u2,&u2,&v3);i_div(&u3,&a->d3,&v2);i_neg(&u3,&u3);i_add(&t.d3,&u1,&u2);i_add(&t.d3,&t.d3,&u3);
 d3_copy(o,&t);i_clear(&v2);i_clear(&v3);i_clear(&v4);i_clear(&u1);i_clear(&u2);i_clear(&u3);d3_clear(&t);}
static void d3_div(D3 *o,const D3*a,const D3*b){D3 inv;d3_init(&inv,o->p);d3_inv(&inv,b);d3_mul(o,a,&inv);d3_clear(&inv);}
static void d3_pow_ui(D3 *o,const D3*a,unsigned n){D3 r,b,t;d3_init(&r,o->p);d3_init(&b,o->p);d3_init(&t,o->p);d3_const_si(&r,1);d3_copy(&b,a);while(n){if(n&1){d3_mul(&t,&r,&b);d3_copy(&r,&t);}n>>=1;if(n){d3_mul(&t,&b,&b);d3_copy(&b,&t);}}d3_copy(o,&r);d3_clear(&r);d3_clear(&b);d3_clear(&t);}
static void d3_scale_si(D3 *o,const D3*a,long n){D3 s;d3_init(&s,o->p);d3_const_si(&s,n);d3_mul(o,a,&s);d3_clear(&s);}
static void d3_sqrt(D3 *o,const D3*a){D3 t;d3_init(&t,o->p);I s2,s3,s5,u1,u2,u3; i_init(&s2,o->p);i_init(&s3,o->p);i_init(&s5,o->p);i_init(&u1,o->p);i_init(&u2,o->p);i_init(&u3,o->p);i_sqrt(&t.v,&a->v);i_pow_ui(&s2,&t.v,2);i_pow_ui(&s3,&t.v,3);i_pow_ui(&s5,&t.v,5);
 i_scale_si(&u1,&t.v,2);i_div(&t.d1,&a->d1,&u1);
 i_scale_si(&u1,&t.v,2);i_div(&u1,&a->d2,&u1);i_pow_ui(&u2,&a->d1,2);i_scale_si(&u3,&s3,4);i_div(&u2,&u2,&u3);i_sub(&t.d2,&u1,&u2);
 i_scale_si(&u1,&t.v,2);i_div(&u1,&a->d3,&u1);i_mul(&u2,&a->d1,&a->d2);i_scale_si(&u2,&u2,3);i_scale_si(&u3,&s3,4);i_div(&u2,&u2,&u3);i_sub(&u1,&u1,&u2);i_pow_ui(&u2,&a->d1,3);i_scale_si(&u2,&u2,3);i_scale_si(&u3,&s5,8);i_div(&u2,&u2,&u3);i_add(&t.d3,&u1,&u2);
 d3_copy(o,&t);i_clear(&s2);i_clear(&s3);i_clear(&s5);i_clear(&u1);i_clear(&u2);i_clear(&u3);d3_clear(&t);}
static void d3_atan(D3 *o,const D3*a){D3 t;d3_init(&t,o->p);I den,den2,den3,u1,u2,u3,u4; i_init(&den,o->p);i_init(&den2,o->p);i_init(&den3,o->p);i_init(&u1,o->p);i_init(&u2,o->p);i_init(&u3,o->p);i_init(&u4,o->p);i_atan(&t.v,&a->v);i_pow_ui(&u1,&a->v,2);i_set_si(&den,1);i_add(&den,&den,&u1);i_pow_ui(&den2,&den,2);i_pow_ui(&den3,&den,3);i_div(&t.d1,&a->d1,&den);
 i_div(&u1,&a->d2,&den);i_pow_ui(&u2,&a->d1,2);i_mul(&u2,&u2,&a->v);i_scale_si(&u2,&u2,2);i_div(&u2,&u2,&den2);i_sub(&t.d2,&u1,&u2);
 i_div(&u1,&a->d3,&den);i_mul(&u2,&a->d1,&a->d2);i_mul(&u2,&u2,&a->v);i_scale_si(&u2,&u2,6);i_div(&u2,&u2,&den2);i_sub(&u1,&u1,&u2);i_pow_ui(&u2,&a->v,2);i_scale_si(&u2,&u2,6);i_set_si(&u3,2);i_sub(&u2,&u2,&u3);i_pow_ui(&u3,&a->d1,3);i_mul(&u2,&u2,&u3);i_div(&u2,&u2,&den3);i_add(&t.d3,&u1,&u2);
 d3_copy(o,&t);i_clear(&den);i_clear(&den2);i_clear(&den3);i_clear(&u1);i_clear(&u2);i_clear(&u3);i_clear(&u4);d3_clear(&t);}

static void x2_init(X2*a,mpfr_prec_t p){a->p=p;d3_init(&a->v,p);d3_init(&a->x,p);d3_init(&a->xx,p);}
static void x2_clear(X2*a){d3_clear(&a->v);d3_clear(&a->x);d3_clear(&a->xx);}
static void x2_copy(X2*o,const X2*a){d3_copy(&o->v,&a->v);d3_copy(&o->x,&a->x);d3_copy(&o->xx,&a->xx);}
static void x2_const_i(X2*o,const I*v){d3_const_i(&o->v,v);d3_const_si(&o->x,0);d3_const_si(&o->xx,0);}
static void x2_const_si(X2*o,long v){d3_const_si(&o->v,v);d3_const_si(&o->x,0);d3_const_si(&o->xx,0);}
static void x2_add(X2*o,const X2*a,const X2*b){X2 t;x2_init(&t,o->p);d3_add(&t.v,&a->v,&b->v);d3_add(&t.x,&a->x,&b->x);d3_add(&t.xx,&a->xx,&b->xx);x2_copy(o,&t);x2_clear(&t);}
static void x2_sub(X2*o,const X2*a,const X2*b){X2 t;x2_init(&t,o->p);d3_sub(&t.v,&a->v,&b->v);d3_sub(&t.x,&a->x,&b->x);d3_sub(&t.xx,&a->xx,&b->xx);x2_copy(o,&t);x2_clear(&t);}
static void x2_neg(X2*o,const X2*a){X2 t;x2_init(&t,o->p);d3_neg(&t.v,&a->v);d3_neg(&t.x,&a->x);d3_neg(&t.xx,&a->xx);x2_copy(o,&t);x2_clear(&t);}
static void x2_mul(X2*o,const X2*a,const X2*b){X2 t;x2_init(&t,o->p);D3 u1,u2,u3;d3_init(&u1,o->p);d3_init(&u2,o->p);d3_init(&u3,o->p);d3_mul(&t.v,&a->v,&b->v);d3_mul(&u1,&a->x,&b->v);d3_mul(&u2,&a->v,&b->x);d3_add(&t.x,&u1,&u2);d3_mul(&u1,&a->xx,&b->v);d3_mul(&u2,&a->x,&b->x);d3_scale_si(&u2,&u2,2);d3_mul(&u3,&a->v,&b->xx);d3_add(&t.xx,&u1,&u2);d3_add(&t.xx,&t.xx,&u3);x2_copy(o,&t);d3_clear(&u1);d3_clear(&u2);d3_clear(&u3);x2_clear(&t);}
static void x2_inv(X2*o,const X2*a){X2 t;x2_init(&t,o->p);D3 v2,v3,u1,u2;d3_init(&v2,o->p);d3_init(&v3,o->p);d3_init(&u1,o->p);d3_init(&u2,o->p);d3_inv(&t.v,&a->v);d3_pow_ui(&v2,&a->v,2);d3_pow_ui(&v3,&a->v,3);d3_div(&u1,&a->x,&v2);d3_neg(&t.x,&u1);d3_pow_ui(&u1,&a->x,2);d3_scale_si(&u1,&u1,2);d3_div(&u1,&u1,&v3);d3_div(&u2,&a->xx,&v2);d3_sub(&t.xx,&u1,&u2);x2_copy(o,&t);d3_clear(&v2);d3_clear(&v3);d3_clear(&u1);d3_clear(&u2);x2_clear(&t);}
static void x2_div(X2*o,const X2*a,const X2*b){X2 inv;x2_init(&inv,o->p);x2_inv(&inv,b);x2_mul(o,a,&inv);x2_clear(&inv);}
static void x2_scale_si(X2*o,const X2*a,long n){X2 s;x2_init(&s,o->p);x2_const_si(&s,n);x2_mul(o,a,&s);x2_clear(&s);}
static void x2_sqrt(X2*o,const X2*a){X2 t;x2_init(&t,o->p);D3 s2,s3,u1,u2;d3_init(&s2,o->p);d3_init(&s3,o->p);d3_init(&u1,o->p);d3_init(&u2,o->p);d3_sqrt(&t.v,&a->v);d3_scale_si(&u1,&t.v,2);d3_div(&t.x,&a->x,&u1);d3_scale_si(&u1,&t.v,2);d3_div(&u1,&a->xx,&u1);d3_pow_ui(&u2,&a->x,2);d3_pow_ui(&s3,&t.v,3);d3_scale_si(&s3,&s3,4);d3_div(&u2,&u2,&s3);d3_sub(&t.xx,&u1,&u2);x2_copy(o,&t);d3_clear(&s2);d3_clear(&s3);d3_clear(&u1);d3_clear(&u2);x2_clear(&t);}
static void x2_atan(X2*o,const X2*a){X2 t;x2_init(&t,o->p);D3 den,den2,u1,u2;d3_init(&den,o->p);d3_init(&den2,o->p);d3_init(&u1,o->p);d3_init(&u2,o->p);d3_atan(&t.v,&a->v);d3_pow_ui(&u1,&a->v,2);d3_const_si(&den,1);d3_add(&den,&den,&u1);d3_div(&t.x,&a->x,&den);d3_div(&u1,&a->xx,&den);d3_pow_ui(&u2,&a->x,2);d3_mul(&u2,&u2,&a->v);d3_scale_si(&u2,&u2,2);d3_pow_ui(&den2,&den,2);d3_div(&u2,&u2,&den2);d3_sub(&t.xx,&u1,&u2);x2_copy(o,&t);d3_clear(&den);d3_clear(&den2);d3_clear(&u1);d3_clear(&u2);x2_clear(&t);}

static void ctx_init(Ctx*c,mpfr_prec_t p){c->p=p;i_init(&c->zero,p);i_init(&c->one,p);i_init(&c->two,p);i_init(&c->sqrt2,p);i_init(&c->kappa,p);i_init(&c->K,p);i_init(&c->pi,p);i_init(&c->psi0,p);i_set_si(&c->zero,0);i_set_si(&c->one,1);i_set_si(&c->two,2);i_sqrt(&c->sqrt2,&c->two);i_add(&c->kappa,&c->one,&c->sqrt2);i_mul(&c->K,&c->kappa,&c->kappa);i_set_pi(&c->pi);I three,sqrt3,twosqrt2,alpha,tmp; i_init(&three,p);i_init(&sqrt3,p);i_init(&twosqrt2,p);i_init(&alpha,p);i_init(&tmp,p);i_set_si(&three,3);i_sqrt(&sqrt3,&three);i_scale_si(&twosqrt2,&c->sqrt2,2);i_atan(&alpha,&twosqrt2);i_scale_si(&tmp,&c->pi,2);i_div(&tmp,&tmp,&sqrt3);i_mul(&tmp,&tmp,&alpha);i_neg(&c->psi0,&tmp);i_clear(&three);i_clear(&sqrt3);i_clear(&twosqrt2);i_clear(&alpha);i_clear(&tmp);}
static void ctx_clear(Ctx*c){i_clear(&c->zero);i_clear(&c->one);i_clear(&c->two);i_clear(&c->sqrt2);i_clear(&c->kappa);i_clear(&c->K);i_clear(&c->pi);i_clear(&c->psi0);}

#define XDECL(name) X2 name; x2_init(&name,p)
#define XCLEAR(name) x2_clear(&name)

static void h_jet(X2*out,const I*qv,const I*xv,const Ctx*c,int correction_sign){mpfr_prec_t p=c->p;
 XDECL(Q);XDECL(X);XDECL(one);XDECL(K);XDECL(sqrt2);XDECL(kappa);XDECL(D);XDECL(R);XDECL(T);XDECL(delta);XDECL(M);XDECL(primary);XDECL(correction);XDECL(algebraic);XDECL(Z);XDECL(A);XDECL(t1);XDECL(t2);XDECL(t3);XDECL(t4);XDECL(t5);XDECL(t6);XDECL(t7);XDECL(t8);XDECL(t9);XDECL(t10);XDECL(t11);
 d3_const_i(&Q.v,qv);i_set_si(&Q.v.d1,1);d3_const_si(&Q.x,0);d3_const_si(&Q.xx,0);
 d3_const_i(&X.v,xv);d3_const_si(&X.x,1);d3_const_si(&X.xx,0);
 x2_const_si(&one,1);x2_const_i(&K,&c->K);x2_const_i(&sqrt2,&c->sqrt2);x2_const_i(&kappa,&c->kappa);
 x2_mul(&t1,&K,&K);x2_mul(&t2,&Q,&Q);x2_add(&t3,&t1,&t2);x2_sqrt(&D,&t3);
 x2_mul(&t4,&X,&X);x2_mul(&t5,&K,&Q);x2_scale_si(&t5,&t5,2);x2_mul(&t5,&t5,&t4);x2_sub(&t6,&t3,&t5);x2_sqrt(&R,&t6);
 x2_mul(&t7,&K,&t3);x2_scale_si(&t7,&t7,2);x2_sub(&t8,&one,&Q);x2_mul(&t9,&t8,&t8);x2_mul(&t10,&K,&K);x2_mul(&t10,&t10,&t9);x2_mul(&t10,&t10,&t4);x2_add(&t11,&t7,&t10);x2_sqrt(&T,&t11);
 x2_sub(&t8,&one,&t4);x2_mul(&t8,&t8,&K);x2_scale_si(&t8,&t8,2);x2_add(&t9,&R,&K);x2_sub(&t9,&t9,&Q);x2_div(&delta,&t8,&t9);
 x2_mul(&t8,&K,&t4);x2_scale_si(&t8,&t8,2);x2_sub(&t8,&Q,&t8);x2_mul(&t8,&t8,&K);x2_add(&t9,&R,&K);x2_div(&M,&t8,&t9);x2_sub(&t8,&one,&K);x2_mul(&t8,&t8,&R);x2_add(&M,&M,&t8);x2_mul(&t8,&K,&K);x2_sub(&M,&M,&t8);x2_mul(&t8,&Q,&R);x2_sub(&M,&M,&t8);x2_sub(&M,&M,&Q);x2_mul(&t8,&Q,&Q);x2_sub(&M,&M,&t8);
 x2_mul(&t8,&sqrt2,&kappa);x2_mul(&t8,&t8,&t3);x2_scale_si(&t8,&t8,-16);x2_mul(&t9,&R,&T);x2_div(&primary,&t8,&t9);
 x2_mul(&t8,&Q,&Q);x2_sub(&t8,&one,&t8);x2_mul(&t8,&t8,&K);x2_mul(&t8,&t8,&t3);x2_mul(&t8,&t8,&delta);x2_mul(&t8,&t8,&M);x2_scale_si(&t8,&t8,-4);x2_mul(&t9,&T,&T);x2_mul(&t9,&t9,&T);x2_mul(&t9,&t9,&R);x2_div(&correction,&t8,&t9);
 x2_mul(&t8,&Q,&Q);x2_sub(&t8,&one,&t8);x2_mul(&t8,&t8,&K);x2_mul(&t8,&t8,&t3);x2_mul(&t8,&t8,&delta);x2_scale_si(&t8,&t8,-4);x2_mul(&t9,&T,&T);x2_mul(&t9,&t9,&R);x2_div(&algebraic,&t8,&t9);
 x2_add(&t8,&one,&Q);x2_mul(&t8,&t8,&D);x2_sub(&t9,&one,&Q);x2_mul(&t9,&t9,&R);x2_add(&t8,&t8,&t9);x2_mul(&t8,&t8,&K);x2_add(&t9,&K,&Q);x2_add(&t9,&t9,&D);x2_mul(&t9,&t9,&T);x2_div(&Z,&t8,&t9);x2_atan(&A,&Z);
 if(correction_sign<0){x2_neg(&correction,&correction);}x2_add(&t8,&primary,&correction);x2_mul(&t8,&t8,&A);x2_add(out,&t8,&algebraic);
 XCLEAR(Q);XCLEAR(X);XCLEAR(one);XCLEAR(K);XCLEAR(sqrt2);XCLEAR(kappa);XCLEAR(D);XCLEAR(R);XCLEAR(T);XCLEAR(delta);XCLEAR(M);XCLEAR(primary);XCLEAR(correction);XCLEAR(algebraic);XCLEAR(Z);XCLEAR(A);XCLEAR(t1);XCLEAR(t2);XCLEAR(t3);XCLEAR(t4);XCLEAR(t5);XCLEAR(t6);XCLEAR(t7);XCLEAR(t8);XCLEAR(t9);XCLEAR(t10);XCLEAR(t11);
}

static void midpoint_endpoint(I*total,FILE*boxes,const Ctx*c,int correction_sign){I width,main,rem,contrib,q0,xm,xb,w3,den; i_init(&width,c->p);i_init(&main,c->p);i_init(&rem,c->p);i_init(&contrib,c->p);i_init(&q0,c->p);i_init(&xm,c->p);i_init(&xb,c->p);i_init(&w3,c->p);i_init(&den,c->p);i_set_frac(&width,1,ENDPOINT_X_PANELS);i_pow_ui(&w3,&width,3);i_set_si(&den,24);i_div(&w3,&w3,&den);i_set_si(&q0,0);i_set_si(total,0);
 fprintf(boxes,"x_panel_index,x_lo,x_hi,contribution_lower,contribution_upper\n");
 for(int j=0;j<ENDPOINT_X_PANELS;j++){i_set_frac(&xm,2*j+1,2*ENDPOINT_X_PANELS);i_set_hull_frac(&xb,j,ENDPOINT_X_PANELS,j+1,ENDPOINT_X_PANELS);X2 jm,jb;x2_init(&jm,c->p);x2_init(&jb,c->p);h_jet(&jm,&q0,&xm,c,correction_sign);h_jet(&jb,&q0,&xb,c,correction_sign);i_mul(&main,&width,&jm.v.v);i_mul(&rem,&w3,&jb.xx.v);i_add(&contrib,&main,&rem);i_add(total,total,&contrib);char*lo=mpstr(contrib.lo,DECIMAL_DIGITS,MPFR_RNDD);char*hi=mpstr(contrib.hi,DECIMAL_DIGITS,MPFR_RNDU);fprintf(boxes,"%d,%d/%d,%d/%d,%s,%s\n",j,j,ENDPOINT_X_PANELS,j+1,ENDPOINT_X_PANELS,lo,hi);mpfr_free_str(lo);mpfr_free_str(hi);x2_clear(&jm);x2_clear(&jb);}i_clear(&width);i_clear(&main);i_clear(&rem);i_clear(&contrib);i_clear(&q0);i_clear(&xm);i_clear(&xb);i_clear(&w3);i_clear(&den);}

static void integral_C(I*total,long qnum,unsigned qden,const Ctx*c,bool derivative, long qlo,unsigned qdlo,long qhi,unsigned qdhi, FILE*boxfile,int slab,int correction_sign){I width,w3,den,qv,xm,xb,main,rem,contrib,tmp1,tmp2; i_init(&width,c->p);i_init(&w3,c->p);i_init(&den,c->p);i_init(&qv,c->p);i_init(&xm,c->p);i_init(&xb,c->p);i_init(&main,c->p);i_init(&rem,c->p);i_init(&contrib,c->p);i_init(&tmp1,c->p);i_init(&tmp2,c->p);i_set_frac(&width,1,X_PANELS);i_pow_ui(&w3,&width,3);i_set_si(&den,24);i_div(&w3,&w3,&den);if(derivative)i_set_hull_frac(&qv,qlo,qdlo,qhi,qdhi);else i_set_frac(&qv,qnum,qden);i_set_si(total,0);
 for(int j=0;j<X_PANELS;j++){i_set_frac(&xm,2*j+1,2*X_PANELS);i_set_hull_frac(&xb,j,X_PANELS,j+1,X_PANELS);X2 jm,jb;x2_init(&jm,c->p);x2_init(&jb,c->p);h_jet(&jm,&qv,&xm,c,correction_sign);h_jet(&jb,&qv,&xb,c,correction_sign);I oneq; i_init(&oneq,c->p);i_set_si(&oneq,1);i_add(&oneq,&oneq,&qv);if(!derivative){i_mul(&tmp1,&oneq,&jm.v.d2);i_scale_si(&tmp2,&jm.v.d1,2);i_add(&tmp1,&tmp1,&tmp2);i_mul(&main,&width,&tmp1);i_mul(&tmp1,&oneq,&jb.xx.d2);i_scale_si(&tmp2,&jb.xx.d1,2);i_add(&tmp1,&tmp1,&tmp2);i_mul(&rem,&w3,&tmp1);}else{i_mul(&tmp1,&oneq,&jm.v.d3);i_scale_si(&tmp2,&jm.v.d2,3);i_add(&tmp1,&tmp1,&tmp2);i_mul(&main,&width,&tmp1);i_mul(&tmp1,&oneq,&jb.xx.d3);i_scale_si(&tmp2,&jb.xx.d2,3);i_add(&tmp1,&tmp1,&tmp2);i_mul(&rem,&w3,&tmp1);}i_add(&contrib,&main,&rem);i_add(total,total,&contrib);if(boxfile){char*lo=mpstr(contrib.lo,DECIMAL_DIGITS,MPFR_RNDD);char*hi=mpstr(contrib.hi,DECIMAL_DIGITS,MPFR_RNDU);fprintf(boxfile,"%d,%d,%d/%d,%d/%d,%s,%s,%s\n",slab,j,j,X_PANELS,j+1,X_PANELS,derivative?"Cq":"C",lo,hi);mpfr_free_str(lo);mpfr_free_str(hi);}i_clear(&oneq);x2_clear(&jm);x2_clear(&jb);}i_clear(&width);i_clear(&w3);i_clear(&den);i_clear(&qv);i_clear(&xm);i_clear(&xb);i_clear(&main);i_clear(&rem);i_clear(&contrib);i_clear(&tmp1);i_clear(&tmp2);}

static void diagnostics(bool*pass,const Ctx*c,FILE*out){I q,x,D2,R2,T2,D,R,T,tmp,tmp2,num,den,Z;I*arr[]={&q,&x,&D2,&R2,&T2,&D,&R,&T,&tmp,&tmp2,&num,&den,&Z};for(size_t k=0;k<sizeof(arr)/sizeof(arr[0]);k++)i_init(arr[k],c->p);i_set_hull_frac(&q,0,1,1,1);i_set_hull_frac(&x,0,1,1,1);i_mul(&D2,&c->K,&c->K);i_mul(&tmp,&q,&q);i_add(&D2,&D2,&tmp);i_mul(&tmp,&c->K,&q);i_mul(&tmp,&tmp,&x);i_mul(&tmp,&tmp,&x);i_scale_si(&tmp,&tmp,2);i_sub(&R2,&D2,&tmp);i_mul(&T2,&c->K,&D2);i_scale_si(&T2,&T2,2);i_sub(&tmp,&c->one,&q);i_mul(&tmp,&tmp,&tmp);i_mul(&tmp2,&c->K,&c->K);i_mul(&tmp,&tmp,&tmp2);i_mul(&tmp,&tmp,&x);i_mul(&tmp,&tmp,&x);i_add(&T2,&T2,&tmp);i_sqrt(&D,&D2);i_sqrt(&R,&R2);i_sqrt(&T,&T2);i_add(&tmp,&R,&c->K);i_sub(&tmp,&tmp,&q);i_add(&tmp2,&c->one,&q);i_mul(&tmp2,&tmp2,&D);i_sub(&num,&c->one,&q);i_mul(&num,&num,&R);i_add(&num,&num,&tmp2);i_mul(&num,&num,&c->K);i_add(&den,&c->K,&q);i_add(&den,&den,&D);i_mul(&den,&den,&T);i_div(&Z,&num,&den);const char*names[]={"D2","R2","T2","delta_denominator","angle_numerator","angle_denominator","Z"};I*vals[]={&D2,&R2,&T2,&tmp,&num,&den,&Z};if(out) fprintf(out,"  \"domain_diagnostics\": {\n");for(int j=0;j<7;j++){bool ok=i_pos(vals[j]);*pass=*pass&&ok;if(out){char*lo=mpstr(vals[j]->lo,40,MPFR_RNDD);char*hi=mpstr(vals[j]->hi,40,MPFR_RNDU);fprintf(out,"    \"%s\": {\"lower\": \"%s\", \"upper\": \"%s\", \"strictly_positive\": %s}%s\n",names[j],lo,hi,ok?"true":"false",j==6?"":",");mpfr_free_str(lo);mpfr_free_str(hi);}}if(out) fprintf(out,"  },\n");for(size_t k=0;k<sizeof(arr)/sizeof(arr[0]);k++)i_clear(arr[k]);}

int main(int argc,char**argv){const char*outdir=NULL;mpfr_prec_t prec=DEFAULT_PREC_BITS;bool reverse=false;int correction_sign=1;int q_slabs=Q_SLABS;for(int i=1;i<argc;i++){if(strcmp(argv[i],"--output-dir")==0&&i+1<argc)outdir=argv[++i];else if(strcmp(argv[i],"--precision-bits")==0&&i+1<argc)prec=strtol(argv[++i],NULL,10);else if(strcmp(argv[i],"--reverse")==0)reverse=true;else if(strcmp(argv[i],"--correction-sign")==0&&i+1<argc)correction_sign=atoi(argv[++i]);else if(strcmp(argv[i],"--q-slabs")==0&&i+1<argc)q_slabs=atoi(argv[++i]);else DIE("unknown argument: %s",argv[i]);}if(correction_sign!=1&&correction_sign!=-1)DIE("correction sign must be +/-1");if(q_slabs<=0)DIE("q slabs must be positive");if(!outdir)DIE("--output-dir required");char cmd[4096];snprintf(cmd,sizeof(cmd),"mkdir -p '%s'",outdir);if(system(cmd)!=0)DIE("cannot create output dir");clock_t start=clock();Ctx c;ctx_init(&c,prec);
 char path[4096];snprintf(path,sizeof(path),"%s/endpoint_terminal_boxes.csv",outdir);FILE*fep=fopen(path,"w");if(!fep)DIE("open endpoint csv");I psi1,phi1,tmp,target; i_init(&psi1,prec);i_init(&phi1,prec);i_init(&tmp,prec);i_init(&target,prec);midpoint_endpoint(&psi1,fep,&c,correction_sign);fclose(fep);i_sub(&tmp,&psi1,&c.psi0);i_set_frac(&target,1,8);i_mul(&phi1,&tmp,&target);i_set_frac(&target,1,4000);bool endpoint_pass=i_lower_gt(&phi1,&target);
 snprintf(path,sizeof(path),"%s/concavity_terminal_boxes.csv",outdir);FILE*fbox=fopen(path,"w");if(!fbox)DIE("open box csv");fprintf(fbox,"q_slab_index,x_panel_index,x_lo,x_hi,kind,contribution_lower,contribution_upper\n");snprintf(path,sizeof(path),"%s/concavity_slab_summary.csv",outdir);FILE*fslab=fopen(path,"w");if(!fslab)DIE("open slab csv");fprintf(fslab,"index,q_lo,q_hi,q_mid,c_lower,c_upper,phi_second_lower,phi_second_upper,below_negative_target\n");bool all_concave=true;I worst; i_init(&worst,prec);bool worst_set=false;i_set_frac(&target,-1,30000);
 for(int step=0;step<q_slabs;step++){int idx=reverse?(q_slabs-1-step):step;I cmid,cq,qdelta,cen,qbox,oneq,factor,phi2;I*aa[]={&cmid,&cq,&qdelta,&cen,&qbox,&oneq,&factor,&phi2};for(size_t k=0;k<8;k++)i_init(aa[k],prec);integral_C(&cmid,2*idx+1,2*q_slabs,&c,false,0,1,0,1,fbox,idx,correction_sign);integral_C(&cq,0,1,&c,true,idx,q_slabs,idx+1,q_slabs,fbox,idx,correction_sign);i_set_hull_frac(&qdelta,-1,2*q_slabs,1,2*q_slabs);i_mul(&tmp,&qdelta,&cq);i_add(&cen,&cmid,&tmp);i_set_hull_frac(&qbox,idx,q_slabs,idx+1,q_slabs);i_add(&oneq,&c.one,&qbox);i_pow_ui(&factor,&oneq,3);i_set_frac(&tmp,1,32);i_mul(&factor,&factor,&tmp);i_mul(&phi2,&factor,&cen);bool ok=i_upper_lt(&phi2,&target);all_concave=all_concave&&ok;if(!worst_set||mpfr_cmp(phi2.hi,worst.hi)>0){i_copy(&worst,&phi2);worst_set=true;}char*cl=mpstr(cen.lo,DECIMAL_DIGITS,MPFR_RNDD);char*cu=mpstr(cen.hi,DECIMAL_DIGITS,MPFR_RNDU);char*pl=mpstr(phi2.lo,DECIMAL_DIGITS,MPFR_RNDD);char*pu=mpstr(phi2.hi,DECIMAL_DIGITS,MPFR_RNDU);fprintf(fslab,"%d,%d/%d,%d/%d,%d/%d,%s,%s,%s,%s,%s\n",idx,idx,q_slabs,idx+1,q_slabs,2*idx+1,2*q_slabs,cl,cu,pl,pu,ok?"true":"false");mpfr_free_str(cl);mpfr_free_str(cu);mpfr_free_str(pl);mpfr_free_str(pu);for(size_t k=0;k<8;k++)i_clear(aa[k]);}
 fclose(fbox);fclose(fslab);bool diag_pass=true;diagnostics(&diag_pass,&c,NULL);bool passed=endpoint_pass&&all_concave&&diag_pass;snprintf(path,sizeof(path),"%s/peabody_mpfr_concavity_certificate.json",outdir);FILE*fj=fopen(path,"w");if(!fj)DIE("open json");fprintf(fj,"{\n  \"certificate_version\": \"PEABODY_MPFR_DIRECTED_CONCAVITY_V1\",\n  \"formula_version\": \"PEABODY_CENTRAL_STABLE_Q_V1\",\n  \"classification\": \"%s\",\n  \"pass\": %s,\n  \"proof_authority\": \"direct libmpfr directed endpoint intervals\",\n  \"mpfr_version\": \"%s\",\n  \"precision_bits\": %ld,\n",passed?"GO_PEABODY_MPFR_DIRECTED_CERTIFICATE":"NO_GO_PEABODY_MPFR_DIRECTED_CERTIFICATE",passed?"true":"false",mpfr_get_version(),(long)prec);bool diag_write=true;diagnostics(&diag_write,&c,fj);char*eplo=mpstr(phi1.lo,90,MPFR_RNDD);char*ephi=mpstr(phi1.hi,90,MPFR_RNDU);char*wup=mpstr(worst.hi,90,MPFR_RNDU);fprintf(fj,"  \"endpoint\": {\"phi_one_lower\": \"%s\", \"phi_one_upper\": \"%s\", \"target\": \"1/4000\", \"pass\": %s},\n",eplo,ephi,endpoint_pass?"true":"false");fprintf(fj,"  \"concavity\": {\"worst_phi_second_upper\": \"%s\", \"target\": \"-1/30000\", \"pass\": %s, \"q_slabs\": %d, \"x_panels_per_slab\": 10},\n",wup,all_concave?"true":"false",q_slabs);fprintf(fj,"  \"terminal_rectangles\": %d,\n  \"correction_sign\": %d,\n  \"deduced_bound\": \"Phi(e) > e/4000 for 0<e<1\",\n  \"subdivision_order\": \"%s\",\n  \"elapsed_seconds\": %.6f\n}\n",4+q_slabs*X_PANELS,correction_sign,reverse?"reverse":"forward",(double)(clock()-start)/CLOCKS_PER_SEC);fclose(fj);mpfr_free_str(eplo);mpfr_free_str(ephi);mpfr_free_str(wup);
 printf("MPFR version: %s\n",mpfr_get_version());printf("Endpoint pass: %s\n",endpoint_pass?"true":"false");printf("Concavity pass: %s\n",all_concave?"true":"false");printf("Overall pass: %s\n",passed?"true":"false");printf("Classification: %s\n",passed?"GO_PEABODY_MPFR_DIRECTED_CERTIFICATE":"NO_GO_PEABODY_MPFR_DIRECTED_CERTIFICATE");
 i_clear(&psi1);i_clear(&phi1);i_clear(&tmp);i_clear(&target);i_clear(&worst);ctx_clear(&c);return passed?0:1;}
