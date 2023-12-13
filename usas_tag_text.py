import spacy

# We exclude the following components as we do not need them.
nlp = spacy.load('en_core_web_sm', exclude=['parser', 'ner'])
# Load the English PyMUSAS rule-based tagger in a separate spaCy pipeline
english_tagger_pipeline = spacy.load('en_dual_none_contextual')
# Adds the English PyMUSAS rule-based tagger to the main spaCy pipeline
nlp.add_pipe('pymusas_rule_based_tagger', source=english_tagger_pipeline)

# Example
# ------------------------------------------------------------
# text = "Heat the beef soup until it boils."
# output_doc = nlp(text)
# for token in output_doc:
#     print(f'{token.text}\t{token.lemma_}\t{token.pos_}\t{token._.pymusas_tags}')
# ------------------------------------------------------------

# For each recipe full text field, run the preprocessing steps
input_fp = open("data/preprocessed/processed_curated_recipes_foodIE.txt", "r")
output_fp = open("data/tagged/tagged_curated_recipes_usas_foodIE.txt", "w")
# output_mwu_fp = open("data/tagged/tagged_curated_recipes_usas_mwu_foodIE.txt", "w")
recipes = input_fp.readlines()

# Header of the output file
output_fp.write('Index\tText\tLemma\tPOS\tUSAS Tags\n')

# For each recipe, run preprocessing methods and write to output file
for recipe in recipes:
    # Remove \n at the end of each line
    recipe_clean = recipe.strip()
    tagged_recipe = nlp(recipe_clean)
    idx = 1
    for token in tagged_recipe:
        output_fp.write(f'{idx}\t{token.text}\t{token.lemma_}\t{token.pos_}\t{token._.pymusas_tags}')
        output_fp.write("\n")
        idx = idx + 1
    output_fp.write('\n')

# # Multi-word-unit expressions
# # Header of the output file
# output_mwu_fp.write('Index\tText\tPOS\tMWE start and end index\tUSAS Tags\n')
#
# # For each recipe, run preprocessing methods and write to output file
# for recipe in recipes:
#     # Remove \n at the end of each line
#     recipe_clean = recipe.strip()
#     tagged_recipe = nlp(recipe_clean)
#     idx_mwu = 1
#     for token in tagged_recipe:
#         start, end = token._.pymusas_mwe_indexes[0]
#         if (end - start) > 1:
#             output_mwu_fp.write(f'{idx_mwu}\t{token.text}\t{token.lemma_}\t{token.pos_}\t{token._.pymusas_tags}')
#             output_mwu_fp.write("\n")
#         idx_mwu = idx_mwu + 1
#     output_mwu_fp.write('\n')
