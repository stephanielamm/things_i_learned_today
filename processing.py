# This script (written mostly by Allan and Ariana) breaks up a fixed width text file into organized chunchs of data 
# The bottom functions spit out a .csv with header rows and data split up according to whitespace and character numbers
# 
#
#
# Imports from python.  # NOQA
import re
import csv


EVALUATION_START_PATTERN = re.compile(r'^ {1,2}201\d\d{4}')
VIOLATION_HEADER_PATTERN_1 = re.compile(
    r'^ {10}Requirement +Code +Status +Description$'
)
VIOLATION_HEADER_PATTERN_2 = re.compile(r'^ {33,42}Violation +Violation$')
VIOLATION_START_PATTERN = re.compile(r'^ {10}((Title)|\d+)')


def get_pages(content_lines):
    page_starts = [
        i for i, line in enumerate(content_lines)
        if line.startswith('\x0c')
    ]

    pages = []

    first_line_of_page = 0
    for page_num0, last_line_of_page in enumerate(page_starts):
        pages.append(
            (
                page_num0 + 1,
                content_lines[first_line_of_page:last_line_of_page]
            )
        )
        first_line_of_page = last_line_of_page

    return pages


def get_all_lines(paged_content):
    headerless_pages = [
        (page_id, lines[7:]) for page_id, lines in paged_content
    ]

    return [
        line
        for pagenum, lines in headerless_pages
        for line in lines
    ]


def get_evaluations(lines):
    eval_starts = [
        i for i, line in enumerate(lines)
        if EVALUATION_START_PATTERN.search(line) is not None
    ]

    evals = []

    for index, first_line_num in enumerate(eval_starts):
        next_index = index + 1

        if (next_index == len(eval_starts)):
            # On the last iteration, get all remaining lines.
            last_line_num = len(lines)
        else:
            last_line_num = eval_starts[next_index]

        evals.append((
            lines[first_line_num],
            # lines[first_line_num + 1:last_line_num]
            [
                line for line in lines[first_line_num + 1:last_line_num]
                if VIOLATION_HEADER_PATTERN_1.search(line) is None
                and VIOLATION_HEADER_PATTERN_2.search(line) is None
                and line != '\n'
            ]
        ))

    return evals


def format_evaluations(raw_evaluations):
    formatted_evaluations = []

    for evaluation_meta, violation_lines in raw_evaluations:
        formatted_violations = []
        current_formatted_violation = ''

        for i, violation_line in enumerate(violation_lines):
            if VIOLATION_START_PATTERN.search(
                violation_line
            ) is not None and current_formatted_violation != '':
                formatted_violations.append(
                    current_formatted_violation.strip()
                )
                current_formatted_violation = violation_line.strip()
            else:
                current_formatted_violation = '{} {}'.format(
                    current_formatted_violation,
                    violation_line.strip()
                )

            if (i + 1) == len(violation_lines):
                formatted_violations.append(
                    current_formatted_violation.strip()
                )

        formatted_evaluations.append(
            (evaluation_meta.strip(), formatted_violations)
        )

    return formatted_evaluations


def transform():
    with open('processed/Evals.layout.txt', 'r') as layout_text:
        content_lines = layout_text.readlines()

    paged_lines = get_pages(content_lines)
    all_lines = get_all_lines(paged_lines)
    limited_lines = all_lines[1:-3]  # Discard first and last three lines.

    # The 'evals' variable is a list containing one tuple for every evaluation.
    # These tuples contain a string (representing the evaluation metadata) and
    # a list of strings (where each string represents a violation raised in
    # this evaluation).
    raw_evaluations = get_evaluations(limited_lines)
    formatted_evaluations = format_evaluations(raw_evaluations)


    return formatted_evaluations

# if__name == '__main__' means that if you just type python filename.py, it'll run this function.
if __name__ == '__main__':
    separated_data = transform()

    # https://docs.python.org/2/library/csv.html writes a new file with the followingheader names 
    with open('clean_fields.csv', 'w') as csvfile:
        fieldnames = ['evaluation_id', 'company_id', 'city', 'begin_eval_date', 'end_eval_date', 'eval_type', 'ip_id' , 'violation_metadata']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        # split by whitespace if there are two or more characters of whitespace. Breaks it for object 0 starting at character 23. 
        for d in separated_data:
            metadata = re.split(r'\s{2,}', d[0][23:])
            
            # .pop removes or returns the last item in a list https://docs.python.org/3.4/tutorial/datastructures.html 
            if metadata[0] == '':
                metadata.pop(0)
            writer.writerow({
                'evaluation_id': d[0][:8], #splits on specified characters
                'company_id': d[0][8:23].strip(), 
                'city': metadata[0].strip(), #first set of whitespace-separated characters
                'begin_eval_date': metadata[1],
                'end_eval_date': metadata[2],
                'eval_type': metadata[3],
                'ip_id': metadata[4],
                'violation_metadata': d[1]
                })


