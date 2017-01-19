# wordcloud-bot

a twitter bot written in python which posts wordclouds 
generated from norwegian newspapers websites

it works for:

- vg.no
- nrk.no
- dagbladet.no

install dependencies with pip

        pip3 install [--user] -r requirements.txt

automate to run once a day (e.g. at 6 pm) by adding as cron-job:

        0 18 * * * cd wordcloud-bot ; python3 cloud.py --tweet vg.no nrk.no dagbladet.no
