#!/usr/bin/python3
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF, RDFS, XSD, OWL
import sys

g = Graph()
g.parse('data-product-ontology.ttl', format='turtle')
g.parse('mobilitydcat-ap.ttl', format='turtle')

# Create DOT file with custom formatting
with open('ontology.dot', 'w') as f:
    f.write('digraph G {\n')
    f.write('  node [shape=box, style=filled, fillcolor=lightblue];\n')
    f.write('  edge [arrowhead=normal];\n\n')
    
    # Process classes
    classes = {}
    # Check for RDFS classes
    for s, p, o in g.triples((None, RDF.type, None)):
        if o in [ RDFS.Class, OWL.Class ]:
            if isinstance(s, URIRef):
                label = str(s).split('#')[-1]
                classes[str(s)] = {'label': label, 'properties': [], 'relationships': []}
                print("Class in type: " + label)

    for s, p, o in g.triples((None, RDFS.domain, None)):
            if isinstance(o, URIRef):
                label = str(o).split('#')[-1]
                classes[str(o)] = {'label': label, 'properties': [], 'relationships': []}
                print("Class in domain: " + label)
        
    for s, p, o in g.triples((None, URIRef('http://purl.org/dc/dcam/domainIncludes'), None)):
            if isinstance(o, URIRef):
                label = str(o).split('#')[-1]
                classes[str(o)] = {'label': label, 'properties': [], 'relationships': []}
                print("Class in domainIncludes: " + label)
        
    for s, p, o in g.triples((None, RDFS.range, None)):
            if not str(o).startswith(str(XSD)) and not str(o).endswith('Literal'):
                label = str(o).split('#')[-1]
                classes[str(o)] = {'label': label, 'properties': [], 'relationships': []}
                print("Class in range: " + label)
        
    for s, p, o in g.triples((None, URIRef('http://purl.org/dc/dcam/rangeIncludes'), None)):
            if not str(o).startswith(str(XSD)):
                label = str(o).split('#')[-1]
                classes[str(o)] = {'label': label, 'properties': [], 'relationships': []}
                print("Class in rangeIncludes: " + label)
        
    # Process properties and their domains/ranges
    # First collect all properties with their domains
    properties = {}
    for s, p, o in g.triples((None, RDFS.domain, None)):
        if str(o) in classes:
            properties[str(s)] = {'domain': str(o)}
    
    # Also check dcam:domainIncludes
    for s, p, o in g.triples((None, URIRef('http://purl.org/dc/dcam/domainIncludes'), None)):
        if str(o) in classes:
            print('Found starting class: ' + str(o))
            if str(s) not in properties:
                properties[str(s)] = {'domain': str(o)}
    
    # Process each property's range
    for prop_uri, prop_info in properties.items():
        domain_class = prop_info['domain']
        prop_label = prop_uri.split('#')[-1]
        
        # Check both RDFS.range and dcam:rangeIncludes
        range_obj = g.value(URIRef(prop_uri), RDFS.range)
        if not range_obj:
            range_obj = g.value(URIRef(prop_uri), URIRef('http://purl.org/dc/dcam/rangeIncludes'))
            print('Found range: ' + str(range_obj))
        
        if range_obj:
            range_label = str(range_obj).split('#')[-1]
            if str(range_obj).startswith(str(XSD)):
                # It's a datatype property
                range_label = str(range_obj).split('#')[-1]
                prop_label += f': {range_label}'
                classes[domain_class]['properties'].append(prop_label)
            elif str(range_obj) in classes:
                # It's an object property - add it both as an attribute and a relationship
                range_class_label = classes[str(range_obj)]['label']
                prop_label += f': {range_class_label}'
                classes[domain_class]['properties'].append(prop_label)
                classes[domain_class]['relationships'].append({
                    'target': str(range_obj),
                    'label': prop_label.split(':')[0]  # Use just the property name for the arrow label
                })
    
    # Write class nodes with their properties
    for class_uri, class_info in classes.items():
        f.write(f'  \"{class_info['label']}\" [label=\"{class_info['label']}\\n')
        for prop in class_info['properties']:
            f.write(f'  + {prop}\\n')
        f.write('\"];\n')
    
    # Write relationships between classes
    for class_uri, class_info in classes.items():
        for rel in class_info['relationships']:
            f.write(f'  \"{class_info['label']}\" -> \"{classes[rel['target']]['label']}\" [label=\"{rel['label']}\"];\n')
    
    # Write inheritance relationships
    for s, p, o in g.triples((None, RDFS.subClassOf, None)):
        if str(s) in classes and str(o) in classes:
            f.write(f'  \"{classes[str(s)]['label']}\" -> \"{classes[str(o)]['label']}\" [arrowhead=empty];\n')
    
    f.write('}\n')
