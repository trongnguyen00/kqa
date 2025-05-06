import os
import pandas as pd
import textfsm
from robot.api.deco import keyword

class TableVerificationLibrary:
    def __init__(self, template_path=None):
        if template_path:
            self.template_path = template_path
        else:
            self.template_path = os.path.join(os.path.dirname(__file__), 'template_file.txt')

    @keyword
    def create_table(self, table_input):
        """
        Keyword: Create Table
        Nhận đầu vào là chuỗi định dạng bảng (pipe separated) hoặc đã là DataFrame.
        Nếu là chuỗi thì chuyển đổi nó thành pandas DataFrame.
        Example:
        ${RAW_OUTPUT}    SEPARATOR=${EMPTY}
        ...
        ...    | Interface    | TYPE        | STATUS    | MODE              | FLOWCTRL    | \n
        ...    | xgspon0/1    | Ethernet    | Up/Up     | Force/Full/10G    | Off/Off     | \n
        ...    | xgspon0/2    | Ethernet    | Up/Up     | Force/Full/10G    | Off/Off     | \n
        ...    | xgspon0/3    | Ethernet    | Up/Up     | Force/Full/10G    | Off/Off     | \n

        ${REFERENCE_TABLE}    SEPARATOR=${EMPTY}
        ...
        ...    | Interface    | STATUS    | \n
        ...    | xgspon0/1    | Up/Up     | \n
        ...    | xgspon0/2    | Up/Up     | \n

        ${table_raw}    Create Table    ${RAW_OUTPUT}
        ${table_ref}    Create Table    ${REFERENCE_TABLE}

        """
        if isinstance(table_input, pd.DataFrame):
            return table_input

        if not isinstance(table_input, str):
            raise ValueError("Input must be a string or DataFrame")

        lines = table_input.strip().splitlines()
        valid_lines = [line for line in lines if set(line.strip()) != {'-'}]
        rows = []
        for line in valid_lines:
            if '|' in line:
                parts = [col.strip() for col in line.split('|') if col.strip()]
                if parts:
                    rows.append(parts)
        if not rows:
            raise ValueError("No valid table data found in the input string")
        header = rows[0]
        data = rows[1:]
        df = pd.DataFrame(data, columns=header)
        return df

    @keyword
    def parse_table(self, raw_string, template_path):
        """
        Keyword: Parse Table
        Use TextFSM to parse the raw_string into a DataFrame.
        Arguments:
          - raw_string: output string need to be parsed.
          - template_path: path to file TextFSM template. File extension: *.template

        Template example:
        -----------------
        Value INTERFACE (\S+)
        Value TYPE (\S+)
        Value STATUS (\S+)
        Value MODE (\S+)
        Value FLOWCTRL (\S+)

        Start
          ^${INTERFACE}\s+${TYPE}\s+${STATUS}\s+${MODE}\s+${FLOWCTRL} -> Record

        
        """
        with open(template_path, 'r') as template_file:
            fsm = textfsm.TextFSM(template_file)
            parsed_results = fsm.ParseText(raw_string)
        if not parsed_results:
            raise ValueError("Cannot parse the raw string with the provided template.")
        df = pd.DataFrame(parsed_results, columns=fsm.header)
        return df

    @keyword
    def verify_table(self, reference_input, raw_input, mode="whitelist"):
        """
        Keyword: Verify Table
        Compare two tables (reference_input and raw_input) based on the specified mode.
        Input can be a string or a DataFrame.
        - If whitelist: all rows in the reference_input must appear in the raw_input.
        - If blacklist: no rows in the reference_input should appear in the raw_input.
        """
        df_ref = reference_input if isinstance(reference_input, pd.DataFrame) else self.create_table(reference_input)
        df_raw = raw_input if isinstance(raw_input, pd.DataFrame) else self.create_table(raw_input)

        if mode.lower() == "whitelist":
            common_cols = [col for col in df_ref.columns if col in df_raw.columns]
            df_raw_subset = df_raw[common_cols]
            df_ref_subset = df_ref[common_cols]

            for _, ref_row in df_ref_subset.iterrows():
                match_found = ((df_raw_subset == ref_row).all(axis=1)).any()
                if not match_found:
                    return False
            return True


        elif mode.lower() == "blacklist":
            common_cols = [col for col in df_ref.columns if col in df_raw.columns]
            df_raw_subset = df_raw[common_cols]
            df_ref_subset = df_ref[common_cols]
            
            for _, ref_row in df_ref_subset.iterrows():
                match_found = ((df_raw_subset == ref_row).all(axis=1)).any()
                if match_found:
                    return False
            return True
