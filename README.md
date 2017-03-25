## Raul's Wiki Crawler
Write a program using Python that performs the following:
Take any random article on Wikipedia (example: http://en.wikipedia.org/wiki/Art) and click on the first link
on the main body of the article that is not within parenthesis or italicized; If you repeat this process for each subsequent article you will often end up on the Philosophy page.

#### Questions:
* What percentage of pages often lead to philosophy? The first few articles usually are random but once you hit one of the subjects in the pattern (Education -> Learning -> Knowledge -> Awareness -> Philosophy), I am currently getting about less than 50% rate on runs of 10, 20, 50 pages. I can make that rate much higher, will have to debug my parser and see why the rate not in the 90's percentage. In my later runs the average path length dropped and the pattern changed to (Knowledge -> Awareness -> Quality_(philosophy) -> Philosophy).

    ````
    My run for often looks like this:
    5 pages:
    Pages that lead to Philosophy: 3
    Avg path length: 10.0
    Path Length Distribution: {'17': 2, '13': 1, 'None': 2}

    10 pages:
    Pages that lead to Philosophy: 2
    Avg: 11.0
    Path Length Distribution: {'None': 3, '16': 1, '6': 1}

    50 pages:
    Pages that lead to Philosophy: 19
    Avg path length: 5.631578947368421
    Path Length Distribution: {'None': 31, '6': 1, '14': 5, '13': 3, '11': 3, '16': 3, '8': 1, '9': 1, '18': 1, '12': 1}

    100 pages
    Pages that lead to Philosophy: 43
    Avg path length: 3.9767441860465116
    Path Length Distribution: {'None': 57, '7': 2, '16': 2, '11': 8, '15': 7, '17': 3, '10': 5, '18': 3, '8': 4, '24': 1, '19': 2, '1': 1, '6': 2, '5': 1, '14': 2}
    ````

* Using the random article link (found on any wikipedia article in the left sidebar),what is the distribution of
path lengths for 500 pages, discarding those paths that never reach the Philosophy page?
Pages that lead to Philosophy: 217
Avg path length: 11.23963133640553
Path Length Distribution: {'None': 283, '9': 23, '12': 14, '19': 3, '6': 14, '5': 11, '15': 10, '0': 3, '17': 16, '8': 6, '11': 22, '10': 17, '1': 3, '16': 24, '14': 14, '13': 9, '7': 11, '2': 3, '20': 4, '4': 3, '18': 6, '3': 1}


* How can you reduce the number of http requests necessary for 500 random starting pages?
We can see a pattern that leads to philosophy Education -> Learning -> Knowledge -> Awareness -> Philosophy (the pattern is changes, but could be after hours or a day, didn't research that, but it stays consistent for some time), to reduce requests, once we are lead to one of the pages in the pattern we can stop and assume that Philosophy will be returned down in the pipeline. This can reduce requests from 1 to 4 in each run depending on which page from the pattern we hit first. Another way is to cache the pages as you go so that on another run if you are about to request a page already visited previously, you will get the cached copy instead.

#### Requirements
* MacOSX Mavericks or greater
* python3.x
* pip must be installed if not follow the following steps from command line prompt:
    * curl https://bootstrap.pypa.io/ez_setup.py -o - | sudo python
    * sudo easy_install pip

#### Installation instructions
##### Perform the following steps from command line prompt:
* python -m venv webcrawler_env
    * If you have more than one version of python in your computer, make sure to use correct one e.g. python3 -m venv webcrawler_env
* source webcrawler_env/bin/activate
* cd wiki_webcrawler
* pip install -r requirements.txt

#### Running program
* For default run of 10 pages:
    * python web_crawler.py
* To specify amount of pages:
    * python web_crawler.py PAGE_AMOUNT
    * e.g. python web_crawler.py 50
* Out of program is being append to results.txt file

#### Issues
* Urllib errors: urllib.error.URLError after too many requests (not running into this issue anymore)
* Takes a long time to run through a path to get to Philosophy (not an issue anymore with (cache_pages_dict))
* Pages that lead to Philosophy seem kind of low, need to debug parser and verify:
    * That I'm retrieving the correct href
    * That my parenthesis matching is either too strict or that it is working properly.
    * Some pages don't have a `<b>` tag so need to find link inside other element tags e.g. `<span>`
* Had to set a threshold do to sometimes it would go back and forth between two articles leading to infinite recursion.
* Also, some pages are not found returning a 404 e.g. https://en.wikipedia.org/wiki/Tax_break
* If the element retrieved is a something other than a webpage e.g. png, then we get an urllib Error as well.

#### Updates after 3/5/2017
* I added a dictionary (cache_pages_dict) that will store the pages visited, so that later they are retrieved from there as opposed to make a request for pages already visited. The run is much faster, previously wasn't able to run 500 pages, due to an error happening at some point or just the wait of over 30 minutes, now 500 pages is done in a few minutes. However, the size of cache_pages_dict increments pretty quickly as we go through random pages and get get very large if we decide to go beyond 500 pages.
* Moved some variables that were being passed around and used in every function to GLOBALS, we can also add them as constants to a separate file if the list gets larger but since its only 3 for now I kept them in same file.
* Added tests to the most basic functions of web_crawler, planned to add more but would require to mock urllib requests. To run them you can perform the following command inside the bash shell.
    * python -m unittest -v test_web_crawler.py
