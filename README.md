# LA-CRIME Database Management System

This project is part of the M149: Database Management Systems course at the University of Athens. It involves designing, implementing, and demonstrating a NoSQL database solution to manage crime data published by the Los Angeles Police Department (LAPD).

## Overview

The project focuses on:

- Designing and implementing a NoSQL database using MongoDB to store LAPD crime reports.
- Enabling efficient queries and aggregations for analyzing crime data.
- Developing a REST API for accessing and updating the database.
  

## Features

### 1. Database Design

- Flexible schema design to store LAPD crime data efficiently.
- Integration of upvote functionality by police officers.

### 2. Query Functionality

The REST API supports the following :

- **Crime Statistics**:

- **Crime Trends**:

- **Upvote Analysis**:
  
- **Data Integrity**:

- **Crime Reports Updates**:
  
- **Upvotes Updates**:

## Technologies Used

- **Database:** MongoDB Community Server.
- **Framework:** Django
- **Programming Language:** Python.

## Dataset

The dataset is sourced from the LAPD's publicly available records: [LAPD Crime Data (2020-Present)](https://data.lacity.org/Public-Safety/Crime-Data-from-2020-to-Present/2nrs-mtv8).

## Usage Instructions

### 1. Clone the Repository

```bash
git  clone  https://github.com/TomusD/NoSQL-LA-CRIME
cd  la-crime
```

### 2. Set Up the Environment

Install MongoDB and set up the database.
Create a virtual environment and install dependencies:

```bash
python  -m  venv  venv
source  venv/bin/activate
pip  install  -r  requirements.txt
```

To connect to your database, create an env file with the properties of the database, like this:

```
'ENGINE': 'djongo',
'NAME': 'LA-CRIME',
HOST=<host> # e.g., localhost
PORT=<port> # e.g., 27017
```

### 3. Load the Dataset

Load the LAPD dataset into the PostgreSQL database using the provided scripts.

```bash
py  manage.py  import_data
```

### 4. Run the Application

```bash
python  manage.py  runserver
```

### 5. Access the Application

```bash
Visit  http://<host>:<port>  in  your  browser.
(Note: The default port is 8000 unless specified otherwise.)
```

## License

This project is licensed under the MIT License.