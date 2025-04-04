*** Settings ***
Documentation    This is a resource file, that can contain variables and keywords.
...              Keywords defined here can be used where this Keywords.resource in loaded.
Resource         /home/ats/ATS/kqa/suites/common/keyword.resource

*** Variables ***
${DEVICE_NAME}    Switch0
${DEVICE_OLT}     Olt0


*** Test Cases ***
Connect To Device
    [Setup]                        Setup
    [Teardown]                     Close All Connections
    Connect To Switch
    Send Command To Config Mode    where
    Connect To Olt



*** Keywords ***
Setup
    Load Topology    /home/ats/ATS/kqa/suites_data/topology.yaml