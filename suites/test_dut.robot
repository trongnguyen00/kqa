*** Settings ***
Library    library.CustomKeywords    WITH NAME    CustomKeywords

*** Variables ***
${CMD}    terminal length 0

*** Test Cases ***
Connect To Device HW
    [Setup]       Setup
    [Teardown]    Close All Connections

    Connect To Dut    Olt3
    ${cur_pr}         Get Current Prompt
    Log To Console    ${cur_pr}
    Send Command      enable                reset_prompt=True
    ${cur_pr}         Get Current Prompt
    Log To Console    ${cur_pr}

    Send Command    ${CMD}
    Send Command    show port status
    # Send Commands From Group    /home/ats/ATS/kqa/suites/resource/dut.yaml    config-profile    mapper_value=1    uni_value=1

*** Keywords ***
Setup
    Close All Connections
    Load Topology            /home/ats/ATS/kqa/suites_data/topology.yaml