import re

def find_exact_word_in_file(file_path, target_word):
    # Use rf"" for a raw f-string so \b is treated as a regex word boundary, not a backspace
    pattern = rf"\b{target_word}\b"

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # re.search checks if the pattern exists anywhere in the line
            line = line.lower()
            if re.search(pattern, line):
                print(f"{line.strip()}")


# Example Usage
find_exact_word_in_file("paragraphs.txt", "marcus")
