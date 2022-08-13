set.seed(123)
n <- 1000
mydata <- rep(0,n)

counter <- 0
for (i in 1:n) {
   repeat{
      counter <- counter + 1
      u <- runif(2,0,1)
      u[1] <- sqrt(3.2)*tan(pi*(u[1]-0.5))
      if (u[2] <= (1+(u[1]^2)/3.2)^(-1.1)) {
         mydata[i] <- u[1]
         break
      }
   }
}

AccProp <- n/counter
AccProp
