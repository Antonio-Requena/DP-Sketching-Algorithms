import csv

def parse_txt_to_csv(txt_file, csv_file):
    with open(txt_file, 'r') as file:
        data = file.read().strip()
    
    # Separar las ejecuciones
    executions = data.split('\n\n')

    # Obtener los nombres de las columnas
    header = set()
    rows = []
    
    for execution in executions:
        lines = execution.split('\n')
        row = {}
        is_param = True

        for line in lines:
            if not line.strip():
                is_param = False
                continue
            
            key, value = line.split(': ')
            if key.startswith('e') or key.startswith('k') or key.startswith('m'):
                row[key] = value
            else:
                row[key] = value

            header.add(key)
        
        rows.append(row)
    
    # Escribir el archivo CSV
    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=sorted(header))
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

if __name__ == 'main':
    parse_txt_to_csv()