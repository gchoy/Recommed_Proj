import os, sys
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "graphicN.settings")

import django
django.setup()

from reviews.models import Comic

def save_comic_from_row(comic_row):
    comic = Comic()
    comic.id = comic_row[0]
    comic.name = comic_row[1]
    comic.save()


if __name__ == "__main__":

    if len(sys.argv) == 2:
        print "Reading from file" + str(sys.argv[1])
        comics_df = pd.read_csv(sys.argv[1])
        print comics_df

        comics_df.apply(save_comic_from_row,axis=1)

        print "There are {} wines".format(Comic.objects.count())

    else:
        print "Please, provide Comic file path"
