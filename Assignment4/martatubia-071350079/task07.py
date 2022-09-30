# -*- coding: utf-8 -*-
"""Task07.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tcI-UWukIOzDsi8MXUOOWQQ8A6S6ju0Y

**Task 07: Querying RDF(s)**
"""

!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2021-2022/master/Assignment4/course_materials"

"""Leemos el fichero RDF de la forma que lo hemos venido haciendo"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")
for s,p,o in g:
  print(s,p,o)

"""**TASK 7.1: List all subclasses of "Person" with RDFLib and SPARQL**"""

# TO DO
from rdflib.plugins.sparql import prepareQuery
ns = Namespace("http://somewhere#")

# Primero con RDFLib
for s,p,o in g.triples((None, RDFS.subClassOf, ns.Person)):
    print(s)
    
    
#Segundo con SPARQL
from rdflib.plugins.sparql import prepareQuery 
q1 = prepareQuery('''
  SELECT 
    ?Subclass 
  WHERE { 
    ?Subclass rdfs:subClassOf ns:Person.
    
  }
  ''',
  initNs = {"rdfs":RDFS, "ns":ns}
)


for s1 in g.query(q1):
  print(s1)

"""**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**

"""

# TO DO
#Primero con RDFLib
#Individuos personas
for s,p,o in g.triples((None, RDF.type, ns.Person)):
  print(s)
#Individuos en subclase de persona
for subClass,p,o in g.triples((None, RDFS.subClassOf, ns.Person)):
  for s2,p2,o2 in g.triples((None, RDF.type, subClass)):
    print(s2)
    

#Segundo con SPARQL
q2 = prepareQuery('''
  SELECT 
    ?persona 
  WHERE { 
    ?subclass rdfs:subClassOf* ns:Person.
    ?persona rdf:type ?subclass. 
        }
  ''',
  initNs = {"rdfs":RDFS, "ns":ns, "rdf":RDF}
)

# Visualize the results
print("\n Ahora con SPARQL")
for r in g.query(q2):
  print(r.persona)

"""**TASK 7.3: List all individuals of "Person" and all their properties including their class with RDFLib and SPARQL**

"""

# TO DO
for s,r,o in g.triples((None,RDF.type, ns.Person)):
  for s2,r2,o2 in g.triples((s,None,None)):
    print(s,r2,o2)

for subclase,p2,o2 in g.triples((None,RDFS.subClassOf,ns.Person)):
    for ins,p3,o3 in g.triples((None, RDF.type, subclase)):
       for s2,r2,o2 in g.triples((ins,None,None)):
          print(s,r2,o2)


q3 = prepareQuery('''
  SELECT 
    ?persona ?r ?o
  WHERE { 
?clase rdfs:subClassOf* ns:Person.
?persona rdf:type ?clase.
?persona ?r ?o.
    }
  ''',
  initNs = {"ns":ns, "rdf":RDF, "rdfs":RDFS}
)

print("\n Ahora con SPARQL")
for r in g.query(q3):
  print(r.persona,r.r,r.o)