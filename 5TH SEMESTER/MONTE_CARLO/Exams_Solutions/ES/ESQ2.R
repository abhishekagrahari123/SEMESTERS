rm(list=ls())

N=10^4
set.seed(111)

# This is for Part (a)
z <- rnorm(N, mean=0, sd=1)
est1 <- mean(z>4)
est1
se1 <- sd(z>4)/sqrt(N)
se1
ci1 <- rep(0,2)
ci1[1] <- max(0,est1 - qnorm(0.005,mean=0,sd=1,lower.tail=FALSE)*se1)
ci1[2] <- est1 + qnorm(0.005,mean=0,sd=1,lower.tail=FALSE)*se1
ci1

# This is for Part (b)
mu=5
sig=3
z <- rnorm(N, mean=5, sd=3)
indx <- which(z>4)
z[indx]  <- dnorm(z[indx], mean=0, sd=1)/dnorm(z[indx], mean=mu, sd=sig)
z[-indx] <- 0
est2 <- mean(z)
est2
se2 <- sd(z)/sqrt(N)
se2
ci2 <- rep(0,2)
ci2[1] <- max(0,est2 - qnorm(0.005,mean=0,sd=1,lower.tail=FALSE)*se2)
ci2[2] <- est2 + qnorm(0.005,mean=0,sd=1,lower.tail=FALSE)*se2
ci2
