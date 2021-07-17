---
theme: gaia
_class: lead
paginate: true
backgroundColor: #fff
backgroundImage: url('../images/ray.jpg')
marp: true
---

# Using GCP and Docker for Schedule Based GO Scripts
Miriah Peterson
___

## Bio
- Data Engineer at Weave in Lehi, Utah
- Board Member with Forge Foundation
- Proud Dog Mom
- [Twitter @captainnobody1](https://www.twitter.com/captainnobody1)
- [GitHub soypete](https://www.github.com/soypete)
- [Twitch soypete01](https://twitch.tv/soypete01)

---

## Set the Stage
- I Want to get a weekly list of upcoming Forge Foundation events
- Meetup Api has oauth requirements
- They would not grant me a token
- I build a Web Scrapper to get the event information

---

## Web Scrapper
- [Github](https://github.com/soypete/event-web-crawler)
<!-- Insert image of forge events page -->
- call web address to get the site file
- parse the site file to get the event information
    - look we get pre-formatted json
- Take the json and Dump it to a cloud firestore

---
## Web Scrapper
<!-- - demo the web scrapper and show it work -->

--- 
## Web Scrapper
- Now that it works I want to get a weekly list of upcoming Forge events
- This list can be used to update a static site

---
## Cron Job

Running cron jobs on Google Cloud Platform.

---
## Cron Job
Options:
- App Engine Cron
- cloud functions
- cloud Run + Scheduler
- Kubernetes Cron on GKE 

---
## Cron Job

### Step 1: Create a docker image

---
## Cron Job

### Step 2: Add the docker image to the Google Cloud Registry

---
## Cron Job

### Step 3: Add image to Cloud Run Instance

---
## Cron Job

### Step 4: Create Endpoint for Calling Cloud Run

--- 
## Cron Job

### Step 5: Create schedule for calling the Cloud Run

---
## Hurrdles
- creaing service accounts 
- adding the firebase permissions
- accessing logs
- exposing enpoints (add a health check)

---
## Summary

---
## Questions
Thanks you for coming out to this talk!
[twitch.tv/soypete01](https://twitch.tv/soypete01)
[twitter.com/captainnobody1](https://twitter.com/captainnobody1)
[youtube.com/captainnobody1]()

---
## Resources
- [Firestore video]
- [Crawler streams]
- [code]
- [GCP docks]