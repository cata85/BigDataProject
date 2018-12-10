import praw


reddit = praw.Reddit(
    client_id = 'Ff85HPhi6wky5Q',
    client_secret='WQkqCePEiMDybqTzJp-rY2mTLCs',
    user_agent='testscript by /u/cata85'
)

print(reddit.read_only)
