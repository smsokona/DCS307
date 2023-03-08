#Sokona Mangane
#Wednesday - 1/25/22

#Demo of Barry creating a histrogram in R and then creating a PDF 

png("hist.png") #anything that you plot will be saved under this name as a png
values <- rnorm(1000,0,1) #randomly generates 1000 obs with a mean of 0 and sd of 1 (normal distribution)
hist(values)
abline(v = mean(values), lwd = 2, col = "blue")
dev.off() #turns the png device off


#simulation

library(simEd)
#single server quence simulation from the simED package
output <- ssq(maxTime = 100, showOutput = FALSE, showProgress = FALSE, saveAllStats = TRUE) #a "list" class, can type output$ to printout a specific result
waits <- output$waitTimes #a "numeric" class
length(waits)
mean(output$avgWait)
meanTPS(output$serverStatusT,output$serverStatusN) #must use this mean fucntion because it's a time persistent statistic



#stats 


values = rexp(1000, rate = 10/9) #randomly generates 1000 obs at a rate (exponential distribution)
hist(values, breaks = "fd", freq = FALSE) #making freq = FALSE gives us the probability densities instead of the frequencny
curve(dexp(x,rate = 10/9), add = TRUE, col = "red") #adds a curve of the density fucntion of the rate we used above, lines up almost perfectly since we outputted the densities 


set.seed(8675309) #to get the same numbers
rnorm(10)


values = rgamma(1000, shape = 2, scale = 0.9) 
hist(values, freq = FALSE, breaks = "fd") 

getService <- function() {
  return(rgamma(1, shape = 2, scale = 0.9))
}


ssq(maxArrivals = 1000, showOutput = FALSE, serviceFcn = getService())$avgWait 
ssq(maxArrivals = 1000, showOutput = FALSE, serviceFcn = NA)$avgWait 



