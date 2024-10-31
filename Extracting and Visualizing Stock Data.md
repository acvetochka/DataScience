# Extracting and Visualizing Stock Data

## Description
Extracting essential data from a dataset and displaying it is a necessary part of data science; therefore individuals can make correct decisions based on the data. In this assignment, you will extract some stock data, you will then display this data in a graph.

## Table of Contents
- [Define a Function that Makes a Graph](https://github.com/acvetochka/DataScience/blob/main/Extracting%20and%20Visualizing%20Stock%20Data.md#define-graphing-function)
- [Question 1: Use yfinance to Extract Stock Data](https://github.com/acvetochka/DataScience/blob/main/Extracting%20and%20Visualizing%20Stock%20Data.md#question-1-use-yfinance-to-extract-stock-data)
- [Question 2: Use Webscraping to Extract Tesla Revenue Data](https://github.com/acvetochka/DataScience/blob/main/Extracting%20and%20Visualizing%20Stock%20Data.md#question-2-use-webscraping-to-extract-tesla-revenue-data)
- [Question 3: Use yfinance to Extract Stock Data](https://github.com/acvetochka/DataScience/blob/main/Extracting%20and%20Visualizing%20Stock%20Data.md#question-3-use-yfinance-to-extract-stock-data)
- [Question 4: Use Webscraping to Extract GME Revenue Data](https://github.com/acvetochka/DataScience/blob/main/Extracting%20and%20Visualizing%20Stock%20Data.md#question-4-use-webscraping-to-extract-gme-revenue-data)
- [Question 5: Plot Tesla Stock Graph](https://github.com/acvetochka/DataScience/blob/main/Extracting%20and%20Visualizing%20Stock%20Data.md#question-5-plot-tesla-stock-graph)
- [Question 6: Plot GameStop Stock Graph](https://github.com/acvetochka/DataScience/blob/main/Extracting%20and%20Visualizing%20Stock%20Data.md#question-6-plot-gamestop-stock-graph)

Estimated Time Needed: 30 min

> Note:- If you are working Locally using anaconda, please uncomment the following code and execute it. Use the version as per your python version.

```bash
!pip install yfinance
!pip install bs4
!pip install nbformat
```

Import dependencies
```python
import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots
```

In Python, you can ignore warnings using the warnings module. You can use the filterwarnings function to filter or ignore specific warning messages or categories.

```python
import warnings
# Ignore all warnings
warnings.filterwarnings("ignore", category=FutureWarning)
```

## Define Graphing Function
In this section, we define the function make_graph. You don't have to know how the function works, you should only care about the inputs. It takes a dataframe with stock data (dataframe must contain Date and Close columns), a dataframe with revenue data (dataframe must contain Date and Revenue columns), and the name of the stock.

```python
def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()
```
Use the make_graph function that we’ve already defined. You’ll need to invoke it in questions 5 and 6 to display the graphs and create the dashboard.

> Note: You don’t need to redefine the function for plotting graphs anywhere else in this notebook; just use the existing function.

## Question 1: Use yfinance to Extract Stock Data
Using the Ticker function enter the ticker symbol of the stock we want to extract data on to create a ticker object. The stock is Tesla and its ticker symbol is TSLA.

```python
tesla = yf.Ticker("TSLA")
```

Using the ticker object and the function history extract stock information and save it in a dataframe named tesla_data. Set the period parameter to "max" so we get information for the maximum amount of time.

```python
tesla_data = tesla.history(period="max")
```

Reset the index using the reset_index(inplace=True) function on the tesla_data DataFrame and display the first five rows of the tesla_data dataframe using the head function. Take a screenshot of the results and code from the beginning of Question 1 to the results below.

```
tesla_data.reset_index(inplace=True)
tesla_data.head()
```

Output: 

| Date                      	| Open	    | High	    | Low      |	Close   	| Volume    |	Dividends |	Stock Splits |
| ----------------------------| --------- | --------- | -------- | --------- | ---------- | --------- | ------------ |
| 0	2010-06-29 00:00:00-04:00	| 1.266667	| 1.666667	| 1.169333 |	1.592667 |	281494500 |	0.0       |	0.0          |
| 1	2010-06-30 00:00:00-04:00	| 1.719333	| 2.028000  |	1.553333 |	1.588667 |	257806500 |	0.0	      | 0.0          |
| 2	2010-07-01 00:00:00-04:00	| 1.666667	| 1.728000	| 1.351333 |	1.464000 |	123282000 |	0.0	      | 0.0          |
| 3	2010-07-02 00:00:00-04:00 |	1.533333  |	1.540000	| 1.247333 |	1.280000 |	77097000  |	0.0	      | 0.0          |
| 4	2010-07-06 00:00:00-04:00 |	1.333333  |	1.333333	| 1.055333 |	1.074000 |	103003500 |	0.0	      | 0.0          |

## Question 2: Use Webscraping to Extract Tesla Revenue Data
Use the requests library to download the webpage https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm Save the text of the response as a variable named html_data.

```python
url = " https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"

html_data  = requests.get(url).text
```

Parse the html data using beautiful_soup using parser i.e html5lib or html.parser.

```python
soup = BeautifulSoup(html_data, 'html.parser')
```

Using BeautifulSoup or the read_html function extract the table with Tesla Revenue and store it into a dataframe named tesla_revenue. The dataframe should have columns Date and Revenue.

<details>
  <summary>Step-by-step instructions</summary>

  Here are the step-by-step instructions:
  
  1. Create an Empty DataFrame
  2. Find the Relevant Table
  3. Check for the Tesla Quarterly Revenue Table
  4. Iterate Through Rows in the Table Body
  5. Extract Data from Columns
  6. Append Data to the DataFrame

</details>

<details>
  <summary>Click here if you need help locating the table</summary>

  Below is the code to isolate the table, you will now need to loop through the rows and columns like in the previous lab
      
  soup.find_all("tbody")[1]
      
  If you want to use the read_html function the table is located at index 1
  
  We are focusing on quarterly revenue in the lab.

</details>

```python
table = soup.find_all("tbody")[1]

tesla_revenue = pd.DataFrame(columns=["Date", "Revenue"])

for row in table.find_all("tr"):
    col = row.find_all("td")
    date = col[0].text
    revenue = col[1].text
    
    tesla_revenue = pd.concat([tesla_revenue, pd.DataFrame({"Date":[date], "Revenue":[revenue]})], ignore_index=True)
```

Execute the following line to remove the comma and dollar sign from the Revenue column.

```python
tesla_revenue["Revenue"] = tesla_revenue["Revenue"].str.replace(r"[,|$]", "", regex=True)
```

Execute the following lines to remove an null or empty strings in the Revenue column.

```python
tesla_revenue.dropna(inplace=True)

tesla_data['Date'] = pd.to_datetime(tesla_data['Date'], errors='coerce')
tesla_revenue['Date'] = pd.to_datetime(tesla_revenue['Date'], errors='coerce')

tesla_data.dropna(subset=['Date'], inplace=True)
tesla_revenue.dropna(subset=['Date'], inplace=True)

tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]
```

Display the last 5 row of the tesla_revenue dataframe using the tail function. Take a screenshot of the results.

```python
tesla_revenue.tail()
```

Output:

|    | Date        | Revenue |
|----| ----------- | ------- |
| 48 |	2010-09-30 | 31      |
| 49 |	2010-06-30 | 28      |
| 50 |	2010-03-31 | 21      |
| 52 |	2009-09-30 | 46      |
| 53 |	2009-06-30 | 27      |

## Question 3: Use yfinance to Extract Stock Data
Using the Ticker function enter the ticker symbol of the stock we want to extract data on to create a ticker object. The stock is GameStop and its ticker symbol is GME.

```python
gme = yf.Ticker("GME")
```

Using the ticker object and the function history extract stock information and save it in a dataframe named gme_data. Set the period parameter to "max" so we get information for the maximum amount of time.

```python
gme_data = gme.history(period="max")
```

Reset the index using the reset_index(inplace=True) function on the gme_data DataFrame and display the first five rows of the gme_data dataframe using the head function. Take a screenshot of the results and code from the beginning of Question 3 to the results below.

```python
gme_data.reset_index(inplace=True)
gme_data.head()
```

Output:

Date	Open	High	Low	Close	Volume	Dividends	Stock Splits

|   |   Date                   | Open	     | High	     | Low      |	Close   	| Volume     |	Dividends|	Stock Splits|
|---|--------------------------| --------- | --------- | -------- | --------- | ---------- | --------- | ------------ |
| 0 |	2002-02-13 00:00:00-05:00|	1.620128 |	1.693350 |	1.603296|	1.691667  |	76216000	 | 0.0       |	0.0         |
| 1 |	2002-02-14 00:00:00-05:00|	1.712707 |	1.716074 |	1.670626|	1.683251  |	11021600	 | 0.0       |	0.0         |
| 2 |	2002-02-15 00:00:00-05:00|	1.683250 |	1.687458 |	1.658002|	1.674834	| 8389600	   | 0.0       |	0.0         |
| 3 |	2002-02-19 00:00:00-05:00|	1.666417 |	1.666417 |	1.578047|	1.607504	| 7410400  	 | 0.0       |	0.0         |
| 4 |	2002-02-20 00:00:00-05:00|	1.615920 |	1.662210 |	1.603296|	1.662210	| 6892800	   | 0.0       |	0.0         |

## Question 4: Use Webscraping to Extract GME Revenue Data
Use the requests library to download the webpage https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html. Save the text of the response as a variable named html_data_2.
```python
url2 = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"

html_data_2 = requests.get(url2).text
```

Parse the html data using beautiful_soup using parser i.e html5lib or html.parser.

```python
gme_soup = BeautifulSoup(html_data_2, 'html.parser')
```

Using BeautifulSoup or the read_html function extract the table with GameStop Revenue and store it into a dataframe named gme_revenue. The dataframe should have columns Date and Revenue. Make sure the comma and dollar sign is removed from the Revenue column.

> Note: Use the method similar to what you did in question 2.

<details>
  <summary>Click here if you need help locating the table</summary>

  Below is the code to isolate the table, you will now need to loop through the rows and columns like in the previous lab
      
  soup.find_all("tbody")[1]
      
  If you want to use the read_html function the table is located at index 1
</details>

```python
gme_table = gme_soup.find_all("tbody")[1]

gme_revenue = pd.DataFrame(columns=["Date", "Revenue"])

for row in gme_table.find_all("tr"):
    col = row.find_all("td")
    date = col[0].text
    revenue = col[1].text

    gme_revenue = pd.concat([gme_revenue, pd.DataFrame({"Date":[date], "Revenue":[revenue]})], ignore_index=True)


gme_revenue["Revenue"] = gme_revenue["Revenue"].str.replace(',|\$', "", regex=True)
gme_revenue.dropna(inplace=True)
gme_revenue = gme_revenue[gme_revenue['Revenue'] != ""]
```

Display the last five rows of the gme_revenue dataframe using the tail function. Take a screenshot of the results.

```python
gme_revenue.tail()
```

|   | Date       | Revenue |
|---| ---------- | ------- |
| 57|	2006-01-31 |	1667   |
| 58|	2005-10-31 |	534    |
| 59|	2005-07-31 |	416    |
| 60|	2005-04-30 |	475    |
| 61|	2005-01-31 |	709    |

## Question 5: Plot Tesla Stock Graph
Use the make_graph function to graph the Tesla Stock Data, also provide a title for the graph. Note the graph will only show data upto June 2021.

Hint

You just need to invoke the make_graph function with the required parameter to print the graphs.The structure to call the `make_graph` function is `make_graph(tesla_data, tesla_revenue, 'Tesla')`.
```python
make_graph(tesla_data, tesla_revenue, 'Tesla')
```

![graph Tesla](https://coursera-assessments.s3.amazonaws.com/assessments/1730368585377/7ec3c1ed-842e-4f34-a8d5-6cd4b80d5549/q_5.png)

## Question 6: Plot GameStop Stock Graph
Use the make_graph function to graph the GameStop Stock Data, also provide a title for the graph. The structure to call the make_graph function is make_graph(gme_data, gme_revenue, 'GameStop'). Note the graph will only show data upto June 2021.

Hint

You just need to invoke the make_graph function with the required parameter to print the graphs.The structure to call the `make_graph` function is `make_graph(gme_data, gme_revenue, 'GameStop')`
```python
gme_data['Date'] = pd.to_datetime(gme_data['Date']) 
gme_revenue['Date'] = pd.to_datetime(gme_revenue['Date']) 

make_graph(gme_data, gme_revenue, 'GameStop')
```

![Graph GME](https://coursera-assessments.s3.amazonaws.com/assessments/1730368614595/3701c75a-0c58-4812-b8b3-3c75799bd7df/q_6.png)
