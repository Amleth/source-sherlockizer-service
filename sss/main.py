import chardet
from fastapi import FastAPI, Form
import hashlib
from lxml import etree
import os
from pydantic import BaseModel
import requests

from mei_sherlockizer import rdfize
from sherlock_xml import idize
from mei_offsets import get_offsets_data

graph = "http://data-iremus.huma-num.fr/graph/meiweb"


class MeiFile(BaseModel):
    uri: str


class Encoding(BaseModel):
    encoding: str
    confidence: float
    language: str


class SherlockMeiFile(BaseModel):
    input_file_encoding: Encoding
    input_file_sha1: str
    input_file_uri: str
    sherlock_file_uri: str
    sherlock_score_uri: str


app = FastAPI()

if not os.path.exists(os.environ['MEI_WEB_FILES_BASE_DIR']):
    os.mkdir(os.environ['MEI_WEB_FILES_BASE_DIR'])


@app.post("/sss/mei", response_model=SherlockMeiFile)
async def root(uri: str = Form(...)):

    # We fetch the input MEI file
    r = requests.get(uri)

    # The SHA1 of the input MEI file will provide a basis for id generation
    input_file_sha1 = hashlib.sha1()
    input_file_sha1.update(r.content)
    input_file_sha1 = input_file_sha1.hexdigest()

    # What is the encoding of the input MEI file? It will enventually be set to UTF-8
    input_file_encoding = chardet.detect(r.content)

    # Let's get some XML
    input_file_doc = etree.fromstring(r.content)

    # We add a unique xml:id to elements that do not have them
    sherlock_file_doc = idize(input_file_doc)

    # We store the new MEI file somewhere on the server, and encode it to UTF-8
    with open(os.environ['MEI_WEB_FILES_BASE_DIR'] + input_file_sha1 + '_sherlockized.mei', 'wb') as f:
        etree.ElementTree(sherlock_file_doc).write(f, encoding='utf-8', xml_declaration=True, pretty_print=True)

    # We analyse the offsets with Music21
    offsets_data = get_offsets_data(sherlock_file_doc)

    # We define the URI where the new MEI file will be published
    sherlock_file_uri = os.environ['MEI_WEB_FILES_BASE_URI'] + input_file_sha1 + '_sherlockized.mei'

    # We generate the RDF graph corresponding to the "augmented" score, and post it to Fuseki
    ttl = rdfize(
        graph,
        sherlock_file_doc,
        input_file_sha1,
        sherlock_file_uri,
        offsets_data["score_offsets"],
        offsets_data["elements"]
    )
    r = requests.post(
        os.environ['FUSEKI']+'?graph='+graph,
        data=ttl,
        headers={'Content-Type': 'text/turtle;charset=utf-8'}
    )

    # That's all folks
    return SherlockMeiFile(
        input_file_encoding=input_file_encoding,
        input_file_sha1=input_file_sha1,
        input_file_uri=uri,
        sherlock_file_uri=sherlock_file_uri,
        sherlock_score_uri=os.environ['SHERLOCK_ID_BASE_URI'] + input_file_sha1,
    )
