# This is the post-processing step in FoodIE
# It will take in the POS tags of CLAWS (or USAS) and coreNLP, and output a modified version of POS tags
import pandas as pd

claws_df = pd.read_csv('data/tagged/claws_pos_conll.txt', sep='\t')
corenlp_df = pd.read_csv('data/tagged/tagged_curated_recipes_corenlp_FoodIE.txt', sep='\t')

# Output file
modified_tags = open('data/tagged/modified_tags.txt', 'w')
modified_tags.write('Index\tText\tPOS Modified\n')

# Get details on the tags and ensure they are ready for post-processing
# ------------------------------------------------------------
print(claws_df.shape)
print(corenlp_df.shape)

# Double check if the two files align
# Resolve unmatched tokenization
for i in range(corenlp_df.shape[0]):
    text = str(corenlp_df['Text'].iloc[i])
    if str(claws_df['Text'].iloc[i]) != text:
        claws_text = claws_df['Text'].iloc[i]
        print("Unmatch found:")
        print(i, text, claws_text)
        print(str(text) == str(claws_text))
        break
# ------------------------------------------------------------

# Main algorithm for post-processing
# Ensure previous code for checking alignment passes before running main algorithm
# ------------------------------------------------------------
for i in range(claws_df.shape[0]):
    index = claws_df['Index'].iloc[i]
    text = claws_df['Text'].iloc[i]
    pos_tag = claws_df['POS CLAWS'].iloc[i]
    # Check if discrepancy exist
    if corenlp_df['POS'].iloc[i] != pos_tag:
        # See if coreNLP marked word as verb
        # If coreNLP marked it as verb, change POS to verb
        if corenlp_df['POS'].iloc[i][0] == 'V':
            corenlp_pos = corenlp_df['POS'].iloc[i]
            modified_tags.write(f'{index}\t{text}\t{corenlp_pos}\n')
        else:
            # If coreNLP is not a verb, use CLAWS tag
            # Check if POS tag is a verb
            if pos_tag == 'VVD' or pos_tag == 'VVN' or pos_tag == 'VVNK' or pos_tag == 'VHN' or pos_tag == 'VHD':
                # Check if the next word is noun
                # If it is a noun, change tag to adjective
                if claws_df['POS CLAWS'].iloc[i + 1][0] == 'N':
                    adj_tag = 'JJ'
                    modified_tags.write(f'{index}\t{text}\t{adj_tag}\n')
                else:
                    modified_tags.write(f'{index}\t{text}\t{pos_tag}\n')
            else:
                # If not a verb, or if it is a verb not followed by noun, go with original tag
                modified_tags.write(f'{index}\t{text}\t{pos_tag}\n')
    else:
        # If the tags match, use original tag from CLAWS
        modified_tags.write(f'{index}\t{text}\t{pos_tag}\n')
# ------------------------------------------------------------
