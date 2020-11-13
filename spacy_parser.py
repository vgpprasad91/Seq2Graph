import database

import spacy

nlp = spacy.load("en_core_web_sm")


class SpacyParser:
    """
    """

    __identifier__ = 'spacy'

    def __init__(self, model='en'):
        """
        Args:
            model (str): a spec for the spaCy model. (default: en). Please refer to the
            official website of spaCy for a complete list of the available models.
            This option is useful if you are dealing with languages other than English.
        """

        self.model = model
        self.doc = None
        self.sentence = None
        self.relation = None
        self.relations = []
        self.fake_noun = set()
        self.filtered_relations = []

        self.nlp = spacy.load(model)

    @staticmethod
    def __locate_noun(chunks, i):
        for j, c in enumerate(chunks):
            if c.start <= i < c.end:
                return j
        return None

    def _get_entity_matches(self, token, entity_dict):
        if token.dep_ == "compound":
            entity_dict["root_lemma"] = token.lemma_ + " " + entity_dict["root_lemma"]
            entity_dict["head"] = token.text + " " + entity_dict["head"]
        elif token.dep_ in ['det','nummod','amod']:
            entity_dict["mod"].append({'span_text': token.text, 'lemma_span': token.lemma_, 'dep_': token.dep_})
        return entity_dict

    def _get_entity_type(self, entity_dict):
        head = entity_dict["root_lemma"].split(' ')[-1]
        s = database.load_list('scene-nouns.txt')
        if entity_dict["root_lemma"] in s or head in s:
            entity_dict['type'] = 'scene'
        else:
            entity_dict['type'] = 'unknown'
        return entity_dict

    def _parse_entities(self):
        entities = []
        entity_chunks = []
        for entity in self.doc.noun_chunks:
            if entity != None:
                if entity.root.lemma_ == '-PRON-': continue
                entity_dict = { "span":entity.text,
                                "range": (entity.start, entity.end),
                                "head":entity.root.text,
                                "root_lemma": entity.root.lemma_,
                                "lemma":entity.lemma_,
                                "mod":[]}
                for child in entity.root.children:
                    entity_dict_copy = self._get_entity_matches(child, entity_dict)
                    if entity_dict_copy != None:
                        entity_dict_copy = self._get_entity_type(entity_dict_copy)
                try:
                    entities.append(entity_dict_copy)
                    entity_chunks.append(entity)
                except:
                    entities.append(entity_dict)
                    entity_chunks.append(entity)
        return entities, entity_chunks

    def _get_verb_subj(self):
        subj_rel = {}
        for token in self.doc:
            if token.dep_ == "nsubj": subj_rel[token.head.i] = token.i
            elif token.dep_ == "acl": subj_rel[token.i] = token.head.i
            elif token.dep_ == 'pobj':
                if token.head.dep_ == 'agent' and token.head.head.pos_ == 'VERB':
                    subj_rel[token.head.head.i] = token.i
        return subj_rel

    def _get_direct_object_relations(self, subj_rel, token):
        return {
            'subj': subj_rel[token.root.head.i],
            'obj': token.root.i,
            'rel': token.root.head.text,
            'lemma_': token.root.head.lemma_
        }

    def _get_verb_obj_relations(self, subj_rel, token):
        return {
            'subj': subj_rel[token.root.head.head.i],
            'obj': token.root.i,
            'rel': token.root.head.head.text + ' ' + token.root.head.text,
            'lemma_': token.root.head.head.lemma_ + ' ' + token.root.head.lemma_
        }

    def _get_clausal_modifier(self, subj_rel, token):
        return {
            'subj': subj_rel[token.root.head.head.i],
            'obj': token.root.i,
            'rel': token.root.head.text,
            'lemma_': token.root.head.lemma_
        }

    def _get_prep_obj_relations(self, token):
        return {
            'subj': token.root.head.head.head.head.i,
            'obj': token.root.i,
            'rel': self.doc[token.root.head.head.head.i:token.root.head.i + 1].text,
            'lemma_': self.doc[token.root.head.head.head.i:token.root.head.i].lemma_
        }

    def _get_noun_tags(self, token):
        return {
            'subj': token.root.head.head.i,
            'obj': token.root.i,
            'rel': token.root.head.text,
            'lemma_': token.root.head.lemma_
        }

    def _get_noun_modifier(self, token):
        return {
            'subj': token.root.head.head.head.i,
            'obj': token.root.i,
            'rel': token.root.head.head.text + ' ' + token.root.head.text,
            'lemma_': token.root.head.head.lemma_ + ' ' + token.root.head.lemma_
        }

    def _get_verb_modifier(self, subj_rel, token):
        return {
            'subj': subj_rel[token.root.head.head.head.i],
            'obj': token.root.i,
            'rel': token.root.head.head.text + ' ' + token.root.head.text,
            'lemma_': token.root.head.head.lemma_ + ' ' + token.root.head.lemma_
        }

    def _get_verb_dependency(self, subj_rel, token):
        return {
            'subj': subj_rel[token.root.head.head.i],
            'obj': token.root.i,
            'rel': token.root.head.text,
            'lemma_': token.root.head.lemma_
        }

    def _get_nominal_subj_dependency(self, subj_rel, token):
        return {
            'subj': subj_rel[token.root.head.i],
            'obj': token.root.i,
            'rel': token.root.head.text,
            'lemma_': token.root.head.lemma_
        }

    def _filter_prep_objects(self, head, head2, head3, head_dep, head_dep2, head_pos_2, head_pos_3, \
                             lemma_head_1, lemma_head_2, subj_rel, entity):
        if head_dep == 'agent':
            pass
        elif (head_pos_2 == 'VERB' and head2.i + 1 == head.i and \
              database.is_phrasal_verb(lemma_head_2 + ' ' + lemma_head_1)
        ) and head2.i in subj_rel:
            self.relation = self._get_verb_obj_relations(subj_rel, entity)
        elif (head_pos_2 == 'VERB' or head_dep2 == 'acl') and head2.i in subj_rel:
            self.relation = self._get_clausal_modifier(subj_rel, entity)
        elif (head_dep2 == 'pobj' and \
              database.is_phrasal_prep(self.doc[head3.i:head.i + 1].lower_)):
            self.fake_noun.add(head2.i)
            self.relation = self._get_prep_obj_relations(entity)
        elif head_pos_2 == 'NOUN':
            self.relation = self._get_noun_tags(entity)
        elif head_dep2 in ('amod', 'advmod') and head_pos_3 == 'NOUN':
            self.relation = self._get_noun_modifier(entity)
        elif head_dep2 in ('amod', 'advmod') and head_pos_3 == 'VERB' and head3.i in subj_rel:
            self.relation = self._get_verb_modifier(subj_rel, entity)
        elif head_dep2 == 'VERB' and head2.i in subj_rel:
            self.relation = self._get_verb_dependency(subj_rel, entity)

    def _get_subj_obj_relations(self, subj_rel):
        for entity in self.doc.noun_chunks:
            head = entity.root.head
            head2 = entity.root.head.head
            head3 = entity.root.head.head.head
            root_dep = entity.root.dep_
            head_dep = entity.root.head.dep_
            head_dep2 = entity.root.head.head.dep_
            head_pos_2 = entity.root.head.head.pos_
            head_pos_3 = entity.root.head.head.head.pos_
            lemma_head_1 = entity.root.head.lemma_
            lemma_head_2 = entity.root.head.head.lemma_
            if root_dep in ('dobj', 'attr') and head.i in subj_rel:
                self.relation = self._get_direct_object_relations(subj_rel, entity)
            elif root_dep == 'pobj':
                self._filter_prep_objects(head, head2, head3, head_dep, head_dep2, head_pos_2, head_pos_3, \
                                     lemma_head_1, lemma_head_2, subj_rel, entity)
            elif root_dep == 'nsubjpass' and head.i in subj_rel:
                self.relation = self._get_nominal_subj_dependency(subj_rel, entity)
            if self.relation is not None: self.relations.append(self.relation)

    def _relation_extraction(self, entities, entity_chunks):
        entities = [e for e, ec in zip(entities, entity_chunks) if ec.root.i not in self.fake_noun]
        entity_chunks = [ec for ec in entity_chunks if ec.root.i not in self.fake_noun]
        for relation in self.relations:
            # Use a helper function to map the subj/obj represented by the position
            # back to one of the entity nodes.
            try:
                relation['subj'] = self.__locate_noun(entity_chunks, relation['subj'])
                relation['obj'] = self.__locate_noun(entity_chunks, relation['obj'])
            except:
                pass
            if relation['subj'] != None and relation['obj'] != None:
                self.filtered_relations.append(relation)

        return {'entities': entities, 'relations': self.filtered_relations}

    def parse_sent(self, sentence):
        self.sentence = sentence
        self.doc = self.nlp(self.sentence)
        entities, entity_chunks = self._parse_entities()
        subj_rel = self._get_verb_subj()
        self._get_subj_obj_relations(subj_rel)
        return self._relation_extraction(entities, entity_chunks)

    @staticmethod
    def __locate_noun(chunks, i):
        for j, c in enumerate(chunks):
            if c.start <= i < c.end:
                return j
        return None

