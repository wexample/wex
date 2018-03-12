

               local                     prod
               mysql                     mysql
              |  ^  ^                   ^  |  ^
              |  |  |                   |  |  |
        dump  |  |  |                   |  |  |
     restore  |  |  |                   |  |  |
              v  |  +------- sync ------+  v  |
             /dumps -------- push -------> /dumps
                    <------- pull --------


Examples :

# Create a dump in production then pull it locally
wex db/dump -e=prod -p

