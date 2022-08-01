import pandas as pd
from argparse import ArgumentParser


def get_output(dataset, num_elements, prev_elements=None):
    output = ""
    for i in range(num_elements):
        row_num = i + 1 if prev_elements is None else prev_elements + i + 1
        row_desc = dataset["desc"][i].replace("[E1]", "<e1>").replace("[/E1]", "</e1>").replace("[E2]", "<e2>").replace("[/E2]", "</e2>")
        row_rel = dataset["rel"][i]

        output += f"{row_num}\t\"{row_desc}\"\n{row_rel}\nComment:\n\n"

    return output


def write_output_file(filename, output):
    f = open(filename, "w", encoding="utf-8")
    f.write(output)
    f.close()


def balance_data(dataset):
    data = dataset.values.tolist()
    cause_effects = others = 0

    for item in data:
        if item[2] == "Cause-Effect(e1,e2)":
            cause_effects += 1
        else:
            others += 1

    while cause_effects < others:
        i = 0
        while i < len(data):
            if data[i][2] == "Other":
                data.pop(i)
                others -= 1
            else:
                i += 1

            if cause_effects >= others:
                break

    for i in range(len(data)):
        data[i] = [data[i][1], data[i][2]]

    return pd.DataFrame(data, columns=["desc", "rel"])


def main():
    parser = ArgumentParser()
    parser.add_argument("--train_input_file", type=str, help="Input dataset containing training labelled data")
    parser.add_argument("--test_input_file", type=str, help="Input dataset containing test labelled data")
    parser.add_argument("--train_output_file", type=str, help="Output file containing training data")
    parser.add_argument("--test_output_file", type=str, help="Output file containing test data")

    args = parser.parse_args()

    train_recipes = pd.read_csv(args.train_input_file)
    test_recipes = pd.read_csv(args.test_input_file)

    train_recipes = train_recipes.sample(frac=1, random_state=1).reset_index()
    train_recipes = balance_data(train_recipes)
    train_recipes = train_recipes.sample(frac=1, random_state=1).reset_index()

    test_recipes = test_recipes.sample(frac=1, random_state=1).reset_index()
    test_recipes = balance_data(test_recipes)
    test_recipes = test_recipes.sample(frac=1, random_state=1).reset_index()

    train_output = get_output(train_recipes, len(train_recipes["desc"]))
    test_output = get_output(test_recipes, len(test_recipes["desc"]), len(train_recipes["desc"]))

    write_output_file(args.train_output_file, train_output)
    write_output_file(args.test_output_file, test_output)


if __name__ == "__main__":
    main()
