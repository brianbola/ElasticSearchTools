from Elastic_tools import ElasticTools


elastic2 = ElasticTools('localhost', 'elastic', 'changeme')

elastic2.delete_index('filebeat-2017.02.24')

