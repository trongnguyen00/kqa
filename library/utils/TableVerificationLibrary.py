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
        ...    | Interface    | TYPE        | STATUS    | MODE              | FLOWCTRL    | \n
        ...    | xgspon0/1    | Ethernet    | Up/Up     | Force/Full/10G    | Off/Off     | \n
        ...    | xgspon0/2    | Ethernet    | Up/Up     | Force/Full/10G    | Off/Off     | \n
        ...    | xgspon0/3    | Ethernet    | Up/Up     | Force/Full/10G    | Off/Off     | \n

        ${REFERENCE_TABLE}    SEPARATOR=${EMPTY}
        ...    | Interface    | STATUS    | \n
        ...    | xgspon0/1    | Up/Up     | \n
        ...    | xgspon0/2    | Up/Up     | \n

        ${table_raw}    Create Table    ${RAW_OUTPUT}
        ${table_ref}    Create Table    ${REFERENCE_TABLE}

        Using with variables(can't use in Variables section):
        ${onu_verify}    Catenate
        ...              | PORT                                 | SN           | VERSION           | MODEL           | \n
        ...              | ${OLT_PON_ALIAS}/${OLT_PON_INDEX}    | ${ONU_SN}    | ${ONU_VERSION}    | ${ONU_MODEL}    | \n
        
        ${onu_verify_table}    Create Table           ${onu_verify}

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
    def verify_table(self, expected_result, actual_result, mode="whitelist"):
        """
        Keyword: Verify Table
        Compare two tables (expected_result and actual_result) based on the specified mode.
        Input can be a string or a DataFrame.
        - If whitelist: all rows in the expected_result must appear in the actual_result.
        - If blacklist: no rows in the expected_result should appear in the actual_result.
        """
        df_ref = expected_result if isinstance(expected_result, pd.DataFrame) else self.create_table(expected_result)
        df_raw = actual_result if isinstance(actual_result, pd.DataFrame) else self.create_table(actual_result)

        common_cols = [col for col in df_ref.columns if col in df_raw.columns]
        if not common_cols:
            raise ValueError("No common columns found between the two tables.")

        df_ref_subset = df_ref[common_cols].copy()
        df_raw_subset = df_raw[common_cols].copy()

        df_ref_subset = df_ref_subset.applymap(lambda x: str(x).strip()).dropna().sort_values(by=common_cols).reset_index(drop=True)
        df_raw_subset = df_raw_subset.applymap(lambda x: str(x).strip()).dropna().sort_values(by=common_cols).reset_index(drop=True)

        set_ref = set(tuple(row) for row in df_ref_subset.to_numpy())
        set_raw = set(tuple(row) for row in df_raw_subset.to_numpy())

        if mode.lower() == "whitelist":
            return set_ref.issubset(set_raw)

        elif mode.lower() == "blacklist":
            return set_ref.isdisjoint(set_raw)

        else:
            raise ValueError("Mode must be either 'whitelist' or 'blacklist'.")

    # @keyword
    # def verify_table(self, expected_result, actual_result, mode="whitelist"):
    #     """
    #     Keyword: Verify Table
    #     Compare two tables (expected_result and actual_result) based on the specified mode.
    #     Input can be a string or a DataFrame.
    #     - If whitelist: all rows in the expected_result must appear in the actual_result.
    #     - If blacklist: no rows in the expected_result should appear in the actual_result.
    #     """
    #     df_ref = expected_result if isinstance(expected_result, pd.DataFrame) else self.create_table(expected_result)
    #     df_raw = actual_result if isinstance(actual_result, pd.DataFrame) else self.create_table(actual_result)

    #     if mode.lower() == "whitelist":
    #         common_cols = [col for col in df_ref.columns if col in df_raw.columns]
    #         df_raw_subset = df_raw[common_cols]
    #         df_ref_subset = df_ref[common_cols]

    #         for _, ref_row in df_ref_subset.iterrows():
    #             match_found = ((df_raw_subset == ref_row).all(axis=1)).any()
    #             if not match_found:
    #                 return False
    #         return True


    #     elif mode.lower() == "blacklist":
    #         common_cols = [col for col in df_ref.columns if col in df_raw.columns]
    #         df_raw_subset = df_raw[common_cols]
    #         df_ref_subset = df_ref[common_cols]
            
    #         for _, ref_row in df_ref_subset.iterrows():
    #             match_found = ((df_raw_subset == ref_row).all(axis=1)).any()
    #             if match_found:
    #                 return False
    #         return True

    @keyword
    def get_value_by_column(self, df, column_name, index_row=0):
        """
        Keyword: Get Cell Value by Column
        """
        try:
            return str(df.loc[index_row, column_name])
        except Exception as e:
            raise ValueError(f"Cannot get value at column '{column_name}': {e}")

    @keyword
    def filter_table(self, df, column_name, target_value):
        """
        Keyword: Filter Table by Column
        Arguments:
          - df: DataFrame to filter.
          - column_name: Name of the column to filter by.
          - target_value: Value to filter the column by.
        Returns a DataFrame filtered by the specified column and value.
        """
        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' does not exist in the DataFrame.")
        
        filtered_df = df[df[column_name] == target_value]
        return filtered_df.reset_index(drop=True)