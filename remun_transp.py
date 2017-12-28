#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib
import re
import optparse
import csv

def crawlPortal(names):
	url = 'http://www.portaltransparencia.gov.br/'
	ret = {}

	for n in names:
		s_query_url = url \
			  + 'servidores/Servidor-ListaServidores.asp?bogus=1&Pagina=1&TextoPesquisa=' \
			  + n.replace(' ', '%20') \

		r = urllib.urlopen(s_query_url).read()
		soup = BeautifulSoup(r, 'html.parser')

		for link in soup.find_all('a'):
			if 'DetalhaServidor' in link.get('href'):
				detailed_url = url + 'servidores/' + link.get('href')
				break


		if detailed_url:
			dr = urllib.urlopen(detailed_url).read()
			d_soup = BeautifulSoup(dr, 'html.parser')

			for link in d_soup.find_all('a'):
				if 'Remuneracao' in link.get('href'):
					comp_url = url + link.get('href')[1:]

		if comp_url:
			cr = urllib.urlopen(comp_url).read()
			r_soup = BeautifulSoup(cr, 'html.parser')

			values = []
			for tag in r_soup.find_all('td', attrs={'class': 'colunaValor'}):
				r = re.findall('\d+.\d+,\d+', str(tag))
				if r:
					values.append(float(r[0].replace('.', '').replace(',', '.')))

			if values:
				values.sort(reverse=True)



		ret[n] = values[0]

	return ret

def getNamesList(filename):
	names = []
	with open(filename, 'r') as f:
		names.append(f.read())

	names = names[0].split('\n')[:-1]

	return names

def main():
	parser = optparse.OptionParser('Usage: -S arquivo com nome dos servidores.')
	parser.add_option('-s', '--servidores', dest='filename')

	(options, args) = parser.parse_args()
	fname = options.filename

	if fname is None:
		print 'Parametro ausente.'
		exit()

	names = getNamesList(fname)
	r = crawlPortal(names)

	with open('remuneracao.csv', 'wb') as csvfile:
	    writer = csv.writer(csvfile, delimiter=',')
	    writer.writerow(('Nome', 'Remuneração'))
	    for i in range(len(names)):
	    	writer.writerow((names[i], r[names[i]]))

if __name__ == '__main__':
	main()



