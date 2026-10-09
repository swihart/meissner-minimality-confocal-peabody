#!/usr/bin/env Rscript
# Exact finite companion to final_certificate_jet_check.py.
# R runtime status at delivery: UNEXECUTED (Rscript unavailable).
# The derivative rules below are independently transcribed from the production
# Python source; unlike the Python audit, this file does not AST-extract them.
# Both sides use exact gmp bigq arithmetic. No Arb or transcendental replay.
# Expected result: 285 identities + one rejected sign mutation = 286 PASS.
if (!requireNamespace('gmp', quietly=TRUE) || !requireNamespace('jsonlite', quietly=TRUE))
  stop('Install the R packages gmp and jsonlite before running this audit.')

args <- commandArgs(trailingOnly=TRUE)
arg_value <- function(name) {
  at <- which(args == name)
  if (length(at) != 1L || at + 1L > length(args)) stop(paste('Required option:', name))
  args[at + 1L]
}
repo_root <- arg_value('--repo-root')
output <- arg_value('--output')
source_path <- file.path(repo_root, 'review/dcg-five-points/arb/peabody_arb_concavity.py')
if (!file.exists(source_path)) stop('Production Python source is missing at --repo-root.')

Q <- function(v=0L) gmp::as.bigq(v)
qr <- function(a,b) Q(a)/Q(b)
zero <- Q(0L)
one <- Q(1L)
qsqrt <- function(v) {
  # The fixtures deliberately use rational perfect-square constant terms.
  for (k in 0:3) if (isTRUE(v == Q(k*k))) return(Q(k))
  stop('Fixture requires an unsupported scalar square root.')
}

# Independently transcribed ordinary q-derivative rules.
d3 <- function(v=zero,d1=zero,d2=zero,d3=zero) list(v=v,d1=d1,d2=d2,d3=d3)
dc <- function(v) d3(Q(v))
dadd <- function(a,b) Map(`+`,a,b)
dneg <- function(a) lapply(a,function(v)-v)
dsub <- function(a,b) dadd(a,dneg(b))
dscale <- function(a,c) lapply(a,function(v)v*Q(c))
dmul <- function(a,b) d3(
  a$v*b$v,
  a$d1*b$v+a$v*b$d1,
  a$d2*b$v+Q(2)*a$d1*b$d1+a$v*b$d2,
  a$d3*b$v+Q(3)*a$d2*b$d1+Q(3)*a$d1*b$d2+a$v*b$d3)
dinv <- function(a) d3(
  one/a$v,
  -a$d1/a$v^2L,
  Q(2)*a$d1^2L/a$v^3L-a$d2/a$v^2L,
  -Q(6)*a$d1^3L/a$v^4L+Q(6)*a$d1*a$d2/a$v^3L-a$d3/a$v^2L)
ddiv <- function(a,b) dmul(a,dinv(b))
dpow <- function(a,n) {
  if (n<0L) return(dinv(dpow(a,-n)))
  out <- dc(1L)
  if (n>0L) for (i in seq_len(n)) out <- dmul(out,a)
  out
}
dsqrt <- function(a) {
  r <- qsqrt(a$v)
  d3(r,a$d1/(Q(2)*r),
     a$d2/(Q(2)*r)-a$d1^2L/(Q(4)*r^3L),
     a$d3/(Q(2)*r)-Q(3)*a$d1*a$d2/(Q(4)*r^3L)+Q(3)*a$d1^3L/(Q(8)*r^5L))
}
datan <- function(a,mutate=FALSE) {
  den <- one+a$v^2L
  # Constant atan(a$v) is intentionally excluded from comparison.
  coefficient <- if (mutate) Q(6)*a$v^2L+Q(2) else Q(6)*a$v^2L-Q(2)
  d3(zero,a$d1/den,
     a$d2/den-Q(2)*a$v*a$d1^2L/den^2L,
     a$d3/den-Q(6)*a$v*a$d1*a$d2/den^2L+coefficient*a$d1^3L/den^3L)
}

# Second x derivatives, with the ordinary q-derivative algebra as coefficients.
x2 <- function(v=dc(0L),x=dc(0L),xx=dc(0L)) list(v=v,x=x,xx=xx)
xc <- function(v) x2(dc(v))
xadd <- function(a,b) Map(dadd,a,b)
xneg <- function(a) lapply(a,dneg)
xsub <- function(a,b) xadd(a,xneg(b))
xmul <- function(a,b) x2(
  dmul(a$v,b$v),
  dadd(dmul(a$x,b$v),dmul(a$v,b$x)),
  dadd(dadd(dmul(a$xx,b$v),dscale(dmul(a$x,b$x),2L)),dmul(a$v,b$xx)))
xinv <- function(a) x2(
  dinv(a$v),
  dneg(ddiv(a$x,dpow(a$v,2L))),
  dsub(dscale(ddiv(dpow(a$x,2L),dpow(a$v,3L)),2L),ddiv(a$xx,dpow(a$v,2L))))
xdiv <- function(a,b) xmul(a,xinv(b))
xpow <- function(a,n) {
  if (n<0L) return(xinv(xpow(a,-n)))
  out <- xc(1L)
  if (n>0L) for (i in seq_len(n)) out <- xmul(out,a)
  out
}
xsqrt <- function(a) {
  r <- dsqrt(a$v)
  x2(r,ddiv(a$x,dscale(r,2L)),
     dsub(ddiv(a$xx,dscale(r,2L)),ddiv(dpow(a$x,2L),dscale(dpow(r,3L),4L))))
}
xatan <- function(a) {
  den <- dadd(dc(1L),dpow(a$v,2L))
  x2(datan(a$v),ddiv(a$x,den),
     dsub(ddiv(a$xx,den),dscale(ddiv(dmul(a$v,dpow(a$x,2L)),dpow(den,2L)),2L)))
}

# Independent Taylor algebra: lists store divided derivatives q^i x^j,
# with q order <=3, x order <=2 and positions j*4+i+1.
pos <- function(i,j) j*4L+i+1L
poly <- function(v=zero) {
  if (is.list(v)) return(v)
  out <- rep(list(zero),12L)
  out[[1L]] <- Q(v)
  out
}
padd <- function(a,b) Map(`+`,poly(a),poly(b))
pscale <- function(a,c) lapply(poly(a),function(v)v*c)
pmul <- function(a,b) {
  a<-poly(a);b<-poly(b);out<-poly()
  for (i in 0:3) for (j in 0:2)
    for (k in 0:(3-i)) for (l in 0:(2-j))
      out[[pos(i+k,j+l)]] <- out[[pos(i+k,j+l)]]+a[[pos(i,j)]]*b[[pos(k,l)]]
  out
}
ppow <- function(a,n) {
  out<-poly(one)
  if (n>0L) for (i in seq_len(n)) out<-pmul(out,a)
  out
}
pcompose <- function(a,coefficients) {
  a<-poly(a);z<-padd(a,-a[[1L]]);out<-poly()
  for (n in 0:5) out<-padd(out,pscale(ppow(z,n),coefficients[[n+1L]]))
  out
}
pinv <- function(a) {
  a0<-poly(a)[[1L]]
  pcompose(a,lapply(0:5,function(n)Q((-1L)^n)/a0^(n+1L)))
}
psqrt <- function(a) {
  a0<-poly(a)[[1L]];r<-qsqrt(a0);c<-one;coefficients<-list()
  for (n in 0:5) {
    coefficients[[n+1L]]<-r*c/a0^n
    c<-c*(qr(1L,2L)-Q(n))/Q(n+1L)
  }
  pcompose(a,coefficients)
}
patan <- function(a) {
  a0<-poly(a)[[1L]];den<-one+a0^2L;derivative<-list()
  for (n in 0:4) {
    rhs<-Q(as.integer(n==0L))
    if (n>=1L) rhs<-rhs-Q(2L)*a0*derivative[[n]]
    if (n>=2L) rhs<-rhs-derivative[[n-1L]]
    derivative[[n+1L]]<-rhs/den
  }
  pcompose(a,c(list(zero),lapply(0:4,function(n)derivative[[n+1L]]/Q(n+1L))))
}
to_jet <- function(a) {
  jets<-lapply(0:2,function(j) {
    v<-lapply(0:3,function(i)a[[pos(i,j)]]*Q(factorial(i))*Q(factorial(j)))
    do.call(d3,v)
  })
  do.call(x2,jets)
}
from_jet <- function(a) {
  out<-poly()
  for (j in 0:2) for (i in 0:3)
    out[[pos(i,j)]]<-a[[j+1L]][[i+1L]]/Q(factorial(i)*factorial(j))
  out
}

checks<-list()
for (seed in 1:3) {
  a<-poly();b<-poly()
  for (j in 0:2) for (i in 0:3) {
    a[[pos(i,j)]]<-qr((-1L)^(i+j+seed)*(1L+seed+i+3L*j),7L+seed)
    b[[pos(i,j)]]<-qr((-1L)^(i+seed)*(2L+2L*seed+2L*i+j),5L+seed)
  }
  a[[1L]]<-Q(4L);b[[1L]]<-Q(9L)
  ja<-to_jet(a);jb<-to_jet(b)
  got<-list(add=xadd(ja,jb),subtract=xsub(ja,jb),multiply=xmul(ja,jb),
            reciprocal=xinv(ja),divide=xdiv(ja,jb),sqrt=xsqrt(ja),atan=xatan(ja),cube=xpow(ja,3L))
  want<-list(add=padd(a,b),subtract=padd(a,pscale(b,-one)),multiply=pmul(a,b),
             reciprocal=pinv(a),divide=pmul(a,pinv(b)),sqrt=psqrt(a),atan=patan(a),cube=ppow(a,3L))
  for (label in names(got)) {
    actual<-from_jet(got[[label]])
    for (j in 0:2) for (i in 0:3) {
      if (label=='atan' && i==0L && j==0L) next
      key<-sprintf('%d:%s:q%dx%d',seed,label,i,j)
      checks[[key]]<-isTRUE(actual[[pos(i,j)]]==want[[label]][[pos(i,j)]])
    }
  }
}
mutout<-datan(to_jet(a)$v,mutate=TRUE)
mutation_rejected<-!isTRUE(mutout$d3/Q(6L)==patan(a)[[pos(3L,0L)]])
checks[['negative_control:atan_third_derivative_sign_rejected']]<-mutation_rejected
passed<-all(unlist(checks)) && length(checks)==286L
result<-list(
  classification=if(passed)'PEABODY_INDEPENDENT_R_JET_EXACT_FINITE_AUDIT_PASS' else 'FAIL',
  pass=passed,checks_count=length(checks),failures=names(checks)[!unlist(checks)],
  scope='Three exact rational mixed-jet assignments, independently transcribed rules versus bivariate Taylor coefficients; no fresh Arb replay and no new scalar bounds.',
  source_extraction='R rules are independently transcribed, not extracted from the Python AST.',
  excluded='Arctangent constant and interval-enclosure semantics are not tested.',
  r_runtime_executed=TRUE,
  negative_controls=list(atan_third_derivative_sign_mutation_rejected=mutation_rejected),
  checks=checks)
dir.create(dirname(output),recursive=TRUE,showWarnings=FALSE)
jsonlite::write_json(result,output,pretty=TRUE,auto_unbox=TRUE)
cat(result$classification, result$checks_count, '\n')
if (!passed) stop('Exact finite jet audit failed; inspect the output JSON.')
