import nltk
import pandas as pd
import stanza
from argparse import ArgumentParser
from nltk.corpus import wordnet


def get_main_verb(doc):
    main_verb = None

    for sent in doc.sentences:
        for word in sent.words:
            if word.upos == "VERB":
                if main_verb is None or word.head < main_verb.head:
                    main_verb = word

    return main_verb


def get_verbs(main_verb):
    verbs = list()
    if main_verb is None:
        return verbs

    syns = wordnet.synsets(main_verb.lemma)
    for syn in syns:
        verbs.append(syn.lemmas()[0].name())

    return list(dict.fromkeys(verbs))


def main():
    parser = ArgumentParser()
    parser.add_argument("--input_file", type=str, help="Input file")
    parser.add_argument("--output_file", type=str, help="Output file")

    args = parser.parse_args()

    recipes = pd.read_csv(args.input_file)
    relations = list()

    nlp = stanza.Pipeline(lang="en", processors="tokenize,mwt,pos,lemma,depparse", download_method=None)
    nltk.download("wordnet")
    nltk.download("omw-1.4")

    for i in range(len(recipes["action"])):
        action = recipes["action"][i]
        action_channel = recipes["action_channel"][i]
        trigger = recipes["trigger"][i]
        trigger_channel = recipes["trigger_channel"][i]

        if action_channel != trigger_channel:
            relations.append(["Other", f"{action} and {trigger}"])
            continue

        action_doc = nlp(action)
        trigger_doc = nlp(trigger)

        action_main_verb = get_main_verb(action_doc)
        trigger_main_verb = get_main_verb(trigger_doc)

        action_verbs = get_verbs(action_main_verb)
        trigger_verbs = get_verbs(trigger_main_verb)

        found = False
        for action_verb in action_verbs:
            for trigger_verb in trigger_verbs:
                if action_verb == trigger_verb:
                    found = True
                    break
            if found:
                break

        if found:
            relations.append(["Cause-Effect(e1,e2)", f"{action} and {trigger}"])
        else:
            relations.append(["Other", f"{action} and {trigger}"])

    recipes_rel = pd.DataFrame(relations, columns=["rel", "desc"])
    recipes_rel.to_csv(args.output_file, index=False)


if __name__ == "__main__":
    main()
