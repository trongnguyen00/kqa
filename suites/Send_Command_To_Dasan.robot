*** Settings ***
Documentation    This is a resource file, that can contain variables and keywords.
...              Keywords defined here can be used where this Keywords.resource in loaded.
Resource         /home/ats/ATS/kqa/suites/common/keyword.resource
Library          /home/ats/ATS/kqa/library/CustomTelnetLibrary.py

*** Variables ***
${DEVICE_NAME}    Switch0
${DEVICE_OLT}     Olt0
${CMD}            show running-config interface eth0/20

*** Test Cases ***
Connect To Device
    [Setup]                                    Setup
    [Teardown]                                 Close All Connections
    Connect To Dut                             ${DEVICE_NAME}
    Write                                      enable
    Open Connection With Current Connection    ${DEVICE_OLT}
    Auto Detect And Set Prompt
    Write                                      enable
    Auto Detect And Set Prompt
    Send Command Terminal                      ${CMD}
    Sleep                                      5s
    Send Command File

*** Keywords ***
Send Command File
    Write                         configure terminal
    Auto Detect And Set Prompt
    ${value}                      Create Dictionary                             mapper_value=1    uni_value=1
    Send Commands From Group      /home/ats/ATS/kqa/suites/resource/dut.yaml    show-all-vlan     &{value}

Setup
    Close All Connections
    Load Topology            /home/ats/ATS/kqa/suites_data/topology.yaml