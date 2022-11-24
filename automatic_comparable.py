import json
import requests
import csv


# Recuperando os dcumentos retornados da requisição em uma lista
def get_doc_list(core, query):
	url = requests.get(f"http://localhost:8983/solr/{core}/select?indent=true&q.op=OR&q={query}")

	text = url.text
	list_doc = []
	data = json.loads(text)

	for doc in data['response']['docs']:
		doc = doc['doc']
		list_doc.append(str(doc).strip("['']"))

	return list_doc

# Lendo e armazendo a matriz de documentos de um CSV
def get_matrix(nome_arquivo):
	file = open(nome_arquivo)
	csvreader = csv.reader(file)
	dict_docs = {}
	numDocs = next(csvreader)
	query1 = next(csvreader)
	query2 = next(csvreader)
	lent = len(numDocs)
	for i in range(lent):
		dict_docs[numDocs[i]] = query1[i], query2[i]

	return dict_docs

# Pegando o numero de documentos relevantes retornados de cada requisição enviada ao servidor
def get_num_docs_relevancy(dict_matriz, query):
	qtd = 0
	for key in dict_matriz.keys():
		if dict_matriz[key][query] == '1':
			qtd+=1

	return qtd


# Armazenando os documentos marcados como relevantes na matriz de relevancia
def get_rel_docs(query):
	docs_rel = []
	for key in dic_matrix.keys():
		key_list = list(key)
		if dic_matrix[key][query] == '1':
			keynew = []
			for i in range(len(key_list)):
				if i == 3:
					keynew.append(' ')
				keynew.append(key_list[i])
			docs_rel.append("".join(keynew))
	return docs_rel

# computando precisão simples do sistema de indexação
def computing_precision(num_docs, num_docs_relevancy):
	if not num_docs == 0:
		return num_docs_relevancy/num_docs
	return -1

# Armazenando uma lista de documentos relevantes recuperados de cada query
def get_doc_rel_rec(list_of_docs,query):
	num_docs_rel_rec = 0
	docs_rel = get_rel_docs(query)
	for doc in docs_rel:
		if doc in list_of_docs:
			num_docs_rel_rec+=1
	return num_docs_rel_rec

# Computando cobertura do SI para cada query
def computing_coverage(list_of_docs, dic_matrix, query):
	num_docs_rel_rec = 0
	docs_rel = get_rel_docs(query)

	for doc in docs_rel:
		if doc in list_of_docs:
			num_docs_rel_rec+=1

	num_docs_rel = get_num_docs_relevancy(dic_matrix, query)
	if num_docs_rel_rec == 0:
		return -1
	return num_docs_rel_rec/num_docs_rel

# Computando a medida F para cada query com base na precisão e cobertura
def computing_f_measure(precision, coverage):
	f = 2/(1/coverage + 1/precision)
	return f

query1 = 'Fingerprint sensor not working after updating the system&q.op=OR&indent=true&rows=110'
query2 = 'Google%20assistant%20problems%20when%20interacting%20with%20other%20apps&rows=110'

bases = {'Base 1': 'SI_baseline', 'Base 2': 'SI_stopwords', 'Base 3': 'SI_stemming',
		 'Base 4': 'SI_stopwords_stemming', 'Base 5': 'SI_stopwords_synonym'}


# Recuperando os documentos da base passando a query1 para a requisição
docs_base_1_query1 = get_doc_list(bases['Base 1'], query1)
docs_base_2_query1 = get_doc_list(bases['Base 2'], query1)
docs_base_3_query1 = get_doc_list(bases['Base 3'], query1)
docs_base_4_query1 = get_doc_list(bases['Base 4'], query1)
docs_base_5_query1 = get_doc_list(bases['Base 5'], query1)

# Recuperando os documentos da base passando a query2 para a requisição
docs_base_1_query2 = get_doc_list(bases['Base 1'], query2)
docs_base_2_query2 = get_doc_list(bases['Base 2'], query2)
docs_base_3_query2 = get_doc_list(bases['Base 3'], query2)
docs_base_4_query2 = get_doc_list(bases['Base 4'], query2)
docs_base_5_query2 = get_doc_list(bases['Base 5'], query2)

# armazenando a matriz de relevancia
dic_matrix = get_matrix('Matriz de relevancia.csv')

print(docs_base_1_query2)

# Base 1
# Query 1
# query1_precision_base1 = computing_precision(len(docs_base_1_query1), get_num_docs_relevancy(dic_matrix, 0))
# query1_coverage_base1 = computing_coverage(docs_base_1_query1, dic_matrix, 0)
# query1_fmeasure = computing_f_measure(query1_precision_base1, query1_coverage_base1)
# print(f"A precisão na base 1 para a query 2 foi {query1_precision_base1} e a cobertura foi {query1_coverage_base1} e a medida-F foi "
# 	  f"{query1_fmeasure}")

# Base 1
# Query 2
query2_precision_base1 = computing_precision(len(docs_base_1_query2), get_num_docs_relevancy(dic_matrix, 1))
query2_coverage_base1 = computing_coverage(docs_base_1_query2, dic_matrix, 1)
query2_fmeasure = computing_f_measure(query2_precision_base1, query2_coverage_base1)
print(f"A precisão na base 1 para a query 2 foi {query2_precision_base1} e a cobertura foi {query2_coverage_base1} e a medida-F foi "
	  f"{query2_fmeasure}")


# Base 2

# Query 1
# query1_precision_base2 = computing_precision(len(docs_base_2_query1), get_num_docs_relevancy(dic_matrix, 0))
# query1_coverage_base2 = computing_coverage(docs_base_2_query1, dic_matrix, 0)
# query1_fmeasure = computing_f_measure(query1_precision_base2, query1_coverage_base2)
# print(f"A precisão na base 2 para a query 2 foi {query1_precision_base2} e a cobertura foi {query1_coverage_base2} e a medida-F foi "
# 	  f"{query1_fmeasure}")

# Query 2
query2_precision_base2 = computing_precision(len(docs_base_2_query2), get_num_docs_relevancy(dic_matrix, 1))
query2_coverage_base2 = computing_coverage(docs_base_2_query2, dic_matrix, 1)
query2_fmeasure = computing_f_measure(query2_precision_base2, query2_coverage_base2)
print(f"A precisão na base 2 para a query 2 foi {query2_precision_base2} e a cobertura foi {query2_coverage_base2} e a medida-F foi "
	  f"{query2_fmeasure}")



# Base 3
# Query 1
# query1_precision_base3 = computing_precision(len(docs_base_3_query1), get_num_docs_relevancy(dic_matrix, 0))
# query1_coverage_base3 = computing_coverage(docs_base_3_query1, dic_matrix, 0)
# query1_fmeasure = computing_f_measure(query1_precision_base3, query1_coverage_base3)
# print(f"A precisão na base 3 para a query 3 foi {query1_precision_base3} e a cobertura foi {query1_coverage_base3} e a medida-F foi "
# 	  f"{query1_fmeasure}")

# Query 2
query2_precision_base3 = computing_precision(len(docs_base_3_query2), get_num_docs_relevancy(dic_matrix, 1))
query2_coverage_base3 = computing_coverage(docs_base_3_query2, dic_matrix, 1)
query2_fmeasure = computing_f_measure(query2_precision_base3, query2_coverage_base3)
print(f"A precisão na base 3 para a query 2 foi {query2_precision_base3} e a cobertura foi {query2_coverage_base3} e a medida-F foi "
	  f"{query2_fmeasure}")

# Base 4
# Query 1
# query1_precision_base4 = computing_precision(len(docs_base_4_query1), get_num_docs_relevancy(dic_matrix, 0))
# query1_coverage_base4 = computing_coverage(docs_base_4_query1, dic_matrix, 0)
# query1_fmeasure = computing_f_measure(query1_precision_base4, query1_coverage_base4)
# print(f"A precisão na base 4 para a query 4 foi {query1_precision_base4} e a cobertura foi {query1_coverage_base4} e a medida-F foi "
# 	  f"{query1_fmeasure}")

# Query 2
query2_precision_base4 = computing_precision(len(docs_base_4_query2), get_num_docs_relevancy(dic_matrix, 1))
query2_coverage_base4 = computing_coverage(docs_base_4_query2, dic_matrix, 1)
query2_fmeasure = computing_f_measure(query2_precision_base4, query2_coverage_base4)
print(f"A precisão na base 4 para a query 2 foi {query2_precision_base4} e a cobertura foi {query2_coverage_base4} e a medida-F foi "
	  f"{query2_fmeasure}")

# Base 5
# query1
# query1_precision_base5 = computing_precision(len(docs_base_5_query1), get_num_docs_relevancy(dic_matrix, 0))
# query1_coverage_base5 = computing_coverage(docs_base_5_query1, dic_matrix, 0)
# query1_fmeasure = computing_f_measure(query1_precision_base5, query1_coverage_base5)
# print(f"A precisão na base 5 para a query 1 foi {query1_precision_base5} e a cobertura foi {query1_coverage_base5} e a medida-F foi "
# 	  f"{query1_fmeasure}")
# Query 2
query2_precision_base5 = computing_precision(len(docs_base_5_query2), get_num_docs_relevancy(dic_matrix, 1))
query2_coverage_base5 = computing_coverage(docs_base_5_query2, dic_matrix, 1)
query2_fmeasure = computing_f_measure(query2_precision_base5, query2_coverage_base5)
print(f"A precisão na base 5 para a query 2 foi {query2_precision_base5} e a cobertura foi {query2_coverage_base5} e a medida-F foi "
	  f"{query2_fmeasure}")

# query2_precision = computing_precision(len(list_of_docs), get_num_docs_relevancy(dic_matrix, 1))
# query2_coverage = computing_coverage(list_of_docs, dic_matrix, 1)
# query2_f = computing_f_measure(query2_precision, query2_coverage)
# print(f"A precisão na base5 para a query 1 foi {query2_precision} e a cobertura foi {query2_coverage} e a medida-F foi "
# 	  f"{query2_f}")
