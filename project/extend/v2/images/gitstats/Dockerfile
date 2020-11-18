FROM wexample/ubuntu18:latest

# Install Ruby / python
# Install git_stats : https://github.com/tomgi/git_stats
# Install gitinspector
# Install git-stats : https://github.com/IonicaBizau/git-stats

RUN apt install ruby ruby-dev gcc zlib1g-dev make python npm -yq && \
    gem install git_stats && \
    git clone https://github.com/ejwa/gitinspector.git /var/www/gitinspector && \
    chmod 777 /root/ && npm i -g git-stats && npm install -g git-stats-importer
