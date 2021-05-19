wget https://repo1.maven.org/maven2/org/apache/jena/jena-fuseki-docker/4.0.0/jena-fuseki-docker-4.0.0.zip
unzip jena-fuseki-docker-4.0.0.zip
rm jena-fuseki-docker-4.0.0.zip
rm -rf fuseki
mv jena-fuseki-docker-4.0.0 fuseki
mkdir -p databases/DB2