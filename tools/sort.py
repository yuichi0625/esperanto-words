import argparse
import locale
from collections import defaultdict
from pathlib import Path
from typing import List

locale.setlocale(locale.LC_ALL, '')

sep2cat = {
    "'o'j": "'oj",
    "'o'j'n": "'ojn",
    "'o'n": "'on",
    "'a'j": "'aj",
    "'a'j'n": "'ajn",
    "'a'n": "'an",
    "'e'n": "'en"}


def pretty_sort(rows: List[str]) -> List[str]:
    """
    rows = e.g. ["katajn\tkat'ajn", "katidajn\tkat'id'ajn", ...]
    """
    result = []

    def sort(rows: List[str], index: int = 0) -> None:
        morph2rows_end = defaultdict(list)
        morph2rows_next = defaultdict(list)
        for row in rows:
            annot = row.split('\t')[1].split("'")
            if index != 0 and len(annot) <= index + 1:
                morph = '-' if len(annot) < index + 1 else annot[index]
                morph2rows_end[morph].append(row)
            else:
                morph2rows_next[annot[index]].append(row)

        for m in sorted(list(morph2rows_end.keys()), key=locale.strxfrm):
            result.extend(sorted(morph2rows_end[m], key=locale.strxfrm))

        for m in sorted(list(morph2rows_next.keys()), key=locale.strxfrm):
            sort(morph2rows_next[m], index + 1)

    sort(rows)

    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_dir', default='../annotations')
    args = parser.parse_args()

    for filename in Path(args.input_dir).glob('*.txt'):
        with open(filename, encoding='utf-8') as f:
            text = f.read()

        rows = []
        for row in text.split('\n'):
            for sep, cat in sep2cat.items():
                if row.endswith(sep):
                    row = row[:-len(sep)] + cat
            rows.append(row)

        sorted_rows = pretty_sort(rows)

        result_rows = []
        for row in sorted_rows:
            for sep, cat in sep2cat.items():
                if row.endswith(cat):
                    row = row[:-len(cat)] + sep
            result_rows.append(row)

        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(result_rows))


if __name__ == '__main__':
    main()
