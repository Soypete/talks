---
theme: gaia
_class: lead
paginate: true
backgroundColor: #fff
backgroundImage: url('../images/ray.jpg')
footer: '[crawler code](https://github.com/soypete/event-web-crawler)'
marp: true
---

# Using GCP and Docker for Schedule Based GO Scripts
Miriah Peterson
___

## Bio
- golang + rust streamer Twitch : [@soypete](https://www.twitch.tv/soypete01)
- Board Member with Forge Foundation
- Proud Dog Mom
- [Twitter @captainnobody1](https://www.twitter.com/captainnobody1)
- [GitHub soypete](https://www.github.com/soypete)

---

## Set the Stage
<!-- - I want to get a weekly list of upcoming Forge Foundation events
- Meetup api has oauth requirements
- They would not grant me a token
- I build a Web Scrapper to get the event information -->
![w:620](../images/meetup-pro.png)

---


## Web Scrappery
1. call web address to get the site file
1. parse the site file to get the event information
1. Take the json and Dump it to a cloud firestore
---
## Web Scrappery
```json
{
  "@context": "http://schema.org",
  "@type": "Event",
  "name ": "Building CLI apps in Golang ",
  "url": "https://www.meetup.com/Women-Who-Go-Utah/events/277283469/",
  "description": "",
  "startDate": "2021-05-25T18:30-06:00",
  "endDate": "2021-05-25T20:30-06:00",
  "eventStatus": "https://schema.org/EventScheduled",
  "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
  "location": {
    "@type": "Place",
    "address": {
      "@type": "PostalAddress",
      "addressRegion": "UT"
    },

  },
  "organizer": {
    "@type": "Organization",
    "name": "Women Who Go  Utah ( + Allies)",
    "url": "https://www.meetup.com/Women-Who-Go-Utah"
  }
}
```
---
## Web Scrapper

CODE TIME!

![w:630 right](https://media.giphy.com/media/mYhd1NHQkHmZLiqN7M/giphy.gif)
<!-- - demo the web scrapper and show it work -->

--- 
## Web Scrapper
Pull weekly report

---
## Cron Job

Running cron jobs on Google Cloud Platform.

---
## Cron Job
Running cron jobs on Google Cloud Platform.

Options:
- [App Engine Cron](https://cloud.google.com/appengine/docs/flexible/nodejs/scheduling-jobs-with-cron-yaml)
![bg right 60%](../images/AppEngine-512-color.png)

---
## Cron Job
Running cron jobs on Google Cloud Platform.

Options:
- [App Engine Cron](https://cloud.google.com/appengine/docs/flexible/nodejs/scheduling-jobs-with-cron-yaml)
- [Cloud Functions + Scheduler](https://cloud.google.com/scheduler/docs/tut-pub-sub)
![bg right 60%](../images/cloud-functions-512-color.png)


---
## Cron Job
Running cron jobs on Google Cloud Platform.

Options:
- [App Engine Cron](https://cloud.google.com/appengine/docs/flexible/nodejs/scheduling-jobs-with-cron-yaml)
- [Cloud Functions + Scheduler](https://cloud.google.com/scheduler/docs/tut-pub-sub)
- [Cloud Run + Scheduler](https://cloud.google.com/run/docs/triggering/using-scheduler)
![bg right 60%](../images/cloud-functions-512-color.png)
---
## Cron Job
Running cron jobs on Google Cloud Platform.

Options:
- [App Engine Cron](https://cloud.google.com/appengine/docs/flexible/nodejs/scheduling-jobs-with-cron-yaml)
- [Cloud Functions + Scheduler](https://cloud.google.com/scheduler/docs/tut-pub-sub)
- [Cloud Run + Scheduler](https://cloud.google.com/run/docs/triggering/using-scheduler)
- [Kubernetes Cron on GKE](https://cloud.google.com/kubernetes-engine/docs/how-to/cronjobs)
![bg right 50%](../images/gke-cron-512-color.png)
---
## Cron Job

### Step 1: Create a docker image
```dockerfile
FROM golang:alpine

WORKDIR /app
COPY go.* ./
RUN go mod download

COPY . ./
COPY --chown=root permissions/meetup-crawler-store-b25be2c787ec.json ./creds.json
RUN go build -v -o scraper

CMD ["/app/scraper"]
```
---
## Cron Job

### Step 2: Add the docker image to the Google Cloud Registry
```bash
bash 
gcloud builds submit --tag gcr.io/meetup-crawler-store/web-crawler
```

---
## Cron Job

### Step 3: Add image to Cloud Run Instance
```bash 
gcloud run deploy --image gcr.io/meetup-crawler-store/web-crawler --platform managed
```
---
## Cron Job

### Step 4: Create Endpoint for Calling Cloud Run
```go
	log.Print("starting server...")
	http.HandleFunc("/crawl", runCrawler)
	http.HandleFunc("/health", healthCheck)

	// Determine port for HTTP service.
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
		log.Printf("defaulting to port %s", port)
	}
```

--- 
## Cron Job

### Step 5: Create schedule for calling the Cloud Run

```bash
gcloud scheduler jobs create http test-handler --schedule "5 * * * *"  
--http-method=Get 
--uri=https://{app_address}/crawl
--oidc-service-account-email=web-crawler-scheduler@meetup-crawler-store.iam.gserviceaccount.com
--oidc-token-audience=https://{app_address}/crawl
```
---
## Hurdles
- Creating service accounts 
- adding the firebase permissions
- Accessing logs
- exposing endpoints
---
## Summary
Docker support makes it really easy to create a containerized applications/scripts. 
Great for deploying and running go your code.

---
## Questions
Thanks you for coming out to this talk!
[twitch.tv/soypete01](https://twitch.tv/soypete01)
[twitter.com/captainnobody1](https://twitter.com/captainnobody1)
[youtube.com/captainnobody1](https://www.youtube.com/channel/UCeXy81WS-kX9JBc2kNzrV3A)

---
## Resources
- [Firestore video](https://www.youtube.com/watch?v=lIyPvpWqxKM)
- [Crawler streams](https://youtu.be/LsJQqa-kW6Q)