# wikitop25
Application that computes the top 25 pages for each sub-domain in Wikipedia.
For instructions on who to use it, cf. section 2.1.

**Author:** João P C Bertoldo
***github:*** github.com/joaopcbertoldo
***linkedin:*** linkedin.com/in/joaopcbertoldo

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
1) Download the black list [here](https://s3.amazonaws.com/dd-interview-data/data_engineer/wikipedia/blacklist_domains_and_pages) and place the file in `src/black_list`.
2) Install all the requirements (cf. `requirements.txt`).
3) (1) Start luigi daemon (luigi's remote scheduler):
```sh
$  luigid
```
3) (2) Otherwise go to `src/configs`, go to the class `Options` and change `use_local_scheduler`'s value to `False`.
4) Call the cript run.py with command `single` or `range` with `-h` to see usage and input format.
```sh
$ python run.py single -h
```
```sh
$ python run.py range -h
```

##### 2.2) Design


##### 2.3) Answers
1) I would add:
    - some sort of progressbar in tasks
    - a logger/log messages
    - something to measure time of the tasks (like a decorator on the run functions)
    - a callback  option for the ComputeRankTask, this way another app could use directly the pickle file (which would be easier for another python script) or just an option to keep the pickle files
    - an option to run it automaticaly (in the background as a sub-option) every hour
    - an alert for completions (to trigger other stuff)
    - option to move the results somewhere else after completion
    - change the results folder to a database
    - take another black list (from folder or url) as an option
        - this could create inconsistency in the outputs because a rank would be in fucntion of the blacklist, so I would store the augmented rank and do the filtering only when creating the final output of a specific call
    - enable several kinds of final outputs (other than json) and, when a certain date-hour has already been called, just convert it
2)
3)
4)
5)
