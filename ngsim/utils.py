# !pip3 install --user ijson yajl
import pandas as pd
import numpy as np
import requests
import ijson
import gzip
from tqdm.auto import tqdm
from urllib.request import urlopen
import os

class Dataset(object):
    
    def __init__(self, path):
        """
        Parameters
        ----------
        path : string
            Local path or URL

        Returns
        -------
        Dataset object
        """
        self.path = path
        self.meta_dict = None
        
        self.m_df = None
        self.d_df = None
        self.c_df = None
    
    def _open_path(self):
        if self.path.startswith("http"):
            return urlopen(self.path)
        elif os.path.exists(self.path):
            if self.path.endswith("gz"):
                return gzip.open(self.path)
            else:
                return open(self.path)
        else:
            raise Exception("File does not exist!")
            
    def _get_meta_dict(self):
        if self.meta_dict is None:
            f = self._open_path()
            self.meta_dict = next(ijson.items(f, "meta"))
        return self.meta_dict
        
    def meta_df(self):
        """
        Returns
        -------
        pd.DataFrame
            Dataframe of dataset global metadata
        """
        meta = self._get_meta_dict()
        if self.m_df is None:
            self.m_df = (
                pd.DataFrame(meta["view"].items())
                .set_index(0)
                .filter(items=["name","category","createdAt","description","downloadCount","oid","publicationDate","tableId","tags"],axis=0)
                .T
            )
            # self.m_df.style.set_properties(subset=["name","description","tags"],**{'width': '30%'})
        return self.m_df
        
    
    def column_df(self):
        """
        Returns
        -------
        pd.DataFrame
            Dataframe of column information
        """
        meta = self._get_meta_dict()
        if self.c_df is None:
            self.c_df = (
                pd.DataFrame(meta["view"]["columns"])
                .drop(["id","name","dataTypeName","format","flags","tableColumnId","width","cachedContents"],axis=1)
                .query("position>=1")
                .reset_index(drop=True)
            )
            # self.c_df.style.set_properties(subset=['description'], **{'width': '100%'})
        return self.c_df
        
    def column_names(self):
        """
        Returns
        -------
        list
            Column names
        """
        return self.column_df().fieldName.tolist()
    
    def data_df(self, max_rows=-1, progress=False, chunk_rows=-1):
        """
        Parameters
        ----------
        max_rows : int (default -1)
            Maximum number of rows over which to iterate. Default is all.
        chunk_rows : int (default -1)
            If >0, yields dataframes with size `chunk_rows`
        progress : bool
            Displays a progress bar

        Returns
        -------
        pd.DataFrame
            (or yields several, depending on `chunk_rows`)
        """
        cnames = self.column_names()
        iterable = ijson.items(self._open_path(), "data.item")
        if progress:
            iterable = tqdm(iterable)

        def transform(row):
            # The row has additional metadata at the beginning which were already dropped from column_names,
            # so reverse the lists before zipping to chop off the metadata
            return dict(zip(reversed(cnames),reversed(row)))

        if chunk_rows > 0:
            def lazy():
                data = []
                for irow,row in enumerate(iterable):
                    if (max_rows > 0) and irow > max_rows - 1:
                        yield pd.DataFrame(data)
                        return
                    if (chunk_rows > 0) and len(data) >= chunk_rows:
                        yield pd.DataFrame(data)
                        data = []
                    data.append(transform(row))
                if len(data):
                    yield pd.DataFrame(data)
                else:
                    return
        else:
            def lazy():
                data = []
                for irow,row in enumerate(iterable):
                    if (max_rows > 0) and irow > max_rows - 1:
                        break
                    data.append(transform(row))
                return pd.DataFrame(data)

        return lazy()
