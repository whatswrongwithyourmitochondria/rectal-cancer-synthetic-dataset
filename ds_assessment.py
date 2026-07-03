import csv
import json
import time
import os
from openai import OpenAI
from dotenv import load_dotenv
from prompts.gpt4_prompt import GPT_PROMPT
from prompts.ds_prompts import (
    EXAMPLES,
    SYSTEM_ASSESSMENT_PROMPT,
    ASSESSMENT_PROMPT,
    SYSTEM_CORRECTION_PROMPT,
    CORRECTION_PROMPT,
)

load_dotenv()
ds_key = os.getenv('DS_API')
client = OpenAI(api_key=ds_key, base_url="https://api.deepseek.com")


with open("generated_datasets/ds_assessment_results.csv", 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    rows = list(reader)


for i, row in enumerate(rows):       
        
    print(f"Processing row {i+1}/{len(rows)}...")
    
    json_line = row["synthetic_structured_report"]
    free_text_report = row["free_text_report"]

    assessment_prompt = ASSESSMENT_PROMPT.format(
        structured=json.dumps(json_line, indent=2),
        report=free_text_report
    )

    messages = [
        {"role": "system", "content": SYSTEM_ASSESSMENT_PROMPT.format(gpt_prompt=GPT_PROMPT)},
        {"role": "user", "content": assessment_prompt}
    ]
    
    try:
        response = client.chat.completions.create(
            model="deepseek-reasoner",
            messages=messages
        )

        content = response.choices[0].message.content
        if content == "":
            print("Empty response")

        try:
            ds_assessment = json.loads(content).get("ds_assessment", "ERROR")
            print(ds_assessment)

        except json.JSONDecodeError:
            ds_assessment = next(
                (label for label in ["Perfect", "Minor issues", "Major issues"]
                 if label.lower() in content.lower()),
                "ERROR"
            )
            print(ds_assessment)

        corrected_report = ""
        if ds_assessment == "Major issues":
            print(f"Major issues found, generating correction of report {i+1}...")
            correction_prompt = CORRECTION_PROMPT.format(
                examples=EXAMPLES,
                structured=json.dumps(json_line, indent=2),
                report=free_text_report
            )
            correction_response = client.chat.completions.create(
                model="deepseek-reasoner",
                messages=[
                    {"role": "system", "content": SYSTEM_CORRECTION_PROMPT},
                    {"role": "user", "content": correction_prompt},
                ],
            )
            corrected_report = correction_response.choices[0].message.content.strip()

    except Exception as e:
        print(f"Error during DeepSeek assessment on row {i+1}: {e}")
        ds_assessment = "ERROR"
        corrected_report = ""

    row["ds_assessment"] = ds_assessment
    row["ds_corrected"] = corrected_report


    with open("generated_datasets/ds_assessment_results.csv", 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"Row {i+1} completed: {ds_assessment}")
    time.sleep(1)  # Rate limiting

print("Assessment completed")