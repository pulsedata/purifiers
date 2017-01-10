import json
import requests
import ast
import argparse

parser = argparse.ArgumentParser(description='Purify the graduates dataset.')
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
		# Begin parsing the badly encoded address
		address_set = ast.literal_eval(item['location_1']['human_address'])
		# Create a new location set
		new_item['location'] = {
			'city': address_set['city'],
			'coordinates': [float(item['location_1']['latitude']), float(item['location_1']['longitude'])],
		}
		# Delete useless keys then merge
		del item['location_1']
		del item['calendario']
		# Merge keys 
		# TODO: Refactor
		new_item['igs'] = float(item['igs'])
		new_item['gpa'] = float(item['gpa'])
		new_item['program'] = item['program']
		new_item['campus'] = item['campus']
		new_item['school'] = item['institucion_de_procedencia'][8:]
		# Push to list
		new_set.append(new_item)
		print("%s items processed" % len(new_set))
	except KeyError:
		print("Skipped an incomplete error...")
		continue

# TODO: Make this smarter, take flags.

print("Writing to file")
with open("out/%s" % args.filename_out, 'a') as f:
	print("Received %s records." % len(new_set))
	f.write(json.dumps(new_set, indent=2))
print("Done")