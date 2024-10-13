# pylint: disable=line-too-long, invalid-name, import-error, multiple-imports, unspecified-encoding, broad-exception-caught, trailing-whitespace, no-name-in-module, unused-import


from math import floor, ceil

import argparse
import sys
import os
import json
import requests



# ---------------------------------------------------------------------------- #
#                               Arguments Parcing                              #
# ---------------------------------------------------------------------------- #


parser = argparse.ArgumentParser(description='Download all posts from kemono user')
parser.add_argument(
    'type', 
    type=str,
    help='Service type'
)
parser.add_argument(
    'id', 
    type=int,
    help='User ID'
)
parser.add_argument(
    'outdir',
    type=str,
    help='Output directory'
)
parser.add_argument(
    '-bs', '--block_size',
    type=int,
    default=4096,
    help="Block size"
)
parser.add_argument(
    '-sf', '--start_from',
    type=int,
    default=0,
    help="Start from post index"
)
parser.add_argument(
    '-ut', '--use_tor',
    action=argparse.BooleanOptionalAction,
    help='Download posts through TOR proxy'
)
args = parser.parse_args()



SIZE_DIVIDER = 1024 # bits to Kbytes
BLOCK_SIZE = args.block_size

TYPE = args.type
USER_ID = args.id



# ---------------------------------------------------------------------------- #
#                                   Functions                                  #
# ---------------------------------------------------------------------------- #


# ------------------------------ Tor Connection ------------------------------ #

def get_tor_session(): # set connection through TOR
    session = requests.session()
    # Tor uses the 9050 port as the default socks port
    session.proxies = { 'http':  'socks5://127.0.0.1:9150',
                        'https': 'socks5://127.0.0.1:9150'}
    return session


# ------------------------------ File Downloader ----------------------------- #

def download_file(url, path, session=requests.session()):
    response = session.get(url, stream=True)

    # Sizes in bytes.
    total_size = int(response.headers.get("content-length", 0))
    
    downloaded_size = 0

    with open(path, "wb") as file:
        
        
        
        # ---------------------------------------------------------------------------- #
        #                                 Download Data                                #
        # ---------------------------------------------------------------------------- #
        
        
        for data in response.iter_content(BLOCK_SIZE):
            #progress_bar.update(len(data))
            downloaded_size += len(data)
            
            
            # ------------------------------- Progress Bar ------------------------------- #

            percent = downloaded_size/total_size
            downloaded_blocks = floor(percent*20)
            
            print(f"""[{  downloaded_blocks*"█"}{
                        "▌" if percent*20-downloaded_blocks > 0.5 else " "}{
                        (20-downloaded_blocks)*" "}] {  round(downloaded_size/SIZE_DIVIDER, 3)}KB/{
                                                        round(total_size/SIZE_DIVIDER, 3)}KB""", end="\r")
            
            sys.stdout.flush()
            
            
            # -------------------------------- Write Data -------------------------------- #
            
            file.write(data)
    
    
    
    # ---------------------------------------------------------------------------- #
    #                                    Finish                                    #
    # ---------------------------------------------------------------------------- #
    
    
    if total_size!= 0 and downloaded_size!= total_size: # if file is empty
        raise RuntimeError("Could not download file")
    
    print("\nDownload completed successfully.")


#download_file("https://download.samplelib.com/png/sample-boat-400x300.png", "./output.png")



# ---------------------------------------------------------------------------- #
#                                   Get Posts                                  #
# ---------------------------------------------------------------------------- #


# -------------------------------- Tor Session ------------------------------- #

if args.use_tor:  
    session = get_tor_session()
else:
    session = requests.session()


# ------------------------------- First Request ------------------------------ #
# where tf my DO WHILE LOOP

all_data = []

data = session.get(f"https://kemono.su/api/v1/{TYPE}/user/{USER_ID}", timeout=30)
if data.status_code != 200:
    print(f"Failed to fetch data from kemono.su with status code: {data.status_code}")
    sys.exit(1)

data = data.json()
all_data += data


# ------------------------------- Request Loop ------------------------------- #
# u can only get 50 messages per request

request_count = 1
while len(data) == 50:
    
    
    # ---------------------------------- Request --------------------------------- #
    
    data = session.get(f"https://kemono.su/api/v1/{TYPE}/user/{USER_ID}?o={request_count*50}", timeout=30)
    if data.status_code != 200:
        print(f"\nFailed to fetch data from kemono.su with status code: {data.status_code}")
        sys.exit(1)

    
    # --------------------------------- Save Data -------------------------------- #
    
    print(f"Request number {request_count} success, total posts count {(request_count+1)*50}", end="\r")
    sys.stdout.flush()
    
    data = data.json()
    request_count += 1
    
    all_data += data

total_posts = len(all_data)
print(f"\nTotal posts count: {total_posts}")



# ---------------------------------------------------------------------------- #
#                          Write Data & Download Pics                          #
# ---------------------------------------------------------------------------- #

# make sure we have output dir
os.makedirs(os.path.join(sys.path[0], args.outdir), exist_ok=True)

for i, post in enumerate(all_data[args.start_from:]):
    
    
    # --------------------------------- Filename --------------------------------- #
    
    filename = post["published"].split("T")[0] + " " + post["published"].split("T")[1].replace(":", "-")
    # convert 2024-06-05T02:17:33 to 2024-06-05 02-17-33
    filename += " " + post["title"]
    
    print(f"\nPost {args.start_from+i}/{total_posts}\n{filename}:")
    
    # remove all unsupported signs
    filename = filename.replace(":", "") \
                        .replace("?", "") \
                        .replace("/", "") \
                        .replace(">", "") \
                        .replace("<", "") 
    
    
    # ------------------------------ Write JSON Data ----------------------------- #
    
    with open(os.path.join(sys.path[0], args.outdir, filename+".json"), "w") as f:
        json.dump(
            post, 
            f, 
            indent=4
        )
    
    
    # ------------------------------- Download Pics ------------------------------ #
    
    if len(post["attachments"]) == 0:
        print("No attachments")
        continue
    
    for j, file in enumerate(post["attachments"]):
        print(filename, file["name"])
        
        download_file(
            "https://kemono.su"+file["path"], 
            os.path.join(
                sys.path[0], 
                args.outdir, 
                filename+file["name"]
            ), 
            session
        )