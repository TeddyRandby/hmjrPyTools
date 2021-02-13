from python_graphql_client import GraphqlClient
import numpy as np

def splitIntoWords(str, badChars):
    return np.array(str.translate(str.maketrans( '', '', badChars)).split(" "))

def validateBook(book):
    strBook = str(book)
    while len(strBook) < 3:
        strBook = "0" + strBook
    return strBook

BAD_CHARS = "\""
BAD_WORDS = "of and to for Book Page in by on from with See"
DEFAULT_MAX = 50

class Entries:
    def __init__(self):
       self.client = GraphqlClient(endpoint="https://hmjrapi-prod.herokuapp.com/")

    def sorted(self, key):
        """Sort the current entries with the given key function."""
        try:
            self.results = sorted(self.results, key=key)
            return self
        except:
            print("No results found. Try running a query first.")

    def entries(self):
        """Return a numpy array of the result entry dictionaries."""
        try:
            return np.array(self.results);
        except:
            print("No results found. Try running a query first.")

    def headers(self):
        """Return a numpy array of the result header strings."""
        try:
            return np.array([i["header"] for i in self.results])
        except:
            print("No results found. Try running a query first.")

    def content(self):
        """Return a numpy array of the result content strings."""
        try:
            return np.array([i["content"] for i in self.results])
        except:
            print("No results found. Try running a query first.")

    def dates(self):
        """Return a numpy array of the result date dictionaries."""
        try:
            return np.array([d for i in self.results for d in i["dates"]])
        except:
            print("No results found. Try running a query first.")

    def indexes(self):
        """Return a numpy array of the result index dictionaries."""
        try:
            return np.array([d for i in self.results for d in i["indexes"]])
        except:
            print("No results found. Try running a query first.")

    def headerWords(self, badChars=BAD_CHARS):
        """Return a numpy array of all the words in all headers. Repetitions are allowed."""
        try:
            return splitIntoWords(' '.join(self.headers()), badChars)
        except:
            print("No results found. Try running a query first.")

    def headerCounts(self):
        """Count the appearances of each unique header."""
        unique, counts = np.unique(self.headers(), return_counts=True)
        return dict(zip(unique, counts))

    def contentWords(self, badChars=BAD_CHARS):
        """Return a numpy array of all the words in all headers. Repetitions are allowed."""
        try:
            return splitIntoWords(' '.join(self.content()), badChars)
        except:
            print("No results found. Try running a query first.")

    def words(self, badChars=BAD_CHARS):
        """Return a numpy array of all the words in each entry. Equivalent to headerWords + contentWords."""
        try:
            return np.concatenate((self.headerWords(badChars),self.contentWords(badChars)))
        except:
            print("No results found. Try running a query first.")

    def associate(self, words, badWords=BAD_WORDS):
        """Count the appearances of each unique word in indexes that contain the given words. """
        indexes = self.indexes()
        if indexes.any():
            containedStrs = [s["content"] for s in indexes for word in words if s["content"] is not None if word in s["content"]]
            words = [word for s in containedStrs for word in s.split(" ") ]
            return {word:words.count(word) for word in words if word not in badWords}

    def query(self, query, variables, name):
        """Make a raw GQL query to the hmjrapi backend."""
        try:
            self.results = self.client.execute(query=query,variables=variables)["data"][name]
        except:
            print("Query resulted in error: ")

    def all(self, offset=0, max=DEFAULT_MAX):
        """Query entries with no criteria."""
        query = """
            query ($max: Float!, $offset: Float!) {
                entries(max: $max, offset: $offset) {
                    book
                    header
                    content
                    dates {
                        day
                        month
                        year
                        stringified
                        content
                    }
                    indexes {
                        book
                        page
                        content
                    }
                }
            }
        """
        variables = {"max": max,"offset": offset}
        self.query(query, variables, "entries")
        return self;

    def withDate(self, date, max=DEFAULT_MAX):
        """Query entries that surround a specific date."""
        query = """
            query ($max: Float!, $date: DateInput!) {
                entriesByDate(max: $max, date: $date) {
                    book
                    header
                    content
                    dates {
                        day
                        month
                        year
                        stringified
                        content
                    }
                    indexes {
                        book
                        page
                        content
                    }
                }
            }
        """
        variables = {"max": max,"date": date}
        self.query(query, variables, "entriesByDate")
        return self;

    def withKeyword(self, keyword, max=DEFAULT_MAX):
        """Query entries that contain at least one of the specified keywords in their header/content."""
        query = """
            query ($max: Float!, $keyword: [String!]!) {
                entriesByKeyword(max: $max, keyword: $keyword) {
                    book
                    header
                    content
                    dates {
                        day
                        month
                        year
                        stringified
                        content
                    }
                    indexes {
                        book
                        page
                        content
                    }
                }
            }
        """
        variables = {"max": max,"keyword": keyword}
        self.query(query, variables, "entriesByKeyword")
        return self


    def withBook(self, book, max=DEFAULT_MAX):
        """Query entries with a specific volume of the diaries."""
        query = """
            query ($max: Float!, $book: [String!]!) {
                entriesByBook(max: $max, book: $book) {
                    book
                    header
                    content
                    dates {
                        day
                        month
                        year
                        stringified
                        content
                    }
                    indexes {
                        book
                        page
                        content
                    }
                }
            }
        """
        variables = {"max": max,"book": [validateBook(x) for x in book]}
        self.query(query, variables, "entriesByBook")
        return self

    def withBookBetween(self, minBook, maxBook, max=DEFAULT_MAX):
        """Query entries between two books, including the lower bound."""
        return self.withBook([x for x in range(minBook, maxBook, 1)], max)



