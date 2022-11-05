import random
import json
import pandas as pd
from argparse import ArgumentParser


def is_channel_shared(actions, triggers):
    for action in actions:
        action_channel = action["actionChannelTitle"]

        for trigger in triggers:
            trigger_channel = trigger["triggerChannelTitle"]

            if action_channel == trigger_channel:
                return True

    return False


def format_desc(desc):
    formatted = desc.split(".")[0]
    formatted = formatted.replace("Action", "action").replace("Trigger", "trigger")
    formatted = formatted.replace("action", "[E1]action[/E1]").replace("trigger", "[E2]trigger[/E2]")

    return formatted


def create_rel(actions, triggers, relations):
    actions_desc = ""
    triggers_desc = ""

    for action in actions:
        desc = format_desc(action["actionDesc"])

        if desc.count("[E1]") != 1:
            return None
        elif len(actions_desc) == 0:
            actions_desc = desc
        else:
            actions_desc = f"{actions_desc}___{desc}"

    for trigger in triggers:
        desc = format_desc(trigger["triggerDesc"])

        if desc.count("[E2]") != 1:
            return None
        elif len(triggers_desc) == 0:
            triggers_desc = desc
        else:
            triggers_desc = f"{triggers_desc}___{desc}"

    for relation in relations:
        relation_action = relation[0]
        relation_trigger = relation[1]

        if actions_desc == relation_action or triggers_desc == relation_trigger:
            return None

    return [actions_desc, triggers_desc]


def main():
    parser = ArgumentParser()
    parser.add_argument("--input_file", type=str, help="Input dataset")
    parser.add_argument("--output_file", type=str, help="Output dataset")
    parser.add_argument("--max_rel_number", type=int, default=200,
                        help="MAX NUMBER OF RELATIONS THAT WILL BE FOUND, "
                             "IT WILL BE USED ONLY WHEN SHARED CHANNEL IS 0, DEFAULT IS 200")

    args = parser.parse_args()

    f = open(args.input_file, encoding="utf8")
    data = json.load(f)
    relations = list()

    while len(relations) < args.max_rel_number:
        actions_index = random.randint(0, 70000)
        triggers_index = random.randint(0, 70000)

        actions = data["recipes"][actions_index]["actions"]
        triggers = data["recipes"][triggers_index]["triggers"]

        if len(actions) <= 1 and len(triggers) <= 1 or not is_channel_shared(actions, triggers):
            continue

        relation = create_rel(actions, triggers, relations)
        if relation is not None:
            relations.append(relation)
            print(f"{len(relations)}")

    recipes_rel = pd.DataFrame(relations, columns=["actions", "triggers"])
    recipes_rel.to_csv(args.output_file, index=False)


if __name__ == "__main__":
    main()
