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
    - better control/use parallelization
    - some sort of progressbar in tasks
    - a logger/log messages
    - something to measure time of the tasks (like a decorator on the run functions)
    - a callback  option for the ComputeRankTask, this way another app could use directly the pickle file (which would be easier for another python script) or just an option to keep the pickle files
    - an option to run it automaticaly (in the background as a sub-option) every hour
    - an alert for completions (to trigger other stuff)
    - option to move/export the results to somewhere else
    - store the results in a database
    - take a custom black list (from folder or url) as an option
    - edit the black list
        - this could create inconsistency in the outputs because a rank would be in fucntion of the blacklist, so I would store the augmented rank and do the filtering only when creating the final output of a specific call
    - enable several kinds of final outputs (other than json) and, when a certain date-hour has already been called, just convert it
    - divide the results in two parts (and tasks as well) because there are several domains a lot less voluminous than others, so I'd separate those that are rather more important than other and give them priority, which could improve performance

2) To run it automatically it should be relatively easy, it would be necessary to create an infinite routine that would schedule new tasks every hour by calling the `main`. It would be interesting to create control commands to operate such routine.
For safety, there could be mechanisms checking for the memory usage and disk space (as files are stored every hour). I would also create a propre process to stop/resume the app, which could be necessary for versioning it.
The logging/alert functionalities would become particularly important to keep basic track of what happens, some the should be implemented.

3) I would creat unity tests for the different encapsulated parts of the app. Overall of what I would do**:
    - DownloadTask
        - tests related to internet connection/http errors (as 404, for example)
        - check proper behavior in case of corrupted files
    - ComputeRankTask
        - test behavior cases of missing values
        - (ideally) run several examples with the black list filtering before computing the rank (which garantees a correct rank) and compare it to the used strategy --> this should estimate how often this strategy would be inconsistent
    - SaveTask
        - test that the result json is correctly loaded
    - BlackList
        - test the loading of the txt and pickle file
        - test behavior in case of missing values
        - check the `has()` and `doesnt_have()` functions with known examples
    - `rank.py` module (`RankItem` and `Rank` classes) to ensure that the logic of the algorithm works well

    ** some of these are already done in the modules them selves when run as __main\__, but not as unit tests

4) Design changes:
    - remove the input validations from `run()` and place it in a new module that would be called by `main()`, because this would make them more reusable in case that another interface or script would to trigger the app
    - decompose the `CleanUpTask` into a clean up for each task --> this could be done with a task that takes another task as parameter and creates the dependency by itself or with an abstract task. This would prevent use of disk by removing temporary stuff as soon as possible.
    - (according to performance) change the black list implementation to
        - read from a stream (thus not needing to load it completely each time)
        - store it in a database
        - use regex to check if a page is in it
    - (if the black list filtering improves enough in speed) do the filtering before creating the rank
    - in rank, rather use an ordered list (which could simplify the implementation to manage the ordering)
    - build the rank directly with the correct size then, when doing the filtering, only in case that the rank gets shorter because of eliminated items, go back to the input and get a new item
    - (if more options/commands are added) manage the parser creation in a separate package with individual/grouped parsers per module

5) luigi was used
- Tasks dependency:
``
DonwloadTask --> ComputeRankTask --> SaveRankTask --> CleanUpTask
``

- Targets:
    - ``DonwloadTask --> LocalTarget (.txt)``
    - ``ComputeRankTask --> LocalTarget (binary from pickle)``
    - ``SaveRankTask --> LocalTarget (.json)``
    - ``CleanUpTask --> nothing``
