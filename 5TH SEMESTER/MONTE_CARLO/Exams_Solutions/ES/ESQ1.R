rm(list=ls())

library(tidyr)
library(ggplot2)

nopath=10
N=5000
set.seed(123)

w <- matrix(0,nrow=N+1, ncol=nopath+1)
w[,1] <- seq(from=0, to=1, by=1/5000) 

for (j in 2:(nopath+1)) {
   z <- rnorm(N,0,1)
   for (i in 2:(N+1)) {
      w[i,j] <- w[i-1,j] + z[i-1]/sqrt(N)
   }
}

w <- data.frame(w)
colnames(w) <- c("time", "BM1", "BM2", "BM3", "BM4", "BM5", "BM6", "BM7", "BM8", "BM9", "BM10")

g <- w %>% gather("id", "value", 2:11) %>% 
   ggplot(., aes(time, value))+
   geom_line(aes(color=factor(id)))

ggsave(g, file="ESQ1BM.eps", device="eps")
