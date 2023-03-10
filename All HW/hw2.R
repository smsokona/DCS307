#Sokona Mangane
#DCS 307, HW 2
#Jan 2023

#loading necessary packages
#install.packages("simEd")
library(simEd)
library("ggplot2")
library("tidyverse")

# Graph 1: a convergence-to-steady-state figure like on that slide, but using your three favorite (different) initial seeds


#seed 1: 1234567
#seed 2: 0852384
#seed 3: 2942502

jobs <- seq(0,5000, by = 100) #based on barrys plot and obs, most sojourn times reach convergence at 6000 jobs
jobs <- jobs[2:51]
output1 <- ssq(seed = 1234567, maxDepartures = 5000, saveSojournTimes = TRUE, showOutput = FALSE, showProgress =  FALSE)
sojourn_times1 <- output1$sojournTimes #saving all my sojourn times in a vector
avg_sojourn_times1 <- c() #creating an empty list to add to for the for loop

#repeating steps above 2x, so each seed has it's on vector sojourn times
output2 <- ssq(seed = 0852384, maxDepartures = 5000, saveSojournTimes = TRUE, showOutput = FALSE, showProgress =  FALSE)
sojourn_times2 <- output2$sojournTimes
avg_sojourn_times2 <- c()

output3 <- ssq(seed = 2942502, maxDepartures = 5000, saveSojournTimes = TRUE, showOutput = FALSE, showProgress =  FALSE)
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
seeds = c(1234567, 0852384, 2942502)
seed = rep(seeds, each = 50)

ssqexp <- data.frame(Jobs, Avg_Sojo_Time, seed) 

ssqexp %>%
  ggplot(aes(Jobs, Avg_Sojo_Time, color = factor(seed))) +
  geom_point(aes(shape = factor(seed))) +
  # geom_smooth(method = "lm", se = FALSE) +
  labs(x = "Jobs", y = "Average Sojourn", title = "Convergence to Steady-State") +
  ylim(0,20)



## not converging??

# Graph 2


getSvc1 = function() { rgamma(1, shape = 1.0, scale = 0.9) }


outputg1 <- ssq(seed = 1234567, maxDepartures = 5000, saveSojournTimes = TRUE, showOutput = FALSE, showProgress =  FALSE,  serviceFcn = getSvc1)
sojourn_timesg1 <- outputg1$sojournTimes #saving all my sojourn times in a vector
avg_sojourn_timesg1 <- c() #creating an empty list to add to for the for loop

#repeating steps above 2x, so each seed has it's on vector sojurn times
outputg2 <- ssq(seed = 0852384, maxDepartures = 5000, saveSojournTimes = TRUE, showOutput = FALSE, showProgress =  FALSE,  serviceFcn = getSvc1)
sojourn_timesg2 <- outputg2$sojournTimes
avg_sojourn_timesg2 <- c()

outputg3 <- ssq(seed = 2942502, maxDepartures = 5000, saveSojournTimes = TRUE, showOutput = FALSE, showProgress =  FALSE,  serviceFcn = getSvc1)
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

Avg_Sojo_Time1 <- c(avg_sojourn_timesg1, avg_sojourn_timesg2, avg_sojourn_timesg3)

ssqexp1 <- data.frame(Jobs, Avg_Sojo_Time1, seed) 

ssqexp1 %>%
  ggplot(aes(Jobs, Avg_Sojo_Time1, color = factor(seed))) +
  geom_point(aes(shape = factor(seed))) +
  # geom_smooth(method = "lm", se = FALSE) +
  labs(x = "Jobs", y = "Average Sojourn", title = "Convergence to Steady-State: 1st Gamma Process", color = "Intial Seed") +
  ylim(0,20)


# Graph 3


getSvc2 = function() { rgamma(1, shape = 1.05, scale = 0.9) }

outputgg1 <- ssq(seed = 1234567, maxDepartures = 5000, saveSojournTimes = TRUE, showOutput = FALSE, showProgress =  FALSE, serviceFcn = getSvc2)
sojourn_timesgg1 <- outputgg1$sojournTimes #saving all my sojourn times in a vector
avg_sojourn_timesgg1 <- c() #creating an empty list to add to for the for loop

#repeating steps above 2x, so each seed has it's on vector sojurn times
outputgg2 <- ssq(seed = 0852384, maxDepartures = 5000, saveSojournTimes = TRUE, showOutput = FALSE, showProgress =  FALSE, serviceFcn = getSvc2)
sojourn_timesgg2 <- outputgg2$sojournTimes
avg_sojourn_timesgg2 <- c()

outputgg3 <- ssq(seed = 2942502, maxDepartures = 5000, saveSojournTimes = TRUE, showOutput = FALSE, showProgress =  FALSE, serviceFcn = getSvc2)
sojourn_timesgg3 <- outputgg3$sojournTimes
avg_sojourn_timesgg3 <- c()

for (i in jobs) {
  avggg = mean(sojourn_timesgg1[1:i])
  avggg2 = mean(sojourn_timesgg2[1:i])
  avggg3 = mean(sojourn_timesgg3[1:i])
  avg_sojourn_timesgg1 = append(avg_sojourn_timesgg1, avggg)
  avg_sojourn_timesgg2 = append(avg_sojourn_timesgg2, avggg2)
  avg_sojourn_timesgg3 = append(avg_sojourn_timesgg3, avggg3)
}

#creating a dataframe to plot

Avg_Sojo_Time2 <- c(avg_sojourn_timesgg1, avg_sojourn_timesgg2, avg_sojourn_timesgg3)


ssqexp2 <- data.frame(Jobs, Avg_Sojo_Time2, seed) 

ssqexp2 %>%
  ggplot(aes(Jobs, Avg_Sojo_Time2, color = factor(seed))) +
  geom_point(aes(shape = factor(seed))) +
  # geom_smooth(method = "lm", se = FALSE) +
  labs(x = "Jobs", y = "Average Sojourn", title = "Convergence to Steady-State: 2nd Gamma Process", color = "Intial Seed") +
  ylim(0,20)


# Graph 4, look at more departures, since graph doesn't seem to converge at 5000!

getSvc3 = function() { rgamma(1, shape = 1.1, scale = 0.9) }



outputggg1 <- ssq(seed = 1234567, maxDepartures = 5000, saveSojournTimes = TRUE, showOutput = FALSE, showProgress =  FALSE, serviceFcn = getSvc3)
sojourn_timesggg1 <- outputggg1$sojournTimes #saving all my sojourn times in a vector
avg_sojourn_timesggg1 <- c() #creating an empty list to add to for the for loop

#repeating steps above 2x, so each seed has it's on vector sojurn times
outputggg2 <- ssq(seed = 0852384, maxDepartures = 5000, saveSojournTimes = TRUE, showOutput = FALSE, showProgress =  FALSE, serviceFcn = getSvc3)
sojourn_timesggg2 <- outputggg2$sojournTimes
avg_sojourn_timesggg2 <- c()

outputggg3 <- ssq(seed = 2942502, maxDepartures = 5000, saveSojournTimes = TRUE, showOutput = FALSE, showProgress =  FALSE, serviceFcn = getSvc3)
sojourn_timesggg3 <- outputggg3$sojournTimes
avg_sojourn_timesggg3 <- c()

for (i in jobs1) {
  avgggg = mean(sojourn_timesggg1[1:i])
  avgggg2 = mean(sojourn_timesggg2[1:i])
  avgggg3 = mean(sojourn_timesggg3[1:i])
  avg_sojourn_timesggg1 = append(avg_sojourn_timesggg1, avgggg)
  avg_sojourn_timesggg2 = append(avg_sojourn_timesggg2, avgggg2)
  avg_sojourn_timesggg3 = append(avg_sojourn_timesggg3, avgggg3)
}

#creating a dataframe to plot

Avg_Sojo_Time3 <- c(avg_sojourn_timesggg1, avg_sojourn_timesggg2, avg_sojourn_timesggg3)

ssqexp3 <- data.frame(Jobs, Avg_Sojo_Time3, seed) 

ssqexp3 %>%
  ggplot(aes(Jobs, Avg_Sojo_Time3, color = factor(seed))) +
  geom_point(aes(shape = factor(seed))) +
  # geom_smooth(method = "lm", se = FALSE) +
  labs(x = "Jobs", y = "Average Sojourn", title = "Convergence to Steady-State: 3rd Gamma Process", color = "Intial Seed")


