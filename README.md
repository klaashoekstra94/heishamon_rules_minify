# HeishaMon Rules Minify
> A Python CLI to minify Heishamon rules

[HeishaMon](https://github.com/Egyras/HeishaMon) is a project to read out a Panasonic air-water heat pump using an ESP8266 board. The HeishaMon firmware also supports the use of rules, to control the heatpump from within the HeishaMon itself. Since the ruleset must be stored within HeishaMon, its size must be limited. Therefore, it is best to use short function and variable names in order to maximize the number of rules that can be stored. Moreover, the rules library does not support comments in a ruleset, making it hard to read and maintain a ruleset, but also making it hard to share the ruleset with other. 

This project aims to overcome these issues by making it possible write a ruleset with comments and descriptive function and variables names, and then minifying it. This way it is still possible to maximize the number of rules on the HeishaMon.

_Note: The minifier should work for both the rule library used in version 3.2.3 and [this updated rule libaray version](https://github.com/IgorYbema/HeishaMon/pull/121). In the rule library from version 3.2.3, the elseif statement cannot be used_

## Installation

```sh
python3 -m pip install heishamon_rules_minify
```

## Usage example

Start by creating a ruleset that adheres to the HeishaMon rules syntax, but can use the following extras:

- Single line comments starting with `--` or block comments between `--[[` and `]]`.
- Custom function and variable names will be minified to only keep the first letter (which will be capitalised) and capital letters, so for example `#WaterTemperature` will become `#WT`, `#allowDHW` will become `#ADHW`.

When the ruleset is finished, minify it using the following command:

```sh
heishamon-rules-minify [input_file] [output_file]
```

This will shorten all custom function and variable names and remove all unneeded spaces and newlines.

### Extra options
There are a couple of extra options to pass with the minifier:
* `--print` or `-p` to also print the output on the command line.
* `--comments_only` or `-c` to only remove the comments from the input file but do no further minifying.

## Release History

* [0.0.1](https://github.com/klaashoekstra94/heishamon_rules_minify/releases/tag/v0.0.1)
    * Initial version
* [0.0.2](https://github.com/klaashoekstra94/heishamon_rules_minify/releases/tag/v0.0.2)
    * Fix incorrect spacing for double operators, minor bugfixes
* [0.0.3](https://github.com/klaashoekstra94/heishamon_rules_minify/releases/tag/v0.0.3)
    * Add option to only remove comments
* [0.0.4](https://github.com/klaashoekstra94/heishamon_rules_minify/releases/tag/v0.0.4)
    * Fix extra space being added after the minus sign of negative values

## Contributing

1. Fork it (<https://github.com/yourname/yourproject/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
