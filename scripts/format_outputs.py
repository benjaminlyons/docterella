#!/usr/bin/env python

import json
import pandas as pd
import sys
import click

@click.command()
@click.argument('filename', type=click.Path(exists=True))
@click.option('--style', '-s', multiple=True, type=str,
              help='Filter metrics by the style column')
@click.option('--suite', '-t', multiple=True, type=str,
              help='Filter metrics by the suite column')
def main(filename, style, suite):
    """filename: Path to csv file containing metrics"""
    df = pd.read_csv(filename)

    if style:
        df = df[df["style"].isin(style)]

    if suite:
        df = df[df["suite"].isin(suite)]

    print(json.dumps(df.to_dict(orient='index'), indent=4))

if __name__ == "__main__":
    main()
