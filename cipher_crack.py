import sys
import re
import libs.data_ingest_wiki as data_ingest
import libs.neural_network as neural_network
import libs.genetic_algorithm as genetic_algorithm
import libs.sub_cipher as sub_cipher
import libs.fitness as fitlib

tests = [
'There had been coin shortages beginning in 1959, and the United States Bureau of the Mint expanded production to try to meet demand',
'The danger in both sides’ cyber-deterrence, however, lies not so much in their converging will and capacity as much as it is rooted in mutual misunderstanding. ',
'Western analysts, fixated on untangling the now-defunct concept of the ‘Gerasimov Doctrine,’ devoted far less attention to the Russian military’s actual cyber-experts, who starting in 2008 wrote a series of articles',
'Despite Cyber Command’s new authorities, Moscow’s hackers are comparatively unfettered by legal or normative boundaries and have a far wider menu of means and methods in competing with the U.S. short of all-out war. ',
'Russian military hackers, for example, have gone after everything from the Orthodox Church to U.S. think tanks, and they launched what the Trump administration called the most costly cyber-attack in history.',
'The U.S. is arriving late to a showdown that many officials in Russian defense circles saw coming a long time ago, when U.S. policymakers were understandably preoccupied with the exigencies of counterterrorism and counterinsurgency.',
'Increasing the diplomatic costs of Russian cyber-aggression, shoring-up cyber-defenses, or even fostering military-to-military or working-level diplomatic channels to discuss cyber redlines, however discretely and unofficially',
'It may only be day one of the Your Collection homewares launch, but a Coles spokesman told news.com.au the stylish Maya Table Top Lamp, on sale for $25, is already proving to be a popular item among customers.',
'For more than a century Coles has been constantly evolving to meet customer needs and we’re committed to continuing that legacy of innovation, Coles chief executive for commercial and express Greg Davis said. ',
'Supermarket shopping is a relatively mundane, habitual activity, so if you can introduce new ranges or categories, even for a short period of time, it gives shoppers the opportunity to engage with new and exciting products.',
]

def train(di, nn, load_size, batch_size, total_jobs):
    print('Rebuilding on', total_jobs, 'jobs')
    # di.reset_data()
    # lines, labels = di.get_data(load_size)
    # nn.rebuild_tokenizer(lines)
    di.reset_data()
    nn.rebuild_model()
    job_count = 0
    for i in range(total_jobs):
        job_count += 1
        print('Job Number:', job_count)
        print('Batch Size:', batch_size)
        print('Batch Count:', int(load_size / batch_size))
        lines, labels = di.get_data(load_size)
        nn.train(lines, labels, batch_size)
        nn.save()

def rebuild(di, nn):
    if len(sys.argv) != 5:
        print('[ingest size] [batch size] [total jobs]')
        quit()
    load_size = int(sys.argv[2])
    batch_size = int(sys.argv[3])
    total_jobs = int(sys.argv[4])
    train(di, nn, load_size, batch_size, total_jobs)

def fitness(guesses):
    guesses_l = [list(g) for g in guesses]
    pred = nn.run_model(guesses_l)
    # input(pred)
    return [pred]

print('________________________________________________________________________________')
print('_________ .__       .__                  _________                       __     ')
print('\_   ___ \|__|_____ |  |__   ___________ \_   ___ \____________    ____ |  | __ ')
print('/    \  \/|  \____ \|  |  \_/ __ \_  __ \/    \  \/\_  __ \__  \ _/ ___\|  |/ / ')
print('\     \___|  |  |_> >   Y  \  ___/|  | \/\     \____|  | \// __ \\  \___|    <  ')
print(' \______  /__|   __/|___|  /\___  >__|    \______  /|__|  (____  /\___  >__|_ \ ')
print('        \/   |__|        \/     \/               \/            \/     \/     \/ ')
print('________________________________________________________________________________')
print('C0MP6841 PR0JECT BY Z5146667')
print('')

cipher = sub_cipher.SubCipher()
di = data_ingest.DataIngest(cipher)
nn = neural_network.CNN('cnn')
ga = genetic_algorithm.GeneticAlgorithm(cipher)
fit = fitlib.Fitness()
ga.set_fitness(fitness, [1.0])

if len(sys.argv) > 1 and sys.argv[1] == '-rebuild':
    rebuild(di, nn)

command = 's'
while command != 'q':

    print('')
    print('Options: ')
    print('  q : quit ')
    print('  k : generate key ')
    print('  e : encrypt message ')
    print('  d : decrypt message ')
    print('  c : crack ciphertext ')
    print('  r : rebuild neuralnet ')
    print('  t : run tests ')
    print('')

    command = input('Enter command : ')
    print('')

    if (command == 'k'):
        print(' | Key :', cipher.gen_key(100))

    if (command == 'e'):
        key = input('Enter key : ')
        message = input('Enter message : ')
        print(' | Ciphertext :',cipher.encipher(key, di.clean(message)))

    if (command == 'd'):
        key = input('Enter key : ')
        ciphertext = input('Enter ciphertext : ')
        print(' | Plaintext :', cipher.decipher(key, di.clean(ciphertext)))

    if (command == 'c'):
        ciphertext = input('Enter ciphertext : ')
        ga.set_ciphertext(ciphertext)
        key, plaintext = ga.crack()
        print('')
        print(' | Key :', key)
        print(' | Plaintext :', plaintext)
        print('')

    if (command == 'r'):
        load_size = int(input('Enter load size : '))
        batch_size = int(input('Enter batch size : '))
        total_jobs = int(input('Enter number of jobs : '))
        print('')
        train(di, nn, load_size, batch_size, total_jobs)

    if (command == 't'):
        for t in tests:
            key = cipher.gen_key(100)
            message = di.clean(t)
            ciphertext = cipher.encipher(key, message)
            ga.set_ciphertext(ciphertext)
            # print('Aim :', message, '|', round(fitness([message])[0][0][0], 2))
            print('Ciphertext :', ciphertext, '|', round(fitness([message])[0][0][0], 2))
            key, plaintext = ga.crack()
            print(' | Key:', key)
            print(' | Plaintext:', plaintext)
            print('')
