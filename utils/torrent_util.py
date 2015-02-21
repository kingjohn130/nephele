import re

# Cut out the movie name from a torrent name
def torrent_to_search_string(name):
    # Strings that mark the end of a movie name, and start of meta data
    ends = ["1280p", "1080p", "720p", "r6", "bluray", "bdrip", "brrip", "blu-ray", "blu", "bd", "hd", "hc", "hdtv", "hdcam", "hdscr", "korsub", "extended", "uncut", "unrated", "repack", "r3", "swesub", "ac3", "xvid", "hdrip", "dvdscr", "rc", "dvdrip", "dvdr", "webrip", "rerip", "proper", "hq", "directors", "retail", "boxset", "x264", "tc", "bdrip720p", "bdrip1080p", "edition", "limited", "french", "swedish", "hindi", "italian", "kor", "nlsubs", "pal", "mkv", "avi", "iso", "mp4", "mpeg", "mov"]
    ends_i = ["iNTERNAL", "CUSTOM", "TS"]  # Case sensitive strings
    ends_double = ["dir cut", "ext cut", "web dl", "dual audio"]
    ends_triple = ["the final cut"]

    # Remove all non-alpha characters
    words = re.split(r"[^\w'-:]+", name)

    # Loop over all words. As soon as a ending is found, cut to there
    for i, word in enumerate(words):
        if word.lower() in ends or word in ends_i or \
                (i + 1 < len(words) and (word + " " + words[i + 1]).lower() in ends_double) or \
                (i + 2 < len(words) and (word + " " + words[i + 1] + " " + words[i + 2]).lower() in ends_triple):
            words = words[:i]
            break
    name = " ".join(words).lower()

    # Remove unnessesary whitespace
    name = name.strip()

    # Remove year from end of name
    name = re.sub(" \d{4}$", "", name)

    return name

def remove_bad_torrent_matches(names):
    # Identify bundles of movies, as opposed to a single movie
    def is_bundle(name):
        # Strings that identify a bundle
        bundle_identifier = [
            "trilogy", "duology", "quadrilogy",
            "movies", "collection", "series", "complete",
            " 1 3 ", " 1 4 ", " 1 5 ", " 1 2 3 "
        ]
        for identifier in bundle_identifier:
            if identifier in name:
                return True
        return False

    # Ignore movies that are cams uploaded to the HD section
    def ignore_movies(name):
        # Strings that identify a bundle
        ignore_identifier = [
            "CAM", "HDCAM", "HDTS", "Screener", "HQSCR", "DVDScr",
        ]
        for identifier in ignore_identifier:
            if identifier in name:
                return True
        return False

    def remove_duplicates_stable(names):
        nodups = []
        for name in names:
            if name not in nodups:
                nodups.append(name)

        return nodups

    names = [name for name in names if not is_bundle(name)]
    names = [name for name in names if not ignore_movies(name)]
    names = remove_duplicates_stable(names)

    return names
