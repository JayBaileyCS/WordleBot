# WordleBot

For this project, I wanted to do some preliminary testing of my fit/suitability for machine learning without spending a bunch of time trying to learn ML. From posts I have read, a major frustration in ML is iteration time - it can take hours to run an experiment. Thus, I decided to create a simple but non-trivial program (estimated effort 2-8 hours if programming normally) and create the following rule: Each day, I am only allowed to run the program once if the program runs at all (i.e, does not fail at compile time). The reasoning here is that even an ML program can fail at compile time and then allow a quick fix. This does mean that I can't use a quick guess-and-check method and throw stuff at the wall like one can easily do in most programs where iteration times are measured in seconds or minutes. This would force me to examine my code more carefully and try to debug with my eyes and brain, not by seeing where the computer throws an error.

Iteration 1:

This is the very first iteration of the code, before ever running the program. I did implement some toy implementations in a different program, reasoning that I could do something similar in real life. I would test things like "Does random.choice(list) work?" or "Should I use letter.count(word) or word.count(letter)"? I also tested the get_words and create_letter_frequency_table functions before deciding to use the WordleBot as an opportunity to employ this ML training idea. Originally I just thought it would be fun. After this, I wrote the entire thing without ever running it.

Output:

10173 contained in word list.
Word guess is ZUNIS
Result was ['grey', 'green', 'grey', 'grey', 'grey']
Filtering words for next guess.
Traceback (most recent call last):
  File "C:/Python38/wordleBot.py", line 126, in <module>
    play_game(starting_word_list)
  File "C:/Python38/wordleBot.py", line 118, in play_game
    word_list = filter_word(guess_result, word_list, word_guess)
NameError: name 'filter_word' is not defined

Notes:

So it turns out when I renamed "filter_word" to the better "filter_word_list", I did not make this change in Line 118. We are off to a fantastic start.

I did, however, observe that ZUNIS was unlikely to be the best fitting word to start out, given how infrequent Z is. I would guess something like STARE would be superior. After checking the code, I determined that I had never actually kept track of the current max_score. As a result, ZUNIS was the word that appeared last in my list, since any word with a score greater than 0 would replace the previous best word no matter what it was.

I also added a line to print the secret word when generated, since I would have liked to verify that the secret word did in fact contain a U as it's second letter, and none of 'Z', 'N', 'I', or 'S'. But that will have to wait for tomorrow as per my rules.
