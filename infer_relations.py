import pandas as pd
from argparse import ArgumentParser
from src.tasks.infer import infer_from_trained


def main():
    parser = ArgumentParser()
    parser.add_argument("--task", type=str, default="semeval", help="semeval, fewrel")
    parser.add_argument("--train_data", type=str, default="./data/SemEval2010_task8_all_data"
                                                          "/SemEval2010_task8_training/TRAIN_FILE.TXT",
                        help="training data .txt file path")
    parser.add_argument("--test_data", type=str, default="./data/SemEval2010_task8_all_data"
                                                         "/SemEval2010_task8_testing_keys/TEST_FILE_FULL.TXT",
                        help="test data .txt file path")
    parser.add_argument("--use_pretrained_blanks", type=int, default=0, help="0: Don't use pre-trained blanks model, "
                                                                             "1: use pre-trained blanks model")
    parser.add_argument("--batch_size", type=int, default=32, help="Training batch size")
    parser.add_argument("--gradient_acc_steps", type=int, default=2, help="No. of steps of gradient accumulation")
    parser.add_argument("--max_norm", type=float, default=1.0, help="Clipped gradient norm")
    parser.add_argument("--fp16", type=int, default=0, help="1: use mixed precision ; 0: use floating point 32")
    parser.add_argument("--num_epochs", type=int, default=11, help="No of epochs")
    parser.add_argument("--lr", type=float, default=0.00007, help="learning rate")
    parser.add_argument("--model_no", type=int, default=0, help="Model ID: 0 - BERT\n1 - ALBERT\n2 - BioBERT")
    parser.add_argument("--model_size", type=str, default="bert-base-uncased", help="For BERT: 'bert-base-uncased', "
                                                                                    "'bert-large-uncased', For "
                                                                                    "ALBERT: 'albert-base-v2_all', "
                                                                                    "'albert-large-v2', For BioBERT: "
                                                                                    "'bert-base-uncased' ("
                                                                                    "biobert_v1.1_pubmed)")
    parser.add_argument("--train", type=int, default=0, help="0: Don't train, 1: train")
    parser.add_argument("--infer", type=int, default=0, help="0: Don't infer, 1: Infer")
    parser.add_argument("--input_dataset", type=str, help="Input dataset from which infer relations")
    parser.add_argument("--output_dataset", type=str, help="Output dataset containing the inferred relations")

    args = parser.parse_args()
    args.num_classes = 2

    inferer = infer_from_trained(args, detect_entities=False)

    recipes = pd.read_csv(args.input_dataset)
    relations = list()

    for i in range(len(recipes["desc"])):
        test = recipes["desc"][i]

        try:
            inferer.infer_sentence(test, relations, detect_entities=False)
        except UnicodeEncodeError:
            print(f"Unicode error with {test}\n")
            relations.append(["Other", test])

    recipes_rel = pd.DataFrame(relations, columns=["rel", "desc"])
    recipes_rel.to_csv(args.output_dataset, index=False)


if __name__ == "__main__":
    main()
