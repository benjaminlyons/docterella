#!/usr/bin/env python

import json
import pandas as pd
import sys

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = "tests/data/results/metrics.csv"

df = pd.read_csv(filename)

df = df[df["style"] == "reasoning"]

print(json.dumps(df.to_dict(orient='index'), indent=4))
