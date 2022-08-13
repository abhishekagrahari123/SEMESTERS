rm(list=ls())

set.seed(123)
N=10^4

y <- cbind(runif(N, 0, 1), runif(N, 0, 1))
y <- apply(y, 1, function(x){ return(-2*log(x[1]*x[2])/3)})
y <- log(1+y)/y
est <- mean(y)
evar <- var(y)/N
est
evar
