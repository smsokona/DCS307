# Sokona Mangane
# DCS 307 
# Mon - Jan 30, 2023

#diff() gives the difference between each element in a vector 

# in R, [-1] gives u back the vector with the first element removed, unlike in Python where it gives you the last element


#whats below was copied from an ?ssq example: example to show use of (simple) trace data for arrivals and service times,
# allowing for reuse (recycling) of trace data times

initArrivalTimes <- function() {
  arrivalTimes      <<- c(15, 47, 71, 111, 123, 152, 232, 245)
  interarrivalTimes <<- c(arrivalTimes[1], diff(arrivalTimes))
}

initServiceTimes <- function() {
  serviceTimes      <<- c(43, 36, 34, 30, 38, 30, 31, 29)
}

getInterarr <- function() {
  if (length(interarrivalTimes) == 0)  initArrivalTimes()
  
  nextInterarr <- interarrivalTimes[1]
  interarrivalTimes <<- interarrivalTimes[-1] # remove 1st element globally
  return(nextInterarr)
}

getService <- function() {
  if (length(serviceTimes) == 0)  initServiceTimes()
  
  nextService <- serviceTimes[1]
  serviceTimes <<- serviceTimes[-1]  # remove 1st element globally
  return(nextService)
}


initArrivalTimes()
initServiceTimes()
output <- ssq(maxArrivals = 100, interarrivalFcn = getInterarr,
              serviceFcn = getService, saveAllStats = TRUE)
mean(output$interarrivalTimes)
mean(output$serviceTimes)

# g(x) = (a * x) mod m

g <- function(x) {return( (9*x)%%17 )}
g(9)
g(7)
g(12)


#chose an a of 9 and we get 8 numbers before we start looping again

g <- function(x) {return( (4*x)%%17 )} #here we get 3 before we start looping again
g(4)
 

#what are the PRNG: Psuedo-random number generator does Python offer? Default? What are thier periods? 
# Same question for R
# same question of java

