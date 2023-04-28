library(simEd)
arr = tylersGrill$arrivalTimes

alg933 <- function(k = 1, times = NULL, S)
{
  arrivals = NULL
  
  # n should not count t_(0) nor t_(n+1)
  n <- length(times)
  
  times <- c(0, times, S)
  
  i <- 1
  e <- rexp(1)
  while (e <= n / k)
  {
    m <- floor((n+1) * k * e/n)
    
    # don't let R's indexing fool you -- the m computed above is relative
    # to C/Java/Python-style indexing starting at 0 -- so m=0 really should
    # be indexing into times[1]...
    
    t <- times[m+1] + (times[m+1+1] - times[m+1]) * (((n+1) * k * e/n) - m)
    arrivals <- c(arrivals, t)
    i <- i + 1
    e <- e + rexp(1)
  }
  
  return(arrivals)
}

# plot the trace of arrivals...
plot(NA, NA, 
     xlab = "time", ylab = "# arrivals", las = 1, main = "Arrival Process",
     xaxt = "n", bty = "n", xlim = c(0,17.5)*3600, ylim = c(0,1500) )
labels = c("07:30","09:00","10:30","12:00","13:30","15:00","16:30","18:00","19:30","21:00")
axis(1, at = c(seq(0, 14.5, by = 1.5)*3600), labels = labels, lwd.ticks = 1, lwd = 0)
axis(1, at = c(0, 14.5)*3600, labels = FALSE, lwd = 1, lwd.ticks = 0)

# plot the empirical CERF for the arrivals data
points(arr, 1:length(arr), type = "l", col = "black", lwd = 2)

# ...with five realizations superimposed
colors <- c("gray","red","blue","darkgreen","purple")
for (i in 1:length(colors))
{
  events = alg933(k = 1, times = arr, S = 14.5*3600)
  points(events, 1:length(events), type="l", col = colors[i])
}
