import markovify
import sys
import numpy
import random
import time


input_file = "kjvc.txt"
chain_order = 4  # 4 is the magic number


def get_last_n(lst, n):
    return lst[-n:]


def find_closest_word(bad_word: str, corpus: list[str]):

    corpus = list(corpus)

    closest_words = []

    shortest_dist = 999  # init with high value

    for cur_word in corpus:
        cur_dist = levenshteinDistanceDP(bad_word, cur_word)

        if cur_dist < shortest_dist:
            closest_words = []  # clear currest best words
            shortest_dist = cur_dist
            closest_words.append(cur_word)
        elif cur_dist == shortest_dist:
            closest_words.append(cur_word)

    return random.choice(closest_words)


def get_user_prompt(the_bible: str) -> str:
    global chain_order
    set_corpus = set(the_bible.replace(".", "", -1).split(" "))
    full_dirty_input = input("Enter prompt: ")
    punc = ["[", "]", ":", ",", ";", "’", "—", "!", "(", ")", "?"]
    for mark in punc:
        full_dirty_input = full_dirty_input.replace(mark, "", -1)
    full_dirty_input = full_dirty_input.strip().split(" ")
    dirty_input = []

    if len(full_dirty_input) > chain_order:
        dirty_input = full_dirty_input[len(full_dirty_input) - chain_order :]
    else:
        dirty_input = full_dirty_input

    bad_words = []
    for word in dirty_input:
        if word not in set_corpus:
            bad_words.append(word)

    good_words = []
    for word in bad_words:
        good_words.append(find_closest_word(word, set_corpus))

    cleaned_input = []

    index_in_good = 0

    for i in range(len(dirty_input)):
        if dirty_input[i] in bad_words:
            cleaned_input.append(good_words[index_in_good])
            index_in_good += 1
        else:
            cleaned_input.append(dirty_input[i])

    # after levinsteine search
    print("Cleaned input: ", cleaned_input)
    temp = find_prompt_chain(the_bible.split(" "), cleaned_input)
    print("Final prompt: ", temp)
    return " ".join(temp)


def convolve_lists(corpus: list[str], cleaned_input: list[str]):
    global chain_order
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


def permutations(elements):
    if len(elements) <= 1:
        yield elements
        return
    for perm in permutations(elements[1:]):
        for i in range(len(elements)):
            # nb elements[0:1] works in both string and list contexts
            yield perm[:i] + elements[0:1] + perm[i:]


def find_prompt_chain(corpus: list[str], cleaned_input: list[str]):
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


def response(model: markovify.Text, prompt: str):
    global chain_order

    usable_words = get_last_n(prompt.split(" "), chain_order)

    real_prompt = " ".join(usable_words)

    if len(real_prompt) > 0:
        temp = tuple(prompt.split(" "))
        print("Initial state: ", temp)
        return model.make_sentence(init_state=temp)
        # return model.make_sentence_with_start(real_prompt, strict=False)
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


def inject_prompt(
    prompt: str, the_bible: str
) -> str:  # TODO decide if its worth killing

    prompt += " amen"
    bible_words = the_bible.split(".")
    index = random.randrange(len(bible_words))

    new_testament = [prompt] + bible_words[index:-1] + bible_words[0:index]
    # bible_words.insert(index, prompt)

    return ". ".join(new_testament)


def printer(text: str) -> None:
    for char in text:
        print(char, end="", flush=True)
        time.sleep(0.05)

    print()  # newline


def main():
    global input_file

    with open(input_file) as f:
        the_bible = f.read().replace("\n", " ", -1)

    while True:
        prompt = get_user_prompt(the_bible)

        text_model = markovify.Text(
            the_bible,
            state_size=min(chain_order, len(prompt.split(" "))),
        )
        res = response(text_model, prompt)

        printer(" ".join(res.split(" ")))


if __name__ == "__main__":
    main()
