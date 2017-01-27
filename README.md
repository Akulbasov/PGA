# **Python Google Analytics Library <br>(Core Reporting API v3 support)**

This is a library for making batch request to Google Analytics Core Reporting v3 API and extracting data from Google Analytics property into Python 3 data structures.

The package uses 

* OAuth 2.0 (protocol) client or server access to Google Analytics API (oauth2client==3.0.0) - for connection to Google Analytics

* Core Reporting v3 API Google Analytics - for extracting data

* Metadata API Google Analytics - integrated dimensions or metrics reference lookup

* Management API Google Analytics - to get View, Property and Account tree. 

Dependency:

* Pandas > 0.13.0 - for transformation data into pandas DataFrame object 

* Numpy > 1.0.0 - for slice numpy array chunk

* google-api-python-client > 1.5.0 - self explanatory 

Best practices usage:

* Interactive shell [Jupyter ](http://jupyter.org/)for analyzing data

## **Installation**

* Via [pip](https://pip.pypa.io/en/stable/installing/#installing-with-get-pip-py): use the following command: # sudo pip install pga

Latest version of Pandas, Numpy and oauth2client will be automatically installed as a dependency.

## **Authentication**

First of all you will need to get [google client_secret json file](https://developers.google.com/identity/sign-in/web/devconsole-project) from [Go](https://console.developers.google.com/project/_/apiui/apis/library)[ogle API Console](https://console.developers.google.com/project/_/apiui/apis/library) 

You may choose the following types of Client ID :

* for Service account client

* for Web application

### PGA.__init__

![image alt text](image_0.png)

**PGA.__init__(key_file_location=None,type_of_connection=None,facet_chunk=10,count_day_slice=1)**

Constructor and set parameters for instance basic functionality.

<table>
  <tr>
    <td><b>Parameters:</b></td>
    <td><b>key_file_location : </b>string</br>
Set path for secret json file</br>
<b>type_of_connection : </b>string</br>
Available methods are Client’, ‘Server’ If use service account, then choose ‘Server’, if use web applicatio use ‘Client.’</br>
<b>facet_chunk :</b> int, optional</br>
Set a number of chunk,which execute all parallels request. More detail about this technology. Important things - Google Universal Analytics make execute only 10 parallel request in one second, if you want more - contact with a Google form to increase this limit.</br>
<b>count_day_slice : </b> int, optional</br>
Set a number of days,which need to slice [start-date, end-date] in your request.</br>
For example:</br>
(input)</br>
   {‘count_day_slice’:2, 'start_date' : '2016-12-01','end_date' : '2016-12-05'}</br>
(output)</br>
  [{ 'start_date' : '2016-12-01','end_date' : '2016-12-02'},</br>
   { 'start_date' : '2016-12-03','end_date' : '2016-12-04'},</br>
   { 'start_date' : '2016-12-05','end_date' : '2016-12-05'}]</br>
</td>
  </tr>
  <tr>
  <td><b>Returns:</b></td>
  <td><b>self :</b> self</br>
return self with current behavior.</td>
  </tr>
</table>


After apply constructor will be create the instance, and redirect the client to a browser for authentication with Google.

## **Request add**

Simply add request in an already instantiated object pga

![image alt text](image_1.png)

### Request.add_settings_request

**Request****.add_settings_request(****settings_products)

<table>
  <tr>
  <td><b>Parameters:</b></td>
    <td><b>**settings_products :</b> kwargs</br>
Specify json request formats Core V3, list of query parameters - https://developers.google.com/analytics/devguides/reporting/core/v3/reference?hl=ru#q_summary</td>
  </tr>
  <tr>
    <td><b>Returns:</b></td>
    <td><b>self :</b> self
return self with current behavior.</td>
  </tr>
</table>


You can update any already used query parameters later with the following method, and make new request. ![image alt text](image_2.png)

## **Execute DataFram****e**

Execute all settings for get DataFrame

![image alt text](image_3.png)

### PGA.get_dataframe

**PGA.get_dataframe(groupby=True)**

<table>
  <tr>
  <td><b>Parameters:</b></td>
  <td><b>groupby :</b> boolean<br>
Available methods are ‘True’, ‘False’<br>
if choose True then DataFrame groupby all date by all dimensions, dates, and start-index. 
Also all columns apply appropriate type based on Google Analytics MetaData API.<br>
if choose False then DataFrame doesn’t groupby data. 
It made for use some other library which can fast aggregate and groupby data, because in some cases data is too large and this process is very low. You may pay attention in to this project - http://dask.pydata.org/en/latest/ </td>
  </tr>
  <tr>
  <td><b>Returns:</b></td>
  <td><b>data :</b> pandas.DataFrame object</td>
  </tr>
</table>


## **Get settings pga**

**All settings**

Print all current settings pga:

### PGA.get_all_settings

**PGA.get_all_settings()**

<table>
  <tr>
  <td><b>Returns:</b></td>
  <td><b>all settings :</b> pandas.DataFrame object</td>
  </tr>
</table>


**All products**

Print all current product settings pga

### PGA.get_all_products

**PGA.get_all_products()**

<table>
  <tr>
  <td><b>Returns:</b></td>
  <td><b>all settings : pandas.DataFrame object</b></td>
  </tr>
</table>


## **Additional extra apps**

**ExtraAppsMetaCdm**

Lookup through metadata of Google Analytics dimensions and metrics:

![image alt text](image_4.png)

### ExtraAppsMetaCdm.get_list_cdcm

**ExtraAppsMetaCdm.get_list_cdcm(clarify=None)**

<table>
  <tr>
  <td><b>Parameters:</b></td>
  <td><b>clarify :</b> string
Specifying the attribute on which the selection will be dimensions and metris</td>
  </tr>
  <tr>
  <td><b>Returns:</b></td>
  <td><b>Table of information :</b> pandas.DataFrame object</td>
  </tr>
</table>


**ExtraAppsManagementAPI**

Get the list of Google Universal Analytics (Account ID, Property id, View id) objects, you have an access to.

![image alt text](image_5.png)

### PGA.get_all_profile

**PGA.get_all_profile()**

<table>
  <tr>
  <td><b>Returns:</b></td>
    <td>Table of information with dimensions or metrics: pandas.DataFrame object</td>
  </tr>
</table>

