#!/usr/bin/env bash

# set up git
git init 
git remote add origin git@'{{ cookiecutter.repo_org }}/{{ cookiecutter.name }}'
git add .
git commit -m "init: init {{ cookiecutter.name }} project from cookiecutter template"
git push --set-upstream origin main
