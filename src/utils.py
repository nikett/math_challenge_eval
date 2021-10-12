# read csv
# abbreviate second column (take the first char of the string)
import csv


def abbreviate_lname(lname:str) -> str:
    # tabdob => T.
    if not lname:
        return ""
    return f"{str.capitalize(lname[0])}."

def abbreviate_all(input_fp: str, output_fp: str):
    '''

    :param input_fp: "data/todo-abbreviate-lastname.csv"
    :return: a new file with updated record
    '''
    with open(input_fp, 'r') as in_csv:
        with open(output_fp, 'w') as out_csv:
            for d in csv.DictReader(in_csv):
                fl = f'{str.capitalize(d["Student"])} {abbreviate_lname(lname=d["name"])}'.strip()
                out_csv.write(f"{fl}\n")


if __name__ == '__main__':
    abbreviate_all(input_fp="data/todo-abbreviate-lastname.csv",
                   output_fp="data/done-abbreviate-lastname.csv")


