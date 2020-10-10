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
<!-- welcome to utah. This is where I work and alot of what I am going to talk about has to do with the tech land scape of the start up heavy and young tech game. -->

![auto](https://2utfff4d3dkt3biit53nsvep-wpengine.netdna-ssl.com/wp-content/uploads/2018/06/utah-1.png)
---


## Intro
<!-- People reach out to me lot with wondering how I do my job because I work at Weave. -->
>I am wondering if you actually get to use Go in your data pipelines or is it still mostly SQL/Python for you? I am curious how do you go about ensuring data quality in your data pipelines? Does Weave have a formal framework for monitoring/alerting on quality?

---

## Intro

<!-- I work at weave. In this area, we are one of the bigger players and our backend is all Go. We are very public being heavily involved in meetups and having a recent unicorn valuation. That being said we are young. Alot of what I am sharing today are due to the nature of the tech land scape in utah, at weave, and my youth in the industry -->
![auto](https://media-exp1.licdn.com/dms/image/C4E0BAQEPIWvZ0fLRoQ/company-logo_200_200/0?e=1609977600&v=beta&t=s10QPTtKJeB4JJ8gWacFKttc9LAgkBCyLgdsLEmD9i0)
- https://www.crunchbase.com/organization/weave
---

## Intro
<!-- I have spent two years at weave building infra for data. Here is what I have learned.  -->
Tips and Tricks I have learned doing Data Engineering in Go:

- Platform
- Extract Data
- Load Data
- Transform Data

---

## Platform

Platform: Infrastructure for storing, transfering, analyzing, and transforming data.

![auto](https://media.giphy.com/media/LscmpwWq2W6CA/giphy.gif)

---

## Platform

If possible don't build your own home grown solution

<!-- ![width:200px height:200px](../images/beam-logo-full-color-name-bottom-500.png)
![width:200px height:200px](../images/pachyderm.svg) -->
![auto](https://media.giphy.com/media/l2Jeiw5zzyd7HNPvG/giphy.gif)

 <!-- - pachydern
 - beam  
 remember beam is dataflow and "has" a go sdk-->

 ---

## Platform
<!-- when you inevitably build your own  -->
<!-- data state over the wire  is important cause that is one of the places where data cn be most vulnerablee-->
<!-- time for iteration. your first Idea in never the best. you will proabably itereate/reebuild your platform serveral timee to meat the constraints -->
Do not over engineer it

- Anticipate constraints and security
- Anticipate compliance
- Budget time to iterate on your design

---

## Platform

Plan for Monolith or Microservice upfront. *No Hybrids*

- You don't want to maintain/create unnecessary services
- Use Caching Layers sparingly
- Consider Number of transfers that the data makes
- Don't cheat yourself with Go routines and channels
<!--  * If you are doing microservice architecture then each consumption point is a unique service 
* We used microservices are weave as that is the general architecture style. * routines and channels are created for concurrent manipulation on large scale transfer. THey are also suseptible to memory leaks.
* nsq, grpc, apis, or databased are often better-->

---

## Platform

Use a messaging/streaming services to manage data flow

- APIs slow things down
- Allows for multiple worker consumption
- Manage batch processing jobs
- Services like Kafka allow for replaying jobs

---

## Platform

Use a schema repository 

- Standardize data types across services (microservice)
- Leverage Generation for all the repos
- Protects againsts stupidity
- (protobuf + go =  :heart:)
<!-- we need a genericized example of protobuf code generation. Possible vitess?  -->

---

## Extraction
<!-- 
* python leverages non-typed data 
* in GO using interfaces for generic types creates redundant type defining processes and the need for lots of code generation and case checking
* You can glean type information from data base procesures and meta-data api scrtaping. this can allow foor single type definition.  
-->
Pick the Data type at Extration and stick to it

- Avoid non-typed data 
- Optimize type for storage
- Leverage Scraping as Needed 

---


## Extraction

Create Struct types for complex data structures

- Pointers make things lighter
- Memory doesn't matter until it does
- Leverage interfaces for complete picture
<!-- you need code here -->
<!-- being smart about naming, functions, processes can allows for new integraions to proceed with ease -->

---

## Extraction

Fail Fast isn't always your friend

- Always pass errors up to stop workers/routines/sub-processes
- Leverage back-off and retry
- Track failed data

---

## Load

Find a good sql library

- [SQLX](https://github.com/jmoiron/sqlx)
- [SQLC](https://github.com/kyleconroy/sqlc)
- Logic in SQL can help protect data

---

## Load

Find the datastore that fits your needs

- Do you need a database, data lake, data warehouse or something else?
- Do you need more than one?

---

## Load

Manage Your Migrations

- Letting migrations get out of hand is gonna kill your data store

---

## Load

Monitor your data change. It makes debugging easier.

- Distributed data systems increase complications
<!-- from you book, talk about the cap theorem and transactions and stuff  -->

---

## Transform

Do not infuse business data model into your storage

- Optimize for Storage
- Pick a type and stick to it
- Make data discoverable
<!-- Transforming for the Database is not the same as transforming for product consumption -->

---

## Transform 

Don't be afraid of generating code
<!-- we need a genericized example of protobuf code generation. Possible vitess?  -->
```go
type example{{ $Type }} struct {
{{- range .TypeDef.TypeMembers}}
  {{ .Name }} {{ .DataType }} {{ if (ne .JSONName "")}}`json:"{{ .JSONName }}"`{{ end }}
{{- end }}
}
func (ex *example{{ $Type }}) Convert(ctx context.Context) (record.Record, error) {
	var dst = record.{{ $Type }}{
    {{- range .Conversions }}
            {{ .ProtoMember }} : {{ if (eq .ConversionType "null.UUID")}}{{ ToPrivate .Cast }}{{ else }}ex.{{ .Cast }}{{end}},
    {{- end}}
	    }
	if ex.ID == "" {
		return nil, werror.New("id must be supplied").SetCode(werror.CodeInvalidArgument)
	}
        return &dst, nil
}
```
---
## Transform

DON'T Add Feature Logic Here!

![auto](https://media.giphy.com/media/G2MPcSmq0DZcs/giphy.gif)
<!-- it is really easy to pinhole yourself buy narrowing scope to one feature or stakeholder. -->

---

## Transform

Live Data insights
![auto](https://media.giphy.com/media/12NUbkX6p4xOO4/giphy.gif)
<!-- Live updates are possible, here are some tools. They’re sexy but harder to build. Most of the time batch processing provides just as much value. 
- Redis
- Streaming and Beam
- Online ML -->
---


## In Summary

Tips and Tricks Go:

- Build a Smart Data Platform
- Know what Data you Extract
- Load the right Data to the right place
- Transform Data carefully

---

## Conclusions

- There are lots of pitfalls when engineerng for data
- If you have to do it yourself do not!
- I do recommend doing using all the tools out there, but Go is the best!

---

## Contact

- [Twitter @captainnobody1](https://www.twitter.com/captainnobody1)
- [GitHub soypete](https://www.github.com/soypete)
- [LinkedIn](https://www.linkedin.com/in/miriah-peterson-35649b5b)

---
## REFERENCE:
- https://news.crunchbase.com/news/utahs-tech-scene-its-rising-profile-and-the-third-generation-of-startups/
- https://blog.gopheracademy.com/advent-2018/apache-beam/ 
- https://www.pachyderm.com/
- https://dataintensive.net/
- http://streamingsystems.net/