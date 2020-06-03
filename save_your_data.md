---
theme: gaia
_class: lead
paginate: true
backgroundColor: #fff
backgroundImage: url('https://marp.app/assets/hero-background.jpg')
marp: true
footer: ![width:200px](images/WeaveLogoDarkGray.png)
---

# Data and the Software Stack: simple data architecture steps that prep for machine learning 
Miriah Peterson

---

![bg right fit rotate:90](images/IMG_3232.jpg)

# Bio

- Engineer at Weave in Lehi, Utah
- Board Member with Forge Foundation
- Proud Dog Mom
- [Twitter captiainnobody1](https://www.twitter.com/captainnobody1)
- [GitHub soypete](https://www.github.com/soypete)
- [LinkedIn](https://www.linkedin.com/in/miriah-peterson-35649b5b)

---

# Types of Data
Data: Data (treated as singular, plural, or as a mass noun) is any sequence of one or more symbols given meaning by specific act(s) of interpretation.

---

# Types of Data
Data: Data (treated as singular, plural, or as a mass noun) is any sequence of one or more symbols given meaning by specific act(s) of interpretation.

Types:
- Machine-generated data
- User generated data

---
## machine-generated data

What are types of machine generated data does your software produce?

---
## Machine-generated data

What are types of machine generated data does your software produce?
* Event Data
* Error Data
* Network Usage Data
* App Actions (click-stream) data
* Change log data


---
## User generated
What are types of user generated data does your software produce?
* Account information
* Personal information
* Transaction (payment/currency)
* Product Data
---
# Types of Data

Which is more important?

---
# Ways to use your data - Direct in Product
![width:1100px](https://images.squarespace-cdn.com/content/v1/51de2380e4b091cde978ef91/1588886509103-ZLTSJ8MUO79FYGC83320/ke17ZwdGBToddI8pDm48kN1dY1Dq4-GP8qanlVosGJJ7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z5QPOohDIaIeljMHgDF5CVlOqpeNLcJ80NK65_fV7S1UVjDcrmeH5fWy8wfaTorp5Rk9NxNSsFtcKUvJT2EfhrlZtJ3qR9G2BYeA0wOAaeYNg/Screen+Shot+2020-05-07+at+3.18.53+PM.png?format=1500w)

---

# Ways to use your data - Dashboard/Reports
<!-- * Reports
* Dashboards
* product use case
* machine learning  -->
![width:1100px](https://grafana.com/static/img/docs/animated_gifs/drag_drop.gif)

---
# Ways to use your data - Dashboard/Reports

In what ways are you using machine-generated or user generated data?

--- 

# Machine Learning

---
# Machine Learning
Monitoring usage to trigger an action.
<!-- kubernetes auto scale 
Cloudera uses ml to auto scale their clusters-->

---
# Machine Learning
Forcasting outages/high network usage
<!-- (att example) -->

![bg right fit width:700px](https://www.amnh.org/var/ezflow_site/storage/images/media/tornado-leading-image/1666587-1-eng-US/tornado-leading-image.jpg)

---
# Machine Learning

* Product enhancement (weave sentiment analysis)

---

# Data Architecture as part of planning process
<!-- * What data is developed in each step?
* What are availability needs?
  - Does the product need to consume this data? 
  - Do other services need to consume this data? 
* Is it worth the storage cost? -->

---

# Data Architecture as part of planning process

Questions to ask when planning or designing 
---

# Data Architecture as part of planning process

Questions to ask when planning
- Am I creating, consuming, or communicating the data?
---

# Data Architecture as part of planning process

Questions to ask when planning
- Am I creating, consuming, or communicating the data?
- Where is the final resting place of my data?
---

# Data Architecture as part of planning process

Questions to ask when planning
- Am I creating, consuming, or communicating the data?
- Where is the final resting place of my data?
- How much does is cost to store the data?

---

# Data Architecture as part of planning process

Questions to ask when planning
- Am I creating, consuming, or communicating the data?
- Where is the final resting place of my data?
- How much does is cost to store the data?
- What are availability needs?

---
# Data Architecture as part of planning process

Questions to ask when planning
- What are availability needs?
  - Does the product need to consume this data? 
---

# Data Architecture as part of planning process

Questions to ask when planning
- What are availability needs?
  - Does the product need to consume this data? 
  - Do other services need to consume this data? 
---

# Data Architecture as part of planning process

Questions to ask when planning
- What are availability needs?
  - Does the product need to consume this data? 
  - Do other services need to consume this data? 
  - How often is the data consumed?
---

# Data Architecture as part of planning process

## Where do we start?

---

# Where do we start?

* Pain points

---
# Where do we start?

* Pain points
* Central Features

---

# Where do we start?

* Pain points
* Central Features
* Product needs

---
Questions?

---
# Resources

*[wikipedia data-computing](https://en.wikipedia.org/wiki/Data_(computing))
*[Software Engineering Daily May 28, 2020](https://softwareengineeringdaily.com/2020/05/28/distributed-systems-research-with-peter-alvaro/)
*[machine-generated vs human-generated](http://dbmsmusings.blogspot.com/2010/12/machine-vs-human-generated-data.html)
*[cloudera autoscaling](https://docs.cloudera.com/machine-learning/cloud/autoscaling-overview/topics/ml-autoscaling-overview.html)
---