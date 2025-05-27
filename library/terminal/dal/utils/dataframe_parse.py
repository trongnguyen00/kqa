# 📁 utils/dataframe_utils.py

import os
import textfsm
import pandas as pd

def parse_table_with_fsm(raw_output: str, template_path: str) -> pd.DataFrame:
    """
    Parse a CLI raw text using a TextFSM template and return as DataFrame.

    Args:
        raw_output (str): Raw CLI output to be parsed.
        template_path (str): Full path to the TextFSM template.

    Returns:
        pd.DataFrame: Parsed output as a DataFrame.
    """
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template file not found: {template_path}")

    with open(template_path, 'r') as template_file:
        fsm = textfsm.TextFSM(template_file)
        parsed_result = fsm.ParseText(raw_output)

    if not parsed_result:
        raise ValueError("TextFSM could not parse any data from the raw output.")

    return pd.DataFrame(parsed_result, columns=fsm.header)

def parse_pipe_table_string(table_str: str) -> pd.DataFrame:
    """
    Parse a pipe-separated table string into a pandas DataFrame.

    Example:
        | PORT | SN        | VERSION | MODEL  |\n
        | 0/2/6 | ABC12345 | 1.0     | PM1191 |\n
    Args:
        table_str (str): Pipe-separated table string.

    Returns:
        pd.DataFrame: Parsed table as DataFrame.
    """
    lines = table_str.strip().splitlines()
    valid_lines = [line for line in lines if set(line.strip()) != {'-'}]
    rows = []
    for line in valid_lines:
        if '|' in line:
            parts = [col.strip() for col in line.split('|') if col.strip()]
            if parts:
                rows.append(parts)

    if not rows:
        raise ValueError("No valid data rows found in the table string.")

    header = rows[0]
    data = rows[1:]
    return pd.DataFrame(data, columns=header)

def normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and normalize DataFrame (trim whitespaces, drop NA, sort columns).

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: Cleaned and normalized DataFrame.
    """
    df_cleaned = df.applymap(lambda x: str(x).strip()).dropna()
    df_cleaned = df_cleaned.sort_index().reset_index(drop=True)
    return df_cleaned
