*** Settings ***
Library    /home/ats/ATS/kqa/library/TableVerificationLibrary.py
Library    Collections

*** Variables ***
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

    # Verify tables using whitelist logic
    ${table_raw}=     Create Table    ${RAW_OUTPUT}
    ${table_ref}=     Create Table    ${REFERENCE_TABLE}
    ${result}=        Verify Table    ${table_ref}          ${table_raw}    whitelist
    Should Be True    ${result}

    # Verify tables using blacklist logic
    ${result}=            Verify Table    ${table_ref}    ${table_raw}    blacklist
    Should Not Be True    ${result}