# This file completes FoodIE processing
import re
from anyascii import anyascii


def preprocessing(data):
    # Step 1: Remove quotation marks
    data = data.replace('\'', '')
    data = data.replace('\"', '')

    # Step 2: Change all white space chars into single space
    # FIXME May need to consider for cases with two tabs
    data = data.replace('\t', ' ')
    data = data.replace('\n', ' ')
    data = data.replace('  ', ' ')

    # Step 3: ASCII transliteration
    data = anyascii(data)

    # Step 4: Convert numbers to decimal
    # However, for the purpose of our study, we will remove all numbers
    data = re.sub(r'[0-9]', '', data)

    # Step 5: Miscellaneous. (Was not in original FoodIE algorithm)
    # Remove '... '
    data = data.replace('... ', '')
    # Remove words like '/-inch' and '-quart'
    data = data.replace(' -', ' - ')
    data = data.replace('(-', '( - ')
    data = data.replace('/-', '/ - ')
    data = data.replace(' - ', ' ')
    # Add space before and after '.', ',', '(', ')', '!', ';', ':', ' ' / '
    data = data.replace('.', ' . ')
    data = data.replace(',', ' , ')
    data = data.replace('(', ' ( ')
    data = data.replace(')', ' ) ')
    data = data.replace('!', ' ! ')
    data = data.replace(';', ' ; ')
    data = data.replace(':', ' : ')
    data = data.replace('/', ' / ')
    data = data.replace('&', ' ')
    # Remove double space that may have been created due to actions before
    data = data.replace('  ', ' ')
    data = data.replace('  ', ' ')
    data = data.replace('  ', ' ')

    return data


# Example
# ------------------------------------------------------------
# sent = ('This is a random \'line\". We removed\t\ttwo tabs in between. Numbers, like 2 and 2.4, are gone too. \n'
#         + 'Some unicode chars are converted as well, like άνθρωποι')
# output = preprocessing(sent)
# print(output)
# ------------------------------------------------------------

# For each recipe full text field, run the preprocessing steps
input_fp = open("data/preprocessing/foodbase_curated.txt", "r")
output_fp = open("data/preprocessed/foodbase_curated_recipes_FoodIE.txt", "w")
recipes = input_fp.readlines()

# For each recipe, run preprocessing methods and write to output file
for recipe in recipes:
    processed_recipe = preprocessing(recipe)
    output_fp.write(processed_recipe)
    output_fp.write("\n")
