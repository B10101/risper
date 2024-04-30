from django.utils.crypto import get_random_string
import re
from django.db.models import Q

# Function to generate a random string
def random_string_generator():
    return get_random_string(length=10, allowed_chars="ABCDEF0123456789")

# Function to generate a unique store ID
def unique_store_id_generator(instance):
    # Generate a random string
    store_new_id = random_string_generator()

    # Get the class of the instance
    Store = instance.__class__

    # Check if any other store with the same ID exists
    qs_exists = Store.objects.filter(store_id=store_new_id).exists()

    # If another store with the same ID exists, generate a new ID
    if qs_exists:
        return unique_store_id_generator(instance)
    
    # Return the unique store ID
    return store_new_id

# Function to normalize a query string
def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string into individual keywords, getting rid of unnecessary spaces
        and grouping quoted words together.
        Example:
        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    '''
    return [normspace(' ', (t[0] or t[1]).strip())
            for t in findterms(query_string)]

# Function to construct a query based on search terms and fields
def get_query(query_string, search_fields):
    ''' Returns a query, which is a combination of Q objects. This combination
        aims to search keywords within a model by testing the given search fields.
    '''
    query = None  # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None  # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query
