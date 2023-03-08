set.seed(8765309)
rexp(5, rate = 1) #uses a fast numerical approximation

set.seed(8765309)
vexp(5, rate = 1)#uses inversion, so it won't print the same numbers even tho we use the same seed


#the code below however prints the same numbers 
runif(5, 3.1, 7.6)

vunif(5, 3.1,7.6)

#ssq is event driven, how change things across time...
set.seed(8765309)

#streams allow us to divide it, isolate
#no notion of streams in the "r" functions, only for the "v" ones
vexp(1, rate = 1, stream = 1) #interarrival
vexp(1, rate = 10/9, stream = 2) #service
vexp(1, rate = 1, stream = 1)#interarrival
vexp(1, rate = 10/9, stream = 2)#service
vexp(1, rate = 1, stream = 1)#interarrival
vexp(1, rate = 10/9, stream = 2)#service


set.seed(8765309)
#different order
vexp(1, rate = 1, stream = 1) #interarrival
vexp(1, rate = 10/9, stream = 2) #service
vexp(1, rate = 1, stream = 1)#interarrival
vexp(1, rate = 1, stream = 1) #interarrival, we see a different number comapred to above
vexp(1, rate = 1, stream = 1) #interarrival
vexp(1, rate = 1, stream = 1) #interarrival
vexp(1, rate = 1, stream = 1) #interarrival
vexp(1, rate = 10/9, stream = 2) #service







