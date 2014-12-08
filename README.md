# Introduction

DeliverMan is a web portal for [Fabric](http://www.fabfile.org/). [![Circle CI](https://circleci.com/gh/dreampuf/deliverman.svg?style=svg)](https://circleci.com/gh/dreampuf/deliverman)

# Features

- Django base, grace implatment of a website and you could customize your want to
- A lot recipes of deploy scripts base on fabric
- The base way of inventories management

# Installation Step

    # checkout static files
    git submodule init
    git submodule update
    # using your python environment
    pip install -r requirements.txt
    ./manage.py syncdb
    ./manage.py runserver
