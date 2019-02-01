## Pycsvparse
This project parses a specified CSV file and inserts the data to an sqllite db. No non-standard libraries are used. 

If you are looking for a production solution to import CSV files don't use this.  Please check out [`pandas`](http://pandas.pydata.org/). 

### Quick Start:
This script presumes you are running a python 3.x environment.

 - Clone this git repo.

    `git clone https://github.com/daesu/pycsvparse`

 - Install requirements.

    `make init`

 - Run shell script cmd.

    `./pycsv <csv-file-path>`

   The CSV is parsed and will be populated into an sqllite db called `data` in the current directory. The database is recreated each run. 

## Testing
Some sample CSV files are included in the test dir and can be automatically ran. 

 - Run tests.

    `make test`
