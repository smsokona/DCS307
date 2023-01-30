#Sokona Mangane
#DCS 307, HW 2
#Jan 2023

#loading necessary packages
library("ggplot2")
library("tidyverse")

# Graph 1: a convergence-to-steady-state figure like on that slide, but using your three favorite (different) initial seeds


#seed 1: 1234567
#seed 2 :2499727
#seed 3: 8555324

jobs <- seq(0,5000, by = 100) #based on barrys plot and obs, most sojourn times reach convergence at 6000 jobs
jobs <- jobs[2:51]
output1 <- ssq(seed = 1234567, maxDepartures = 5000, saveSojournTimes = TRUE, showOutput = FALSE, showProgress =  FALSE)
sojourn_times1 <- output1$sojournTimes #saving all my sojourn times in a vector
avg_sojourn_times1 <- c() #creating an empty list to add to for the for loop

#repeating steps above 2x, so each seed has it's on vector sojourn times
output2 <- ssq(seed = 5551212, maxDepartures = 5000, saveSojournTimes = TRUE, showOutput = FALSE, showProgress =  FALSE)
sojourn_times2 <- output2$sojournTimes
avg_sojourn_times2 <- c()

output3 <- ssq(seed = 8675309, maxDepartures = 5000, saveSojournTimes = TRUE, showOutput = FALSE, showProgress =  FALSE)
sojourn_times3 <- output3$sojournTimes
avg_sojourn_times3 <- c()

for (i in jobs) {
  avg = mean(sojourn_times1[1:i])
  avg2 = mean(sojourn_times2[1:i])
  avg3 = mean(sojourn_times3[1:i])
  avg_sojourn_times1 = append(avg_sojourn_times1, avg)
  avg_sojourn_times2 = append(avg_sojourn_times2, avg2)
  avg_sojourn_times3 = append(avg_sojourn_times3, avg3)
}

#creating a dataframe to plot

Jobs <- c(jobs, jobs, jobs)
# Jobs <- Jobs[2:181]
Avg_Sojo_Time <- c(avg_sojourn_times1, avg_sojourn_times2, avg_sojourn_times3)
seeds = c(1234567, 5551212, 8555324)
seed = rep(seeds, each = 50)

ssqexp <- data.frame(Jobs, Avg_Sojo_Time, seed) 

ssqexp %>%
  ggplot(aes(Jobs, Avg_Sojo_Time, color = factor(seed))) +
  geom_point(aes(shape = factor(seed))) +
  # geom_smooth(method = "lm", se = FALSE) +
  labs(x = "Jobs", y = "Average Sojourn") +
  ylim(0,20)



## not converging??

# Graph 2


getSvc1 = function() { rgamma(1, shape = 1.0, scale = 0.9) }


outputg1 <- ssq(seed = 1234567, maxDepartures = 15000, saveSojournTimes = TRUE, showOutput = FALSE, showProgress =  FALSE, getSvc1 = function() { rgamma(1, shape = 1.0, scale = 0.9) })
sojourn_timesg1 <- outputg1$sojournTimes #saving all my sojourn times in a vector
avg_sojourn_timesg1 <- c() #creating an empty list to add to for the for loop

#repeating steps above 2x, so each seed has it's on vector sojurn times
outputg2 <- ssq(seed = 5551212, maxDepartures = 15000, saveSojournTimes = TRUE, showOutput = FALSE, showProgress =  FALSE, getSvc1 = function() { rgamma(1, shape = 1.0, scale = 0.9) })
sojourn_timesg2 <- outputg2$sojournTimes
avg_sojourn_timesg2 <- c()

outputg3 <- ssq(seed = 8555324, maxDepartures = 15000, saveSojournTimes = TRUE, showOutput = FALSE, showProgress =  FALSE, getSvc1 = function() { rgamma(1, shape = 1.0, scale = 0.9) })
sojourn_timesg3 <- outputg3$sojournTimes
avg_sojourn_timesg3 <- c()

for (i in jobs) {
  avgg = mean(sojourn_timesg1[1:i])
  avgg2 = mean(sojourn_timesg2[1:i])
  avgg3 = mean(sojourn_timesg3[1:i])
  avg_sojourn_timesg1 = append(avg_sojourn_timesg1, avgg)
  avg_sojourn_timesg2 = append(avg_sojourn_timesg2, avgg2)
  avg_sojourn_timesg3 = append(avg_sojourn_timesg3, avgg3)
}

#creating a dataframe to plot

Avg_Sojo_Time1 <- c(avg_sojourn_times1, avg_sojourn_times2, avg_sojourn_times3)

ssqexp <- data.frame(Jobs, Avg_Sojo_Time, seed) 

ssqexp %>%
  ggplot(aes(Jobs, Avg_Sojo_Time, color = factor(seed))) +
  geom_point(aes(shape = factor(seed))) +
  # geom_smooth(method = "lm", se = FALSE) +
  labs(x = "Jobs", y = "Average Sojourn") +
  ylim(0,20)


# Graph 3


getSvc2 = function() { rgamma(1, shape = 1.05, scale = 0.9) }

output1 <- ssq(seed = 1234567, maxDepartures = 15000, saveSojournTimes = TRUE, showOutput = FALSE, showProgress =  FALSE)
sojourn_times1 <- output1$sojournTimes #saving all my sojourn times in a vector
avg_sojourn_times1 <- c() #creating an empty list to add to for the for loop

#repeating steps above 2x, so each seed has it's on vector sojurn times
output2 <- ssq(seed = 5551212, maxDepartures = 15000, saveSojournTimes = TRUE, showOutput = FALSE, showProgress =  FALSE)
sojourn_times2 <- output2$sojournTimes
avg_sojourn_times2 <- c()

output3 <- ssq(seed = 8555324, maxDepartures = 15000, saveSojournTimes = TRUE, showOutput = FALSE, showProgress =  FALSE)
sojourn_times3 <- output3$sojournTimes
avg_sojourn_times3 <- c()

for (i in jobs) {
  avg = mean(sojourn_times1[1:i])
  avg2 = mean(sojourn_times2[1:i])
  avg3 = mean(sojourn_times3[1:i])
  avg_sojourn_times1 = append(avg_sojourn_times1, avg)
  avg_sojourn_times2 = append(avg_sojourn_times2, avg2)
  avg_sojourn_times3 = append(avg_sojourn_times3, avg3)
}

#creating a dataframe to plot

Avg_Sojo_Time <- c(avg_sojourn_times1, avg_sojourn_times2, avg_sojourn_times3)


ssqexp <- data.frame(Jobs, Avg_Sojo_Time, seed) 

ssqexp %>%
  ggplot(aes(Jobs, Avg_Sojo_Time, color = factor(seed))) +
  geom_point(aes(shape = factor(seed))) +
  # geom_smooth(method = "lm", se = FALSE) +
  labs(x = "Jobs", y = "Average Sojourn") +
  ylim(0,20)


# Graph 4

getSvc3 = function() { rgamma(1, shape = 1.1, scale = 0.9) }

output1 <- ssq(seed = 1234567, maxDepartures = 15000, saveSojournTimes = TRUE, showOutput = FALSE, showProgress =  FALSE)
sojourn_times1 <- output1$sojournTimes #saving all my sojourn times in a vector
avg_sojourn_times1 <- c() #creating an empty list to add to for the for loop

#repeating steps above 2x, so each seed has it's on vector sojurn times
output2 <- ssq(seed = 5551212, maxDepartures = 15000, saveSojournTimes = TRUE, showOutput = FALSE, showProgress =  FALSE)
sojourn_times2 <- output2$sojournTimes
avg_sojourn_times2 <- c()

output3 <- ssq(seed = 8555324, maxDepartures = 15000, saveSojournTimes = TRUE, showOutput = FALSE, showProgress =  FALSE)
sojourn_times3 <- output3$sojournTimes
avg_sojourn_times3 <- c()

for (i in jobs) {
  avg = mean(sojourn_times1[1:i])
  avg2 = mean(sojourn_times2[1:i])
  avg3 = mean(sojourn_times3[1:i])
  avg_sojourn_times1 = append(avg_sojourn_times1, avg)
  avg_sojourn_times2 = append(avg_sojourn_times2, avg2)
  avg_sojourn_times3 = append(avg_sojourn_times3, avg3)
}

#creating a dataframe to plot

Avg_Sojo_Time <- c(avg_sojourn_times1, avg_sojourn_times2, avg_sojourn_times3)

ssqexp <- data.frame(Jobs, Avg_Sojo_Time, seed) 

ssqexp %>%
  ggplot(aes(Jobs, Avg_Sojo_Time, color = factor(seed))) +
  geom_point(aes(shape = factor(seed))) +
  # geom_smooth(method = "lm", se = FALSE) +
  labs(x = "Jobs", y = "Average Sojourn") +
  ylim(0,20)

