# Some technical thoughts on processing MEI sources to facilitate their future scholarly semantic annotation

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