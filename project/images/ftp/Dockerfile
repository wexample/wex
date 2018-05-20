FROM stilliard/pure-ftpd:hardened-1.0.36

# startup
CMD /run.sh -c 5 -C 5 -l puredb:/etc/pure-ftpd/pureftpd.pdb -E -j -R -P $PUBLICHOST -p 30000:30009 -s -A -j -Z -H -4 -E -R -G -X -x