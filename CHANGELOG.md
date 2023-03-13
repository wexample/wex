# Changelog

## [Unreleased](https://github.com/wexample/wex/tree/HEAD)

[Full Changelog](https://github.com/wexample/wex/compare/3.5...HEAD)

**Implemented enhancements:**

- Improve install on Docker Toolbox [\#2](https://github.com/wexample/wex/issues/2)

**Fixed bugs:**

- Shared folders froms windows machine contains \r [\#4](https://github.com/wexample/wex/issues/4)
-  ./tmp/mysql.cnf: Permission denied  [\#3](https://github.com/wexample/wex/issues/3)

**Closed issues:**

- Tail on app/logs [\#66](https://github.com/wexample/wex/issues/66)
- App owner [\#65](https://github.com/wexample/wex/issues/65)
- Dynamic port assignation [\#64](https://github.com/wexample/wex/issues/64)
- Split building a composing [\#61](https://github.com/wexample/wex/issues/61)
- Create build rules and checkup [\#60](https://github.com/wexample/wex/issues/60)
- Restrict proxy companion in prod / local [\#59](https://github.com/wexample/wex/issues/59)
- Inherit services on install [\#58](https://github.com/wexample/wex/issues/58)
- Use Ansible docker container for core [\#57](https://github.com/wexample/wex/issues/57)
- Install addons [\#56](https://github.com/wexample/wex/issues/56)
- Support docker profiles [\#55](https://github.com/wexample/wex/issues/55)
- Check phpMyAdmin install [\#53](https://github.com/wexample/wex/issues/53)
- Log executed methods when testing [\#52](https://github.com/wexample/wex/issues/52)
- Unit test for service init [\#51](https://github.com/wexample/wex/issues/51)
- Sudo should be asked at startup [\#50](https://github.com/wexample/wex/issues/50)
- Improve autocomplete [\#49](https://github.com/wexample/wex/issues/49)
- Create a wex core/checkup  [\#48](https://github.com/wexample/wex/issues/48)
- nginx/proxy : big logs [\#42](https://github.com/wexample/wex/issues/42)
- \(wishlist\) Apache: add a volume to allow customization of number of process [\#41](https://github.com/wexample/wex/issues/41)
- Check if port 80 is used [\#40](https://github.com/wexample/wex/issues/40)
- Nice warn when not in projet [\#39](https://github.com/wexample/wex/issues/39)
- Migrating wex cert/generate [\#33](https://github.com/wexample/wex/issues/33)
- Improve requirements display [\#32](https://github.com/wexample/wex/issues/32)
- PHP My Admin does not start [\#31](https://github.com/wexample/wex/issues/31)
- Use iproute2 instead of ifconfig [\#30](https://github.com/wexample/wex/issues/30)
- Automate site first install and updates [\#25](https://github.com/wexample/wex/issues/25)
- Adding a branded grub initialization [\#18](https://github.com/wexample/wex/issues/18)
- Install on Docker Toolbox [\#10](https://github.com/wexample/wex/issues/10)

**Merged pull requests:**

- Update README.md [\#47](https://github.com/wexample/wex/pull/47) ([remiFaucon](https://github.com/remiFaucon))

## [3.5](https://github.com/wexample/wex/tree/3.5) (2022-12-11)

[Full Changelog](https://github.com/wexample/wex/compare/3.1...3.5)

**Implemented enhancements:**

- Manage updating [\#7](https://github.com/wexample/wex/issues/7)
- Rename ci site folder to hooks [\#6](https://github.com/wexample/wex/issues/6)

**Fixed bugs:**

- Cannot initialize a project [\#21](https://github.com/wexample/wex/issues/21)
- db/dump / restore zip support [\#5](https://github.com/wexample/wex/issues/5)

**Closed issues:**

- Two untranslated alerts on wrong credentials [\#34](https://github.com/wexample/wex/issues/34)
- Allow wex reverse proxy to work on a different port than 80 [\#24](https://github.com/wexample/wex/issues/24)
- Remove old PHP version in php base Docker image [\#23](https://github.com/wexample/wex/issues/23)
- Missing ifconfig [\#17](https://github.com/wexample/wex/issues/17)
- Install on OSX [\#15](https://github.com/wexample/wex/issues/15)
- Wex releases process is broken [\#14](https://github.com/wexample/wex/issues/14)
- Bad counter [\#11](https://github.com/wexample/wex/issues/11)
- Cannot start site - Undefined network tmp\_wex\_net [\#9](https://github.com/wexample/wex/issues/9)
- Bug - Tag problem [\#8](https://github.com/wexample/wex/issues/8)

**Merged pull requests:**

- Release/3.3 [\#35](https://github.com/wexample/wex/pull/35) ([weeger](https://github.com/weeger))
- Laravel5/install: remove composer update [\#29](https://github.com/wexample/wex/pull/29) ([xlii-chl](https://github.com/xlii-chl))
- Check ifconfig availability [\#28](https://github.com/wexample/wex/pull/28) ([xlii-chl](https://github.com/xlii-chl))

## [3.1](https://github.com/wexample/wex/tree/3.1) (2019-09-05)

[Full Changelog](https://github.com/wexample/wex/compare/test_site_name_internal...3.1)

**Implemented enhancements:**

- Autocomplete namespaces / groups / function [\#12](https://github.com/wexample/wex/issues/12)
- SSH Connection issue [\#1](https://github.com/wexample/wex/issues/1)

## [test_site_name_internal](https://github.com/wexample/wex/tree/test_site_name_internal) (2019-07-28)

[Full Changelog](https://github.com/wexample/wex/compare/2.2019.942...test_site_name_internal)

**Merged pull requests:**

- Avoid error message if /var/www folder exists on Wex install [\#22](https://github.com/wexample/wex/pull/22) ([LucileDT](https://github.com/LucileDT))
- Help improvement [\#20](https://github.com/wexample/wex/pull/20) ([weeger](https://github.com/weeger))
- Ssh conversions [\#19](https://github.com/wexample/wex/pull/19) ([weeger](https://github.com/weeger))
- Watcher hang on /var/www/html being absent [\#16](https://github.com/wexample/wex/pull/16) ([xlii-chl](https://github.com/xlii-chl))

## [2.2019.942](https://github.com/wexample/wex/tree/2.2019.942) (2019-02-27)

[Full Changelog](https://github.com/wexample/wex/compare/2.2018.1011...2.2019.942)

**Closed issues:**

- Container watcher does not start [\#13](https://github.com/wexample/wex/issues/13)

## [2.2018.1011](https://github.com/wexample/wex/tree/2.2018.1011) (2018-05-23)

[Full Changelog](https://github.com/wexample/wex/compare/2.2018.1007...2.2018.1011)

## [2.2018.1007](https://github.com/wexample/wex/tree/2.2018.1007) (2018-05-23)

[Full Changelog](https://github.com/wexample/wex/compare/2018.2.772...2.2018.1007)

## [2018.2.772](https://github.com/wexample/wex/tree/2018.2.772) (2018-05-03)

[Full Changelog](https://github.com/wexample/wex/compare/2018.2.710...2018.2.772)

## [2018.2.710](https://github.com/wexample/wex/tree/2018.2.710) (2018-04-16)

[Full Changelog](https://github.com/wexample/wex/compare/2018.2.709...2018.2.710)

## [2018.2.709](https://github.com/wexample/wex/tree/2018.2.709) (2018-04-16)

[Full Changelog](https://github.com/wexample/wex/compare/2018.2.707...2018.2.709)

## [2018.2.707](https://github.com/wexample/wex/tree/2018.2.707) (2018-04-16)

[Full Changelog](https://github.com/wexample/wex/compare/latest...2018.2.707)

## [latest](https://github.com/wexample/wex/tree/latest) (2018-04-16)

[Full Changelog](https://github.com/wexample/wex/compare/2018.2.686...latest)

## [2018.2.686](https://github.com/wexample/wex/tree/2018.2.686) (2018-04-16)

[Full Changelog](https://github.com/wexample/wex/compare/2018.2.667...2018.2.686)

## [2018.2.667](https://github.com/wexample/wex/tree/2018.2.667) (2018-04-12)

[Full Changelog](https://github.com/wexample/wex/compare/2018.2.656...2018.2.667)

## [2018.2.656](https://github.com/wexample/wex/tree/2018.2.656) (2018-04-12)

[Full Changelog](https://github.com/wexample/wex/compare/2018.2.652...2018.2.656)

## [2018.2.652](https://github.com/wexample/wex/tree/2018.2.652) (2018-04-12)

[Full Changelog](https://github.com/wexample/wex/compare/2018.2.651...2018.2.652)

## [2018.2.651](https://github.com/wexample/wex/tree/2018.2.651) (2018-04-11)

[Full Changelog](https://github.com/wexample/wex/compare/2018.2.650...2018.2.651)

## [2018.2.650](https://github.com/wexample/wex/tree/2018.2.650) (2018-04-11)

[Full Changelog](https://github.com/wexample/wex/compare/2018.2.649...2018.2.650)

## [2018.2.649](https://github.com/wexample/wex/tree/2018.2.649) (2018-04-11)

[Full Changelog](https://github.com/wexample/wex/compare/2018.2.645...2018.2.649)

## [2018.2.645](https://github.com/wexample/wex/tree/2018.2.645) (2018-04-11)

[Full Changelog](https://github.com/wexample/wex/compare/2018.2.643...2018.2.645)

## [2018.2.643](https://github.com/wexample/wex/tree/2018.2.643) (2018-04-11)

[Full Changelog](https://github.com/wexample/wex/compare/2018.2.644...2018.2.643)

## [2018.2.644](https://github.com/wexample/wex/tree/2018.2.644) (2018-04-11)

[Full Changelog](https://github.com/wexample/wex/compare/2018.2.639...2018.2.644)

## [2018.2.639](https://github.com/wexample/wex/tree/2018.2.639) (2018-04-11)

[Full Changelog](https://github.com/wexample/wex/compare/2018.2.636...2018.2.639)

## [2018.2.636](https://github.com/wexample/wex/tree/2018.2.636) (2018-04-11)

[Full Changelog](https://github.com/wexample/wex/compare/2018.2.635...2018.2.636)

## [2018.2.635](https://github.com/wexample/wex/tree/2018.2.635) (2018-04-11)

[Full Changelog](https://github.com/wexample/wex/compare/2018.2.634...2018.2.635)

## [2018.2.634](https://github.com/wexample/wex/tree/2018.2.634) (2018-04-11)

[Full Changelog](https://github.com/wexample/wex/compare/2.0.0...2018.2.634)

## [2.0.0](https://github.com/wexample/wex/tree/2.0.0) (2018-04-11)

[Full Changelog](https://github.com/wexample/wex/compare/2018.2.633...2.0.0)

## [2018.2.633](https://github.com/wexample/wex/tree/2018.2.633) (2018-04-11)

[Full Changelog](https://github.com/wexample/wex/compare/e32b113188ca59c0d73decbe1eda339c3adfbfc9...2018.2.633)



\* *This Changelog was automatically generated by [github_changelog_generator](https://github.com/github-changelog-generator/github-changelog-generator)*
