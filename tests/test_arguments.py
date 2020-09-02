# argument testcase for niiview

import pytest
import sys
import os

def test_help():
    return os.system("python ../niiview --help")


def test_answer():
    assert test_help() == 0
