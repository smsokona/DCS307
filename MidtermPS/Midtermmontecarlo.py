import random
import matplotlib.pyplot as plt

scores = []

#monte carlo simulation
for i in range(1000):
  #create a test, 12 #'s picked randomly and w/o replacement from a list of 120 #'s
  testquestions = random.sample(range(1,120),12) #returns a list of 12 random #'s
  #generating an answer for each question on the test
  answers = []
  for i in range(12):
    if testquestions[i] <= 90: #first 90 is class I questions 
      probs = [4, 4, 4, 4, 4, 4, 3, 3, 3, 2]
      answers.append(random.sample(probs,1))
    else:
      probs = [3, 2, 2, 2, 2, 1, 1, 1, 1, 0]
      answers.append(random.sample(probs,1))
    #setting score for this test
    score = sum(sum(answers, []))  
      
  #setting score for this test  
  score = sum(sum(answers, [])) #concatenate nested lists to a single list and sum! 
  scores.append(score)
  
  
#histogram  
# Initialize layout
fig, ax = plt.subplots(figsize = (9, 9))

#plot
ax.hist(scores, edgecolor="black")  
   
