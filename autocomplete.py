import json
from typing import TypedDict, List

from markupsafe import Markup
from requests import Session

class Result(TypedDict):
    result: str
    subtext: str
    image: str
    

session = Session()

# A browser user agent is required to get result subtext
session.headers.update(
    {
        "user-agent": "Mozilla/5.0 (X11; CrOS x86_64 13505.73.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.109 Safari/537.36"
    }
)

def google_autocomplete(query: str) -> List[Result]:
    if not query:
        return []

    # Make request to endpoint
    res = session.get(
        "https://www.google.com/complete/search",
        params={
            "q": query,
            "cp": len(query),
            # Have no idea what the rest of these do
            "client": "gws-wiz",
            "xssi": "t",
            "gs_ri": "gws-wiz",
            "hl": "en",
            "authuser": 0,
            "psi": "xsDxYLmCO5Dx-gTjj6moCg.1626456261239",
            "dpr": "2"
        }
    )

    # Valid JSON is stored on the second line
    body = json.loads(
        res.text.splitlines()[1]
    )
    
    results = []

    # Iterate over results
    for item in body[0]:
        # Either get the nice looking version of the result or remove <b> tags from the normal version
        result_text = Markup(item[3]["zh"] if len(item) > 3 else Markup(item[0]).striptags()).unescape()
        # Get subtext/image if exists
        result_subtext = Markup(item[3]["zi"]).unescape() if len(item) > 3 else ''
        result_image = item[3]["zs"] if len(item) > 3 else ''
        results.append({
            "result": result_text,
            "subtext": result_subtext,
            "image": result_image
        })

    return results

def boogle_autocomplete(query: str) -> List[Result]:
    """Ultra-basic implementation of https://dcgross.com/a-new-google."""
    results = []
    results_base = google_autocomplete(query)

    for result in results_base:
        # Sites
        if "reddit" in result["result"]:
            result["result"] += " (site:reddit.com)"
        elif "bbb" in result["result"]:
            result["result"] += " (site:bbb.org)"
        elif "yelp" in result["result"]:
            result["result"] += " (site:yelp.com)"
        elif "rotten tomatoes" in result["result"]:
            result["result"] += " (site:rottentomatoes.com)"
        elif "imdb" in result["result"]:
            result["result"] += " (site:imdb.com)"
        elif "amazon" in result["result"]:
            result["result"] += " (site:amazon.com)"
        elif "github" in result["result"]:
            result["result"] += " (site:github.com)"
        elif "npm" in result["result"] or "yarn" in result["result"]:
            result["result"] += " (site:npmjs.com OR site:yarnpkg.com)"
        elif "spotify" in result["result"]:
            result["result"] += " (site:spotify.com)"
        elif "tv tropes" in result["result"] or "tvtropes" in result["result"]:
            result["result"] += " (site:tvtropes.org)"
        elif "google drive" in result["result"] or "googledrive" in result["result"]:
            result["result"] += " (site:drive.google.com)"
        elif "archive" in result["result"]:
            result["result"] += " (site:archive.org)"
        elif "archive of our own" in result["result"] or "archiveofourown" in result["result"] or "ao3" in result["result"]:
            result["result"] += " (site:archiveofourown.org)"
        elif "fanfiction.net" in result["result"] or "ff.net" in result["result"]:
            result["result"] += " (site:fanfiction.net)"
        elif "wattpad" in result["result"]:
            result["result"] += " (site:wattpad.com)"
        elif "wikipedia" in result["result"]:
            result["result"] += " (site:wikipedia.org)"
        elif "wikipedia" in result["result"]:
            result["result"] += " (site:wikipedia.org)"
        elif "wikia" in result["result"]:
            result["result"] += " (site:fandom.com)"
        # Filetypes
        elif "pdf" in result["result"]:
            result["result"] += " (filetype:pdf)"
        # Concepts
        # Google already shows lyrics and song info
        # elif "lyrics" in result["result"]:
        #     result["result"] += " (site:genius.com OR site:azlyrics.com)"
        # Google already shows trailers and movie/show info
        # elif "trailer" in result["result"]:
            # result["result"] += " (site:youtube.com)"
        elif "docs" in result["result"]:
            result["result"] += " (inurl:docs)"
        # Google will sometimes show you where you can watch something,
        # but not enough for it to be useful
        elif "where to watch" in result["result"]:
            result["result"] += " (site:justwatch.com)"
        # Overlap with PDFs
        elif "read online" in result["result"]:
            result["result"] += " (filetype:pdf OR site:gutenberg.org OR site:openlibrary.org OR site:books.google.com)"
        elif result["result"].endswith("website") :
            result_without_website = result["result"].split("website")[0].replace(" ", "")
            result["result"] += f' (inurl:{result_without_website})'
        elif "wiki" in result["result"]:
            result["result"] += " (inurl:wiki OR site:wikipedia.org OR site:fandom.com OR site:tvtropes.org)"
        elif "fanfiction" in result["result"]:
            result["result"] += " (site:archiveofourown.org OR site:wattpad.com OR site:fanfiction.net)"

        results.append(result)

    return results

def autocomplete(query: str, kind: str) -> List[Result]:
    if kind == "google":
        return google_autocomplete(query)
    elif kind == "boogle":
        return boogle_autocomplete(query)
    else:
        return google_autocomplete(query)        
