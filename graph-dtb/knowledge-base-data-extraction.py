import os
import csv
import re

def extract_fields_from_md(md_content):
    def extract_block(start, end=None):
        pattern = rf"{start}:\s*(.*?)(?={end}:|\Z)" if end else rf"{start}:\s*(.*)"
        match = re.search(pattern, md_content, re.DOTALL | re.IGNORECASE)
        return match.group(1).strip() if match else ""

    # Extract each field
    vulnerable_code = extract_block("vulnerable code", "Abstract purpose")
    abstract_purpose = extract_block("Abstract purpose", "Detail Behaviors")
    detail_behaviors = extract_block("Detail Behaviors", "fixed code")
    fixed_code = extract_block("fixed code", "Abstract Vulnerability Description")
    vuln_description = extract_block("Abstract Vulnerability Description", "Solution Description")
    solution_description = extract_block("Solution Description")

    return [
        vulnerable_code,
        abstract_purpose,
        detail_behaviors,
        fixed_code,
        vuln_description,
        solution_description,
    ]

def convert_md_to_csv(md_folder_path, output_csv_path):
    rows = []

    for filename in os.listdir(md_folder_path):
        if filename.endswith(".md") or filename.endswith(".txt"):
            with open(os.path.join(md_folder_path, filename), "r", encoding="utf-8") as f:
                content = f.read()
                fields = extract_fields_from_md(content)
                rows.append([filename] + fields)

    headers = [
        "filename",
        "vulnerable code",
        "Abstract purpose",
        "Detail Behaviors",
        "fixed code",
        "Abstract Vulnerability Description, Trigger Action, Detailed Vulnerability Description",
        "Solution Description"
    ]

    with open(output_csv_path, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(rows)

    print(f"✅ Converted {len(rows)} files to CSV at: {output_csv_path}")

# --- Thay đường dẫn bên dưới bằng thư mục chứa file .md và file .csv output bạn muốn ---
if __name__ == "__main__":
    md_folder = "D:\HK2-Nam3\dacn\crawl-2\RAG-SmartVuln\documents"  # 📁 Thư mục chứa các file .md
    output_csv = "output.csv"  # 📄 Tên file CSV đầu ra
    convert_md_to_csv(md_folder, output_csv)
