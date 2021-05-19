from lxml import etree
from music21 import *


def get_offsets_data(score_xml):
    score = etree.tostring(score_xml, pretty_print=True)

    conv = mei.MeiToM21Converter(score)
    the_score = conv.run()

    identified_elements_offset_data = {}
    score_offsets = set()

    for el in the_score.recurse().sorted:
        if type(el.id) == str:
            if type(el.duration) == duration.Duration:
                score_offsets.add(el.offset)
                identified_elements_offset_data[el.id] = {
                    "from": el.offset,
                    "to": el.offset + el.duration.quarterLength,
                    "duration": el.duration.quarterLength
                }

    for xmlid, data in identified_elements_offset_data.items():
        if not "offsets" in data:
            data["offsets"] = set()
            data["offsets"].add(data["from"])
        for _xmlid, _data in identified_elements_offset_data.items():
            if xmlid != _xmlid:
                if data["from"] <= _data["from"] and _data["from"] < data["to"]:
                    data["offsets"].add(_data["from"])

    for xmlid, data in identified_elements_offset_data.items():
        if "offsets" in data:
            data["offsets"] = list(sorted(data["offsets"]))

    return {
        "score_offsets": list(sorted(score_offsets)),
        "elements": identified_elements_offset_data
    }
