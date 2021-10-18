# Code Climate Cppcheck Addons Engine

`codeclimate-cppcheck-addons` is a Code Climate engine that wraps [Cppcheck][cppcheck].
You can run it on your command line using the Code Climate CLI, or on our
hosted analysis platform.

[Cppcheck][cppcheck] is a static analysis tool for C/C++ code.

## Installation

1. If you haven't already, [install the Code Climate CLI][codeclimate-cli].
2. Pull the [`codeclimate-cppcheck-addons`][cppcheck-addons-image] image.
3. Retag the image as `codeclimate/codeclimate-cppcheck-addons:latest`.
5. Configure your `.codeclimate.yml` file. See example below.
6. You're ready to analyze! Browse into your project's folder and run
   `CODECLIMATE_DEV=1 codeclimate analyze`.
   1. Note that `read` / `write` permissions may need to be granted to
      other users in the code directory to allow CodeClimate to write
      new files. CodeClimate is configured to use `9000:9000` for the
      engine user permissions.

## Configuration

Like the `cppcheck` command line tool itself, you can configure various
aspects of the static analysis. Right now, the following options are supported
in `.codeclimate.yml`:

* `addons`: addons to include.
  By default, no addons are enabled.
  Refer to the `--addon` option of `cppcheck` for more information.
* `misra_blockers`: MISRA rules to mark as `blocker` if violated.
  By default, rules use `cppcheck` defaults.
  Use to highlight rules that _must_ not be violated.
* `check`: issue categories to check.
  By default, no additional checks are enabled.
  Available values are: `all`, `warning`, `style`, `performance`, `portability`,
  `information`, `unusedFunction`, etc.
  Refer to the `--enable=` option of `cppcheck` for more information.
* `project`: use Visual Studio project/solution (`*.vcxproj`/`*sln`) or compile
  database (`compile_commands.json`) for files to analyse, include paths,
  defines, platform and undefines.
  Refer to the `--project=` option of `cppcheck` for more information.
* `language`: forces `cppcheck` to check all files as the given language.
  Valid values are: `c`, `c++`.
  Refer to the `--language=` option of `cppcheck` for more information.
* `stds`: multiple language standards to check against.
  Refer to the `--std=` option of `cppcheck` for more information.
* `platform`: specifies platform specific types and sizes. Available builtin
  platforms are: `unix32`, `unix64`, `win32A`, `win32W`, `win64`, etc.
  Refer to the `--platform=` option of `cppcheck` for more information.
* `defines`: define preprocessor symbols.
  Refer to the `-D` option of `cppcheck` for more information.
* `undefines`: undefine preprocessor symbols.
  Refer to the `-U` option of `cppcheck` for more information.
* `includes`: paths for searching include files. First given path is searched
  for contained header files first. If paths are relative to source files,
  this is not needed.
  Refer to the `-I` option of `cppcheck` for more information.
* `max_configs`: maximum number of configurations to check in a file before
  skipping it. Default is 12. `max_configs` can also be set to `force`, which
  forces `cppcheck` to check all configs.
  Refer to the `--max-configs=` and `--force` options of `cppcheck` for more
  information.
* `inconclusive`: allow reporting issues that are not inconclusive.
  Refer to the `--inconclusive` option of `cppcheck` for more information.
* `suppressions-list`: suppress warnings listed in the file.
  Refer to the `--suppressions-list` option of `cppcheck` for more information.
* `suppressions-xml`: suppress warnings listed in XML file.
  Refer to the `--suppressions-xml` option of `cppcheck` for more information.
* `inline-suppr`: allow suppression of warnings with inline comments,
  for example: `// cppcheck-suppress arrayIndexOutOfBounds`.
  Refer to the `--inline-suppr` option of `cppcheck` for more information

Additional options may be supported later.

An example `.codeclimate.yml` file:

```yaml
version: "2"
plugins:
  cppcheck-addons:
    enabled: true
    config:
      check: all
      project: compile_commands.json
      language: c
      stds:
        - c89
      platform: mips32
      addons:
        - misra.json
      misra_blockers:
        - misra-c2012-17.2
      defines:
        - "DEBUG=1"
      undefines:
        - "DEBUG"
      includes:
        - include/
      max_configs: 42
      inconclusive: false
      suppressions-list: .cppcheck-suppressions
      suppressions-xml: .cppcheck-suppressions.xml
      inline-suppr: true
```

## Need help?

For help with [Cppcheck][cppcheck], check out their documentation.

If you're running into a Code Climate issue, first look over this project's
GitHub Issues, as your question may have already been covered.

[cppcheck]: http://cppcheck.sourceforge.net/
[codeclimate-cli]: https://github.com/lizalc/codeclimate
[cppcheck-addons-image]: https://github.com/lizalc/codeclimate-cppcheck-addons/pkgs/container/codeclimate%2Fcodeclimate-cppcheck-addons
