# MDAproject

Group: New-Zealand

Topic: Politicians and Climate Change

Members: Kendall	Brown, Balazs	Fazekas, Yang	He, Yuanyuan	Li, Chiel	Mues

### Main topic: Politicians and climate 
Original data link: [link](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/0TJX8Y)

### Requirements for Topic Modelling

```
- Jupyter
- Gensim Version (>=0.13.1 would be preferred since we will be using topic coherence briefly)
- matplotlib
- spaCy
- pyLDAVis
- numpy
- pandas
- seaborn
- smart_open
- nltk
```

In case the user finds it difficult to download any of the above, there will be a Jupyter Notebook with all the cells already run, so you can just follow the same.


### Setup

- Start by cloning the repo using

`git clone https://github.com/Kenbrown3/MDAproject`

- Go into the `notebook/` directory

- Install `virtualenv` using

`pip install virtualenv`

- Start the environment with

```
virtualenv venv
source venv/bin/activate
```

- Download requirements with  `pip install -r REQUIREMENTS.txt`

Alternatively, if you are using anaconda as your virtual environment, running `conda install gensim` and `conda install spacy` should also do the trick.

### LDA Topic Modeling

For the LDA Topic Modeling Project, you will be following the same instructions as above, but will need to run

`pip install -r REQUIREMENTS.txt`

Alternatively, you can look up which of the libraries you would still need to download and go ahead and just download those.

### Downloading spaCy language model

We will be using the spaCy English language model, so we will be needing to download it first.
This [link](https://spacy.io/usage/models) contains instructions to download this model. You can also run the following code in notebook:

```python
import spacy
from spacy.cli import download
spacy.load('en_core_web_sm')
```
### LDA Mallet loading instruction
- To load LDA Mallet, it's advised to use gensim 3.8 to apply `gensim.wrapper( )`. 
- The Java JDK needs to be downloaded before running the Mallet script. Mallet script is Java based and you need to check whether Java has been installed in you computer. If you are mac user, trying to run `java -version` in your terminal. You can follow this [link](https://www.gitmemory.com/issue/RaRe-Technologies/gensim/2851/756970247) for more details
- You can download Mallet via [link](http://mallet.cs.umass.edu/)
- To successfully run the Mallet script, follow the following code to run it in notebook

**Windows**
```python
import os
os.environ.update({'MALLET_HOME':r'C:/Users/Desktop/mallet-2.0.8/'})

mallet_path = 'C:\Users\Desktop\mallet-2.0.8\bin\mallet' # update this path

```
**Mac**
```python
import os
os.environ.update({'MALLET_HOME':r'/User/Desktop/new_mallet/mallet-2.0.8/'})
mallet_path = '/Users/Desktop/new_mallet/mallet-2.0.8/bin/mallet

```


