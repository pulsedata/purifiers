from sys import argv
import json
import requests
import ast

gf = open("../originals/schools.json", 'r')
data = json.loads(gf.read())

new_set = []
original_count = len(data)
print("Processing %s records..." % original_count)

for item in data:
	try:
		new_item = {}
		human_address_parse = ast.literal_eval(item['direccion_fisica_zipcode']['human_address'])
		new_item['id'] = int(item['codigo'])
		new_item['name'] = item['escuela']
		new_item['level'] = item['nivel']
		new_item['location'] = {
			'coordinates': [float(item['direccion_fisica_zipcode']['latitude']), float(item['direccion_fisica_zipcode']['longitude'])],
			'municipality': item['direccion_fisica_pueblo'],
			'zip': human_address_parse['zip'],
			'region': item['region'],
			'metadata': {
				'district': item['distrito'],
				'educative_region': item['municipio_escolar'],
			}
		}
		new_item['information'] = {
			'grades': item['grado'],
			'performance': {
				'prestige': item['clasificacion_flex'],
			},
			'administration': {
				'director': item['director']
			},
			'phone': item['telefono_1']
		}

		new_set.append(new_item)
		print("%s items processed" % len(new_set))
	except KeyError as e:
		print(e)
		print("Skipped an incomplete item...")
		continue

# TODO: Make this smarter, take flags.

if len(argv) == 2:
	print("Writing to file")
	output_file = open(argv[1], 'w')
	output_file.write(json.dumps(new_set, indent=4))
	print("Done")
else:
	print("Assuming debug run")
	error = original_count - len(new_set)
	print("Skipped %d records" % error)
	print("Sample item:")
	print(json.dumps(new_set[1], indent=4))