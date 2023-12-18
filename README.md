# Data Engineer Challenge

This repository intention is to solve Globant’s Data Engineering Coding Challenge statements.

## How does it work?

It starts by reading CSV files that are stored locally.
![image](https://github.com/juancarlosp94/data-engineer-challenge/assets/70818906/4663ec52-639c-4b4c-afa2-b3fd7ecd3d8f)

A Flask API REST will allow us to define source paths which map to specfic URL patterns. Route '/update' handel the POST request. 

Files data is then sent to a MySQL database as input values of previously created tables

![image](https://github.com/juancarlosp94/data-engineer-challenge/assets/70818906/a4ebdfaf-f21d-4f0a-b11e-2a577f6be31a)


