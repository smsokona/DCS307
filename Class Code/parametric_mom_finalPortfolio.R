ouput <- ssq(numJobs + warmup, seeds[i], showOutput = FALSE, saveServiceTimes = TRUE)

svc <- output$sojournTimes
  
acf(svc) #check for autocorrelation

#based on math we did for MOM's, k = mean^2/s^2 and theta = s^2/mean
k_hat = mean(svc)^2 / var(svc)
theta_hat = var(svc) / mean(svc)
print(paste("MOM parameter estimates when fitting gamma (k,theta):", 
            k_hat, theta_hat))

plot.stepfun(ecdf(svc), pch = "", main = "gamma fit to servicetimes")
curve(pgamma(x, shape = k_hat, scale = theta_hat), col = "red", 
      lwd = 2, add = TRUE)

mu_hat = mean(svc)
print(paste("MOM parameter estimate when fitting exponential:", mu_hat))

plot.stepfun(ecdf(svc), pch = "", main = "exponential fit to servicetimes")
curve(pexp(x, rate = 1/mu_hat), col = "red", lwd = 2, add = TRUE)