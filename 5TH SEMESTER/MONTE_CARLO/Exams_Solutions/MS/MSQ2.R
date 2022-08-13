set.seed(123)
n <- 1000
mydata <- matrix(0,ncol=2,nrow=n)

for (i in 1:n) {
   u <- runif(2,0,1)
   R <- sqrt(-2*log(u[1]))
   theta <- 2*pi*u[2]
   mydata[i,1] <- R*cos(theta)
   mydata[i,2] <- R*sin(theta)
   mydata[i,2] <- 1 + 2*mydata[i,1] + 2*mydata[i,2]
}

means <- apply(mydata,2,mean)
vars <- apply(mydata,2,var)
corr <- cor(mydata[,1],mydata[,2])
means
vars
corr
