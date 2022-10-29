import pandas as pd
from argparse import ArgumentParser


def main():
    parser = ArgumentParser()
    parser.add_argument("--input_file", type=str, help="Input file")
    parser.add_argument("--output_file", type=str, help="Ouput file, reformatted for baseline")

    args = parser.parse_args()

    dataset = pd.read_csv(args.input_file).values.tolist()
    relations = list()

    for data in dataset:
        relation = data[0].replace("[E1]action[/E1]", "action").replace("[E2]trigger[/E2]", "trigger")
        relations.append([relation])

    dataset_formatted = pd.DataFrame(relations, columns=["desc"])
    dataset_formatted.to_csv(args.output_file, index=False)


if __name__ == "__main__":
    main()
