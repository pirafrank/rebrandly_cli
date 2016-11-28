# Rebrandly CLI utility

This is an unofficial CLI utility for Rebrandly service.

## Requirements

- Python 2.7.x

## Configuration

1. Go to Rebrandly [dashboard API](https://www.rebrandly.com/api-settings) and create a new API token
2. Create a `config.json` in the same folder where the script lives and paste there the API token. You can also specify a custom json config file using the `-j` option.
3. Done!

## Usage

`python shorten.py [OPTIONS] [URL]`

## Options

- `-h` show help
- `-j` specify custom `config.json` file path
- `-l` list custom domains (they MUST be set in your Rebrandly account to work!)
- `-c` shorten URL using favorite custom domain set in `config.json`
- `-t` specify title. It will be shown in [Rebrandly dashboard](https://www.rebrandly.com/links)

### License

The software in this repository are released under the GNU GPLv3 License by Francesco Pira (dev[at]fpira[dot]com, fpira.com). You can read the terms of the license [here](http://www.gnu.org/licenses/gpl-3.0.html).
