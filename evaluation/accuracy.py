"""
-------------------------------------------
This script evaluates the performance of LMMs on MDI-Benchmark problems and different problem domains.
-------------------------------------------

"""


import json
import os
import pandas as pd
import numpy as np
import argparse


# get arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description='Evaluate the performance of different LMMs on MDI-Benchmark.')
    parser.add_argument('--model_name', type=str, required=True, help='Model name.')
    parser.add_argument('--output_json', type=str, required=True, help='Output json.')
    parser.add_argument('--main_results_csv_path', type=str, help='Path to save the main results CSV file.')
    return parser.parse_args()


def load_and_process_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    df = pd.DataFrame(data)
    df['processed_answer'] = df['response'].str.split('Answer').str[-1].str.strip().str.replace(r'[>><<:.]', '', regex=True).str.strip()
    df['processed_answer'] = df['processed_answer'].apply(lambda x: x[0] if x and x[0] in 'ABCDEFGH' else None)
    df['joker'] = df['processed_answer'] == df['answer']
    return df


def calculate_metrics(data, model_name):
    cnt_level1 = 0
    cnt_level2 = 0
    cnt_old = 0
    cnt_mid = 0
    cnt_young = 0

    categories = ["architecture", "education", "housework", "social_service", "sport", "transport"]
    cnt_level1_cats = {cat: 0 for cat in categories}
    cnt_level2_cats = {cat: 0 for cat in categories}

    for index, line in data.iterrows():
        level, filed, age = line["key"].split('-')
        if line["joker"] == True:
            if level == "level1":
                cnt_level1 += 1
                cnt_level1_cats[filed] += 1
            elif level == "level2":
                cnt_level2 += 1
                cnt_level2_cats[filed] += 1
            if age == "old":
                cnt_old += 1
            elif age == "mid":
                cnt_mid += 1
            elif age == "young":
                cnt_young += 1
    

    total_level1 = 311
    total_level2 = 311
    total_old = 204
    total_mid = 204
    total_young = 204


    metric = {}
    metric['Model'] = model_name
    metric['Final Score'] = f"{((cnt_level1/total_level1) * 0.5 + (cnt_level2/total_level2) * 0.5):.2%}"
    metric['Avg (Level 1)'] = f"{cnt_level1/total_level1:.2%}"
    metric['Arc (Level 1)'] = f"{cnt_level1_cats['architecture']/51:.2%}"
    metric['Edu (Level 1)'] = f"{cnt_level1_cats['education']/51:.2%}"
    metric['Hou (Level 1)'] = f"{cnt_level1_cats['housework']/51:.2%}"
    metric['Soc (Level 1)'] = f"{cnt_level1_cats['social_service']/51:.2%}"
    metric['Spo (Level 1)'] = f"{cnt_level1_cats['sport']/51:.2%}"
    metric['Tra (Level 1)'] = f"{cnt_level1_cats['transport']/51:.2%}"
    metric['Avg (Level 2)'] = f"{cnt_level2/total_level2:.2%}"
    metric['Arc (Level 2)'] = f"{cnt_level2_cats['architecture']/51:.2%}"
    metric['Edu (Level 2)'] = f"{cnt_level2_cats['education']/51:.2%}"
    metric['Hou (Level 2)'] = f"{cnt_level2_cats['housework']/51:.2%}"
    metric['Soc (Level 2)'] = f"{cnt_level2_cats['social_service']/51:.2%}"
    metric['Spo (Level 2)'] = f"{cnt_level2_cats['sport']/51:.2%}"
    metric['Tra (Level 2)'] = f"{cnt_level2_cats['transport']/51:.2%}"
    metric['Avg (age)'] = f"{((cnt_old/total_old) + (cnt_mid/total_mid) + (cnt_young/total_young)) / 3:.2%}"
    metric['old'] = f"{cnt_old/total_old:.2%}"
    metric['mid'] = f"{cnt_mid/total_mid:.2%}"
    metric['young'] = f"{cnt_young/total_young:.2%}"

    return metric

    
def evaluate_models(model_name, output_json, main_results_csv_path = None):
    main_results_df = pd.DataFrame(columns=['Model', 'Final Score', 'Avg (Level 1)', 'Arc (Level 1)', 'Edu (Level 1)', 'Hou (Level 1)', 'Soc (Level 1)', 'Spo (Level 1)', 'Tra (Level 1)', 'Avg (Level 2)', 'Arc (Level 2)', 'Edu (Level 2)', 'Hou (Level 2)', 'Soc (Level 2)', 'Spo (Level 2)', 'Tra (Level 2)', 'Avg (age)', 'old', 'mid', 'young'])
    print(f"Evaluating model: {model_name}, JSON path: {output_json}")
    data = load_and_process_data(output_json)
    metric = calculate_metrics(data, model_name)
    main_results_df = main_results_df.append(metric, ignore_index=True)
    print(main_results_df.to_string(index = False))
    if main_results_csv_path is not None:
        main_results_df.to_csv(main_results_csv_path, index=False)
    else:
        main_results_df.to_csv(f"{model_name}_evaluate_res.csv", index=False)
    print("Evaluation completed and results saved to CSV.")


# python accuracy.py 
if __name__ == "__main__":
    args = parse_arguments()
    evaluate_models(args.model_name, args.output_json)


