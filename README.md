# Markov-chain-text-generator
This is text generator based on order-2 markov chain.

`lib` directory is an example of small text corpus.

### Modules

Please modify `path.py` to specify pathes to the corpus of texts, stop words and pathes to saved data. 

`preprocessing_tools.py` - module with methods for text file preprocessing,

`worddict_tools.py` - module for collecting word dictionary and word frequency dictionary,

`generating_tools.py` - module for text generation.

### Run

To collect a word frequency dictionary run

    python worddict_tools.py

To generate text using saved word frequency dictionary run

    python generating_tools.py
