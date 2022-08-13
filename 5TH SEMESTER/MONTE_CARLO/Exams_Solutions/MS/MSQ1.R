set.seed(123)
n <- 1000
u <- runif(n,0,1)
indicator <- u<0.8
u[u<=0.8]  <- 0
u[u>0.8]  <- - 0.5 * log(5*(1-u[u>0.8]))
setEPS()
postscript("Q1Q1Hist.eps")
hist(u)
dev.off()
mean(u)
