"""Download approved UCI SMS Spam Collection and convert to the required CSV."""
from pathlib import Path
from io import BytesIO
import urllib.request, zipfile
import pandas as pd
url='https://archive.ics.uci.edu/static/public/228/sms+spam+collection.zip'
dest=Path(__file__).resolve().parent/'data'/'dataset.csv'
try:
    with urllib.request.urlopen(url,timeout=60) as f: raw=f.read()
    with zipfile.ZipFile(BytesIO(raw)) as z: rows=z.read('SMSSpamCollection')
except Exception as exc:
    manual=dest.parent/'SMSSpamCollection'
    if manual.exists():
        rows=manual.read_bytes()
        print('Using manually downloaded UCI source file:', manual)
    else:
        raise SystemExit('UCI download failed. Download the official ZIP from https://archive.ics.uci.edu/dataset/228/sms+spam+collection, extract SMSSpamCollection into data/, and rerun this script. Original error: '+str(exc))
from io import StringIO
df=pd.read_csv(BytesIO(rows),sep='\t',header=None,names=['label','text'],encoding='latin-1')
dest.parent.mkdir(exist_ok=True)
df.to_csv(dest,index=False,encoding='utf-8')
print('Saved',len(df),'messages to',dest)
