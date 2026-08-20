In `.wex/knowledge/usage/installation.md.j2`, line 3:

    Install {{ package_naem }} globally.

The variable is `package_naem`, whereas the rest of the file (line 10) uses
`package_name`. This is very probably a typo in the variable name, but it is Jinja
code, not prose: renaming it falls outside the scope of a spelling pass and could
break the rendering if `package_naem` really is defined somewhere.

To do: check which variables are passed to this template's rendering. If
`package_naem` does not exist, fix it to `package_name` (depending on the Jinja
config, an unknown name renders an empty string instead of raising an error — hence
the typo going unnoticed).
