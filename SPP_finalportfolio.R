events = runif(500, 0, 250) #event times generated at random
events = sort(events) #sort them in order
interevents = diff(events) #get interevent times, there differences
hist(interevents, breaks = "fd", freq = FALSE) #how interevents are distributed
interarrivals_avg = mean(interevents) #shows that the average interevent time is ~1/2 (0.4989109), can use this to superimose
curve(dexp(x, rate = 1/interarrivals_avg), col = "red", add = TRUE) #superimposing the PDF of the exponential
