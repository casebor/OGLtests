#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  Copyright 2021 Carlos Eduardo Sequeiros Borja <carseq@amu.edu.pl>
#  

import json
from sys import argv

output = {}
with open(argv[1], "r") as f:
    for line in f:
        if line.startswith("info "):
            i = line.find("\"") + 1
            j = line[i:].find("\"")
            output["name"] = line[i:i+j].replace(" ", "")
        if line.startswith("common "):
            i = line.find("scaleW") + 7
            j = line.find("scaleH") + 7
            output["scaleW"] = int(line[i:i+4])
            output["scaleH"] = int(line[j:j+4])
        if line.startswith("char id="):
            cid = int(line[8:15])
            if cid == 0 or cid == 10 or cid == 32:
                continue
            char = chr(cid)
            x = int(line[18:23])
            y = int(line[25:30])
            w = int(line[36:41])
            h = int(line[48:53])
            output[char] = {"x":x, "y":y, "w":w, "h":h}

with open(argv[1].replace(".fnt", ".json"), "w") as outjson:
    json.dump(output, outjson, indent=2, ensure_ascii=False)

