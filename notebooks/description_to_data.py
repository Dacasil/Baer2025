from docx import Document
import pandas as pd
import re


def parse_checked_value(value):
    """
    Extracts and returns the text of checked boxes (☒) from a given string.
    If no checked box is found, returns the original value (after cleaning).
    """
    # Look for patterns like "☒ Married" or "☒   Married"
    # This regex captures everything after the ☒ until a whitespace or a checkbox symbol appears.
    matches = re.findall(r'☒\s*([^☒☐]+)', value)
    if matches:
        # Join multiple checked entries if needed.
        return ", ".join(match.strip() for match in matches)
    else:
        # No checkbox is checked; return the cleaned original value.
        return value.strip()


def extract_from_docx_tables(docx_file):
    doc = Document(docx_file)
    grouped = {}  # Dictionary to group values by key

    for table in doc.tables:
        for row in table.rows:
            cells = [cell.text.strip() for cell in row.cells]
            # Skip rows with no content.
            if not any(cells):
                continue

            # If all cells in the row have the same non-empty text, assume it's a section header and skip it.
            if len(set(cells)) == 1 and cells[0]:
                continue

            if len(cells) >= 2:
                key = cells[0]  # Use the first cell as the field name
                # Combine all remaining cells into a single string.
                value = ' '.join(cells[1:])

                # If the value contains the checked box symbol, parse and keep only those entries.
                if "☒" in value:
                    value = parse_checked_value(value)
                else:
                    # Otherwise, simply clean up any tabs/whitespace.
                    value = value.replace("\t", " ").strip()

                # Group rows having the same key (concatenate values with "; " as delimiter)
                if key in grouped:
                    grouped[key].append(value)
                else:
                    grouped[key] = [value]

    # Flatten the grouped dictionary into a list of tuples (key, combined value)
    extracted_data = []
    for key, values in grouped.items():
        combined_value = "; ".join(values)
        extracted_data.append((key, combined_value))

    df = pd.DataFrame(extracted_data, columns=["Field", "Value"])
    return df


# === Usage ===
docx_file = "description.docx"  # path to your docx file
df = extract_from_docx_tables(docx_file)

with pd.option_context(
        'display.max_rows', None,
        'display.max_columns', None,
        'display.max_colwidth', None,
        'display.width', None
):
    print(df)

# Save as CSV
df.to_csv("desc_preprocessed.csv", index=False)
