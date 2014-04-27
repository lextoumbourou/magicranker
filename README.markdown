# MagicRanker.com repo

Codebase for the MagicRanker project. Visit https://www.magicranker.com to see it in action.

## Quick Start

1. Clone project and install dependancies

```
> git clone https://github.com/lextoumbourou/magicranker.com.git
> virtualenv ENV
> . ENV/bin/activate
> pip install -r requirements.txt
```

2. Prepare database

```
> sudo apt-get install postgres9.2
> createdb -U postgres magicranker
> createuser -U postgres magicranker
```

3. Run webserver

```
> python manage.py runserver
```

## Tests

```
> python manage.py test rank
```
