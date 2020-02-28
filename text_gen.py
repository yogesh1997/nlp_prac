from collections import defaultdict
import random

text = 'A Markov chain is a stochastic process, but it differs from a general stochastic process in that a Markov chain must be "memory-less." That is, (the probability of) future actions are not dependent upon the steps that led up to the present state. This is called the Markov property. While the theory of Markov chains is important precisely because so many "everyday" processes satisfy the Markov property, there are many common examples of stochastic properties that do not satisfy the Markov property.'


def markovchain(text):
  '''input is string of text and output will be a key value pair'''
  words = text.split(' ')
  
  #initialize default dictionary
  worddict = defaultdict(list)

  for current_word, next_word in zip(words[0:-1],words[1:]):
    worddict[current_word].append(next_word)

  wdict = dict(worddict)
  return wdict

def generate_sent(chain,count=10):

  wrd = random.choice(list(chain.keys()))
  sent = wrd.capitalize()

  for i in range(count-1):
    wrd1 = random.choice(chain[wrd])
    wrd = wrd1
    sent+=' '+wrd1

  return(sent)

d = markovchain(text)
generated_sent = generate_sent(d)
print(generated_sent)

