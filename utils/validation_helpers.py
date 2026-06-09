import validators

def is_valid_domain(domain: str) -> bool:
    """
    Check if the provided string is a valid domain name without network calls required by dnspython.
    May be updated in the future to use a more robust validation method as needed.   
    """
    try: 
       return validators.domain(domain) is True
    except validators.ValidationError:
        return False
