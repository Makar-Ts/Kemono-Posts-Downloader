# Kemono Post Downloader

## Overview

This project is a Python script designed to download posts from a user on the [Kemono](https://kemono.su) platform. The script retrieves the user's posts and saves them as JSON files, along with any attached media. It supports downloading through a Tor proxy for enhanced privacy.

## Features

- Download all posts from a specified Kemono user.
- Save posts as JSON files, including all relevant metadata.
- Download attached files to a specified output directory.
- Optional use of a Tor proxy for anonymity or bypassing restrictions.
- Progress feedback during file downloads.

## Requirements

- Python 3.x
- `requests` library (install via `pip install requests`)
- `requests[socks]` library (install via `pip install requests[socks]`)
- (Optional) Tor installed on your machine if you wish to use the Tor proxy feature.

## Usage

To use the script, run it from the command line with the required arguments:

```bash
python kemono_downloader.py <type> <user_id> <output_directory> [-bs <block_size>] [-sf <start_from>] [-ut <use_tor>]
```

### Parameters

- `<type>`: The service type ("patreon", "boosty" etc.).
- `<user_id>`: The numerical ID of the user you wish to download posts from.
- `<output_directory>`: The directory where the downloaded files will be stored.
- `-bs`, `--block_size`: (Optional) Specify the block size for downloading (default is 4096 bytes).
- `-sf`, `--start_from`: (Optional) Specify the index to start downloading from (default is 0).
- `-ut`, `--use_tor`: (Optional) Enable downloading through Tor.

### Example

```bash
python kemono_downloader.py user 12345 ./downloads -bs 8192 -ut
```

This command will download posts from the user with ID `12345` and save them to the `./downloads` directory using a block size of 8192 bytes and Tor proxy.

## Notes

- Ensure that the output directory exists or the script will create it.
- The script includes error handling for failed requests from the Kemono API.
- Progress is shown for each file as it downloads to keep users informed of the download status.

## Contributing

If you'd like to contribute to this project, feel free to submit a pull request or open an issue for any bugs or feature requests.

## License

This project is open-source and available under the MIT License. Please see the LICENSE file for more details.

## Acknowledgments

Special thanks to the creators of the Kemono platform for providing the API that makes this project possible. 