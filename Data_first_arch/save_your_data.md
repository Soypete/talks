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

![bg right fit](images/IMG_3232.jpg)

# Bio

- Engineer at Weave in Lehi, Utah
- Board Member with Forge Foundation
- Proud Dog Mom
- [Twitter @captainnobody1](https://www.twitter.com/captainnobody1)
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
<!-- 
structured: data with a schema
unstructed data: raw loose data
-->

---
## Machine-generated data

What are types of machine generated data does your software produce?

---
## Machine-generated data

What are types of machine generated data does your software produce?
* Event Data
* Error Data
* Network Usage Data
* App Actions (click-stream) data
* Database change capture (anamoly detection)

---
## User generated
What are types of user generated data does your software produce?
* Account information
* Personal information
* Transaction (payment/currency)
* Product Data
*  *Metadata  <!--- number of times logged into account --->

---
# Types of Data

Which is more important?

---
# Ways to use your data - Direct in Product
![fit width:1100px](https://images.squarespace-cdn.com/content/v1/51de2380e4b091cde978ef91/1588886509103-ZLTSJ8MUO79FYGC83320/ke17ZwdGBToddI8pDm48kN1dY1Dq4-GP8qanlVosGJJ7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z5QPOohDIaIeljMHgDF5CVlOqpeNLcJ80NK65_fV7S1UVjDcrmeH5fWy8wfaTorp5Rk9NxNSsFtcKUvJT2EfhrlZtJ3qR9G2BYeA0wOAaeYNg/Screen+Shot+2020-05-07+at+3.18.53+PM.png?format=1500w)

---

# Ways to use your data - Dashboard/Reports
<!---* The Crutch --->
![width:1100px](https://grafana.com/static/img/docs/animated_gifs/drag_drop.gif)

---
# Ways to use your data

In what ways are you using machine-generated or user generated data?

--- 
 
# Ways to use your data

Machine Learning from stored data.

--- 

# Machine Learning
<!-- the Easier the data is to consume by a data scientist the quicker you see ROI --->
![bg right fit](https://media.giphy.com/media/9PrqNHPAdWyJVOXntF/giphy.gif)

---
# Machine Learning
Monitoring usage to trigger an action (predictive autoscaling).
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
![bg right fit](https://www.getweave.com/wp-content/uploads/2019/12/messaging-hero-image.png)

---

# Data Architecture as part of planning process
<!-- * What data is developed in each step?
* What are availability needs?
  - Does the product need to consume this data? 
  - Do other services need to consume this data? 
* Is it worth the storage cost? -->

---

# Data Architecture as part of planning process

Questions to ask when planning

---

# Data Architecture as part of planning process

Questions to ask when planning
- Who is creating, consuming, or communicating the data?
---

# Data Architecture as part of planning process
<!-- counting errors -->
Questions to ask when planning
- Who is creating, consuming, or communicating the data?
  - Where is the final resting consumption of my data?

---

# Data Architecture as part of planning process

Questions to ask when planning
- Who is creating, consuming, or communicating the data?
  - Where is the final resting place of my data?
- How much does it cost to store the data?

---

# Data Architecture as part of planning process

Questions to ask when planning
- Who is creating, consuming, or communicating the data?
  - Where is the final resting place of my data?
- How much does it cost to store the data?
- What are availability needs?
<!-- OLTP Online transactional processing/ OLAP Online Analysis processing--->

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
<!--When do you run into these problems --->
Questions to ask when planning
- What are availability needs?
  - Does the product need to consume this data? 
  - Do other services need to consume this data? 
  - How often is the data consumed?
---

# Data Architecture as part pf planning process
 ![bg fit](https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Google-BigQuery-Logo.svg/1200px-Google-BigQuery-Logo.svg.png)
 ![bg fit](images/1_aNSe9ZERfX5-Dl0wAVBOOg.png)
 ![bg fit](images/vitess-stacked-color.png)
 ![bg fit](https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Vertica_pos_blk_rgb.svg/440px-Vertica_pos_blk_rgb.svg.png)
![bg fit](https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Hadoop_logo.svg/1280px-Hadoop_logo.svg.png)
![bg fit](https://svn.apache.org/repos/asf/kafka/site/logos/originals/png/ICON%20-%20Black%20on%20Transparent.png)

 ---

 # Data Architecture as part of planning process
 Methods for adding Machine Learning Models
 - API calls
 - Static Model <!--- static file/database -->
 - Part of Event Stream

 ---

# Data Architecture as part of planning process

## Where do we start?

---

# Where do we start?

* **Pain points**

---
# Where do we start?

* **Pain points**
* Central Features

---

# Where do we start?

* **Pain points**
* Central Features
* Product needs

---
# Questions?

---
# Resources

*[wikipedia data-computing](https://en.wikipedia.org/wiki/Data_(computing))
*[Software Engineering Daily May 28, 2020](https://softwareengineeringdaily.com/2020/05/28/distributed-systems-research-with-peter-alvaro/)
*[machine-generated vs human-generated](http://dbmsmusings.blogspot.com/2010/12/machine-vs-human-generated-data.html)
*[cloudera autoscaling](https://docs.cloudera.com/machine-learning/cloud/autoscaling-overview/topics/ml-autoscaling-overview.html)
*[Data Driven Applications](https://www.amazon.com/gp/product/1449373321/ref=ppx_yo_dt_b_asin_title_o05_s02?ie=UTF8&psc=1)
*[kubernetes autoscaling](https://kubernetes.io/blog/2016/07/autoscaling-in-kubernetes/)
*[autoscale wikipedia](https://en.wikipedia.org/wiki/Autoscaling#Predictive_autoscaling)
*[predictive autoscaling aws](https://aws.amazon.com/blogs/aws/new-predictive-scaling-for-ec2-powered-by-machine-learning/)
---