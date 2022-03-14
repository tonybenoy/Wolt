# Wolt Restaurant Opening hours

An endpoint that accepts JSON-formatted opening hours of a
restaurant as an input and returns the rendered human readable format as a text output.

## Running the project
The project uses `fastapi` as the api server and can be run with `poetry` or using `gunicorn` as described below. There is the option of running the same through docker using the `docker-compose.yaml` file.
### Dependency setup
The project is configured with `poetry`. The use of `poetry` is optional  as the same is exported to `requirements.txt` and you can use pip to install all the project dependencies.
##### Using poetry
Install poetry [refer](https://python-poetry.org/docs/#installation)
###### Using pip
`pip install poetry`
###### Using the script
`curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
`
##### Installing dependencies
`poetry install`

##### Using pip
`pip install -r requirements.txt`

### Running the project
#### Using poetry
`poetry run gunicorn -b 0.0.0.0:8000 src.main:app -w 1 -k uvicorn.workers.UvicornWorker --preload`

#### Using docker
```
docker-compose build
docker-compose up
```
#### Dependencies through pip
`gunicorn -b 0.0.0.0:8000 src.main:app -w 1 -k uvicorn.workers.UvicornWorker --preload`
## Running tests
All the config for tests are setup in pyproject.toml. Simply run pytest to run the complete tests and get coverage report.
#### Using poetry
```
poetry run pytest
```
#### pytest
If dev dependencies are installed using pip
`pytest`

## Development
Install the dev dependencies
### Run the project
Running using poetry is highly recommended for the entire dev dependencies to work such as black, flake8 so on.
#### Initial Setup
Install dev dependency
```
poetry --dev-dependency
```
The project uses pre-commit to fix code before committing
```
pre-commit install
```
#### Running the project
```
poetry shell
poetry run gunicorn -b 0.0.0.0:8000 src.main:app -w 1 -k uvicorn.workers.UvicornWorker --preload --reload
```

## Part 2
Is the current JSON structure the best way
to represent that kind of data or can you come up with a better version?

The handling though timestamps with the fixed date does not allow me to handle the restaurant closing the next day efficiently. Having the timestamp varied as a week i.e. from 1 Jan 1970 to 7 Jan 1970 would allow for day checks. Also I can skip the entire day handling as well by having 1 Jan be the timings for Thursday and so on.
Also having the special case with the timestamp for the next day seems inefficient given the current use case as we do not care about the day it closed and are appending to the previous day itself.
Another  structure would be adding more verbosity to the json response ad having the open close as a common set rather than having the index/position of the time to determine the order so has to avoid the handling and improving on the processing time to return the response as below.
```
{
    "sunday": [{
            "open": {
                "hour": 3,
                "minute": 30
            },
            "close": {
                "hour": 10,
                "minute": 30
            }
        },
        {
            "open": {
                "hour": 11,
                "minute": 30
            },
            "close": {
                "hour": 12,
                "minute": 30
            }
        }
    ],
    "monday": [{
        "open": {
            "hour": 3,
            "minute": 30
        },
        "close": {
            "hour": 10,
            "minute": 30
        }
    }]
}
```
