#!/usr/bin/env bash

# Gitinspector
python /var/www/gitinspector/gitinspector.py --format=html /var/www/project/ > /var/www/reports/gitinspector.html

# Git stats
cd /var/www/project && git_stats && mv git_stats /var/www/reports/git_stats

# Git-stats (manual usage only)
# cd /var/www/project
# Import by email : git-stats-importer -e mail@domain.com
# Show table : git-stats
# Or : git-stats --authors
