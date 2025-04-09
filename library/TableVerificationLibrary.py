import os
import pandas as pd
import textfsm

class TableVerificationLibrary:
    def __init__(self, template_path=None):
        # Nếu không truyền vào đường dẫn template thì mặc định lấy file cùng thư mục với thư viện
        if template_path:
            self.template_path = template_path
        else:
            self.template_path = os.path.join(os.path.dirname(__file__), 'template_file.txt')

    def create_table(self, table_input):
        """
        Keyword: Create Table
        Nhận đầu vào là chuỗi định dạng bảng (pipe separated) hoặc đã là DataFrame.
        Nếu là chuỗi thì chuyển đổi nó thành pandas DataFrame.
        Ví dụ đầu vào (chuỗi):
            | Interface    | TYPE      | STATUS  | MODE            | FLOWCTRL  |
            | xgspon0/1    | Ethernet  | Up/Up   | Force/Full/10G  | Off/Off   |
        """
        # Nếu đầu vào đã là DataFrame thì trả về ngay
        if isinstance(table_input, pd.DataFrame):
            return table_input

        # Nếu đầu vào là chuỗi
        if not isinstance(table_input, str):
            raise ValueError("Đầu vào phải là chuỗi hoặc DataFrame")

        # Tách các dòng và loại bỏ các dòng chỉ chứa dấu gạch (nếu có)
        lines = table_input.strip().splitlines()
        valid_lines = [line for line in lines if set(line.strip()) != {'-'}]
        rows = []
        for line in valid_lines:
            if '|' in line:
                # Tách theo ký tự "|" và loại bỏ khoảng trắng thừa
                parts = [col.strip() for col in line.split('|') if col.strip()]
                if parts:
                    rows.append(parts)
        if not rows:
            raise ValueError("Không tìm thấy dữ liệu hợp lệ trong chuỗi input")
        # Giả sử dòng đầu tiên là header
        header = rows[0]
        data = rows[1:]
        df = pd.DataFrame(data, columns=header)
        return df

    def parse_table(self, raw_string):
        """
        Keyword: Parse Table
        Sử dụng TextFSM để parse raw output thành DataFrame.
        File template TextFSM (ví dụ template_file.txt) cần được định nghĩa trước với cú pháp của TextFSM.
        """
        if not os.path.exists(self.template_path):
            raise FileNotFoundError(f"Không tìm thấy file template tại: {self.template_path}")
        with open(self.template_path, 'r') as template_file:
            fsm = textfsm.TextFSM(template_file)
            # Parse raw_string trả về list các list chứa giá trị theo thứ tự header của TextFSM
            parsed_results = fsm.ParseText(raw_string)
        if not parsed_results:
            raise ValueError("Không parse được dữ liệu từ raw_string bằng TextFSM")
        # Chuyển kết quả thành DataFrame với header từ TextFSM
        df = pd.DataFrame(parsed_results, columns=fsm.header)
        return df

    def verify_table(self, reference_input, raw_input, mode="whitelist"):
        """
        Keyword: Verify Table
        So sánh bảng tham chiếu (reference_input) với bảng raw (raw_input).
        Đầu vào có thể là chuỗi định dạng bảng hoặc DataFrame.
        
        - Với mode = whitelist: Mỗi dòng trong reference_input phải có trong raw_input.
        - Với mode = blacklist: Không dòng nào trong reference_input được phép có trong raw_input.
        
        Trả về True hoặc False dựa vào kết quả so sánh.
        """
        # Chuyển đổi đầu vào thành DataFrame nếu cần
        df_ref = reference_input if isinstance(reference_input, pd.DataFrame) else self.create_table(reference_input)
        df_raw = raw_input if isinstance(raw_input, pd.DataFrame) else self.create_table(raw_input)

        # Whitelist: mọi dòng trong bảng tham chiếu phải xuất hiện trong bảng raw.
        if mode.lower() == "whitelist":
            # Giữ lại các cột chung giữa df_ref và df_raw
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
