*** Settings ***
Library     /home/ats/ATS/kqa/library/TableVerificationLibrary.py
Library     Collections
Resource    /home/ats/ATS/kqa/suites/common/keyword.resource

*** Variables ***
${DEVICE_NAME}    Switch0
${DEVICE_OLT}     Olt0
${CMD}            show interface status

${RAW_OUTPUT}    SEPARATOR=${EMPTY}
...
...    | Interface    | TYPE        | STATUS    | MODE              | FLOWCTRL    | \n
...    | xgspon0/1    | Ethernet    | Up/Up     | Force/Full/10G    | Off/Off     | \n
...    | xgspon0/2    | Ethernet    | Up/Up     | Force/Full/10G    | Off/Off     | \n
...    | xgspon0/3    | Ethernet    | Up/Up     | Force/Full/10G    | Off/Off     | \n

${REFERENCE_TABLE}    SEPARATOR=${EMPTY}
...
...    | Interface    | STATUS    | \n
...    | xgspon0/1    | Up/Up     | \n
...    | xgspon0/2    | Up/Up     | \n

*** Test Cases ***
Verify Tables Example
    # Convert raw output to table
    Load Topology                              /home/ats/ATS/kqa/suites_data/topology.yaml
    Connect To Dut                             ${DEVICE_NAME}
    Write                                      enable
    Open Connection With Current Connection    ${DEVICE_OLT}
    Auto Detect And Set Prompt
    Write                                      enable
    Auto Detect And Set Prompt
    Set Terminal Length
    ${logcmd}                                  Send Command Terminal                          ${CMD}

    # Verify tables using whitelist logic
    ${table_raw}=     Parse Table     ${logcmd}             /home/ats/ATS/kqa/suites/resource/interface_status.template
    ${table_ref}=     Create Table    ${REFERENCE_TABLE}
    ${result}=        Verify Table    ${table_ref}          ${table_raw}                                                   whitelist
    Should Be True    ${result}

    # Verify tables using blacklist logic
    ${result}=            Verify Table    ${table_ref}    ${table_raw}    blacklist
    Should Not Be True    ${result}