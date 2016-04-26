# totally not done! ba cpastad fra LoadToXy

mep = OngoingsLoader(start_time, end_time, interval)
mep.set_match({"filtered" : {
    "filter": {
        "bool": {
            "must": {
                "or": [
                    {
                        "match" : {"ReasonForVisit" :"MEP"}
                    },
                    {
                        "match" : {"ReasonForVisit" :"TRAU"}
                    }
                ]
            }
        }
    }
}})

x5 = mep.load_vector()

