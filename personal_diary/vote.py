## 單次執行
import csv ,os ,django

os.environ.setdefault("DJANGO_SETTINGS_MODULE",'personal_diary.settings')

django.setup()

from mysite.models import  Vote

with open("votes.csv","r",encoding='utf-8-sig') as fp:
    csvdata = csv.DictReader(fp)
    data = [item for item in csvdata]

for item in data :
    if len(Vote.objects.filter(name=item['name'].strip())) ==0:
        rec = Vote(
            name=item['name'],
            no=int(item['no']),
            sex=(True if item['sex']=='男' else False),
            byear=int(item['byear']),
            party=item['party'],
            votes=int(item['votes']),
            )
        rec.save()

print('Done')