import markovify
import os
import numpy
import random
import time


input_file = "kjvc.txt"
chain_order = 4 # 4 is the magic number



def get_last_n(lst, n):
    return lst[-n:]


def find_closest_word(bad_word: str, corpus: list[str]):
    
    corpus = list(corpus)
    
    closest_words = []
    
    shortest_dist = 999 # init with high value
    
    for cur_word in corpus:
        cur_dist = levenshteinDistanceDP(bad_word, cur_word)
        
        if cur_dist < shortest_dist:
            closest_words = [] # clear currest best words
            shortest_dist = cur_dist
            closest_words.append(cur_word)
        elif cur_dist == shortest_dist:
            closest_words.append(cur_word)
            
    return random.choice(closest_words)
    
        

def get_user_prompt(corpus: list[str]) -> str:
    dirty_input = input("Enter prompt: ").split(" ")
    
    
    bad_words = []
    for word in dirty_input:
        if word not in corpus:
            bad_words.append(word)

    
    good_words = []
    for word in bad_words:
        good_words.append(find_closest_word(word, corpus))
    
    
    cleaned_input = []
    
    index_in_good = 0
    
    for i in range(len(dirty_input)):
        if dirty_input[i] in bad_words:
            cleaned_input.append(good_words[index_in_good])
            index_in_good += 1
        else:
            cleaned_input.append(dirty_input[i])
    
    print(cleaned_input)
    
    return " ".join(cleaned_input)



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


def inject_prompt(prompt: str, the_bible: str) -> str:
    
    prompt += " amen"
    bible_words = the_bible.split(".")
    index = random.randrange(len(bible_words))
    
    bible_words.insert(index, prompt)
    
    return ". ".join(bible_words)
    
    
# print(inject_prompt("god satan", "sentence sen. sentency sentecner. sentern."))


def main():
    global input_file


    with open(input_file) as f:
        the_bible = f.read().replace("\n", " ",-1)



    corpus = set(the_bible.replace(".","", -1).split(" "))
    # print(corpus)


    while True:
        prompt = get_user_prompt(corpus)
        
        # print("Prompt: " + prompt)
        # time.sleep(2)
        # print(the_bible)
        
        
        text_model = markovify.Text((prompt + " amen. " + the_bible), state_size=chain_order)
        # print("he")
        res = response(text_model, prompt)
        
        cleaned_output = ""
        print(" ".join(res.split(" ")[(chain_order + 10):]))

if __name__ == "__main__":
    main()
    
    