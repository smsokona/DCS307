rollDie <- function() {
  die <- sample(1:6, 1)
  return(die)
}

oneEstimate <- function(num_rolls = 10000) {
  # this function returns the estimate of a sum of 7
  # when rolling two fair dice
  count <- 0
  for (i in 1:num_rolls) {
    if (rollDie() + rollDie() == 7) {
      count <- count + 1
    }
  }
  return(count / num_rolls)
}

getEstimates <- function(num_estimates = 1000, num_rolls = 100)
{
  # this function creates a vector of size num_estimates and fills
  # that vector with estimates of rolling a sum of seven using
  # num_rolls rolls per computed estimate
  estimates <- rep(0, num_estimates)
  for (i in 1:num_estimates) {
    estimates[i] <- oneEstimate(num_rolls)
  }
  return(estimates)
}

oneHistogram <- function(num_rolls = 1000)
{
  all_estimates <- getEstimates(1000, num_rolls)
  hist(all_estimates, xlim = c(0.05, 0.3))
  m <- mean(all_estimates)
  abline(v = m, col = "blue", lwd = 2)
  s <- sd(all_estimates)
  abline(v = c(m - 2*s, m + 2*s), col = "red", lwd = 2, lty = "dashed") 
}


#par(mfrow = c(1,3)) # display 1 row, 3 columns
par(mfrow = c(3,1)) # display 3 rows, 1 column

oneHistogram(100)
oneHistogram(500)
oneHistogram(1000)

