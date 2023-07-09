'''
 *  Project             :   Screenipy
 *  Author              :   Pranjal Joshi
 *  Created             :   29/04/2021
 *  Description         :   Automated Test Script for pkscreener
'''


import pytest
import sys
import os
import numpy as np
import pandas as pd
import configparser
import requests
import json
import platform
import shutil

shutil.copyfile('../src/.env.dev', '.env.dev')
sys.path.append(os.path.abspath('../src'))
import classes.ConfigManager as ConfigManager
from classes.Changelog import changelog, VERSION
from classes.OtaUpdater import OTAUpdater
import globals 
from pkscreener import *
last_release = 0
configManager = ConfigManager.tools()

# Generate default configuration if not exist


def test_generate_default_config(mocker, capsys):
    mocker.patch('builtins.input', side_effect=['5','0', '\n'])
    with pytest.raises(SystemExit):
        configManager.setConfig(ConfigManager.parser, default=True)
    out, err = capsys.readouterr()
    assert err == ''

def test_if_release_version_increamented():
    global last_release
    r = requests.get(
        "https://api.github.com/repos/pkjmesra/PKScreener/releases/latest")
    try:
        last_release = float(r.json()['tag_name'])
    except:
        if r.json()['message'] == 'Not Found':
            last_release = 0
    assert float(VERSION) > last_release

def test_option_X_0(mocker):
    try:
        mocker.patch('builtins.input', side_effect=['X', '0', globals.TEST_STKCODE, 'y'])
        main(testing=True)
        assert globals.screenResults is not None
        assert len(globals.screenResults) == 1 
    except StopIteration:
        pass


def test_option_X_5_1(mocker):
    try:
        mocker.patch('builtins.input', side_effect=['X', '5', '1', 'y'])
        main(testing=True)
        assert globals.screenResults is not None
        assert len(globals.screenResults) > 0
    except StopIteration:
        pass


def test_option_X_5_2(mocker):
    try:
        mocker.patch('builtins.input', side_effect=['X', '5', '2', 'y'])
        main(testing=True)
        assert globals.screenResults is not None
        assert len(globals.screenResults) > 0
    except StopIteration:
        pass


def test_option_X_5_3(mocker):
    try:
        mocker.patch('builtins.input', side_effect=['X', '5', '3', 'y'])
        main(testing=True)
        assert globals.screenResults is not None
        assert len(globals.screenResults) > 0
    except StopIteration:
        pass


def test_option_X_5_4_7(mocker):
    try:
        mocker.patch('builtins.input', side_effect=['X', '5', '4', '7', 'y'])
        main(testing=True)
        assert globals.screenResults is not None
        assert len(globals.screenResults) > 0
    except StopIteration:
        pass


def test_option_X_5_5(mocker):
    try:
        mocker.patch('builtins.input', side_effect=['X', '5', '5', '30', '70'])
        main(testing=True)
        assert globals.screenResults is not None
        assert len(globals.screenResults) > 0
    except StopIteration:
        pass


def test_option_X_5_6_1(mocker):
    try:
        mocker.patch('builtins.input', side_effect=['X', '5', '6', '1', 'y'])
        main(testing=True)
        assert globals.screenResults is not None
        assert len(globals.screenResults) > 0
    except StopIteration:
        pass


def test_option_X_5_7_1_7(mocker):
    try:
        mocker.patch('builtins.input', side_effect=['X', '5', '7', '1', '7', 'y'])
        main(testing=True)
        assert globals.screenResults is not None
        assert len(globals.screenResults) > 0
    except StopIteration:
        pass


def test_option_E(mocker, capsys):
    try:
        mocker.patch('builtins.input', side_effect=['E', 
            str(configManager.period),
            str(configManager.daysToLookback),
            str(configManager.duration),
            str(configManager.minLTP),
            str(configManager.maxLTP),
            str(configManager.volumeRatio),
            str(configManager.consolidationPercentage),
            'y',
            'y',
        ])
        with pytest.raises((SystemExit, configparser.DuplicateSectionError)):
            main(testing=True)
        out, err = capsys.readouterr()
        assert err == 0 or err == ''
    except StopIteration:
        pass


def test_option_configManager():
    configManager.getConfig(ConfigManager.parser)
    assert configManager.duration is not None
    assert configManager.period is not None
    assert configManager.consolidationPercentage is not None


def test_option_Z(mocker, capsys):
    try:
        mocker.patch('builtins.input', side_effect=['Z',''])
        with pytest.raises(SystemExit):
            main(testing=True)
        out, err = capsys.readouterr()
        assert err == ''
    except StopIteration:
        pass

def test_option_X_Z(mocker, capsys):
    try:

        mocker.patch('builtins.input', side_effect=['X','Z',''])
        with pytest.raises(SystemExit):
            main(testing=True)
        out, err = capsys.readouterr()
        assert err == ''
    except StopIteration:
        pass

def test_option_X_12_Z(mocker, capsys):
    try:
        mocker.patch('builtins.input', side_effect=['X','12','Z',''])
        with pytest.raises(SystemExit):
            main(testing=True)
        out, err = capsys.readouterr()
        assert err == ''
    except StopIteration:
        pass

def test_option_X_14_0(mocker):
    # Scanners > F&O Stocks > All indicators
    try:
        mocker.patch('builtins.input', side_effect=['X','14', '0', 'y'])
        main(testing=True)
        assert globals.screenResults is not None
        assert len(globals.screenResults) > 0
    except StopIteration:
        pass

def test_ota_updater():
    try:
        OTAUpdater.checkForUpdate(globals.proxyServer,VERSION)
        assert (
            "exe" in OTAUpdater.checkForUpdate.url or "bin" in OTAUpdater.checkForUpdate.url)
    except StopIteration:
        pass


def test_release_readme_urls():
    global last_release
    f = open('../src/release.md', 'r')
    contents = f.read()
    f.close()
    failUrl = [f"https://github.com/pkjmesra/PKScreener/releases/download/{last_release}/pkscreener.bin",
               f"https://github.com/pkjmesra/PKScreener/releases/download/{last_release}/pkscreener.exe"]
    passUrl = [f"https://github.com/pkjmesra/PKScreener/releases/download/{VERSION}/pkscreener.bin",
               f"https://github.com/pkjmesra/PKScreener/releases/download/{VERSION}/pkscreener.exe"]
    for url in failUrl:
        assert not url in contents
    for url in passUrl:
        assert url in contents


def test_if_changelog_version_changed():
    global last_release
    v = changelog.split(']')[-2].split('[')[-1]
    assert float(v) > float(last_release)
