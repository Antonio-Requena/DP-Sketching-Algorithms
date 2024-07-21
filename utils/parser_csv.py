import csv
import argparse
import os

def parse_txt_to_csv(txt_file):
    base_name = os.path.splitext(txt_file)[0]
    csv_file = base_name + '.csv'

    with open(txt_file, 'r') as file:
        data = file.read().strip()
    
    # Separar las ejecuciones
    executions = data.split('\n\n')

    header = []
    rows = []
    
    for execution in executions:
        lines = execution.split('\n')
        row = {}

        for line in lines:
            if not line.strip():
                continue
            
            key, value = line.split(': ')
            row[key] = value

            if key not in header:
                header.append(key)
        
        rows.append(row)
    
    # Escribir el archivo CSV
    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)