from argparse import ArgumentParser

import pandas as pd


def main():
    parser = ArgumentParser()
    parser.add_argument("--input_file", type=str, help="Input file")
    parser.add_argument("--output_file", type=str, help="Output file")

    args = parser.parse_args()

    dataset = pd.read_csv(args.input_file).values.tolist()
    actions = list()
    triggers = list()

    for data in dataset:
        relation = data[0].lower()
        found = relation.find(" and this")
        if found != -1:
            action = relation.split(" and this")[0]
            trigger = f"this{relation.split(' and this')[1]}"
        else:
            action = relation
            trigger = "MANUAL"

        actions.append(action)
        triggers.append(trigger)

    new_data = {"action": actions, "trigger": triggers}
    dataset_splitted = pd.DataFrame(data=new_data)
    dataset_splitted.to_csv(args.output_file, index=False)


if __name__ == "__main__":
    main()
