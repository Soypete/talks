---
theme: gaia
_class: lead
paginate: true
backgroundColor: #fff
backgroundImage: url('../images/gopher_slide.png')
marp: true
footer: ![width:200px](../images/WeaveLogoDarkGray.png)
---

# Tips and Tricks for Data Engineering in the #GOshop
Miriah Peterson
<!-- 
Abstract: Data Engineers today work primarily in Python and Java to create large scale piplines and Data platforms for their companies. As a Data Engineer I have spent the past two years working exclusively in Go. 
In this talk I want to share what I have learn and tips and tricks for success.--> 

___


<!-- ![bg right fit](../images/IMG_3232.jpg) -->

## Bio

- Data Engineer at Weave in Lehi, Utah
- Board Member with Forge Foundation
- Proud Dog Mom
- [Twitter @captainnobody1](https://www.twitter.com/captainnobody1)
- [GitHub soypete](https://www.github.com/soypete)
- [LinkedIn](https://www.linkedin.com/in/miriah-peterson-35649b5b)

---

## Intro

>I am wondering if you actually get to use Go in your data pipelines or is it still mostly SQL/Python for you? I am curious how do you go about ensuring data quality in your data pipelines? Does Weave have a formal framework for monitoring/alerting on quality?
---

## Intro

Tips and Tricks I have learned doing Data Engineering in Go:
- Platform
- Extract Data
- Load Data
- Transform Data

---

## Platform

Platform: Infrastructure for storing, transfering, analyzing, and transforming data.

---

## Platform

Use If you don't have to make it in house, if you do, do not over engineer it
- anticipate constraints and security
<!-- over the wire  -->
- anticipate compliance
- budget time to iterate on your design
 <!-- - pachydern
 - beam -->

---

## Platform

Plan for Monolith or Microservice upfront. no hybrids
- You don't want to maintain/create unnecessary services
- Caching layer
- Number of transfer points
- Don't cheat yourself with Go routines and channels
<!-- - If you are doing microservice architecture then each consumption point is a unique service -->

---

## Platform

Use a messaging/streaming services to manage data flow
- nats
- nsq
- api calls slow things down

---

## Platform

Use a schema repository (grpc + go =  :heart:)
- Standardize data types across services (microservice)
- Leverage Generation
<!-- we need a genericized example of protobuf code generation. Possible vitess?  -->


---

## Extraction

Pick the Data type at Extration and stick to it
- Avoid non-typed data <!-- This is leveraged alot in python and can require thought process switching -->
- Optimize type for storage
- Can you leverage scraping?

---

## Extraction

Don't be afraid of generating code
<!-- we need a genericized example of protobuf code generation. Possible vitess?  -->

---

## Extraction

Create Struct types for complex data structures
- Pointers make things lighter
- memory doesn't matter until it does
- Leverage interfaces for complete picture
<!-- you need code here -->
<!-- being smart about naming, functions, processes can allows for new integraions to proceed with ease -->

---

## Extraction

Fail Fast isn't always your friend
- Always pass errors up
- Leverage back-off and retry
- Track failed data

---

## Transform

Rely on your database
- Optimize for Storage 
<!-- Transforming for the Database is not the same as transforming for product consumption -->


---

## Transform

Find a good sql library

---

## Load

Can you use scraping to help define data?

---

## Load

Don't be afraid of generating code

---

## Load

Monitor your data change. It makes debugging easier.