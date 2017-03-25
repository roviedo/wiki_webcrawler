import pprint
import ssl
import sys
import urllib.request #need to import request this way http://stackoverflow.com/questions/37042152/python-3-5-1-urllib-has-no-attribute-request

import bs4

# SSL Certificate set to none. Don't want to do in production environment
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

#GLOBALS
DOMAIN = 'https://en.wikipedia.org'
RANDOM_PAGE_PATH = '/wiki/Special:Random'
ENTRY_PATH = '/wiki/Main_Page'

def spider(pages_amount=10):
    url = "{}{}".format(DOMAIN, ENTRY_PATH)
    cache_pages_dict = {}

    soup = get_soup(url, cache_pages_dict)

    random_page_link = get_random_page_link(soup)
    path_length_distribution = {}

    pages_amount_to_iterate_over = pages_amount
    while pages_amount_to_iterate_over > 0:
        path = 0 # Reset the path on every itertion
        random_page_soup = get_soup(random_page_link, cache_pages_dict)
        subject_count_dict = {}

        path = first_link_in_main_body(
            random_page_soup,
            subject_count_dict,
            path,
            cache_pages_dict
        )

        update_path_length_distribution(path_length_distribution, path)

        pages_amount_to_iterate_over -= 1

    (pages_that_lead_to_phi, average, path_length_distribution) = \
             output_metrics(path_length_distribution, pages_amount)

    output_metrics_to_file(pages_amount, pages_that_lead_to_phi, average,
                                                path_length_distribution)


def output_metrics(path_length_distribution, pages_amount):
    pages_that_lead_to_phi = pages_amount - path_length_distribution.get('None', 0)
    total_paths = 0
    average = 0
    for k, v in path_length_distribution.items():
        if k == 'None':
            continue
        else:
            total_paths += (int(k) * v)

    if pages_that_lead_to_phi > 0: #in case no pages led to Philosophy
        average = total_paths/pages_that_lead_to_phi

    return pages_that_lead_to_phi, average, path_length_distribution


def output_metrics_to_file(pages_amount, pages_that_lead_to_phi, average,
                                               path_length_distribution):
    with open('results.txt', 'a') as outfile: #use a to append to file
        outfile.write(
            "{} pages\n" \
            "Pages that lead to Philosophy: {}\n" \
            "Avg path length: {}\n" \
            "Path Length Distribution: {}\n".format(
                pages_amount,
                pages_that_lead_to_phi,
                average,
                path_length_distribution
            )
        )
    print("Pages that lead to Philosophy: {}\nAvg: {}\nPath Length Distribution:" \
        "{}".format(pages_that_lead_to_phi, average, path_length_distribution))


def update_path_length_distribution(path_length_distribution, path):
    """Updates the path length distribution, if the path length doesn't
    exist, it is added to distribution otherwise the count is incremented
    for the existing one.
    """
    if path_length_distribution.get(str(path)):
        path_length_distribution[str(path)] += 1
    else:
        path_length_distribution[str(path)] = 1


def first_link_in_main_body(random_page_soup, subject_count_dict, path,
                                                     cache_pages_dict):
    """This function takes a page, finds the main body, loops through the
    paragraphs and open the first href not inside a parenthesis and recursively
    does this for until a Philosophy page is reached.
    """
    # Then main content is inside id mw-content-text, then get al paragraphs
    # currently it is not continuing if wikipedia return some short articles that don't contain p
    main_content = random_page_soup.find(id="mw-content-text").find('p')
    if not main_content:
        return None

    parenthesis_stack = []
    for element in main_content:
        if isinstance(element, bs4.element.NavigableString):
            parenthesis_match(element.string, parenthesis_stack)

        if isinstance(element, bs4.element.Tag) and element.name == 'b':
            if not isinstance(element.contents[0], bs4.element.Tag) and "Philosophy" in element.contents[0]:
                print("Found Philosophy with path length of: {}".format(path))
                return path
            elif path > 30: # Setting this a threshold do to it going back and forth between two articles leading to infinite recursion.
                return None
            else:
                path += 1
        elif isinstance(element, bs4.element.Tag) and element.name == 'a' and not parenthesis_stack:
            soup = get_soup("{}{}".format(DOMAIN, element['href']), cache_pages_dict)
            # if soup was unsuccessful return path and follow up by collecting data for pages processed successfully
            if soup:
                return first_link_in_main_body(
                    soup,
                    subject_count_dict,
                    path,
                    cache_pages_dict
                )
            else:
                return path


def get_soup(url, cache_pages_dict):
    """Takes url parameter and returns the soup object
    """
    # Make sure we don't cache the random page
    if cache_pages_dict.get(url) and url != "{}{}".format(DOMAIN, RANDOM_PAGE_PATH):
        soup = cache_pages_dict[url]
    else:
        try:
            with urllib.request.urlopen(url, context=CTX, timeout=10) as response:
                html_doc = response.read()
                soup = bs4.BeautifulSoup(html_doc, 'html.parser')
                cache_pages_dict[url] = soup
        except:
            return None

    return soup


def get_random_page_link(soup):
    """Takes a soup object parameter and returns the random page link.
    """
    random_page_element = soup.find(id="n-randompage")
    for tag in random_page_element:
        # domain needed since tag['href'] is a relative path
         return "{}{}".format(DOMAIN, tag['href'])


def parenthesis_match(string, parenthesis_stack):
    """Adds open parenthesis to stack, once it gets a
    close parenthesis it pops
    """
    string = str(string) # need to convert NavigableString to str
    for char in string:
        if char == '(':
            parenthesis_stack.append(char)
        elif parenthesis_stack and char == ')':
            parenthesis_stack.pop()


def main():
    if len(sys.argv) > 1:
        try:
            spider(int(sys.argv[1]))
        except ValueError:
            print("Invalid argument, please try again")
    else:
        spider()


if __name__=="__main__":
    main()
