#setup elasticsearch service
curl -L http://github.com/elasticsearch/elasticsearch-servicewrapper/tarball/master | tar -xz
sudo mv *servicewrapper*/service /usr/local/share/elasticsearch/bin/
rm -Rf *servicewrapper*
sudo /usr/local/share/elasticsearch/bin/service/elasticsearch install
sudo ln -s 'readlink -f /usr/local/share/elasticsearch/bin/service/elasticsearch' /usr/local/bin/rcelasticsearch

#start elasticsearch service
sudo service elasticsearch start
