# This file joins the USAS semantic tags with the modified POS tags
# Ensure each section is ran separately, i.e, all other sections are commented out.
import pandas as pd

# Step 1: modifiy USAS tags, such that hyphenated words are considered as one word
# ------------------------------------------------------------------------------------------
# Input files
usas_tags_df = pd.read_csv('data/tagged/tagged_curated_recipes_usas_foodIE.txt', sep='\t')

# Output file
modified_usas_tags = open('data/tagged/modified_usas_tags.txt', 'w')
modified_usas_tags.write('Index\tText\tLemma\tPOS\tUSAS Tags\n')

# count how many hyphenated words there are
count_1 = 0
count_2 = 0
# Count how many words are in form "A're"
count_3 = 0
# Count how many words are in form "An't"
count_4 = 0
# Combine hyphenated words in USAS
for i in range(usas_tags_df.shape[0]):
    index = usas_tags_df['Index'].iloc[i]
    text = usas_tags_df['Text'].iloc[i]
    lemma = usas_tags_df['Lemma'].iloc[i]
    pos = usas_tags_df['POS'].iloc[i]
    usas_tag = usas_tags_df['USAS Tags'].iloc[i]
    if usas_tags_df['Text'].iloc[i] == '-':
        # Skip line if it is '-'
        count_1 += 1
    elif usas_tags_df['Text'].iloc[i - 1] == '-':
        # Skip line if word is included but not first word of hyphenated word
        count_2 += 1
    elif usas_tags_df['Text'].iloc[i] == 're':
        # Skip line if word if 're'
        count_3 += 1
    elif usas_tags_df['Text'].iloc[i] == 'nt' and usas_tags_df['Text'].iloc[i - 1] != 'do' and usas_tags_df['Text'].iloc[i - 1] != 'Do':
        # Skip line if word if 'nt'
        count_4 += 1
    elif (i + 3) < (usas_tags_df.shape[0] - 1) and usas_tags_df['Text'].iloc[i + 1] == '-' and usas_tags_df['Text'].iloc[i + 3] == '-':
        # Check for words 'A-B-C'
        new_text = text + usas_tags_df['Text'].iloc[i + 1] + usas_tags_df['Text'].iloc[i + 2] + usas_tags_df['Text'].iloc[i + 3] + usas_tags_df['Text'].iloc[i + 4]
        new_lemma = lemma + ' ' + usas_tags_df['Lemma'].iloc[i + 2] + ' ' + usas_tags_df['Lemma'].iloc[i + 4]
        new_usas_tag = usas_tag + usas_tags_df['USAS Tags'].iloc[i + 2] + usas_tags_df['USAS Tags'].iloc[i + 4]  # this will return ['xxx']['xxx']['xx']
        new_usas_tag = new_usas_tag.replace('][', ', ')
        # POS and index is not important, thus used the value of first word in the hyphenated word
        modified_usas_tags.write(f'{index}\t{new_text}\t{new_lemma}\t{pos}\t{new_usas_tag}\n')
    elif (i + 1) < (usas_tags_df.shape[0] - 1) and usas_tags_df['Text'].iloc[i + 1] == '-':
        # Check for words 'A-B'
        new_text = text + usas_tags_df['Text'].iloc[i + 1] + usas_tags_df['Text'].iloc[i + 2]
        new_lemma = lemma + ' ' + usas_tags_df['Lemma'].iloc[i + 2]
        new_usas_tag = usas_tag + usas_tags_df['USAS Tags'].iloc[i + 2] # this will return ['xxx']['xxx']
        new_usas_tag = new_usas_tag.replace('][', ', ') # this will return ['xxx', 'xxx']
        # POS and index is not important, thus used the value of first word in the hyphenated word
        modified_usas_tags.write(f'{index}\t{new_text}\t{new_lemma}\t{pos}\t{new_usas_tag}\n')
    elif (i + 1) < (usas_tags_df.shape[0] - 1) and usas_tags_df['Text'].iloc[i + 1] == 're':
        # Check for words "A're"
        new_text = text + usas_tags_df['Text'].iloc[i + 1]
        new_lemma = lemma + ' be'
        new_usas_tag = usas_tag + '[\'A3+\', \'Z5\']'  # this will return ['xxx']['xxx']
        new_usas_tag = new_usas_tag.replace('][', ', ')  # this will return ['xxx', 'xxx']
        # POS and index is not important, thus used the value of first word in the hyphenated word
        modified_usas_tags.write(f'{index}\t{new_text}\t{new_lemma}\t{pos}\t{new_usas_tag}\n')
    elif (i + 1) < (usas_tags_df.shape[0] - 1) and usas_tags_df['Text'].iloc[i + 1] == 'nt' and usas_tags_df['Text'].iloc[i] != 'do' and usas_tags_df['Text'].iloc[i] != 'Do':
        # Check for words "A're"
        new_text = text + usas_tags_df['Text'].iloc[i + 1]
        new_lemma = lemma + ' ' + usas_tags_df['Lemma'].iloc[i + 1]
        new_usas_tag = usas_tag + usas_tags_df['USAS Tags'].iloc[i + 1]  # this will return ['xxx']['xxx']
        new_usas_tag = new_usas_tag.replace('][', ', ')  # this will return ['xxx', 'xxx']
        # POS and index is not important, thus used the value of first word in the hyphenated word
        modified_usas_tags.write(f'{index}\t{new_text}\t{new_lemma}\t{pos}\t{new_usas_tag}\n')
    else:
        modified_usas_tags.write(f'{index}\t{text}\t{lemma}\t{pos}\t{usas_tag}\n')

# Count for '-'
print(count_1)
# Count for word is included but not first word of hyphenated word
print(count_2)
# Count for 're'
print(count_3)
# Count for 'nt'
print(count_4)
# ------------------------------------------------------------------------------------------


# Step 2: check USAS semantic tags align with modified POS
# ------------------------------------------------------------------------------------------
# Input file
modified_usas_tags_df = pd.read_csv('data/tagged/modified_usas_tags.txt', sep='\t')
modified_pos_df = pd.read_csv('data/tagged/modified_tags.txt', sep='\t')

print(modified_usas_tags_df.shape)
print(modified_pos_df.shape)

# Double check if the two files align
# Resolve unmatched tokenization
for i in range(modified_usas_tags_df.shape[0]):
    usas_text = str(modified_usas_tags_df['Text'].iloc[i])
    pos_text = str(modified_pos_df['Text'].iloc[i])
    if pos_text != usas_text:
        print("Unmatch found:")
        print(i, usas_text, pos_text)
        break
# ------------------------------------------------------------------------------------------


# Step 3: merge USAS semantic tags with modified POS tags
# ------------------------------------------------------------------------------------------
# Input file
modified_usas_tags_df = pd.read_csv('data/tagged/modified_usas_tags.txt', sep='\t')
modified_pos_df = pd.read_csv('data/tagged/modified_tags.txt', sep='\t')

# Output file
output_fp = open('data/tagged/finalized_tags.txt', 'w')
output_fp.write('Index\tText\tLemma\tPOS\tSemantics\n')

# Count index
count_recipes = 0
count_total_lines = 0
# Main algorithm to combine USAS semantics with modified POS
for i in range(modified_usas_tags_df.shape[0]):
    usas_text = modified_usas_tags_df['Text'].iloc[i]
    pos_text = modified_pos_df['Text'].iloc[i]
    if str(pos_text) == str(usas_text):
        index = modified_usas_tags_df['Index'].iloc[i]
        text = usas_text
        lemma = modified_usas_tags_df['Lemma'].iloc[i]
        pos = modified_pos_df['POS Modified'].iloc[i]
        semantics = modified_usas_tags_df['USAS Tags'].iloc[i]
        count_total_lines += 1
        if index == 1:
            count_recipes += 1
        output_fp.write(f'{index}\t{text}\t{lemma}\t{pos}\t{semantics}\n')


print(count_total_lines)
print(count_recipes)