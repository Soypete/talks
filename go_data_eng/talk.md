---
theme: gaia
_class: lead
paginate: true
backgroundColor: #fff
backgroundImage: url('https://marp.app/assets/hero-background.jpg')
marp: true
footer: ![width:200px](images/WeaveLogoDarkGray.png)
---

# Tips and Tricks for Data Engineering in the #GOshop
Miriah Peterson
<!-- 
Abstract: --> 

___


![bg right fit](images/IMG_3232.jpg)

# Bio

- Data Engineer at Weave in Lehi, Utah
- Board Member with Forge Foundation
- Proud Dog Mom
- [Twitter @captainnobody1](https://www.twitter.com/captainnobody1)
- [GitHub soypete](https://www.github.com/soypete)
- [LinkedIn](https://www.linkedin.com/in/miriah-peterson-35649b5b)

---

>Bob: I am wondering if you actually get to use Go in your data pipelines or is it still mostly SQL/Python for you? I am curious how do you go about ensuring data quality in your data pipelines? Does Weave have a formal framework for monitoring/alerting on quality?
Me:  We are all go
Bob: Wow! What runs Go for ETL besides Beam/DataFlow?
Me: We are very creative with sql
Bob: I am intrigued! Anything open-sourced?
Me: The only non-open source product we have in our data stack is vertica (except homegrown of course )
Bob: Aha. So you express your ETL in Go which then translates to SQL? Or writing good old SQL? just curious

---

Tips and Tricks I have learned doing Data Engineering in Go

---

Do ELT not ETL

--- 

Use a messaging/streaming service over channels
- nats
- nsq
- api calls slow things down

---

Pick the Data type at Extration and stick to it
- unstructured data is popular in other platforms *avoid it*
- Can you use scraping to help define data

---

Rely on your database

--- 

Transforming for the Database is not the same as transforming for product consumption

--- 

If you are doing microservice architecture they each consumption point is a unique service

--- 

Don't be afraid of generating code

--- 

Use a schema repository (grpc + go =  heart)

--- 

Find a good sql library

--- 

Use If you don't have to make it in house, if you do, do not over engineer it 
 - pachydern
 - beam
___

Pointers make things lighter

--- 

Always pass errors up

---