This project is based on the inspiration from the paper, "[Matching the Blanks: Distributional Similarity for Relation Learning](https://arxiv.org/pdf/1906.03158.pdf)" published in ACL 2019. 

Before zeroing on this approach, I had considered two other approaches for this project. Below are them, with their papers:
1. [LEVERAGING SEMANTIC PARSING FOR
RELATION LINKING OVER KNOWLEDGE BASES](https://arxiv.org/pdf/2009.07726.pdf)
2. [Transition words based link prediction](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7153060/#:~:text=Transition%20words%20are%20used%20to,information%20in%20the%20second%20sentence.) 


### Download all the models from this [link](https://drive.google.com/drive/folders/14gg832CJ39CosbGGgY3VHRo4A9hdvjSz?usp=sharing)

1. Run Python main.py

#### Requirements:
Python: 3.6+
Spacy: 2.1.8+
Pytorch: 1.7.0+

The following steps are involved in the process of creation of graphs:
1. Masking the entities extracted based on Spacy's dependency Parsing and POS tagging linguistic features from the reddit dumps.
2. Fine tuning on the Semeval 2010 relation extraction paper.
3. Based on spacy's linguistic features, we can automatically annotate and infer the relationship between  the extracted entities using the pretrained model.

Training Stages:
1. The objective here is that given a relation pair, predict a relation type from a fixed dictionary of relation types. For ex: "Cause-Effect" is one among the fixed dictionary of relation types from the SemEval 2010 Task 8.
2. 


--contd...



