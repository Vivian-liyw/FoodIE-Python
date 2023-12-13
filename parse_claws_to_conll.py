# This file doesn't actually convert CLAWS output to conll format
# It would only output a tab delimited file with columns index, word, POS tag

input = open("data/tagged/claws_pos.txt", "r")
output = open("data/tagged/claws_pos_conll.txt", "w")
recipes = input.readlines()
output.write('Index\tText\tPOS CLAWS\n')

idx = 1
for line in recipes:
    line_clean = line.strip()
    # Misc. cases that requires removal
    if line_clean == 'NEWRECIPE_NP1 ._.':
        output.write('\n')
        idx = 1
    elif line_clean == 'NEWRECIPE_VV0 ._.':
        output.write('\n')
        idx = 1
    elif line_clean == 'NEWRECIPE_NN1 ._.':
        output.write('\n')
        idx = 1
    else:
        tokenize_sent = line_clean.split(' ')
        for word in tokenize_sent:
            split_text = word.split('_')
            output.write(f'{idx}\t{split_text[0]}\t{split_text[1]}\n')
            idx = idx + 1