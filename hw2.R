#Sokona Mangane
#DCS 307, HW 2
#Jan 2023

#loading necessary packages
library("ggplot2")
library("tidyverse")


#seed 1: 1234567
#seed 2 :2499727
#seed 3: 8555324

jobs <- seq(0,10000, by = 100) #based on barrys plot and obs, most sojourn times reach convergence at 6000 jobs
jobs <- jobs[2:101]
output1 <- ssq(seed = 1234567, maxDepartures = 10000, saveSojournTimes = TRUE, showOutput = FALSE, showProgress =  FALSE)
sojourn_times1 <- output1$sojournTimes #saving all my sojourn times in a vector
avg_sojourn_times1 <- c() #creating an empty list to add to for the for loop

#repeating steps above 2x, so each seed has it's on vector sojurn times
output2 <- ssq(seed = 2499727, maxDepartures = 10000, saveSojournTimes = TRUE, showOutput = FALSE, showProgress =  FALSE)
sojourn_times2 <- output2$sojournTimes
avg_sojourn_times2 <- c()

output3 <- ssq(seed = 8555324, maxDepartures = 10000, saveSojournTimes = TRUE, showOutput = FALSE, showProgress =  FALSE)
sojourn_times3 <- output3$sojournTimes
avg_sojourn_times3 <- c()

for (i in jobs) {
  avg = mean(sojourn_times1[2:i])
  avg2 = mean(sojourn_times2[2:i])
  avg3 = mean(sojourn_times3[2:i])
  avg_sojourn_times1 = append(avg_sojourn_times1, avg)
  avg_sojourn_times2 = append(avg_sojourn_times2, avg2)
  avg_sojourn_times3 = append(avg_sojourn_times3, avg3)
}

#creating a dataframe to plot

Jobs <- c(jobs, jobs, jobs)
# Jobs <- Jobs[2:181]
Avg_Sojo_Time <- c(avg_sojourn_times1, avg_sojourn_times2, avg_sojourn_times3)
seeds = c(1234567, 2499727, 8555324)
seed = rep(seeds, each = 100)

ssqexp <- data.frame(Jobs, Avg_Sojo_Time, seed) 

ssqexp %>%
  ggplot(aes(Jobs, Avg_Sojo_Time, color = factor(seed))) +
  geom_point(aes(shape = factor(seed))) +
  # geom_smooth(method = "lm", se = FALSE) +
  labs(x = "Jobs", y = "Average Sojourn")
