
# coding: utf-8

# In[ ]:

#fix street types
import re
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE) #recognize street types

#list of expected street types
expected_streets = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons", 'Turnpike', 'Plaza', 'South', 'North', 'A', 'B', 'C', 'D',
                   'Broadway', 'Expressway', 'Terrace', 'Way', 'Concourse', 'Heights', 'Alley',
                   'Extension', 'East', 'West', 'Bowery', 'Terminal', 'Slip', 'Americas', 'Walk', 'Row',
                   'Circle', 'Hill', 'Crescent', 'Bush', 'Center', 'Piers', 'Walk', 'Loop', 'Highway', 'Rico',
                   'Oval', 'Finest', 'Island', 'Village', 'Mews', 'Park']

#this handles the case of finding a highway, e.g. 'Route 287' - we won't want to take any action on this
highways = ['Route', 'Highway']

#map to expected street types
street_mapping = { "St": "Street",
            "St.": "Street",
            "Ave": "Avenue",
            "Rd.": "Road",
           'Rd': 'Road',
           'st': 'Street',
           'Pky': 'Parkway',
           'avenue': 'Avenue',
           'street': 'Street',
           'Ct': 'Court',
           'ave': 'Avenue',
           'Avene': 'Avenue',
           'Ave.': 'Avenue',
           'Dr.': 'Drive',
           'Plz': 'Plaza',
           'Steet': 'Street',
           'drive': 'Drive',
           'road': 'Road',
           'Ave,': 'Ave',
           'Blvd': 'Boulevard',
           'Pkwy': 'Parkway',
           'ST': 'Street',
           'Broadway.': 'Broadway'
            }

def fix_street(street, mapping):
    if street.split()[-1] not in mapping: #if not something we're fixing
        return None
    else:
        x = re.search(street_type_re, street).start() #find where street name starts
        if street.split()[0] in highways: #don't want to correct 'Route 287' for example. 
            return street
        else:
            return street[:x] + mapping[street[x:]]


#fix street prefixes
prefix_map = {'N': 'North',
              'N.': 'North',
              'S': 'South',
              'S.': 'South',
              'W': 'West',
              'W.': 'West',
              'E': 'East',
              'E.': 'East',
              'Rt': 'Route',
              'Rt.': 'Route',
              'Hwy': 'Highway',
              'Hwy.': 'Highway'}

def fix_streetprefix(street, mapping):
    prefix = street.split()[0] #get first word in street name
    if prefix in prefix_map: #adjust if necessary
        return street.replace(prefix, prefix_map[prefix], 1)
    return street

#postal code fixer function
def fix_postcode(postcode):
    if postcode.isdigit() and len(postcode) == 5: #valid postal code
        return postcode
    elif len(postcode) < 5: #definitely invalid if fewer than 5 characters
        return None
    elif postcode[3:].isdigit() and len(postcode[3:]) == 5: #fixes, for example, 'NJ 07036'
        return postcode[3:]
    elif postcode[:5].isdigit() and postcode[5] == '-': #fixes, for example, '08901-1340'
        return postcode[:5]
    elif postcode.strip().isdigit() and len(postcode.strip()) == 5: #fixes, for example, ' 10010'
        return postcode.strip()
    else: #if still not fixed, skip this tag
        return None
    
def fix_city(city):
    city = city.title() #correct capitalization scheme
    city = city.strip() #strip whitespace
    if city == 'New York City': #'New York City' should be 'New York'
        return 'New York'
    elif re.search(',', city): #capture 'New York, NY' for example
        a = city[:re.search(',', city).start()]
        if a == 'New York City':
            return 'New York'
        return a
    splits = city.split() #capture 'Queens NY' for example
    if splits[-1].upper() in ['NY', 'NJ', 'CT']:
        a = city[:-2].strip()
        if a == 'New York City':
            return 'New York'
        return a
    return city #just leave it as is if none of these issues are captured

expected_cuisine = ['nepalese', 'mexican', 'chinese', 'german', 'japanese', 'russian', 'wine bar', 'asian', 
                    'brazilian', 'coffee shop', 'burger', 'vietnamese', 'ramen', 'sandwich', 'american', 'irish',
                    'venezuelan', 'french', 'vegan', 'indian', 'spanish', 'italian', 'indonesian', 'serbian', 
                    'austrian', 'steak', 'caribbean', 'mediterranean', 'barbecue', 'falafel', 'colombian', 
                    'cuban', 'scandinavian', 'oysters', 'korean', 'diner', 'filipino', 'latin american', 
                    'vegetarian', 'turkish', 'ethiopian', 'kosher', 'romanian', 'jamaican', 'southern', 
                    'peruvian', 'belgian', 'taiwanese', 'nordic', 'crepe', 'thai', 'scottish', 'lebanese', 
                    'pakistani', 'ecuadorian', 'donut', 'israeli', 'swiss', 'ice cream', 'tibetan', 'australian',
                    'greek', 'seafood', 'pizza', 'english', 'cambodian', 'dominican', 'chicken']

cuisine_mapping = {'brasilian': 'brazilian', 'doughnut': 'donut', 'tacos': 'mexican', 'fish': 'seafood',
                  'steakhouse': 'steak', 'steak house': 'steak', 'subs': 'sandwich', 'sandwiches': 'sandwich',
                  'tapas': 'spanish', 'sushi': 'japanese', 'taco': 'mexican', 'basque': 'spanish'}

#clean up cuisine data
def fix_cuisine(cuisine):
    cuisine = cuisine.lower() #convert to lower case
    if cuisine in expected_cuisine:
        return cuisine
    if cuisine in cuisine_mapping:
        return cuisine_mapping[cuisine]
    if cuisine.find(';'): #for lists with semicolon
        words = cuisine.split(';')
        for word in words:
            clean = clean_cuisine(word)
            if clean:
                return clean
    if cuisine.find(','): #for lists with commas
        words = cuisine.split(',')
        for word in words:
            clean = clean_cuisine(word)
            if clean:
                return clean
    if cuisine.find('/'): #for lists with slashes
        words = cuisine.split('/')
        for word in words:
            clean = clean_cuisine(word)
            if clean:
                return clean
    if cuisine.find('-'): #for cuisines split with a hyphen
        words = cuisine.split('-')
        for word in words:
            clean = clean_cuisine(word)
            if clean:
                return clean            
    if cuisine.find('_'): #if separated with _'s
        cuisine = cuisine.replace('_', ' ')
        if cuisine in expected_cuisine:
            return cuisine
        words = cuisine.split()
        for word in words:
            clean = clean_cuisine(word)
            if clean:
                return clean 
    return None

#helper function
def clean_cuisine(word):
    word = word.replace('_', ' ') #change _'s to spaces
    word = word.strip()
    if word in expected_cuisine:
        return word
    if word[:-1] in expected_cuisine: #if simple plural (e.g. 'donuts')
        return word[:-1]
    if word in cuisine_mapping:
        return cuisine_mapping[word]
    if word[:-1] in cuisine_mapping:
        return cuisine_mapping[word[:-1]]
    return None

import shapefile
sf = shapefile.Reader('/Users/chadhorner/Downloads/ZillowNeighborhoods-NY/ZillowNeighborhoods-NY')

#function that tests if a point is inside a polygon; 
#source: http://gis.stackexchange.com/questions/121469/get-shape-file-polygon-attribute-value-at-a-specific-point-using-python-e-g-vi
def point_in_poly(x,y,poly):

   # check if point is a vertex
   if (x,y) in poly: return False

   # check if point is on a boundary
   for i in range(len(poly)):
      p1 = None
      p2 = None
      if i==0:
         p1 = poly[0]
         p2 = poly[1]
      else:
         p1 = poly[i-1]
         p2 = poly[i]
      if p1[1] == p2[1] and p1[1] == y and x > min(p1[0], p2[0]) and x < max(p1[0], p2[0]):
         return True

   n = len(poly)
   inside = False

   p1x,p1y = poly[0]
   for i in range(n+1):
      p2x,p2y = poly[i % n]
      if y > min(p1y,p2y):
         if y <= max(p1y,p2y):
            if x <= max(p1x,p2x):
               if p1y != p2y:
                  xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
               if p1x == p2x or x <= xints:
                  inside = not inside
      p1x,p1y = p2x,p2y

   if inside: return True
   else: return False
    
#creates list of name-points tuples
neighborhoods = [] 
for entry in sf.iterShapeRecords():
    if entry.record[1] == 'New York': #if county is New York (this is the island of Manhattan)
        neighborhoods.append((entry.record[3], entry.shape.points))
        

#assigns neighborhood, given x and y coordinates.
def assign_neighborhood(x, y, neighborhoods):
    for neighborhood in neighborhoods:
        if point_in_poly(float(x),float(y),neighborhood[1]):
            return neighborhood[0]
    return None

import csv
import codecs
import re
import xml.etree.cElementTree as ET

import cerberus
import schema

#file names for csvs to create
NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

#REs to find problem tags or tags with colons (e.g. 'addr:postcode')
LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

SCHEMA = schema.schema

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp', 'neighborhood']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']

#shape element function. handles the cases outlined above - different address fields as well as cuisine
def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, neighborhoods = neighborhoods):

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements

    #do tags first; same for either node or way
    for tag in element.findall('tag'):
        tagdict = {}
        tagdict['id'] = element.attrib['id']
        k = tag.attrib['k']
        if re.search(problem_chars, k): #skip if problem characters
            continue
        elif k == 'addr:postcode': #if postcode
            postcode = tag.attrib['v']
            tagdict['type'] = 'addr'
            tagdict['key'] = 'postcode'
            if (postcode.isdigit() and len(postcode) == 5): #if this is valid postcode
                tagdict['value'] = postcode
            else:
                postcode = fix_postcode(postcode) #else try to fix
                if postcode: #if fixed, use it
                    tagdict['value'] = postcode
                else: #if not, skip this tag
                    continue
        elif k == 'addr:street': #if street
            street = tag.attrib['v']
            tagdict['type'] = 'addr'
            tagdict['key'] = 'street'
            street = fix_streetprefix(street, prefix_map) #fix prefix, if necessary            
            m = street_type_re.search(street) #find where street starts
            if m:
                street_type = m.group()
                if street_type in expected_streets: #if this is a good street
                    tagdict['value'] = street
                if street_type not in expected_streets: #if not, try to fix
                    street = fix_street(street, street_mapping)
                    if street:
                        tagdict['value'] = street
                    else:
                        continue
            else: #if this doesn't contain a street name at all
                continue
        elif k == 'addr:city': #if city
            tagdict['value'] = fix_city(tag.attrib['v'])
            tagdict['type'] = 'addr'
            tagdict['key'] = 'city'
        elif k == 'cuisine': #if cuisine
            cuisine = tag.attrib['v']
            tagdict['type'] = 'regular'
            tagdict['key'] = 'cuisine'
            if cuisine in expected_cuisine: #if expected, we're good
                tagdict['value'] = cuisine
            else: #else fix it
                cuisine = fix_cuisine(cuisine)
                if cuisine:
                    tagdict['value'] = cuisine
                else: #skip it if it's bad
                    continue                
        elif re.search(LOWER_COLON, k): #if colon in k
            start = re.search(':', k).start()
            tagdict['type'] = k[:start]
            tagdict['key'] = k[start+1:]
            tagdict['value'] = tag.attrib['v']
        else: #else it is a normal tag
            tagdict['type'] = 'regular'
            tagdict['key'] = k
            tagdict['value'] = tag.attrib['v']
        tags.append(tagdict)

    if element.tag == 'node':
        for field in node_attr_fields[:-1]:
            node_attribs[field] = element.attrib[field]
        neighborhood = assign_neighborhood(float(element.attrib['lon']), float(element.attrib['lat']), neighborhoods)
        if neighborhood: #if in a neighborhood, assign
            node_attribs['neighborhood'] = neighborhood
        return {'node': node_attribs, 'node_tags': tags}
    elif element.tag == 'way':
        for field in way_attr_fields:
            way_attribs[field] = element.attrib[field]
        count = 0 #initialize counter
        for tag in element.findall('nd'): #look through nd tags
            tagdict = {}
            tagdict['id'] = element.attrib['id']
            tagdict['node_id'] = tag.attrib['ref']
            tagdict['position'] = count
            count += 1
            way_nodes.append(tagdict)            
        return {'way': way_attribs, 'way_tags': tags, 'way_nodes': way_nodes}
    
#this code is the same as the code used in the exercises in class
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w') as nodes_file, \
         codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file, \
         codecs.open(WAYS_PATH, 'w') as ways_file, \
         codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file, \
         codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])

def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)
        
        raise Exception(message_string.format(field, error_string))


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
            
#process_map(OSM_FILE, False)

