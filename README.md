# wikitop25
Application that computes the top 25 pages for each sub-domain in Wikipedia.
For instructions on who to use it, cf. section 2.1.

### 1) Subject

Build a simple application that computes the top 25 pages on Wikipedia for each of the Wikipedia sub-domains.

##### 1.1) Requirements

1) Accept input parameters for the date and hour of data to analyze (default to the current date/hour if not passed).
2) Download the page view counts from wikipedia for the given date/hour [...] from https://dumps.wikimedia.org/other/pageviews/.
3) Eliminate any pages found in this blacklist: https://s3.amazonaws.com/dd-interview-data/data_engineer/wikipedia/blacklist_domains_and_pages
4) Compute the top 25 articles for the given day and hour by total pageviews for each unique domain in the remaining data.
5) Save the results to a file, either locally or on S3, sorted by domain and number of pageviews for easy perusal.
6) Only run these steps if necessary; that is, not rerun if the work has already been done for the given day and hour.
7) Be capable of being run for a range of dates and hours.

##### 1.2) Questions
1) What additional things would you want to operate this application in a production setting?
2) What might change about your solution if this application needed to run automatically for each hour of the day?
3) How would you test this application?
4) How you’d improve on this application design?
5) You can write your own workflow or use existing libraries (Luigi, Drake, etc).

## 2) Application

##### 2.1) Instructions to use it

##### 2.2) Design

##### 2.3) Answers
1)
2)
3)
4)
5)
