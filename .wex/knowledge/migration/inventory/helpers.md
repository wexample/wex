# Helpers

## v5 reference

`wex-5/src/helper/`

## Modules

### command.py
- [ ] `execute_command_sync` / `execute_command_async`
- [ ] `execute_command_tree_sync` — nested command execution
- [ ] `internal_command_to_shell`
- [ ] `command_exists`, `command_escape`, `command_to_string`, `is_same_command`
- [ ] `apply_command_decorator`

### string.py
- [ ] `string_to_camel_case`, `string_to_pascal_case`
- [ ] `string_format_ignore_missing`
- [ ] `string_truncate`, `string_multiline_center`, `string_trim_leading`
- [ ] `string_count_lines_needed`, `string_replace_multiple`
- [ ] `string_random_password_secure`, `string_random_password`
- [ ] `string_has_trailing_new_line`, `string_add_lines_numbers`
- [ ] `string_list_calculate_max_widths`

### file.py
- [ ] `file_create_parent_dir`
- [ ] `file_remove_file_if_exists`
- [ ] File listing, reading, writing utilities

### service.py
- [ ] `service_get_dir`, `service_load_config`
- [ ] `service_get_inheritance_tree`
- [ ] `service_copy_sample_dir`, `service_get_all_dirs`

### routing.py
- [ ] `routing_get_route_name`, `routing_get_route_info`
- [ ] `routing_is_allowed_route`
- [ ] `routing_build_webhook_route_map`

### prompt.py
- [ ] `prompt_build_progress_bar`, `prompt_progress_steps`
- [ ] `prompt_choice`, `prompt_choice_dict`
- [ ] `prompt_pick_a_file`, `prompt_pick_a_dir`

### user.py
- [ ] `get_sudo_username`, `get_user_or_sudo_user`
- [ ] `get_uid_from_user_name`, `get_gid_from_group_name`
- [ ] `get_user_group_name`, `get_sudo_gid`, `get_sudo_group`
- [ ] `get_user_or_sudo_user_home_data_path`
- [ ] `set_owner_recursively`, `set_permissions_recursively`
- [ ] `is_current_user_sudo`, `user_exists`

### Other modules
- [ ] `core.py` — `core_kernel_get_version`, `core_dir_get_version`
- [ ] `registry.py` — `registry_get_all_commands_from_registry_part`
- [ ] `test.py` — test class/method naming, `create_test_from_command`
- [ ] `module.py` — `module_load_from_file` (dynamic module loading)
- [ ] `package.py` — `package_enable_logging`
- [ ] `patch.py` — file patching operations
- [ ] `process.py` — process management

## v6 target

- Generic helpers → `PACKAGES/PYTHON/packages/helpers`
- Prompt helpers → `PACKAGES/PYTHON/packages/prompt`
- File helpers → `PACKAGES/PYTHON/packages/file`
- Wex-specific helpers → `wex-core`
