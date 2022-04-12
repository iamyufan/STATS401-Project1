# STATS401-Project1

Personal repo for STATS 401 Project 1 at DKU

## **Data Scraping**

### Step 1. Get DUID

Get the Duke Unique Identifiers (DUID) of all the faculty members at Duke from [Duke internal directory](https://directory.duke.edu/directory/search).

```bash
getList.py
db.py
work.py
```

**output**

```python
../data/duid.csv		# table containing faculty's name and duid
../data/scholars_url.csv	# table containing faculty's URL on Scholars@Duke
```

### Step 2. Get Faculty Info from Scholars@Duke

Get the information of faculty members from [Scholars@Duke](https://scholars.duke.edu/) via [Scholars widgets API](https://scholars.duke.edu/widgets/docs/#/). The informations are stored as JSON files.

```bash
DataCrawlClean.ipynb
```

**output**

```python
../data/sholors_duke/[duid]/json
```

# Data Cleaning

### Step 3. Clean the Faculty Data

Clean up the JSON files from Step 2.

```bash
DataCrawlClean.ipynb
```

**output**

```
../data/cleaned_info.csv
../data/cleaned.json
```

### Step 4. Get DKU Course Info

Get DKU courses and major information from DKU [UGstudies Majors](https://ugstudies.dukekunshan.edu.cn/academics/majors/).

```bash
getCourse.py
```

**output**

```
../data/course_description/[major].csv

```
