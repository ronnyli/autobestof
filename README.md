# autobestof 
Bot that posts to [r/AutoBestOf](https://www.reddit.com/r/AutoBestOf/).

Searches all of Reddit for the most useful comments. Like [**r/bestof**](https://www.imgur.com/ngnPo6F) but automated.

### Usage
- install dependencies
```
python3 -m pipenv install
python3 -m pipenv shell
```
- create `.env` file and make sure it has the following environment variables:
```
CLIENT_ID=abc
CLIENT_SECRET=def
REDDIT_USER=ghi
REDDIT_PASS=jkl
```
- Run the following commands in two separate screens
```
python3 autobestof.py
python3 autobestof_cleanup.py
```
