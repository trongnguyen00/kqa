*** Settings ***
Library    library.CustomKeywords    WITH NAME    CustomKeywords

*** Variables ***


*** Keywords ***

Get Onu Unprovision
    [Arguments]              ${device}                   ${link}
    Access Config Mode
    Access Interface Mode    ${device}                   ${link}
    ${index}                 Get Port Index From Link    ${device}                        ${link}
    ${result}                Send Command                display ont autofind ${index}
    RETURN                   ${result}

Connect To Huawei
    Connect To Dut         Olt0
    Unset Interactive
    Set Terminal Length
    Send Command           enable    reset_prompt=True

Access Interface Mode
    [Arguments]    ${device}    ${link}

    ${interface_name}    Get Port Name From Link        ${device}            ${link}
    Send Command         interface ${interface_name}    reset_prompt=True

Access Config Mode
    Send Command    config    reset_prompt=True

Go To Previous Mode
    Send Command    quit    reset_prompt=True

Teardown Common
    Close All Connections

Setup Common
    Close All Connections
    Load Topology            /home/ats/ATS/kqa/KGPON-BR/suites_data/topology.yaml