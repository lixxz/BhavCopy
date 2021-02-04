import csv
import requests
import zipfile
import os
from django.utils import timezone
from django.core.cache import cache
from celery import shared_task


@shared_task
def cache_bhavcopy():
    # url info
    bhav_zip = f"EQ{timezone.now().date().strftime('%d%m%y')}_CSV.ZIP"
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0"}
    url = f"https://www.bseindia.com/download/BhavCopy/Equity/{bhav_zip}"

    r = requests.get(url, headers=headers)

    if r.status_code == 200:
        # saving locally
        with open(bhav_zip, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=128):
                fd.write(chunk)

        with zipfile.ZipFile(bhav_zip, 'r') as fp:
            bhav_csv = fp.namelist()[0]
            fp.extractall()

        with open(bhav_csv, newline='') as fp:
            reader = csv.DictReader(fp)
            # saving to redis
            for row in reader:
                row['DATE'] = timezone.now().strftime('%d/%m/%y')
                cache.set(f"{row['SC_NAME'].strip()+row['DATE']}", row, timeout=None)

        # cleaning
        os.remove(bhav_zip)
        os.remove(bhav_csv)

    return r.status_code
