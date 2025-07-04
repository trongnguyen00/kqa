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
    ${ONU_MODEL}          Get Device Model            Onu0
    Set Suite Variable    ${ONU_MODEL}
    ${ONU_SN}             Get Device Custom Field     Onu0    serial
    Set Suite Variable    ${ONU_SN}
    ${ONU_VERSION}        Get Device Custom Field     Onu0    version
    Set Suite Variable    ${ONU_VERSION}
    ${OLT_PON_ALIAS}      Get Port Alias From Link    Olt0    olt0-pon0
    Set Suite Variable    ${OLT_PON_ALIAS}
    ${OLT_PON_NAME}       Get Port Name From link     Olt0    olt0-pon0
    Set Suite Variable    ${OLT_PON_NAME}
    ${OLT_PON_INDEX}      Get Port Index From Link    Olt0    olt0-pon0
    Set Suite Variable    ${OLT_PON_INDEX}
    ${ONU_UNI_ALIAS}      Get Port Alias From Link    Onu0    onu0-ixia-1
    Set Suite Variable    ${ONU_UNI_ALIAS}
    ${ONU_UNI_NAME}       Get Port Name From Link     Onu0    onu0-ixia-1
    Set Suite Variable    ${ONU_UNI_NAME}

Get Onu Id
    ${ONU_ID}            Get Onuid From Serial    olt0-pon0    ${ONU_SN}
    Set Test Variable    ${ONU_ID}

Check ONT Activation Status
    Get Onu Id
    ${find_onu}              Get Onu Info    olt0-pon0              ${ONU_ID}
    ${find_onu_table}        Parse Table     ${find_onu}            /home/ats/ATS/kqa/KGPON-BR/suites/resource/onu_info_hw.template
    Create Onu Info Table
    ${result}                Verify Table    ${onu_verify_table}    ${find_onu_table}
    Should Be True           ${result}

Create Onu Info Table
    ${onu_info}    Catenate
    ...            | PORT                                 | SN           | CONTROL_FLAG    | RUN_STATE    | CONFIG_STATE    | MATCH_STATE    | \n
    ...            | ${OLT_PON_ALIAS}/${OLT_PON_INDEX}    | ${ONU_SN}    | active          | online       | normal          | match          | \n

    ${onu_verify_table}    Create Table           ${onu_info}
    Set Test Variable      ${onu_verify_table}

Get Onu Version Via Omci
    ${version_onu}      Get Onu Version     olt0-pon0         ${ONU_ID}
    ${onu_ver_table}    Parse Table         ${version_onu}    /home/ats/ATS/kqa/KGPON-BR/suites/resource/parse_ont_version.template
    RETURN              ${onu_ver_table}

Get Onu Version Via Console
    [Teardown]             Close Connection
    Connect To Dut         Onu0
    ${actual_rlt}          Send Command           sw_info
    ${actual_rlt_table}    Parse Table            ${actual_rlt}    /home/ats/ATS/kqa/library/terminal/dal/template/ont_console_version.template
    RETURN                 ${actual_rlt_table}

Verify Onu Version
    ${onu_ver_omci}    Get Onu Version Via Omci
    ${onu_ver_cs}      Get Onu Version Via Console
    ${result}          Verify Table                   ${onu_ver_cs}    ${onu_ver_omci}
    Should Be True     ${result}

Teardown Common
    Close All Connections

Setup Common
    Close All Connections
    Load Topology            /home/ats/ATS/kqa/KGPON-BR/suites_data/topology.yaml
    Make Suite Variables