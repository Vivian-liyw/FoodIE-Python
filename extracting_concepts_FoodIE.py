# This file will conduct the final extraction of identifying food concepts, following the rules defined by FoodIE
import pandas as pd


def condition_1(sem_lst):
    for i in range(len(sem_lst)):
        one_tag = sem_lst[i]
        if one_tag == 'F1' or one_tag == 'F2' or one_tag == 'F3' or one_tag == 'F4':
            return True
        if one_tag == 'L2' or one_tag == 'L3':
            return True
        if one_tag == 'O1.1' or one_tag == 'O1.2':
            return True

    return False


def condition_2(sem_lst):
    B1 = False
    N4 = False
    M6 = False
    M45 = False

    for i in range(len(sem_lst)):
        one_tag = sem_lst[i]
        if one_tag == 'B1':
            B1 = True
        if one_tag == 'N4':
            N4 = True
        if one_tag == 'M6':
            M6 = True
        if one_tag == 'O4.5':
            M45 = True

    if B1 and (not N4) and (not M6) and (not M45):
        return True
    else:
        return False


# Does not have tags AG.01.t.08, AG.01.u, nor AH.02
def condition_3(sem_lst):
    O2 = False
    N5 = False
    B5 = False

    for i in range(len(sem_lst)):
        one_tag = sem_lst[i]
        if one_tag == 'O2':
            O2 = True
        if one_tag == 'N5':
            N5 = True
        if one_tag == 'B5':
            B5 = True

    if (not O2) and (not N5) and (not B5):
        return True
    else:
        return False


def rule2(sem_lst):
    O2 = False
    B5 = False
    B1 = False
    L2 = False
    L3 = False

    for i in range(len(sem_lst)):
        one_tag = sem_lst[i]
        if one_tag == 'O2':
            O2 = True
        if one_tag == 'B5':
            B5 = True
        if one_tag == 'B1':
            B1 = True
        if one_tag == 'L2':
            L2 = True
        if one_tag == 'L3':
            L3 = True

    if (O2 or B5) and (not B1) and (not L2) and (not L3):
        return True
    else:
        return False


def rule3(sem_lst):
    for i in range(len(sem_lst)):
        one_tag = sem_lst[i]
        if one_tag == 'O4.3':
            return True

    return False


# Tags AG.01.t.08, AG.01.u, and AH.02 are not found
def rule4(sem_lst):
    O46 = False
    N3 = False

    for i in range(len(sem_lst)):
        one_tag = sem_lst[i]
        if one_tag == 'O4.6':
            O46 = True
        if one_tag == 'N3':
            N3 = True

    if O46 and N3:
        return True
    else:
        return False


def rule_labeling(tags, output_file):
    for i in range(tags.shape[0]):
        rule_1 = False

        pos = tags['POS'].iloc[i]
        semantics = tags['Semantics'].iloc[i]

        # Parse and clean the semantic tags
        txt = semantics.replace('[', '')
        txt = txt.replace(']', '')
        txt = txt.replace('+', '')
        txt = txt.replace('-', '')
        txt = txt.replace('\'', '')
        txt = txt.replace(' ', '')
        sem_lst = txt.split(',')

        # Check if token is food token
        # Check if the word is adjective or noun
        if pos[0] == 'J' or pos[0] == 'N':
            cond_1 = condition_1(sem_lst)
            cond_2 = condition_2(sem_lst)
            cond_3 = condition_3(sem_lst)

            if (cond_1 or cond_2) and cond_3:
                rule_1 = True
                tags.at[i, 'Food Token'] = 'T'
            else:
                tags.at[i, 'Food Token'] = 'F'
        else:
            tags.at[i, 'Food Token'] = 'F'

        # Check if token is object token
        if rule2(sem_lst) and (not rule_1):
            tags.at[i, 'Object Token'] = 'T'
        else:
            tags.at[i, 'Object Token'] = 'F'

        # Check if token is color noun
        if rule3(sem_lst):
            tags.at[i, 'Color Noun'] = 'T'
        else:
            tags.at[i, 'Color Noun'] = 'F'

        # Check if token is explicitly disallowed
        if rule4(sem_lst):
            tags.at[i, 'Explicitly Disallowed'] = 'T'
        else:
            tags.at[i, 'Explicitly Disallowed'] = 'F'

    # Save a copy as backup
    tags.to_csv(output_file, index=False)

    return tags


def main():
    # Section 1: get the updated tags where all rule tags are given to individual tokens
    # -------------------------------------------------------------------------------------------
    # input file
    tags = pd.read_csv('data/tagged/finalized_tags.txt', sep='\t')

    # Categories text needs to be sorted into
    # Food token
    # Object token
    # Color noun
    # Explicitly disallowed

    tags.insert(5, 'Food Token', '-')
    tags.insert(6, 'Object Token', '-')
    tags.insert(7, 'Color Noun', '-')
    tags.insert(8, 'Explicitly Disallowed', '-')

    output_file = 'data/backup/tags_w_rules.csv'
    rule_labeling(tags, output_file)
    # -------------------------------------------------------------------------------------------

    # Section 2: process the tags to find food chunks
    # Ensure Section 1 finished processing before running Section 2, else error warning may arise
    # -------------------------------------------------------------------------------------------
    # Input file
    tags_updated = pd.read_csv('data/backup/tags_w_rules.csv', sep=',')

    # Output files
    extracted = open('data/extracted_entities/extracted_FoodIE.txt', 'w')

    i = 0
    length = tags_updated.shape[0]
    while i < length:
        # New variable to save updated i
        i_new = i

        tmp_list = []
        if tags_updated['Food Token'].iloc[i] == 'T':
            # Food token added to list
            tmp_list.append(tags_updated['Text'].iloc[i])
            if (i != 0 and tags_updated['Index'].iloc[i] != 1 and (
                    tags_updated['POS'].iloc[i - 1] == 'JJ' or tags_updated['POS'].iloc[i - 1] == 'VBN'
                    or tags_updated['POS'].iloc[i - 1] == 'GE' or
                    tags_updated['POS'].iloc[i - 1] == 'NN' or tags_updated['POS'].iloc[i - 1] == 'NN1' or
                    tags_updated['POS'].iloc[i - 1] == 'NN2' or tags_updated['POS'].iloc[i - 1] == 'NP' or
                    tags_updated['POS'].iloc[i - 1] == 'NP1' or tags_updated['POS'].iloc[i - 1] == 'NP2' or
                    tags_updated['POS'].iloc[i - 1] == 'Z99' or tags_updated['Food Token'].iloc[i - 1] == 'T')
                    and tags_updated['Object Token'].iloc[i - 1] != 'T'):
                # Left of the food token added
                tmp_list.insert(0, tags_updated['Text'].iloc[i - 1])

            if ((i < (length - 1)) and tags_updated['Index'].iloc[i + 1] != 1 and (
                    tags_updated['POS'].iloc[i + 1] == 'JJ' or tags_updated['POS'].iloc[i + 1] == 'GE' or
                    tags_updated['POS'].iloc[i + 1] == 'NN' or tags_updated['POS'].iloc[i + 1] == 'NN1' or
                    tags_updated['POS'].iloc[i + 1] == 'NN2' or tags_updated['POS'].iloc[i + 1] == 'NP' or
                    tags_updated['POS'].iloc[i + 1] == 'NP1' or tags_updated['POS'].iloc[i + 1] == 'NP2' or
                    tags_updated['POS'].iloc[i + 1] == 'Z99' or tags_updated['Food Token'].iloc[i + 1] == 'T'
                    or tags_updated['Color Noun'].iloc[i + 1] == 'T')):
                # Right of the food token added
                tmp_list.append(tags_updated['Text'].iloc[i + 1])

                if (tags_updated['POS'].iloc[i + 1] == 'NN' or tags_updated['POS'].iloc[i + 1] == 'NN1' or
                    tags_updated['POS'].iloc[i + 1] == 'NN2') and tags_updated['Food Token'].iloc[i + 1] == 'F':
                    tmp_list = []
                elif tags_updated['Explicitly Disallowed'].iloc[i + 1] == 'T':
                    tmp_list = []

                i_new = i_new + 2
            else:
                i_new = i_new + 1
        else:
            i_new = i_new + 1

        if tags_updated['Index'].iloc[i] == 1:
            extracted.write('---------\n')
            # extracted_modified_exclusion.write('\n')

        if tmp_list:
            # Check if list is empty, if empty will return false
            word = ''
            for idx in range(len(tmp_list)):
                word = word + tmp_list[idx] + ' '
            word = word.strip()
            extracted.write(word + '\n')
            # extracted_modified_exclusion.write(word + '\n')

        if i % 1000 == 0:
            print(i)

        # Update the parameter i
        i = i_new
    # -------------------------------------------------------------------------------------------


if __name__ == "__main__":
    main()
