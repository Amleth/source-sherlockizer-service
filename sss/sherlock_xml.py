from lxml import etree

xml_ns = {'xml': 'http://www.w3.org/XML/1998/namespace'}


def idize(doc):
    i = 0
    for e in doc.xpath('//*'):
        xmlida = '{' + xml_ns['xml'] + '}id'
        if xmlida not in e.attrib:
            e.attrib[xmlida] = etree.QName(e.tag).localname + '-' + str(i)
            i += 1

    return doc
