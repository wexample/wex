# To do

You are reading this file because you want to check, update or add task to do in the migration process.

- [x] Add coding style documentation
- [x] Explore actual kernel development status on v6
- [x] Implement basic command resolver
- [x] Check the command detection system works as expected
- [ ] Fix the command execution system
- [ ] Implement addon resolver:
  - [ ] Create AddonCommandResolver class
  - [ ] Implement command format parsing (addon::group/command)
  - [ ] Add addon directory registration system
  - [ ] Implement Python file path resolution
  - [ ] Add method name conversion (path to Python method)
  - [ ] Test with default::info/show command
- [ ] Test complete command execution flow:
  - [ ] Verify Python script location resolution
  - [ ] Test internal module execution
  - [ ] Implement proper response handling