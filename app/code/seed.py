import sys
import time
from sqlite3 import Error
import requests
from db import GithubDatabase


def get_user_data_from_github(total=150):
    """
        Connects to the GitHub API to extract user information.
        Params:
            - total. Number of users to retrieve. Default: 150
        Returns:
            - Dict structure with user information on a list:
            [{
                "login": username,
                "id": id,
                "avatar_url": image_url,
                "type": type,
                "url": github_url
            },
            {...}]
    """
    github_url = 'https://api.github.com/users'
    # Determine how many pages need to be requested and the remainder elements
    # to the extracted from the last page. Max. of elements from page: 100
    per_page_param = "?per_page=100"
    remainder = 0
    since_param = ''
    # Determine the number of pages to iterate and the number of remainder
    # results, in case there is.
    if total < 100:
        pages = 1
        per_page_param = "?per_page=" + str(total)
    elif total % 100 == 0:
        pages = total // 100
    else:
        pages = (total // 100) + 1
        remainder = total % 100
    # Start sending requests to GitHub
    if pages == 1:  # Only need to send a request once
        resp = requests.get(github_url + per_page_param)
        users_data = resp.json()
        return users_data
    else:
        users_data = []
        for i in range(pages):
            resp = requests.get(github_url + per_page_param + since_param)
            users_data = users_data + resp.json()
            if len(users_data) == total:
                return users_data
            else:
                # Obtain link for next page of results
                header_link = resp.headers["Link"]
                start_index = header_link.find("since=") + 6
                end_index = header_link.find(">")
                since_param = "&since=" + header_link[start_index:end_index]
                if i+2 == pages and remainder != 0:
                    per_page_param = "?per_page=" + str(remainder)


def convert_user_data(users_data):
    """
        Converts user_data structure to the corresponding format to be used
        when inserting to database.
        Params:
            - List of dictionary with all the data from the extracted users
        Returns:
            - users_rows. List of tuples with the values to be inserted on the
            database. E.g.: ('login', 'id', 'avatar_url', 'type', 'url')
    """
    users_rows = []
    for user_data in users_data:
        user_row = (
            user_data["login"],
            user_data["id"],
            user_data["avatar_url"],
            user_data["type"],
            user_data["html_url"]
        )
        users_rows.append(user_row)
    return users_rows


# Database function
def process_user_data_to_db(users_rows, db=None):
    """
        Inserts data extracted to SQLite database.
        Params:
            - users_data. List with dict structure to be inserted to the db
        Returns:
            - inserted_rows. String with the number of rows inserted.
    """
    try:
        gdb = GithubDatabase(db)
        gdb.create_table()
        inserted_rows = gdb.insert_many(users_rows)
        gdb.close()
    except Error as e:
        print("An error has ocurred:", e)
        gdb.close()
    return inserted_rows


def main():
    print("Getting users data from GitHub...")
    if len(sys.argv) > 1:
        total = int(sys.argv[1])
        users_data = get_user_data_from_github(total)
    else:
        users_data = get_user_data_from_github()
    time.sleep(1)
    print("Done! A total of {} users was extracted.".format(len(users_data)))
    print("Converting data...")
    time.sleep(1)
    users_rows = convert_user_data(users_data)
    print("Done. Inserting data...")
    time.sleep(1)
    inserted_rows = process_user_data_to_db(users_rows)
    print("Done!")
    if inserted_rows:
        print(
            "A total of {} rows where updated in the database."
            .format(inserted_rows)
        )
    else:
        print("No rows where inserted into the database.")


if __name__ == "__main__":
    main()
