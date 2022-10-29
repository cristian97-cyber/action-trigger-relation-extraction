from argparse import ArgumentParser

import pandas as pd


def main():
    parser = ArgumentParser()
    parser.add_argument("--input_file", type=str, help="Input file")
    parser.add_argument("--output_file", type=str, help="Output file")

    args = parser.parse_args()

    dataset = pd.read_csv(args.input_file).values.tolist()
    recipes_all = pd.read_csv("./data/recipes/recipes_all.csv")

    actions = list()
    actions_channel = list()
    triggers = list()
    triggers_channel = list()

    for data in dataset:
        action = data[0]
        action_channel = None
        trigger = data[1]
        trigger_channel = None

        for i in range(0, len(recipes_all.index)):
            if action in recipes_all["actionDesc"][i].lower():
                action_channel = recipes_all["actionChannelTitle"][i]
            if trigger in recipes_all["triggerDesc"][i].lower():
                trigger_channel = recipes_all["triggerChannelTitle"][i]

            if action_channel is not None and trigger_channel is not None:
                break

        actions.append(action)
        actions_channel.append(action_channel)
        triggers.append(trigger)
        triggers_channel.append(trigger_channel)

    new_data = {"action": actions, "action_channel": actions_channel, "trigger": triggers,
                "trigger_channel": triggers_channel}
    dataset_final = pd.DataFrame(data=new_data)
    dataset_final.to_csv(args.output_file, index=False)


if __name__ == "__main__":
    main()
