# Audit appels git

## ✅ Fait

- `repo.py` déplacé `helpers` → `helpers-git`, migré vers `git_run()`
- `git_commit_all_with_message()` : `shell_run(["git", "add/commit"])` → `git_run()`
- `merge_to_main()` : deux `shell_run(["git", "merge"])` → `self.git_run()`
- Grep exhaustif `shell_run.*"git"` → seul résultat : `git_run()` elle-même ✅

## ⬜ Reste (bloqué sur ssh-auth-unified)

- Supprimer `_git_resolve_ssh_env()` de `git.py:362-386` une fois `SshAgentResolver` en place
- Retirer son appel dans `git_run()`, remplacer par `SshAgentResolver`
