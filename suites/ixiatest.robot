*** Settings ***
Library    /home/ats/ATS/kqa/Telnet.py
Library    /home/ats/ATS/kqa/library/terminal/TopologyLoader.py
Library    /home/ats/ATS/kqa/library/ixia/ixia_library.py


*** Variables ***
${CMD}    terminal length 0

*** Test Cases ***
Connect Ixia Test
    [Setup]       Setup
    [Teardown]    Disconnect From Ixia

    Connect To Ixia       192.168.150.230    4
    Get Session Active
    Set Session Label     4                  trongnk1

*** Keywords ***
Setup
    Load Topology    /home/ats/ATS/kqa/suites_data/topology.yaml