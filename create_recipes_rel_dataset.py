import random
import pandas as pd
from argparse import ArgumentParser


def format_desc(desc, channel):
    formatted = desc.split(".")[0]

    formatted = formatted.replace("This Action", "This action").replace("This Trigger", "this trigger")
    formatted = formatted.replace("action", "[E1]action[/E1]").replace("trigger", "[E2]trigger[/E2]")

    channel_words = channel.split(" ")
    found = False
    for word in channel_words:
        if word.lower() in formatted.lower():
            found = True
            break

    if not found:
        formatted += f" on {channel}"

    return formatted


def create_rel(action_desc, action_channel, trigger_desc, trigger_channel, relations):
    formatted_action = format_desc(action_desc, action_channel)
    formatted_trigger = format_desc(trigger_desc, trigger_channel)
    relation = f"{formatted_action} and {formatted_trigger}."

    if relation.count("[E1]") != 1 or relation.count("[E2]") != 1:
        return None

    already_added = False
    for found_rel in relations:
        if relation == found_rel[0]:
            already_added = True
            break

    if not already_added:
        return relation
    else:
        return None


def main():
    parser = ArgumentParser()
    parser.add_argument("--input_file", type=str, default="./data/recipes/recipes_all.csv", help="Input dataset")
    parser.add_argument("--output_file", type=str, help="Output dataset")
    parser.add_argument("--start_index", type=int, default=0, help="Start index from input dataset from which "
                                                                   "generate relations")
    parser.add_argument("--end_index", type=int, default=1000, help="End index from input dataset from which generate "
                                                                    "relations")
    parser.add_argument("--shared_channel", type=int, default=1,
                        help="(1: ACTION AND TRIGGER MUST SHARE THE CHANNEL, 0: "
                             "ACTION AND TRIGGER DON'T NECESSARILY HAVE TO SHARE THE CHANNEL)")
    parser.add_argument("--max_rel_number", type=int, default=200,
                        help="MAX NUMBER OF RELATIONS THAT WILL BE FOUND, "
                             "IT WILL BE USED ONLY WHEN SHARED CHANNEL IS 0, DEFAULT IS 200")

    args = parser.parse_args()

    recipes_all = pd.read_csv(args.input_file)
    relations = list()

    if args.shared_channel == 0:
        while len(relations) < args.max_rel_number:
            action_index = random.randint(args.start_index, args.end_index)
            trigger_index = random.randint(args.start_index, args.end_index)

            action_desc = recipes_all["actionDesc"][action_index]
            action_channel = recipes_all["actionChannelTitle"][action_index]
            trigger_desc = recipes_all["triggerDesc"][trigger_index]
            trigger_channel = recipes_all["triggerChannelTitle"][trigger_index]

            relation = create_rel(action_desc, action_channel, trigger_desc, trigger_channel, relations)

            if relation is not None:
                relations.append([relation])
                print(f"{action_index}-{trigger_index}")

    if args.shared_channel == 1:
        for i in range(args.start_index, args.end_index):
            action_desc = recipes_all["actionDesc"][i]
            action_channel = recipes_all["actionChannelTitle"][i]

            for j in range(args.start_index, args.end_index):
                trigger_desc = recipes_all["triggerDesc"][j]
                trigger_channel = recipes_all["triggerChannelTitle"][j]

                if action_channel != trigger_channel:
                    continue

                relation = create_rel(action_desc, action_channel, trigger_desc, trigger_channel, relations)

                if relation is not None:
                    relations.append([relation])
                    print(f"{i}-{j}")

    recipes_rel = pd.DataFrame(relations, columns=["desc"])
    recipes_rel.to_csv(args.output_file, index=False)


if __name__ == "__main__":
    main()
