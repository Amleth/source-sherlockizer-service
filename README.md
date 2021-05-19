# Some technical thoughts on processing MEI sources to facilitate their future scholarly semantic annotation

## Scientific goals

<div style="border: 3px solid darkturquoise; ; padding: 1em;">
<div style="color: darkturquoise">
To support modal & tonal analysis, which implies (at least) two functional prerequisites regarding the addressability of MEI elements:
</div><br/>

- **PREREQUISITE 1 —** The possibility <span style="color: darkturquoise">to address arbitrary sets of MEI elements</span> that do not necessarily follow the logical organization of the MEI file structure. _For example: groupings of notes which forms a relevant observable on the musicological level but they are disjointed in the MEI XML structure._
- **PREREQUISITE 2 —** The possibility <span style="color: darkturquoise;">to address "verticalities"</span> (musical offsets expressed in rhythmic values), for example to annotate the score with fundamentals that have been identified by the analysts. These verticalities are not materialized in the MEI encoding.
</div><br/>

Since the question we are trying to answer here is: _"How to create anchors in MEI documents that are relevant to musicological analysis?"_, and since we are trying to answer it in the LOD paradigm, this work is related to other ongoing reflections, approaches & tools:

- The [MEI Linked Data Interest Group](https://music-encoding.org/community/interest-groups.html)
- [SPARQL-Anything](https://github.com/SPARQL-Anything/sparql.anything)
- [MIDI Linked Data](https://midi-ld.github.io/)
- Thoughts on non-trivial addressing of fragments in online documents
- Semantic modeling of annotation anchors related aspects
- _Aspects related to score edition_ vs. _aspects related to score annotation_
- _Encoding of musical sources_ vs. _musical meaning_
- …

## Technical analysis

### PREREQUISITE 1 implications & decisions

The addressability of arbitrary sets of MEI elements implies that:

- each and every XML element in a MEI file should be identified by an unique IRI ;
- each and every arbitrary sets of elements should also be identified by an unique IRI, so as to provide anchors for scholarly annotations on the Web.

#### IRIs generation strategy

If each and every MEI XML element should receive its own IRI, then it would be convenient if they were uniquely identified within the file (for example with `xml:id`). We could then generate their IRIs based on their XML identifiers.

### Document or semantic data?

### A few words about viewing & dereferencing IRIs

[![](https://mermaid.ink/img/eyJjb2RlIjoiXG5ncmFwaCBMUlxuYSAtLT4gYlxuIiwibWVybWFpZCI6eyJ0aGVtZSI6ImRlZmF1bHQifX0)](https://mermaid-js.github.io/mermaid-live-editor/#/edit/eyJjb2RlIjoiXG5ncmFwaCBMUlxuYSAtLT4gYlxuIiwibWVybWFpZCI6eyJ0aGVtZSI6ImRlZmF1bHQifX0)

### RDFizing & SPARQLing the score

## The infratructure

### What are the components and what are their technical roles?

- A REST service developped with [FastAPI](https://fastapi.tiangolo.com/), which processes an input MEI file with [lxml](https://lxml.de/) and [music21](https://web.mit.edu/music21/), and generates RDF data with [rdflib](https://rdflib.readthedocs.io/en/stable/).
- [Jena Fuseki](https://jena.apache.org/documentation/fuseki2/), which receives the aforementioned RDF data.
- [Apache](https://httpd.apache.org/), which statically hosts the aforementioned processed MEI file.
- [PostgreSQL](https://www.postgresql.org/), which is used as a cache system that stores unique UUID generated for RDF resources which creation results from the score analysis.

Everything works together thanks to some [docker-compose wizardry](docker-compose.yml).

### How to test it?

1. Fetch official Apache Fuseki Dockerfile by running this script: `./init-fuseki-docker.sh` (see: https://jena.apache.org/documentation/fuseki2/fuseki-docker.html)
2. `docker-compose up --build`
