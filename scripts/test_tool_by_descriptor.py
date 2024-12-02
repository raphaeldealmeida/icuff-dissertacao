#!/usr/bin/env python3
# coding: utf-8

# Descripton: Verifica em cada projeto, quais ferramentas de teste utilizada pelos projetos

# ===== Configuration variables ======
PROG_LANG = "JavaScript"
REPO_PATH = "../repos"
DATASET_PATH = "../dataset/projects_2022.2.xlsx"
DATASET_PATH_TEST_PROJECTS = f"../dataset/{PROG_LANG}_projects_tests_tools.csv"

DESC_FILE = {
    "Ruby": "Gemfile",
    "Python": [
        "requirements.txt",
        "requirements-*.txt",
        "*.txt",
        "setup.cfg",
        "setup.py",
        "test_*.py",
    ],
    "JavaScript": ["package.json", "karma.conf.js"],
    "PHP": ["composer.*"],
    "TEST": ["pom.xml"],
    "Java": ["pom.xml", "*.gradle", "dependencies.lock"],
}
TEST_TOOLS = {
    "Ruby": ["rspec", "minitest", "test-unit", "cucumber-ruby"],
    "Python": [
        "robot",
        "pytest",
        "unittest",
        "mongomock",
        "requests_mock",
        "doublex",
        "freezegun",
        "httmock",
        "httpretty",
        "mocket",
        "responses",
        "vcrpy",
        "pytest-vcr",
        "pytest-recording",
        "factory_boy",
        "mixer",
        "model_mommy",
        "model_bakery",
        "fake2db",
        "Faker",
        "mimesis",
        "radar",
    ],
    "JavaScript": [
        "jest",
        "jasmine",
        "mocha",
        "puppeteer",
        "cypress",
        "qunit",
        "tape",
        "mockjs",
        "ava",
        "meteor-node-stubs",
        "hapi/lab",
        "ckeditor/ckeditor5-dev-tests",
        "sinon",
        "testdouble",
        "proxyquire",
        "nock",
    ],
    "PHP": [
        "phpunit",
        "codeception",
        "phpspec",
        "mockery",
        "prophecy",
        "phpunit-easymock",
        "codeception/stub",
        "php-mock",
        "vfsstream",
    ],
    "TEST": ["spring-boot-starter-test", "mockito", "junit"],
    "Java": [
        "powermock",
        "mockito",
        "easymock",
        "jmock",
        "javafaker",
        "hoverfly-java",
        "com.intuit.karate",
        "needle4j",
        "beanmother-core",
        "fixture-factory",
        "jfairy",
        "wiremock",
        "mock-server",
        "jmockit",
    ],
}
# =====================================

import os
import pandas as pd
import csv
import re


def _remove_duplicates(array):
    return list(set(array))


def _remove_all(array, param):
    while param in array:
        array.remove(param)
    return array


def _get_proj_names():
    dirname = f"{REPO_PATH}/{PROG_LANG}/"
    if not os.path.exists(dirname):
        print(f"Error: Directory for {PROG_LANG} does not exists!\n")
        return None
    proj_names = os.popen(f"ls {dirname}").read()
    return _remove_all(proj_names.split("\n"), "")


def _get_used_tools(desc_path):
    used_tools = []
    for tool in TEST_TOOLS[PROG_LANG]:
        result = os.popen(f"cat {desc_path} | grep {tool}").read()
        result = _remove_all(result.split("\n"), "")
        if len(result) > 0:
            used_tools.append(tool)
    return used_tools


def _read_descriptor(desc_paths):
    tools_used = []
    for desc_path in desc_paths:
        if os.path.isfile(desc_path):
            tools_used += _get_used_tools(desc_path)
    return _remove_duplicates(tools_used)


def _write_csv(result):
    with open(DATASET_PATH_TEST_PROJECTS, mode="w") as csv_file:
        fieldnames = ["lang", "owner", "name", "test_tools"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, dialect="unix")
        writer.writeheader()
        for li in result:
            writer.writerow(li)


def _get_owner_from_repo(path_repo):
    print(path_repo)
    remote = os.popen(f'cd "{path_repo}" && git remote -v').read().split("\n")[0]
    pattern = (
        "^origin	http[s]*:\/\/[www.]*[github|gitlab]*\.com\/(.*)\/(.*)\.git \(fetch\)$"
    )
    m = re.search(pattern, remote)
    return str(m.group(1))


def execute_analisys():
    proj_names = _get_proj_names()
    dados = []
    for proj_name in proj_names:
        dir_name = f"{REPO_PATH}/{PROG_LANG}/{proj_name}"
        desc_file_name = DESC_FILE[PROG_LANG]
        owner = _get_owner_from_repo(f"{REPO_PATH}/{PROG_LANG}/{proj_name}")
        desc_files_name = "' -o -name '".join(desc_file_name)

        desc_paths = os.popen(f"find {dir_name} -name '{desc_files_name}'").read()
        # desc_paths = os.popen(f'find {dir_name} -path \'*requirements/*.txt\'')

        test_tools = _read_descriptor(desc_paths.split("\n"))
        print(f"Project: {proj_name}")
        print(f"Testing Tools: {test_tools}")
        print("\n")
        dados.append(
            {
                "lang": PROG_LANG,
                "owner": owner,
                "name": proj_name,
                "test_tools": test_tools,
            }
        )
    _write_csv(dados)


if __name__ == "__main__":
    execute_analisys()
