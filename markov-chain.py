import markovify
import os
import numpy

input_file = "kjvc.txt"



def get_last_n(lst, n):
    return lst[-n:]

def userPrompt(corpus: list[str]) -> str:
    dirty_input = input("Enter prompt: ")
    
    
    bad_words = []
    for word in dirty_input:
        if bad_words not in corpus:
            bad_words.append(word)


    good_words = []
    for word in bad_words:
        good_words.append(findClosestWord(word))
    
    
    for i in enumerate(good_words):
        dirty_input = dirty_input.replace(bad_words[i], good_words[i])

    return dirty_input


def response(model: markovify.Text, prompt: str):
    global chain_order
    
    usable_words = get_last_n(prompt.split(" "), chain_order)
    
    real_prompt = " ".join(usable_words)
    
    if len(real_prompt) > 0:
        return model.make_sentence_with_start(real_prompt, strict=False)    
    else:
        return "Prompt too short :("

    
    
    
    
def levenshteinDistanceDP(token1, token2):
    distances = numpy.zeros((len(token1) + 1, len(token2) + 1))

    for t1 in range(len(token1) + 1):
        distances[t1][0] = t1

    for t2 in range(len(token2) + 1):
        distances[0][t2] = t2
        
    a = 0
    b = 0
    c = 0
    
    for t1 in range(1, len(token1) + 1):
        for t2 in range(1, len(token2) + 1):
            if (token1[t1-1] == token2[t2-1]):
                distances[t1][t2] = distances[t1 - 1][t2 - 1]
            else:
                a = distances[t1][t2 - 1]
                b = distances[t1 - 1][t2]
                c = distances[t1 - 1][t2 - 1]
                
                if (a <= b and a <= c):
                    distances[t1][t2] = a + 1
                elif (b <= a and b <= c):
                    distances[t1][t2] = b + 1
                else:
                    distances[t1][t2] = c + 1

    return distances[len(token1)][len(token2)]



def main():
    global input_file

    chain_order = 2

    with open(input_file) as f:
        the_bible = f.read().replace("\n", " ",-1).replace("—", "", -1).replace("!","",-1).replace(")","",-1).replace("(","",-1).replace("?","",-1).lower()


    text_model = markovify.Text(the_bible, state_size=chain_order)

    corpus = set(the_bible.replace(".","", -1).split(" "))
    print(corpus)


    while True:
        prompt = userPrompt()
        res = response(text_model, prompt)
        print(res)

if __name__ == "__main__":
    main()
    
    