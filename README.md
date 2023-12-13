# How to use FoodIE-Python
A sample usage of FoodIE-Python extracting from FoodBase curated reciepes is stored in `data`.

Folders in `data`
--
- backup
  - contain all backup files created within the extraction process.
- concept-mapping 
  - contain raw FoodBase recipes.
  - each line represent a new recipe.
- extracted_entities
  - store the final set of extracted entities.
- foodbase
  - original xml FoodBase recipes.
- preprocessed
  - recipes after preprocessing steps (either by FoodIE preprocess steps or our defined pipeline).
- preprocessing
  - contain the parsed raw data that are ready for preprocessing.
  - This store both the raw input recipe data and the raw labels.
- tagged
  - recipes tagged for index, word, lemma, POS, (sentiment) using USAS and coreNLP.
  - mwu indicate multi-word-unit tagging, for USAS only.

FoodIE preprocessing
--
- Run `preprocessing_FoodIE`
  - Requirements: re, anyascii
  - Change `input_fp` and `output_fp` for desired input and output locations.
  - `Preprocessing` function takes in one line at one time.

Create USAS Tags
-- 
- Run `usas_tag_text`
  - Side note: `usas_tag_conll` generates TSV file, which works similar to `usas_tag_text`.
  - Requirements: SpaCy
  - Change `input_fp`, `output_fp`, and `output_mwu_fp` for desired input and output locations.
  - Output: 
    - txt file, with columns `Index, Text, Lemma, POS, USAS Tags`; separated by tabs.
    - However, the POS tags here uses the default SpaCy tagger. We need to utilize CLAWS POS tagging.
    - The CLAWS POS tagged documents are stored in claws_pos.txt
  - Side note: USAS semantic tags does not work for hyphenated words.
    - Thus, the all hyphenated words are tokenized to three parts.

CLAWS POS Tags
--
- Used online CLAWS web tagger for POS tagging https://ucrel-api.lancaster.ac.uk/claws/free.html
  - Parameter: C7, horizontal
  - Modified punctuation: Place a space before and after `'.', ',', '(', ')', '!', ';', ':', ' '/', and '-' (with whitespace before it, i.e., -quart)`
  - The tagger conduct sentence splitting. Thus added term `NEWRECIPE.` to the end of each recipe for separation.
  - C7 tagset can be found here: https://ucrel.lancs.ac.uk/claws7tags.html
- Convert CLAWS output to conll format
  - Run `parse_claws_to_conll`
  - Modify `input` and `output` to their desired locations.
    - Current output file is claws_pos_conll.txt
  - It will output columns `Index, Text, POS CLAWS`
- Side note: CLAWS tokenization is similar to coreNLP. When post-processing tag sets, first align index of claws and coreNLP outputs, then match USAS for semantics.

Create coreNLP Tags
--
- Download coreNLP from https://stanfordnlp.github.io/CoreNLP/
- Requirement: Java 8. If using a higher version of java see coreNLP website for installation instructions.
- Steps to use coreNLP and generate desired tags.
  - Modified punctuation as CLAWS
  - Run `./corenlp.sh -file input.txt` to ensure successful installation.
    - Make sure you are in the stanford-corenlp-xxx folder when executing above line.
  - Import desired text to the stanford_corenlp-xxx folder.
  - Run `./corenlp.sh -annotators tokenize,pos,lemma -ssplit.eolonly true -outputFormat conll -output.columns idx,word,lemma,pos -file YOUR_FILE.txt`
    - This will output a conll file with columns `idx,word,lemma,pos`
    - `Tokenize` integrated sentence splitting as default. We included `-ssplit.eolonly true` to enforce `ssplit` to split sentences only on new line character. This allows one recipe (which is multiple sentences in one line) to be considered as one entry.
    - As coreNLP sometimes split words with '-' into two/three words. To align with CLAWS, we use `-tokenize.options splitHyphenated=false` to keep hyphenated words as one word.

Modified Tags/Post-processing
--
- This combines the CLAWS POS tags with coreNLP tags.
- Steps to conduct post-processing
  - Requirements: pandas
  - Run `post_processing_FoodIE`
  - Contain a section to ensure the two tag files are aligned. Run the sanity check prior to "Main algorithm".
    - If unmatch is found, a short message with `index` and `text` from both documents will be printed.
    - No printed output indicate successful alignment. Proceed to main algorithm.

Join USAS semantic and POS tags
--
 This combines the USAS semantic tags with modified POS.
- Steps to conduct joining
  - Requirements: pandas
  - Run `join_usas_modified_pos`
  - Contain 2 sections to ensure the two tag files are aligned. Run the sanity check prior to "Main algorithm".
    - Section 1
      - Generate the modified USAS semantic tags
      - Combine hyphenated words as one word
      - Combine words with 're' into one word
      - Combine words ending in 'nt', excluding 'dont', into one word
    - Section 2
      - Check if there are misalignments between USAS and modified POS tags
      - If unmatch is found, a short message with `index` and `text` from both documents will be printed.
      - No printed output indicate successful alignment. Proceed to main algorithm.

Get Extracted Food Entities
--
This is the last step of the FoodIE algorithm, which implements the rules defined for identifying food entities.
- Steps to conduct entity identification
  - Run `extracting_concepts_FoodIE`
  - Multiple functions are defined to support `main()`
  - Two sections are within main function
    - Section 1
      - Generate the rule tags for each of the tokens.
      - 4 categories/rules are applied.
      - This will output a DataFrame with columns, `Index, Text, Lemma, POS, Semantics, Food Token, Object Token, Color Noun, Explicitly Disallowed`.
        - Last 4 columns are newly generated in section 1.
        - Last 4 columns will return 'T' for rule to be ture, and 'F' for rule to be false. No null values are given.
    - Section 2
      - Determine which token(s) are food entities.
      - Entities from different recipes are separated by new line.