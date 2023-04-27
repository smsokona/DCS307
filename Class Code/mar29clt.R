#central limit thereom visualization - for final portfolio

clt <- function(n, numSamples, sh) {
  samples <- rep(0, numSamples)
  for (i in 1:numSamples) {
    xbar <- mean( rgamma(n, shape = sh) )
    samples[i] <- xbar
  }
  return(samples)
}

par(mfrow = c(2,1))

n <- 9
sh <- 2.0
sigma <- 2.0
hist(clt(n, 10000, sh), freq = FALSE, xlim = c(0,5))
curve(dnorm(x, sh, 1/2), add = TRUE)

n <- 36
hist(clt(n, 10000, sh), freq = FALSE, xlim = c(0,5))
curve(dnorm(x, sh, 1/4), add = TRUE)