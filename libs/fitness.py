import nltk
from collections import Counter

ALPHA = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
# http://pi.math.cornell.edu/~mec/2003-2004/cryptography/subs/frequencies.html
CLF = {
    'E' : 0.1202,
    'T' : 0.0910,
    'A' : 0.0812,
    'O' : 0.0768,
    'I' : 0.0731,
    'N' : 0.0695,
    'S' : 0.0628,
    'R' : 0.0602,
    'H' : 0.0592,
    'D' : 0.0432,
    'L' : 0.0398,
    'U' : 0.0288,
    'C' : 0.0271,
    'M' : 0.0261,
    'F' : 0.0230,
    'Y' : 0.0211,
    'W' : 0.0209,
    'G' : 0.0203,
    'P' : 0.0182,
    'B' : 0.0149,
    'V' : 0.0111,
    'K' : 0.0069,
    'X' : 0.0017,
    'Q' : 0.0011,
    'J' : 0.0010,
    'Z' : 0.0007
}

COMMON = ['THE','BE','TO','OF','AND','A','IN','THAT','HAVE','I','IT','FOR','NOT','ON','WITH','HE','AS','YOU','DO','AT','THIS','BUT','HIS','BY','FROM','THEY','WE','SAY','HER','SHE','OR','AN','WILL','MY','ONE','ALL','WOULD','THERE','THEIR','WHAT','SO','UP','OUT','IF','ABOUT','WHO','GET','WHICH','GO','ME','WHEN','MAKE','CAN','LIKE','TIME','NO','JUST','HIM','KNOW','TAKE','PEOPLE','INTO','YEAR','YOUR','GOOD','SOME','COULD','THEM','SEE','OTHER','THAN','THEN','NOW','LOOK','ONLY','COME','ITS','OVER','THINK','ALSO','BACK','AFTER','USE','TWO','HOW','OUR','WORK','FIRST','WELL','WAY','EVEN','NEW','WANT','BECAUSE','ANY','THESE','GIVE','DAY','MOST','US']

class Fitness():
    def __init__(self):
        self.decipher = None
        self.ciphertext = ''
        self.fitness = None

    def word_counter(self, guesses):
        counts = []
        for guess in guesses:
            words = guess.split(' ')
            letters = [l for l in list(guess) if l.isalpha()]
            score = 0
            for w in words:
                if w in COMMON:
                    score += len(w)
            counts.append([score / len(letters)])
        return counts

    def letter_prob(self, guesses):
        probs = []
        for guess in guesses:
            letters = [l for l in list(guess) if l.isalpha()]
            l_cnt = Counter(letters)
            prob = 1
            for l in ALPHA:
                prob *= CLF[l]**(l_cnt[l] if l in l_cnt else 0)
            probs.append([prob])
        return probs

    # def frequency_based_guess(text):
    #     LC = Counter()
    #     for word in text:
    #         LC += Counter([l for l in word if l.isalpha()])
    #     t_order = [l[0] for l in LC.most_common()]
    #     for l in list('abcdefghijklmnopqrstuvwxyz'):
    #         if l not in t_order:
    #             t_order.append(l)
    #     clf_order = [l[0] for l in CLF]
    #     key_map = {}
    #     for i, l in enumerate(clf_order):
    #         key_map[l] = t_order[i]
    #     input(key_map)
    #     key = []
    #     for l in list('abcdefghijklmnopqrstuvwxyz'):
    #         key.append(key_map[l])
    #     input("".join(key))
