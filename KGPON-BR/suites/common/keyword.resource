*** Settings ***
Library    library.CustomKeywords    WITH NAME    CustomKeywords

*** Variables ***


*** Keywords ***
Get Onu Unprovision
    Access Config Mode
    Access Interface Mode
    ${result}                Send Command    display ont autofind ${OLT_PON_INDEX} 
    RETURN                   ${result}

Connect To Huawei
    Connect To Dut         Olt0
    Unset Interactive
    Set Terminal Length
    Send Command           enable    reset_prompt=True

Access Interface Mode
    Send Command    interface ${OLT_PON_NAME}    reset_prompt=True

Access Diagnose Mode
    Send Command    diagnose    reset_prompt=True

Access Config Mode
    Send Command    config    reset_prompt=True

Go To Previous Mode
    Send Command    quit    reset_prompt=True

Make Suite Variables
    ${ONU_INFO}           Get Device Info          Onu0
    Set Suite Variable    ${ONU_MODEL}             ${ONU_INFO['model']}
    Set Suite Variable    ${ONU_SN}                ${ONU_INFO['custom']['serial']}
    Set Suite Variable    ${ONU_VERSION}           ${ONU_INFO['custom']['version']}
    ${OLT_LINK}           Get Connection Info      Olt0
    Set Suite Variable    ${OLT_PON_ALIAS}         ${OLT_LINK['pon'][0]['alias']}
    Set Suite Variable    ${OLT_PON_NAME}          ${OLT_LINK['pon'][0]['name']}
    Set Suite Variable    ${OLT_PON_INDEX}         ${OLT_LINK['pon'][0]['index']}

Teardown Common
    Close All Connections

Setup Common
    Close All Connections
    Load Topology            /home/ats/ATS/kqa/KGPON-BR/suites_data/topology.yaml
    Make Suite Variables