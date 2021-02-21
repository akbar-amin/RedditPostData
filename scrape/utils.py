import pandas as pd 
from types import MappingProxyType

"""
Various formatting and parsing operations.
"""

__all__ = ["attributes"]

attributes = MappingProxyType({
    'path': 'permalink',
    'content': 'url',
    'subreddit': 'subreddit_name_prefixed',
    'title': 'title',
    'flair': 'link_flair_text',
    'author': 'author',
    'awards': 'total_awards_received', 
    'votes': 'score', 
    'ratio': 'upvote_ratio',
    'comments': 'num_comments', 
    'created': 'created', 
    'unique': 'name', 
    'hint': 'post_hint',
    'secure': 'secure_media.reddit_video.fallback_url',
    'media': 'media.reddit_video.fallback_url',
    'video': 'secure_media.reddit_video.fallback_url',
    'tweet': 'media.oembed.url'
})

def buildExpr(*keys):
    return 'data.children[*].data.{%s}' % ', '.join(['%s: %s' % (k, attributes[k]) for k in keys])
    
def defaultExpr():
    return buildExpr(*list(attributes.keys()))

def insert(df, nextTo: str, name: str, data: pd.Series) -> pd.DataFrame:
    df.insert(df.columns.get_loc(nextTo) + 1, name, data)
    return df 

def upvotes(df):
    uvotes = (df.ratio * df.votes).astype(int)
    return insert(df, "votes", "upvotes", uvotes)    

def downvotes(df):
    dvotes = ((1 - df.ratio) * df.votes).astype(int)
    return insert(df, "votes", "downvotes", dvotes)

def timestamps(df):
    df.created = (df.created.apply(lambda x: pd.Timestamp(x, unit = "s")
                    .tz_localize("America/Los_Angeles")
                    .strftime("%Y-%m-%d %H:%M:%S"))
                )
    return df 

def transform(df):

    if isinstance(df, list):
        df = pd.DataFrame(df)

    df = (df.pipe(downvotes)
            .pipe(upvotes)
            .pipe(timestamps)
          )
    return df 


