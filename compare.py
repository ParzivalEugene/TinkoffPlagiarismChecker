import argparse
import tokenize
import io


def LevenshteinDistance(text1: str, text2: str) -> int:
    """Calculate Levenshtein distance between two strings."""
    m, n = len(text1), len(text2)
    table = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        table[i][0] = i
    for j in range(n + 1):
        table[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                table[i][j] = table[i - 1][j - 1]
            else:
                table[i][j] = 1 + min(
                    table[i - 1][j], table[i][j - 1], table[i - 1][j - 1]
                )

    return table[-1][-1]


def remove_docstring(text: str) -> str:
    """Remove docstring from text."""
    editted_text = text.replace("'''", '"""')
    editted_text = editted_text.split('"""')
    editted_text = editted_text[::2] if text.startswith('"""') else editted_text[1::2]
    return "".join(editted_text)


def remove_comments(text: io.TextIOWrapper) -> str:
    """Remove comments from text."""
    tokens = tokenize.generate_tokens(text.readline)
    editted_text = ""
    for token in tokens:
        if token.type == tokenize.COMMENT:
            continue
        editted_text += token.string
    return editted_text


def remove_spaces(text: str) -> str:
    """Remove spaces from text."""
    return text.replace(" ", "").replace("\n", "")


def clear(text: io.TextIOWrapper) -> str:
    """Clear text from comments, docstrings and spaces."""
    return remove_spaces(remove_docstring(remove_comments(text)))


def compare(input_text1: io.TextIOWrapper, input_text2: io.TextIOWrapper) -> float:
    """Compare two texts."""
    text1 = clear(input_text1)
    text2 = clear(input_text2)
    distance = LevenshteinDistance(text1, text2)
    return 1 - distance / max(len(text1), len(text2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare two files")
    parser.add_argument("input_file", type=str, help="First file")
    parser.add_argument("output_file", type=str, help="Second file")
    args = parser.parse_args()

    with open(args.input_file, "r", encoding="utf-8") as input_file, open(
        args.output_file, "x", encoding="utf-8"
    ) as output_file:
        input_text = input_file.read()
        tests = input_text.split("\n")

        for test in tests:
            original, plagiarized = test.split()
            with open(original, "r", encoding="utf-8") as original_file, open(
                plagiarized, "r", encoding="utf-8"
            ) as plagiarized_file:
                result = compare(original_file, plagiarized_file)
                output_file.write(f"{result:.2f}\n")
