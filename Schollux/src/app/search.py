from scholarly import scholarly
import logging

def search_papers(category, query):
    try:
        res = []
        # Convert query to string if it's not already
        query_str = str(query)
        logging.info(f"Searching for: {query_str}")
        
        # Initialize the search
        search_query = scholarly.search_pubs(query_str)
        counter = 0
        max_attempts = 10  # Set a maximum number of attempts
        attempts = 0

        if category == "topic":
            target_results = 3  # Reduced from 5 to improve reliability
        else:
            target_results = 1

        while counter < target_results and attempts < max_attempts:
            try:
                pub = next(search_query)
                bib = pub.get('bib', {})
                
                title = bib.get('title')
                authors = bib.get('author', [])
                year = bib.get('year', 'N/A')
                
                if title and authors:
                    # Format authors list if it's a list
                    if isinstance(authors, list):
                        authors = ', '.join(authors)
                    
                    # Add year to the result
                    res.append({
                        'title': title,
                        'authors': authors,
                        'year': year
                    })
                    counter += 1
                    logging.info(f"Found paper: {title}")
                
            except StopIteration:
                logging.warning("No more results available")
                break
            except Exception as e:
                logging.error(f"Error processing result: {str(e)}")
            
            attempts += 1

        if not res:
            logging.warning("No results found")
            return [{
                'title': 'No relevant papers found',
                'authors': 'Please try a different search query',
                'year': ''
            }]

        return res

    except Exception as e:
        logging.error(f"Search error: {str(e)}")
        return [{
            'title': 'Error searching for papers',
            'authors': f'Error: {str(e)}',
            'year': ''
        }]