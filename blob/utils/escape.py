def flask_real_escape(s):
    
    """
    * This function is use to defence
    * NoSQL injection
    """

    if not s:
        return s, False
    sqli_flag = False
    words = [
        "$lt", "$lte", "$gt", "$gte", "$ne", "$eq", "$type", "$in", "$nin", "$or", "$and", "$not", "$nor", "$exists", "$mod",
        "$regex", "$text", "$where", "$all", "$elemMatch", "$size", "$inc", "$mul", "$rename", "$setOnInsert", "$set", "$unset",
        "$min", "$max", "$addToSet", "$pop", "$pull", "$each", "$sort", "$position", "})", "))", ");", "};", "//"
    ]
    for i in words:
        if i in s:
            sqli_flag = True
            return "", sqli_flag
    s = s.replace("}", r"\}")
    s = s.replace("]", r"\]")
    s = s.replace("[", r"\[")
    s = s.replace("{", r"\{")
    s = s.replace("'", r"\'")
    s = s.replace("$", r"\$")
    s = s.replace("/", r"\/")
    s = s.replace("(", r"\(")
    s = s.replace(")", r"\)")
    s = s.replace("=", r"\=")
    s = s.replace(";", r"\;")    
    return s, sqli_flag

def flask_real_escape_list(s_list):
    flag_list = []
    for i in s_list:
        flag_list.append(False)
    for i in range(len(s_list)):
        s_list[i], flag_list[i] = flask_real_escape(s_list[i])
    return s_list, True in flag_list 

def xss_escape(s):
    
    '''
    * not escape `>` because of markdown=>reference
    * escape dangerous byte by mistune when rendering
    '''
    
    if not s:
        return s
    s = s.replace('&', '&amp;')
    s = s.replace('<', '&lt;') 
    #s = s.replace('>', '&gt;')
    return s

if __name__ == "__main__":
    a = ["$ne", "a", "1"]
    tmp, flag = flask_real_escape_list(a)
    print(tmp)
    print(flag)