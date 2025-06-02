*** Settings ***
Resource    /home/ats/ATS/kqa/KGPON-BR/suites/common/keyword.resource

Suite Setup       Setup Common
Suite Teardown    Teardown Common

*** Variables ***


*** Test Cases ***
Check ONT Activation Status Via Omci
    Connect To Huawei
    Access Config Mode
    Access Interface Mode
    Check ONT Activation Status

*** Keywords ***
