import datetime
import re
from django.utils.html import strip_tags

def count_words(html_str):
	# html_str = """<h3> this is a title </h3> """
	words_str = strip_tags(html_str)
	matching_str = re.findall(r'\w+',words_str)
	count = len(matching_str)
	return count

def get_read_time(html_str):
	countw = count_words(html_str)
	read_time_min = (countw/200)
	# read_time_sec = read_time_min*60
	# read_time = str(datetime.timedelta(seconds=read_time_sec))
	return int(read_time_min)