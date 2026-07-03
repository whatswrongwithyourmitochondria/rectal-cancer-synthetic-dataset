import csv
import json
import time
import os
from openai import OpenAI
from dotenv import load_dotenv
from prompts.gpt4_prompt import GPT_PROMPT

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API'))
input_file = 'code_to_obtain_SR_data/jsonl_data_vscode/balanced_synthetic_SR_modified.jsonl'
csv_output_file = "generated_datasets/synthetic_reports_gpt4.csv"

synthetic_reports_count = 0

with open(input_file, "r") as infile, open(csv_output_file, "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["synthetic_structured_report", "free_text_report"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
    writer.writeheader()
    
    for i, line in enumerate(infile, 1):
        print(f"Processing line {i}...")

        try:
            input_data = json.loads(line)
        except json.JSONDecodeError as e:
            print(f"JSON decode error on line {i}: {e}")
            continue

        messages = [
            {"role": "system", "content": GPT_PROMPT},
            {"role": "user", "content": "Here is the structured version of the report to create a free-text one based on it:" + json.dumps(input_data, indent=2)}
        ]

        try:
            response = client.chat.completions.create(
                model="gpt-4.1-2025-04-14",
                messages=messages,
                temperature=0.3,
                top_p=0.95,
                max_tokens=550
            )
        except Exception as e:
            print(f"Error processing line {i}: {e}")
            continue

        report = response.choices[0].message.content

        writer.writerow({
            "synthetic_structured_report": json.dumps(input_data),
            "free_text_report": report
        })

        synthetic_reports_count += 1
        print(f"Successfully processed and saved report {synthetic_reports_count}")

        time.sleep(1)


print(f"Generated {synthetic_reports_count} synthetic reports. CSV saved to '{csv_output_file}'.")