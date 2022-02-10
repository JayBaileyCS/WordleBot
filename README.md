# WordleBot

For this project, I wanted to do some preliminary testing of my fit/suitability for machine learning without spending a bunch of time trying to learn ML. From posts I have read, a major frustration in ML is iteration time - it can take hours to run an experiment. Thus, I decided to create a simple but non-trivial program (estimated effort 2-8 hours if programming normally) and create the following rule: Each day, I am only allowed to run the program once if the program runs at all (i.e, does not fail at compile time). The reasoning here is that even an ML program can fail at compile time and then allow a quick fix. This does mean that I can't use a quick guess-and-check method and throw stuff at the wall like one can easily do in most programs where iteration times are measured in seconds or minutes. This would force me to examine my code more carefully and try to debug with my eyes and brain, not by seeing where the computer throws an error.

**Iteration 1:**

This is the very first iteration of the code, before ever running the program. I did implement some toy implementations in a different program, reasoning that I could do something similar in real life. I would test things like "Does random.choice(list) work?" or "Should I use letter.count(word) or word.count(letter)"? I also tested the get_words and create_letter_frequency_table functions before deciding to use the WordleBot as an opportunity to employ this ML training idea. Originally I just thought it would be fun. After this, I wrote the entire thing without ever running it.

**Output:**

10173 contained in word list.<br>
Word guess is ZUNIS<br>
Result was ['grey', 'green', 'grey', 'grey', 'grey']<br>
Filtering words for next guess.<br>
```
Traceback (most recent call last):
  File "C:/Python38/wordleBot.py", line 126, in <module>
    play_game(starting_word_list)
  File "C:/Python38/wordleBot.py", line 118, in play_game
    word_list = filter_word(guess_result, word_list, word_guess)
NameError: name 'filter_word' is not defined
```

**Notes:**

So it turns out when I renamed "filter_word" to the better "filter_word_list", I did not make this change in Line 118. We are off to a fantastic start.

I did, however, observe that ZUNIS was unlikely to be the best fitting word to start out, given how infrequent Z is. I would guess something like STARE would be superior. After checking the code, I determined that I had never actually kept track of the current max_score. As a result, ZUNIS was the word that appeared last in my list, since any word with a score greater than 0 would replace the previous best word no matter what it was.

I also added a line to print the secret word when generated, since I would have liked to verify that the secret word did in fact contain a U as it's second letter, and none of 'Z', 'N', 'I', or 'S'. But that will have to wait for tomorrow as per my rules.

**Iteration 2:**

For this iteration, I did a quick run-through of the code and then ran it, since I was tired. I expect most of the work on fixing each iteration to be done after the Output section, in the Notes section, and then with the next iteration running pretty quickly the day after unless I come up with something.

**Output:**

SITAO is the word to guess.<br>
10173 words contained in word list.<br>
Word guess 1 is AESIR<br>
Result was ['gold', 'grey', 'gold', 'gold', 'grey']<br>
Filtering words for next guess.<br>
DEBUG: 10173 words at start of filter.<br>
DEBUG: 21455 words remain.<br>
DEBUG: 19930 words remain.<br>
```
Traceback (most recent call last):
  File "C:\Python38\wordleBot.py", line 128, in <module>
    play_game(starting_word_list)
  File "C:\Python38\wordleBot.py", line 120, in play_game
    word_list = filter_word_list(guess_result, word_list, word_guess)
  File "C:\Python38\wordleBot.py", line 61, in filter_word_list
    word_list = filter_gold(word_list, word_guess[i], i)
  File "C:\Python38\wordleBot.py", line 80, in filter_gold
    if letter in word and word[index] != letter:
IndexError: string index out of range
```

**Notes:**

Alright, so what have we got here? AESIR seems like a solid guess here. All these letters are very common (and indeed, consulting the frequency table I have saved, are indeed the five most common letters, the computer is just better at selecting words than I am) and the score has to be beaten, not tied, in order to pick a new word. So it makes sense that AESIR, not ARISE, would be used, and I is more common than T for our set of five-letter words chosen.

The guess result also appears correct. A, S, and I were all in the word but in the wrong position, wheras E and R were not present in SITAO. Our problem lies when we begin the filter. The filter starts by INCREASING the number of words. How could this happen? My immediate hypothesis is that when we first collect our starting word list, we remove all items that aren't five letters. If these are being added back in somehow, that would explain this. Let's take a look.

The first result is gold, which means we should call ```filter_gold``` on it. filter_gold is the following:

```
def filter_gold(word_list, letter, index):
    """Return all words with the letter not in position but present."""
    filtered_word_list = []
    for word in word_list:
        if letter in word and word[index] != letter:
            filtered_word_list += word
    return filtered_word_list
```

After a bit of a look, it becomes clear that I'm wrong. filtered_word_list += word is the problem. 21455 is a multiple of five: when you add a string to a list in this way, I suspect you add each letter of the string. I do a quick test and this is correct. We should actually have 4,291 words, which seems roughly accurate when there were 4,902 A's in the original word count. Since we aren't yet handling doubles and are filtering all words with double letters out, that leaves 4,902 - 4,291 = 617 words left over, which are five-letter words which start with A. This seems reasonable, since 10173/617 is about 16.5, there are 26 letters in the alphabet, and A is a relatively common one.

This also explains our out of bounds error after a successful second filter. The next filter we check is filter_grey, which doesn't care about index size (but does have the same error of += word)

```
def filter_grey(word_list, letter):
    """Return all words that don't contain the letter."""
    filtered_word_list = []
    for word in word_list:
        if letter not in word:
            filtered_word_list += word
    return filtered_word_list
```

But after that, we get filter_gold again, which checks for ```word[index]``` on Line 80 where index = 2, and finds a single letter of length 1 in our list of what should be five letter words, which causes this error.

I fix all three filters from ```filtered_word_list += word``` to ```filtered_word_list.append(word)```. Let's do a quick sanity check of ```filter_grey``` before we wrap up. filter_grey filters from 21455 items, consisting of the individual letters of all five-letter words that contain A but do not start with A, to 19930. The code checks each letter, and says "If the letter is not E, add it back into the word list." This seems reasonable. We're removing about 1 in 13 items, and E is the most common letter in the English language. It should work just as well when passed actual words instead of letters.

This level of examination of the code so soon into finding bugs is new to me. Normally I would try just printing out some things or rapid-fire test some ideas, and I would focus on just one bug at a time. But here, every run is precious, just like an ML experiment. We need to try and solve everything going wrong using all the data we have, before we run the next iteration.

In summary, I believe our ability to select a random word, ability to generate good word guesses, and ability to return correct results from those guesses are working correctly. Our filtering isn't, on account of using the wrong term to add items to the list. That said, filtering out words that don't meet our criteria is the last step in our guess loop, so I am hoping we get a lot more data next time! I have the code set to run ten full games for maximum data collection, so if it actually does run to completion, I will spoiler the full output and only share choice sections.
