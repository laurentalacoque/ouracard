# -*- coding: utf-8 -*-

contract_status = {
        0:"Never validated",
        1:"Used once",
        2:"Validated",
        3:"Renewment notification sent",
        4:"Punched",
        5:"Cancelled",
        6:"Interrupted",
        7:"Status OK",
        13:"Not available for validation",
        14:"Free entry",
        15:"Active",
        16:"Pre-allocated",
        17:"Completed and to be removed",
        18:"Completed and cannot be removed",
        19:"Blocked",
        20:"Data group encrypted flag",
        21:"Data group anonymous flag",
        33:"Pending",
        63:"Suspended",
        88:"Disabled",
        125:"Suspended contract",
        126:"Invalid",
        127:"Invalid et reimbursed",
        255:"Deletable",
} #courtesy CalypsoInspector

card_status = {
    0:"Anonyme", 
    1:"Declarative", 
    2:"Personnalisee", 
    3:"Codage specifique"
} #Courtesy CalypsoInspector
    
modalities = {
    0 : "Non specifie",
    1 : "Bus urbain",
    2 : "Bus interurbain",
    3 : "Metro",
    4 : "Tram",
    5 : "Train",
    6 : "Parking"
}

transitions  = {
    0 : "Non specifie",
    1 : "Entree",
    2 : "Sortie",
    4 : "Inspection",
    6 : "changement (Entree)",
    7 : "changement (Sortie)"
}

en1545_alpha4 = [ "-","A","B","C","D","E","F","G",
          "H","I","J","K","L","M","N","O",
          "P","Q","R","S","T","U","V","W",
          "X","Y","Z","?","?","?","?"," " ] #Courtesy cardpeek