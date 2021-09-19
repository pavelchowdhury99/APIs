# Proxy API

## Aim
To create an API to return latest active proxies for countries in json.


## Technology it will make me familier
* Flask
* Rest API
* Storing data in DB
* Running program in regular intervals
* Creating async functions and promises
* Postman
* Deployment 
* Better structuring in Python

## Approch
* Programs for 
    1. Scraping website that provides proxies
    2. Test proxies against some urls to check validness
    2. Populate country wise db columns with proxies
    3. Regularly check validity of proxies
    4. Update if not valid anymore
* Creating Flask app
    1. Creating app
    2. Creating json return struncture
    3. Deploy it
* Things to take care while designing
    1. Using async methodology
    2. Logging
    3. Making variables as from external file
    4. Writing tests and logging
    5. Regulary update to git.

## References
1. [Configuration file](https://towardsdatascience.com/from-novice-to-expert-how-to-write-a-configuration-file-in-python-273e171a8eb3)
2. [Hostname required error in requests](https://stackoverflow.com/questions/66642705/why-requests-raise-this-exception-check-hostname-requires-server-hostname) use http:// instead of https:// in proxy value to avoid this error 
3. [SQLite3](https://towardsdatascience.com/sqlite-3-using-pythons-sqlite-3-module-to-save-program-data-bc6b34dcc721)
4. [Dynamic query parameter](https://stackoverflow.com/questions/16856647/sqlite3-programmingerror-incorrect-number-of-bindings-supplied-the-current-sta)
5. [Run something after flask app has started running](https://www.py4u.net/discuss/141357)
6. [Multiprocessing](https://www.geeksforgeeks.org/multiprocessing-python-set-1/)