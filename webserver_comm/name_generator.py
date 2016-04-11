# coding=utf-8
first = ["John", "Jenny", "Test", "Hej", "Hejsan", "Tjohej", u"Hallå", "Hejdu", "Lagom", "Batman", "Kaffe"]
last = ["Doe","Presley", "Parsley", "Efternamn", "Elvisson", "von Elvis", "Elvissen", "Elvisp", "Elvioso", "El'vis",
        u"Älvis"]

len_first = len(first)
len_last = len(last)


def get_name(id):
    return first[id % len_first] + " " + last[id % len_last]


def get_name_as_array(id):
    return [first[id % len_first].capitalize(), last[id % len_last].capitalize()]