import praw
import datetime
import yagmail

class Chapter(object):
    """A class to represent a manga chapter"""
    def __init__(self, series, chapter, link, timestamp):
        self.series = series
        self.chapter = chapter
        self.link = link
        self.timestamp = timestamp

    @classmethod
    def from_submission(cls, submission):
        """constructs a Chapter from a submission"""
        return cls(get_series(submission), get_chapter_number(submission),
                   submission.url, get_date(submission))

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            # equality based on chapter and series
            return self.chapter == other.chapter and self.series == other.series
        return NotImplemented

    def __ne__(self, other):
        """Define a non-equality test"""
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

# Add your secret, id, and useragent here. Note that not using a descriptive useragent is against reddit's policy and may result in revoked API acess
SECRET = ''
ID = ''
AGENT = ''

# subreddit for all manga
SUBREDDIT = "manga"
# prefix for discussion posts which come with specific chapters
PREFIX = "[disc] "

# will contain partial post titles to search for
TITLES = []

# read in titles from file
MANGA_FILE = open("manga_names.txt", "r")
TITLES = [PREFIX + line.rstrip('\n').lower() for line in MANGA_FILE]
MANGA_FILE.close()

# will contain latest chapters that have been sent to the user.
CHAPTERS = []

# obtain reddit instance
INSTANCE = praw.Reddit(client_id=ID, client_secret=SECRET, user_agent=AGENT)

MANGA_SUBREDDIT = INSTANCE.subreddit(SUBREDDIT)

def get_date(submission):
    """function that gets the date a submission was posted to reddit"""
    time = submission.created
    return datetime.datetime.fromtimestamp(time)

def send_error_msg(msg):
    """function that sends an error message to your email in case the script crashes while processing a submission"""
    yag = yagmail.SMTP()
    subject = "CHAPTER: ERROR, INVALID SUBMISSION"
    yag.send(subject = subject, contents = msg)

def valid_title(title):
    """function that takes in a post title and determines if it's a valid submission."""
    title = title.lower()
    for target in TITLES:
        if title[:len(target)] == target:
            return True
    return False

def get_series(submission):
    """function that takes in a submission and returns the series it belongs to. raises ValueError if a series cannot be
    found in manga_names.txt"""
    title = submission.title.lower()
    for target in TITLES:
        if title[:len(target)] == target:
            # return the title from the file minus the prefix attached to it.
            return target[len(PREFIX):]
    raise ValueError('could not find series for post with title: ' + submission.title)

def get_chapter_number(submission):
    """function that takes in a submission and returns the chapter number. raises ValueError if the submission's
    title doesn't contain a chapter number"""
    series = get_series(submission)
    # strip out prefix and series name from submission title. This way, if a series name contains a number
    # e.g. 'Eyeshield 21', it will not be considered.
    rest_of_title = submission.title[len(PREFIX + series):]
    # taken from https://stackoverflow.com/questions/4289331/python-extract-numbers-from-a-string/4289415#4289415
    chapter_candidates = []
    for t in rest_of_title.split():
        try:
            chapter_candidates.append(float(t))
        except ValueError:
            pass
    return chapter_candidates[len(chapter_candidates) -1]

def is_new_chapter(chapter):
    """function that takes in a chapter and determines if an email regarding the contents of
    the post has already been sent"""
    for chap in CHAPTERS:
        if chap == chapter:
            return False
    return True

def update_chapter(chapter):
    """takes in a chapter and updates the log of the previous chapter. i.e. if we had previously logged
    manga 'a' chapter 3 in latest_chapters.txt and this post was manga 'a' chapter 4, we would update the file."""
    new_series = True
    for chap in CHAPTERS:
        if chap.series == chapter.series:
            new_series = False
            chap = chapter
    if new_series:
        # in the case that this series has not been sent to the user yet, we must add the chapter
        # to the list of sent chapters as a new entry (since we couldn't change an existing entry)
        CHAPTERS.append(chapter)

def send_chapter(chapter, comments_link):
    """function that takes in chapter and a link to the comments section discussing it and processes it, alerting the user"""
    # note that this only works if you use keyring to save your email password and create a .yagmail file
    # in your home directory to specify the email. See the yagmail readme on github for full details on
    # how to set this up.
    yag = yagmail.SMTP()
    contents = [chapter.link, comments_link]
    # this yag.send sends an email to yourself using the email in the .yagmail file.
    yag.send(subject='CHAPTER: ' + chapter.series + ' ' + '{0:g}'.format(chapter.chapter), contents=contents)

def get_comments_link(submission):
    """function that gets the link to the comments section for a given submission to the manga subreddit"""
    return "https://www.reddit.com/r/manga/comments/" + submission.id

def main():
    # Iterate over all submissions to the manga subreddit
    for sub in MANGA_SUBREDDIT.stream.submissions():
        title = sub.title.encode("utf-8")
        if valid_title(title):
            try:
                chapter = Chapter.from_submission(sub)
                if is_new_chapter(chapter):
                    update_chapter(chapter)
                    send_chapter(chapter, get_comments_link(sub))
            except ValueError as e:
                contents = [title, get_comments_link(sub), e.message]
                send_error_msg(contents)
# run main
if __name__ == "__main__":
    main()
