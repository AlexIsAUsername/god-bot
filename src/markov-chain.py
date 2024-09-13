from gtts import gTTS
import markovify
import vlc
import numpy
import random
import time
import sys

from logger import Logger, LoggerConfig
from conf import load_config, Config

conf: Config = load_config(None if len(sys.argv) == 1 else sys.argv[1])

logger_mode = None
if conf.get("debug_mode"):
    logger_mode = LoggerConfig.DEBUG
else:
    logger_mode = LoggerConfig.NONE


logger = Logger(logger_mode)


input_file = conf.get("source_text")
chain_order = conf.get("chain_order")  # 4 is the magic number

def permutations(elements):
    """permutations function taken from https://stackoverflow.com/a/104436

    Args:
        elements (_type_): _description_

    Yields:
        _type_: _description_
    """
    if len(elements) <= 1:
        yield elements
        return
    for perm in permutations(elements[1:]):
        for i in range(len(elements)):
            # nb elements[0:1] works in both string and list contexts
            yield perm[:i] + elements[0:1] + perm[i:]


def levenshteinDistanceDP(token1, token2):
    """levenshtein distance function taken from https://blog.paperspace.com/implementing-levenshtein-distance-word-autocomplete-autocorrect/

    Args:
        token1 (_type_): _description_
        token2 (_type_): _description_

    Returns:
        _type_: _description_
    """
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
            if token1[t1 - 1] == token2[t2 - 1]:
                distances[t1][t2] = distances[t1 - 1][t2 - 1]
            else:
                a = distances[t1][t2 - 1]
                b = distances[t1 - 1][t2]
                c = distances[t1 - 1][t2 - 1]

                if a <= b and a <= c:
                    distances[t1][t2] = a + 1
                elif b <= a and b <= c:
                    distances[t1][t2] = b + 1
                else:
                    distances[t1][t2] = c + 1

    return distances[len(token1)][len(token2)]


def get_user_prompt(the_bible: str) -> str:
    """gets user input and cleans it by removing punctuation, 
    converting the input to words in the_bible (uses find_closest_word), 
    and the longest contiguous string of those words in the_bible (uses find_prompt_chain)

    Args:
        the_bible (str): text that will turn into the markov chain, preprocessed by kjv-clean.py

    Returns:
        str: fully cleaned initial state for markovify
    """
    # makes a set of all the words in the_bible
    set_corpus = set(the_bible.replace(".", "", -1).split(" "))
    full_dirty_input = input("Enter prompt: ")
    
    if full_dirty_input.lower() == "exit":
        sys.exit(0)

    punc = ["[", "]", ":", ",", ";", "’", "—", "!", "(", ")", "?"]
    # strips the input of punctuation
    for mark in punc:
        full_dirty_input = full_dirty_input.replace(mark, "", -1)
    full_dirty_input = full_dirty_input.strip().split(" ")
    
    dirty_input = []

    # keeps only the last chain_order number of words from the input
    if len(full_dirty_input) > chain_order:
        dirty_input = full_dirty_input[len(full_dirty_input) - chain_order :]
    else:
        dirty_input = full_dirty_input

    bad_words = []
    
    # tracks all words that are not in the_bible
    for word in dirty_input:
        if word not in set_corpus:
            bad_words.append(word)

    good_words = []
    
    # tracks all the closest replacement words for bad_words from the words in the_bible
    for word in bad_words:
        good_words.append(find_closest_word(word, set_corpus))# levenshtein Distance search the closest words in the bible

    cleaned_input = []
    index_in_good = 0

    # replace all bad words with good words and store in cleaned_input
    for i in range(len(dirty_input)):
        if dirty_input[i] in bad_words:
            cleaned_input.append(good_words[index_in_good])
            index_in_good += 1
        else:
            cleaned_input.append(dirty_input[i])

    # returns longest chain of fully cleaned input
    logger.debug("Cleaned input: ", cleaned_input)
    temp = find_prompt_chain(the_bible.split(" "), cleaned_input) # finds longest chain of cleaned_input
    logger.debug("Final prompt: ", temp)
    return " ".join(temp)


def find_closest_word(bad_word: str, corpus: list[str]) -> str:
    """uses levenshteinDistanceDP to find the most similar word in the corpus for a given bad_word

    Args:
        bad_word (str): word not in corpus
        corpus (list[str]): list of valid words

    Returns:
        str: valid word most similar to bad_word
    """
    corpus = list(corpus)

    closest_words = []

    shortest_dist = 999  # init with high value

    # loop to check how similar each valid word is to the bad_word
    for cur_word in corpus:
        cur_dist = levenshteinDistanceDP(bad_word, cur_word)

        if cur_dist < shortest_dist:
            closest_words = []  # clear currest best words
            shortest_dist = cur_dist
            closest_words.append(cur_word)
        elif cur_dist == shortest_dist:
            closest_words.append(cur_word)

    return random.choice(closest_words)


def find_prompt_chain(corpus: list[str], cleaned_input: list[str])-> list[str]:
    """permutes the list of cleaned_input to find the longest contiguous chain 
    that appears in corpus with a preference for the original cleaned_input

    Args:
        corpus (list[str]): the starting text
        cleaned_input (list[str]): chain of words that exist in corpus

    Returns:
        list[str]: longest contiguous chain of cleaned_input words
    """
    final_prompt = temp_prompt = []
    permutated_input_list = list(permutations(cleaned_input))
    for permutated_input in permutated_input_list:
        temp_prompt = convolve_lists(corpus, permutated_input)
        if len(temp_prompt) > len(final_prompt):
            final_prompt = temp_prompt
            if len(final_prompt) == len(cleaned_input):
                return final_prompt
    return final_prompt
    # return convolve_lists(corpus, cleaned_input)


def convolve_lists(corpus: list[str], cleaned_input: list[str]) ->list[str]:
    """performs convolution on corpus and cleaned_input to determine the 
    longest contiguous chain of cleaned_input that appears in corpus

    Args:
        corpus (list[str]): starting text
        cleaned_input (list[str]): list of words that appear in corpus

    Returns:
        list[str]: longest chain of cleaned_input in corpus
    """
    reversed_input = []
    max = count = 0
    for i in range(len(cleaned_input) - 1, -1, -1):
        reversed_input.append(cleaned_input[i])  # deep copy reverse input
    for i in range(len(corpus) - 1, -1, -1):
        if reversed_input[count] == corpus[i]:
            count += 1
            if count > max:
                max = count
                if max == len(cleaned_input):
                    return cleaned_input
        else:
            count = 0

    return cleaned_input[len(cleaned_input) - max :]


def response(model: markovify.Text, prompt: str) -> str:
    """generate the the response from the markov chain

    Args:
        model (markovify.Text): markov chain
        prompt (str): initial state of the markov chain

    Returns:
        str: response from the markov chain
    """

    if len(prompt) > 0:
        temp = tuple(prompt.split(" "))
        logger.debug("Initial state: ", temp)
        return model.make_sentence(init_state=temp)
        # return model.make_sentence_with_start(real_prompt, strict=False)
    else:
        return "Prompt too short :("


def printer(text: str) -> None:
    """prints each character of the markov chain response

    Args:
        text (str): markov chain response
    """
    for char in text:
        print(char, end="", flush=True)
        time.sleep(0.05)
    print()  # newline


def run_god_bot():    
    
    with open(input_file) as f:
        the_bible = f.read().replace("\n", " ", -1)

    curr_state_size = 0
    prompt = ""
    while True:
        prompt = get_user_prompt(the_bible)

        # determine the next state size and only recompute markov chain if its different
        next_state_size = min(chain_order, len(prompt.split(" ")))
        if(curr_state_size != next_state_size):
            text_model = markovify.Text(
                the_bible,
                state_size=next_state_size,
            )
            curr_state_size = next_state_size

        res = response(text_model, prompt)
        gTTS(text=res, lang=conf.get("tts_language"), slow=False).save("temp/god.mp3") # properties of the text to speech audio file and save
        vlc.MediaPlayer("temp/god.mp3").play() # play the generated audio file
        printer(" ".join(res.split(" ")))


if __name__ == "__main__":
    
    try:
        run_god_bot()
    except KeyboardInterrupt:
        print("\nExiting...")
