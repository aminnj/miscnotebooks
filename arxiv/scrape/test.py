import requests
import os
import time
from xmljson import yahoo
import json
from lxml import etree
import requests_cache
from pprint import pprint
import gzip
import re

# requests_cache.install_cache("cache",backend="sqlite",expire_after=1e7)

def get_json(url,key="ListRecords"):
    r = requests.get(url)
    if not getattr(r,"from_cache",False):
        time.sleep(5.1)
    # https://stackoverflow.com/questions/13412496/python-elementtree-module-how-to-ignore-the-namespace-of-xml-files-to-locate-ma
    content = re.sub(' (xmlns(:xsi|)|xsi:schemaLocation)="[^"]+"', '', r.content)
    dom = etree.fromstring(content)
    x = yahoo.data(dom)
    try:
        return x.values()[0][key]
    except KeyError:
        print r.content

def get_category_info():
    url = "http://export.arxiv.org/oai2?verb=ListSets"
    js = get_json(url,key="ListSets")
    return dict([(x["setName"],x["setSpec"]) for x in js["set"]])

def scrape_arxiv(category="q-fin",until="2019-07-10",outputdir="data/",skip_if_folder_exists=True):

    basedir = "{outputdir}/{category}".format(outputdir=outputdir,category=category.replace(":","_"))
    if os.path.exists(basedir) and skip_if_folder_exists:
        return
    os.system("mkdir -p {basedir}".format(basedir=basedir))

    url = "http://export.arxiv.org/oai2?verb=ListRecords&until={until}&metadataPrefix=arXiv&set={category}".format(until=until,category=category)
    cursor = 0
    while True:

        js = get_json(url)
        cursor = js["resumptionToken"]["cursor"]
        resumption_token = js["resumptionToken"].get("content",None)
        total_count = js["resumptionToken"]["completeListSize"]
        records = js["record"]

        fname = "{basedir}/{cursor}.json.gz".format(basedir=basedir,cursor=cursor)
        with gzip.open(fname,"w") as fh:
            json.dump(records,fh)

        print "[{}] [{}/{}] got {} records, saved to {}".format(category,cursor,total_count,len(records),fname)

        if not resumption_token:
            break

        url = "http://export.arxiv.org/oai2?verb=ListRecords&resumptionToken={resumption_token}".format(resumption_token=resumption_token)

if __name__ == "__main__":
    # print get_category_info()
    for category in get_category_info().values():
        if "physics" not in category: continue
        scrape_arxiv(category=category,until="2019-07-10",skip_if_folder_exists=True)
