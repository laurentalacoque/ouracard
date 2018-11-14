# -*- coding: utf-8 -*-
from oura import *
from intercode import *
# Environment and holder informations (2001)
environment_version = [
    {"length":6, "type": "bin", "name":"app-version"},
]

environment_schema = [
    {"length":7, "type": "bitmap", "name":"bitmap", "schema": [
        # a Network ID
        {"length":0, "type": "complex", "name":"NetworkId", "schema": [
                {"length":12, "type": "bcd3", "name":"country"},
                {"length":12, "type": "bcd3", "name":"network"}
        ]},
        {"length":8, "type": "lookup", "as":networks, "name":"issuer-network"},
        {"length":14, "type": "date", "name":"validity"},
        {"length":11, "type": "bin", "name":"pay-method"},
        {"length":16, "type": "hex", "name":"authenticator"},
        {"length":32, "type": "hex", "name":"env-select-list"},
        {"length":2, "type": "bitmap", "schema":[
            {"length":1, "type": "bin", "name": "env-card-status"},
            {"length":0, "type": "bin", "name": "env-extra"},
        ]}
    ]}
]

holder_schema = [
    {"length":8, "type": "bitmap", "name":"holder-bitmap", "schema":[
        # Name
        {"length":2, "type": "bitmap", "name":"holder-name", "schema": [
                {"length":85, "type": "alpha5", "name":"surname"},
                {"length":85, "type": "alpha5", "name":"name"}
        ]},
        # birth
        {"length":2, "type": "bitmap", "name":"birth-bitmap", "schema":[
            {"length":32, "type": "bcddate", "name":"date-of-birth"},
            {"length":115, "type": "alpha5", "name":"place-of-birth"},
        ]},

        {"length":85, "type": "alpha5", "name":"birthname"},
        {"length":32, "type": "number", "name":"holder-id"},
        {"length":24, "type": "hex", "name":"holder-country-alpha"},
        {"length":32, "type": "hex", "name":"company"},
        {"length":4, "type": "repeat", "name":"holder profiles", "schema":[
            {"length":3, "type": "bitmap", "name":"profile-bitmap", "schema":[
                # a Network ID
                {"length":0, "type": "complex", "name":"NetworkId", "schema": [
                    {"length":12, "type": "bcd3", "name":"country"},
                    {"length":12, "type": "bcd3", "name":"network"}
                ]},
                {"length":8, "type":"int","name":"profile-id"},
                {"length":14, "type":"date","name":"profile-date"} 
           ]},
                
        ]},
        {"length":12, "type": "bitmap", "name":"holder-bitmap", "schema":[
            { "name":"HolderDataCardStatus"            , "length":4   , "type":"lookup", "as":card_status},
            { "name":"HolderDataTelereglement"         , "length":4   , "type":"bin"},
            { "name":"HolderDataResidence"             , "length":17  , "type":"bin"},
            { "name":"HolderDataCommercialID"          , "length":6   , "type":"bin"},
            { "name":"HolderDataWorkPlace"             , "length":17  , "type":"bin"},
            { "name":"HolderDataStudyPlace"            , "length":17  , "type":"bin"},
            { "name":"HolderDataSaleDevice"            , "length":16  , "type":"bin"},
            { "name":"HolderDataAuthenticator"         , "length":16  , "type":"bin"},
            { "name":"HolderDataProfileStartDate1"     , "length":14  , "type":"bin"},
            { "name":"HolderDataProfileStartDate2"     , "length":14  , "type":"bin"},
            { "name":"HolderDataProfileStartDate3"     , "length":14  , "type":"bin"},
            { "name":"HolderDataProfileStartDate4"     , "length":14  , "type":"bin"},
        ]}
    ]}
]

environment_holder_schema = environment_version + environment_schema + holder_schema


#contract schema (data depends on issuer)
#
contract_schema = [
    {"length":0, "type": "peekremainder"},
    {"length":7, "type": "bitmap", "name":"bitmap", "schema":[
            {"length":8, "type": "lookup", "as":networks, "name":"provider", "extended-data-id": True}, #extended-data-id stores the current number of the issuer to interpret extended data
            {"length":16, "type": "hex", "name":"contract-fare"},
            {"length":32, "type": "hex", "name":"contract-serial"},
            {"length":8,  "type": "int", "name":"passenger-class"},
            #validity
            {"length":2, "type": "bitmap", "name":"validity bitmap", "schema":[
                    {"length":14, "type": "date", "name":"abostart"},
                    {"length":14, "type": "date", "name":"aboend"},
            ]},
            {"length":8, "type": "lookup", "as":contract_status, "name":"status"},
            {"length":0, "type": "contractextradata", "name":"data"},
    ]},
]

#schema based on best-contracts Tariff type
contract_schemas = {
    0x20: [ #CAPV, Transisère, TAG abo
        {"length":0, "type": "peekremainder"},
        {"length":7, "type": "bitmap", "name":"bitmap", "schema":[
                {"length":8, "type": "lookup", "as":networks, "name":"provider", "extended-data-id": True}, #extended-data-id stores the current number of the issuer to interpret extended data
                {"length":16, "type": "hex", "name":"contract-fare"},
                {"length":32, "type": "hex", "name":"contract-serial"},
                {"length":8,  "type": "int", "name":"passenger-class"},
                #validity
                {"length":2, "type": "bitmap", "name":"validity bitmap", "schema":[
                        {"length":14, "type": "date", "name":"abostart"},
                        {"length":14, "type": "date", "name":"aboend"},
                ]},
                {"length":8, "type": "lookup", "as":contract_status, "name":"status"},
                {"length":0, "type": "contractextradata", "name":"data"},
        ]},
    ],
    0x50: [ #TAG tickets
        {"length":0, "type": "peekremainder"},
        {"length":7, "type": "bin", "name":"bitmap?"},
        {"length":8, "type": "lookup", "as":networks, "name":"provider", "extended-data-id": True},
        {"length":8, "type": "lookup", "as":contract_status, "name":"status?"},
        {"length":9, "type": "bin", "name":"unknown"},
        {"length":14, "type": "date", "name":"purchase-date"},
        {"length":11, "type": "time", "name":"purchase-time"},
        {"length":97, "type": "bin", "name":"unknown"},
    ],
    
    "default": [ #default contract (unknown)
        {"length":29*8, "type":"bin", "name":"undetermined-contract-format"}
    ]
}

bc_pointer_to_idcontract_record_idcounter = {
    1:("2000:2020",0,"2000:202a"),
    2:("2000:2020",1,"2000:202b"),
    3:("2000:2020",2,"2000:202c"),
    4:("2000:2020",3,"2000:202d"),
    5:("2000:2030",0,None),
    6:("2000:2030",1,None),
    7:("2000:2030",2,None),
    8:("2000:2030",3,None),
}
    
    


# This defaults to "default" and is replaced by extended_data_id if a field was marked before
contract_extra_data = {
    38 : [
        # specific to 250:502:38
        {"length":26, "type": "bin", "name":"unknown"},
        {"length":14, "type": "date", "name":"sale-date"},
        {"length":8, "type": "bin", "name":"unknown"},
        {"length":8, "type": "int", "name":"country"},
        {"length":8, "type": "lookup", "as":networks, "name":"sale-op"},
    ],
    41 : [
        # specific to 250:502:41
        {"length":0, "type":"peekremainder", "name":"remainder"},
        {"length":24, "type": "bin", "name":"unknown"},
        {"length":8, "type": "hex", "name":"counter-pointer"},
        {"length":4, "type": "int", "name":"ride-count?"},
        #{"length":59, "type": "bin", "name":"unknown"}
        {"length":4, "type": "bin", "name":"unknown"},
        {"length":8, "type": "lookup", "as":networks, "name":"network"},
        {"length":11, "type": "bin", "name":"unknown"},
        {"length":16, "type": "int", "name":"price-cents"},

        {"length":20, "type": "bin", "name":"unknown"},
    ],
    "default" : [
        {"length":0, "type":"peekremainder", "name":"remainder"},
    ]
}

#Simple counter
simulated_counter_schema = [
    {"length":24, "type": "int", "name":"remaining-journeys"},
    {"length":52*8, "type": "hex", "name":"data"}
]

best_contracts_schema = [
    # counter of 
    {"length":4, "type": "repeat", "name":"count", "schema" : [
            # best contracts
            {"length":3, "type": "bitmap", "name":"bc-bitmap", "schema":[  
                    # a Network ID
                    {"length":0, "type": "complex", "name":"NetworkId", "schema": [
                            {"length":12, "type": "bcd3", "name":"country"},
                            {"length":12, "type": "bcd3", "name":"network"}
                    ]},
                    # a Tariff structure
                    {"length":0, "type": "complex", "name":"Tariff", "schema": [
                            {"length":4, "type": "bin", "name":"bc-tariff-expl"},
                            {"length":8, "type": "hex", "name":"bc-tariff-type"},
                            {"length":4, "type": "int", "name":"bc-tariff-priority"}
                    ]},
                    # a best-contract pointer
                    {"length":5, "type": "int", "name":"bc-pointer"}
            ]}
    ]}
]


#event structure (2010, 2030)

event_schema = [
    { "description":"Event Date"                              , "length":14  , "type":"date" },
    { "description":"Event Time"                              , "length":11  , "type":"time" },
    { "description":"Event"                                   , "length":28  , "type":"bitmap", "schema": [
        { "description":"EventDisplayData"                    , "length":8   , "type":"undefined"},
        { "description":"EventNetworkId"                      , "length":24  , "type":"undefined"},
        { "description":"EventCode"                           , "length":0   , "type":"complex", "schema" :[
            {"length":4, "type": "lookup", "as":modalities, "name":"modality"},
            {"length":4, "type": "lookup", "as":transitions, "name":"transition"}
        ]},
        { "description":"EventResult"                         , "length":8   , "type":"undefined"},
        { "description":"EventServiceProvider"                , "length":8   , "type":"lookup", "as":networks},
        { "description":"EventNotOkCounter"                   , "length":8   , "type":"int"},
        { "description":"EventSerialNumber"                   , "length":24  , "type":"hex"},
        { "description":"EventDestination"                    , "length":16  , "type":"lookup","as":locations},
        { "description":"EventLocationId"                     , "length":16  , "type":"lookup","as":locations},
        { "description":"EventLocationGate"                   , "length":8   , "type":"int"},
        { "description":"EventDevice"                         , "length":16  , "type":"int"},
        { "description":"EventRouteNumber"                    , "length":16  , "type":"int"},
        { "description":"EventRouteVariant"                   , "length":8   , "type":"int"},
        { "description":"EventJourneyRun"                     , "length":16  , "type":"int"},
        { "description":"EventVehicleId"                      , "length":16  , "type":"int"},
        { "description":"EventVehicleClass"                   , "length":8   , "type":"bin"},
        { "description":"EventLocationType"                   , "length":5   , "type":"bin"},
        { "description":"EventEmployee"                       , "length":240 , "type":"hex"},
        { "description":"EventLocationReference"              , "length":16  , "type":"int"},
        { "description":"EventJourneyInterchanges"            , "length":8   , "type":"int"},
        { "description":"EventPeriodJourney"                  , "length":16  , "type":"hex"},
        { "description":"EventTotalJourneys"                  , "length":16  , "type":"hex"},
        { "description":"EventJourneyDistance"                , "length":16  , "type":"int"},
        { "description":"EventPriceAmount"                    , "length":16  , "type":"int"},
        { "description":"EventPriceUnit"                      , "length":16  , "type":"int"},
        { "description":"EventContractPointer"                , "length":5   , "type":"int"},
        { "description":"EventAuthenticator"                  , "length":16  , "type":"hex"},
        { "description":"EventData"                           , "length":5   , "type":"bitmap", 
            "schema" : [
                { "description":"EventDataFirstStamp"         , "length":14  , "type":"date"},
                { "description":"EventDataFirstStamp"         , "length":11  , "type":"time"},
                { "description":"EventDataSimulation"         , "length":1   , "type":"int"},
                { "description":"EventDataTrip"               , "length":2   , "type":"bin"},
                { "description":"EventDataRouteDirection"     , "length":2   , "type":"int"}
            ]
        }
    ]}
]

# application name such as 1TIC.ICA (many files ending in 4
application_name_schema = [
    {"name": "tag", "length":8*8, "type":"ascii"},   
    {"name": "info", "length":8*8, "type":"hex"},   
]

# ICC (:2)
icc_schema=[
    {"length":4*8, "type":"hex", "name":"tagid"},
    {"length":8*8, "type":"hex", "name":"data"}
]

file_schemas = {
    ":2": icc_schema,
    ":1000:1004": application_name_schema,
    ":2000:2004": application_name_schema,
    ":3100:3104": application_name_schema,
    ":3f04":      application_name_schema,
    ":2000:2001": environment_holder_schema,
    ":2000:2050": best_contracts_schema,
    ":2000:2030": contract_schemas[0x20],
    ":2000:2020": contract_schemas[0x20],
    ":2000:2010": event_schema,
    ":2000:2040": event_schema,
    ":2000:202a": simulated_counter_schema,
    ":2000:202b": simulated_counter_schema,
    ":2000:202c": simulated_counter_schema,
    ":2000:202d": simulated_counter_schema,
}