# description: Pull important data from Wikipedia film pages stored locally.
# authors: Paul Prae, Daniel Joensen
# since: 3/08/2015
# tested with Python 3.3 on CentOS 7

import os
import sys
import re
from bs4 import BeautifulSoup
import wikipedia

wikipediaRoot = 'http://en.wikipedia.org';


def director_extractor(filmPageSoup):
	summaryTable = filmPageSoup.find('table',{ 'class' : 'infobox vevent'});	
	directorData = [];

	try:
		summaryTableRows = summaryTable.find_all('tr');

		for row in summaryTableRows:
			if 'Directed' in row.text:
				directorNameATags = row.find_all('a');
				if not directorNameATags:
					directorName = row.text.replace(',','').replace('\'','').replace('"','').replace('\u014d','o');
					directorName = directorName.replace('\n','').replace('Directed by','');
					directorURL = 'null'
					directorTuple = {'name': directorName, 'url': directorURL};
					directorData.append(directorTuple);
				else:
					for tag in directorNameATags:
						if tag['href'][0] == "/":			
							directorName = tag['title'].replace(',','').replace('\'','').replace('"','').replace('\u014d','o');
							directorURL = wikipediaRoot + tag['href'].replace(',','').replace('\'','').replace('"','');
							directorTuple = {'name': directorName, 'url': directorURL};
							directorData.append(directorTuple);
	except AttributeError:
		directorTuple = {'name': "null", 'url': "null"};
		directorData.append(directorTuple);

	return directorData;

def actor_extractor(filmPageSoup):

	summaryTable = filmPageSoup.find('table',{ 'class' : 'infobox vevent'});
	actorData = [];

	try:
		summaryTableRows = summaryTable.find_all('tr');
		for row in summaryTableRows:
			if 'Starring' in row.text:
				actorNameATags = row.find_all('a');
				for tag in actorNameATags:
					if tag['href'][0] == "/":			
						actorName = tag['title'].replace(',','').replace('\'','').replace('"','');
						actorURL = wikipediaRoot + tag['href'].replace(',','').replace('\'','').replace('"','');
						actorTuple = {'name': actorName, 'url': actorURL};
						actorData.append(actorTuple);
	except AttributeError:
		actorTuple = {'name': actorName, 'url': actorURL};
		actorData.append(actorTuple);

	return actorData;


if __name__=="__main__":

	relativeFilmFilePath = './data/films/test/';
	filmFiles = os.listdir(relativeFilmFilePath);
	for filmFileName in filmFiles:
		print('-----------');
		print(filmFileName);
		filmPage = open(relativeFilmFilePath + filmFileName);
		filmPageSoup = BeautifulSoup(filmPage.read());
		directorData = director_extractor(filmPageSoup);
		actorData = actor_extractor(filmPageSoup);
		for directorTuple in directorData:
			print('Director:');
			print(directorTuple);
		for actorTuple in actorData:
			print('Actor:');
			print(actorTuple);

