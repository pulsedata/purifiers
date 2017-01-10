import json
import requests
import ast
import argparse

parser = argparse.ArgumentParser(description='Purify the schools dataset.')
parser.add_argument('filename', metavar="set_id", type=str, help="The filename to purify.")
parser.add_argument('filename_out', metavar="filename_out", type=str, help="The filename for the result.")
args = parser.parse_args()

gf = open(args.filename, 'r')
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

# TODO: Make this smarter, take flags argparse rewrite!!

print("Writing to file")
with open("out/%s" % args.filename_out, 'a') as f:
	print("Received %s records." % len(new_set))
	f.write(json.dumps(new_set, indent=2))
print("Done")