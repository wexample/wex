Dans `.wex/knowledge/usage/installation.md.j2`, ligne 3 :

    Install {{ package_naem }} globally.

La variable est `package_naem`, alors que le reste du fichier (ligne 10) utilise
`package_name`. C'est très probablement une coquille dans le nom de la variable,
mais c'est du code Jinja, pas de la prose : le renommer sort du périmètre d'une
passe orthographique et pourrait casser le rendu si `package_naem` est réellement
défini quelque part.

À faire : vérifier quelles variables sont passées au rendu de ce template. Si
`package_naem` n'existe pas, corriger en `package_name` (selon la config Jinja, un
nom inconnu rend une chaîne vide au lieu de lever une erreur — d'où le fait que la
coquille passe inaperçue).
