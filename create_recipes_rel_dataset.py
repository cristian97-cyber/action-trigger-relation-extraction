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


def main():
    parser = ArgumentParser()
    parser.add_argument("--input_file", type=str, default="./data/recipes/recipes_all.csv", help="Input dataset")
    parser.add_argument("--output_file", type=str, help="Output dataset")
    parser.add_argument("--start_index", type=int, default=0, help="Start index from input dataset from which "
                                                                   "generate relations")
    parser.add_argument("--end_index", type=int, default=1000, help="End index from input dataset from which generate "
                                                                    "relations")

    args = parser.parse_args()

    recipes_all = pd.read_csv(args.input_file)
    relations = list()

    for i in range(args.start_index, args.end_index):
        action_desc = recipes_all["actionDesc"][i]
        action_channel = recipes_all["actionChannelTitle"][i]

        for j in range(args.start_index, args.end_index):
            trigger_desc = recipes_all["triggerDesc"][j]
            trigger_channel = recipes_all["triggerChannelTitle"][j]

            if action_channel == trigger_channel:
                formatted_action = format_desc(action_desc, action_channel)
                formatted_trigger = format_desc(trigger_desc, trigger_channel)
                relation = f"{formatted_action} and {formatted_trigger}."

                if "[E1]" not in relation or "[E2]" not in relation:
                    continue

                already_added = False
                for found_rel in relations:
                    if relation == found_rel[0]:
                        already_added = True
                        break

                if not already_added:
                    relations.append([f"{formatted_action} and {formatted_trigger}."])
                    print(f"{i}-{j}")

    recipes_rel = pd.DataFrame(relations, columns=["desc"])
    recipes_rel.to_csv(args.output_file, index=False)


if __name__ == "__main__":
    main()
