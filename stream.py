# Source: https://www.reddit.com/r/redditdev/comments/8s5iek/is_it_possible_to_stream_every_comment_on_reddit/e0wsyih
def stream_all_comments(reddit, subreddit='all'):
    print('Get Latest Comment')
    start_id = reddit.subreddit(subreddit).comments().__next__().id

    start_index = int(start_id, 36)
    while(True):
        comments = reddit.info(list(map(lambda num: "t1_{0}".format(to_base(num, 36)), range(start_index, start_index+100))))
        newest_id = 0
        counter = 0
        for comment in comments:
            comment_id = int(comment.id, 36)
            if(newest_id < comment_id):
                newest_id = comment_id
                if(comment.author!=None):
                    counter+=1
                    yield comment
        start_index = newest_id

def to_base(num,b):
    convStr = "0123456789abcdefghijklmnopqrstuvwxyz"
    if num<b:
        return convStr[num]
    else:
        return to_base(num//b,b) + convStr[num%b]
