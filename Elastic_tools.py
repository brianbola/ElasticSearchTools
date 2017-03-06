import requests
sess = requests.Session()
adapter = requests.adapters.HTTPAdapter(max_retries=100)
sess.mount('http://', adapter)


class ElasticTools(object):
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password


    def stop_shard_allocation(self):
        req = sess.get('http://%s:9200/_cat/health' % self.host, auth=(self.user, self.password))
        if not req.ok:
            print "Error Connecting to Elastic Response code %s" % req.status_code
            req.close()
        else:
            print "Stopping shard allocation"
            shard_req = sess.put('http://%s:9200/_cluster/settings' % self.host, json={"transient": {"cluster.routing.allocation.enable": "none"}}, auth=(self.user, self.password))
            if shard_req.ok:
                print shard_req.content

    def start_shard_allocation(self):
        req = sess.get('http://%s:9200/_cat/health' % self.host, auth=(self.user, self.password))
        if not req.ok:
            print "Error Connecting to Elastic Response code %s" % req.status_code
            req.close()
        else:
            print "Starting shard allocation"
            shard_req = sess.put('http://%s:9200/_cluster/settings' % self.host, json={"transient": {"cluster.routing.allocation.enable": "all"}}, auth=(self.user, self.password))
            if shard_req.ok:
                print shard_req.content

    def delete_index(self, index):
        req = sess.delete('http://%s:9200/%s' % (self.host, index),  auth=(self.user, self.password))
        if req.ok:
            print req.content
        else:
            print "Error Connecting to Elastic Response code %s" % req.status_code

    def reindex(self, index):
        req = sess.put('http://%s:9200/%s_reindex' % (self.host, index),  auth=(self.user, self.password))
        if req.ok:
            print req.content
            print "reindexing"
        reindex = sess.post('http://%s:9200/_reindex' % self.host, json={"source": {"index": "%s" % index},"dest": {"index": "%s_reindex" % index}}, auth=(self.user, self.password))
        if reindex.ok:
            print reindex.content

    def alias(self, index):
        req = sess.post('http://%s:9200/_aliases' % self.host, json={"actions": [{"add": {"index": "%s_reindex" % index, "alias": "%s" % index}}]}, auth=(self.user, self.password))
        print req.content


    def update_mapping(self):
        pass
