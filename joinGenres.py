import csv
ACADEMY_DATA_CSV = "AcademyData.csv"
GENRE_CSV = "genres.csv"
OUTFILE_NAME = 'genresOfAcademyAwards.csv'

f_out = open(OUTFILE_NAME, 'wb')
f_out_writer = csv.writer(f_out);
f_out_writer.writerow(['Year','Category','Nominee','Won?','Genre'])

with open(ACADEMY_DATA_CSV, 'rU') as f_academyData, open(GENRE_CSV, 'rU') as f_genre:
	academyLineNum = 0
	genresLineNum = 0
	try:
		#read academy data and sort by movie name
		csv_academyData = list(csv.DictReader(f_academyData))
		csv_academyData.sort(key=lambda x:x['Nominee'])

		#read genre data and sort by movie name
		csv_genreData = list(csv.DictReader(f_genre))
		csv_genreData.sort(key=lambda x:x['title'])

		print "Finished reading and sorting both CSV files; now commencing join"

		#sort merge join
		for academyLine in csv_academyData:
			genresLine = csv_genreData[genresLineNum]
			while genresLine['title'] < academyLine['Nominee']:
				#while the current genre title is earlier in the alphabet than the current award title
				#i.e. we stop at where it is or where it should be
				genresLineNum += 1
				genresLine = csv_genreData[genresLineNum]

			#if we're indeed at the right position
			if genresLine['title'] == academyLine['Nominee'] and genresLine['year'] == academyLine['Year']:
				genresBackpointer = genresLineNum
				while genresLine['title'] == academyLine['Nominee'] and genresLine['year'] == academyLine['Year']:
					#loop through all the genres
					f_out_writer.writerow([academyLine['Year'], academyLine['Category'], academyLine['Nominee'], academyLine['Won?'], genresLine['genre']])
					genresLineNum += 1
					genresLine = csv_genreData[genresLineNum]
				genresLineNum = genresBackpointer #reset line number in case the next award is for the same movie
			else:
				f_out_writer.writerow([academyLine['Year'], academyLine['Category'], academyLine['Nominee'],academyLine['Won?'], None])
				#if not found in the genres database, print it anyway with no genre
			if(academyLineNum % 1000):
				#periodically print stuff out for monitoring purposes
				print academyLine['Year'] + "," + academyLine['Category'] + "," + academyLine['Nominee']
			academyLineNum += 1
	except:
		print "Error at: Academy Data Line %d, Genres Data Line %d" % (academyLineNum, genresLineNum)
		raise