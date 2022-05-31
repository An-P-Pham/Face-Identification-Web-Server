from face_Identification import load_known, detect_unknown

def access_control():
    matches = detect_unknown()
    if(len(matches) == 0):
        return "No Matches Found"
    else:
        return "Match: " + matches[0]

