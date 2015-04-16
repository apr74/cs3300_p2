import re
FILE_NAME = 'genres.list'
OUTFILE_NAME = 'genres.csv'

NUM_HEADER_LINES = 380

TITLE_YEAR_RE = re.compile('.+\(.+?\)')
YEAR_RE = re.compile(' \(.+?\)')
NON_NUMERIC = re.compile(r'[^\d.]+')

f_out = open(OUTFILE_NAME, 'w')
f_out.write('title,year,genre\n')

with open(FILE_NAME, 'r') as f:
	try:
		#skip header
		for i in range(0, NUM_HEADER_LINES):
			next(f)
		thisLineNum = 0
		for line in f:
			thisTitle = TITLE_YEAR_RE.search(line).group(0)
			thisYear = YEAR_RE.search(thisTitle).group(0)
			thisYear = NON_NUMERIC.sub('', thisYear) #remove nonnumeric characters
			thisTitle = YEAR_RE.sub('', thisTitle) #remove the year from the title
			thisTitle = thisTitle.replace('"', '""') #escape any quotes

			thisGenre = line.split('\t')[-1] #includes newline

			f_out.write('"' + thisTitle + '",' + thisYear + ',' + thisGenre)
			if not (thisLineNum % 10000):
				#print periodically so that we can see that it's working
				print(thisTitle + ',' + thisYear + ',' + thisGenre),
			thisLineNum += 1
	except:
		print thisLineNum
		raise