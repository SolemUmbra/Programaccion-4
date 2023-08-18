import requests

def get_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Pregunta a) En cuántas películas aparecen planetas cuyo clima sea árido?
def get_arid_planets_films_count():
    planets_url = 'https://swapi.dev/api/planets/?search=arid'
    planets_data = get_data(planets_url)
    
    if planets_data:
        planet_count = len(planets_data['results'])
        return planet_count
    else:
        return None

# Pregunta b) Cuántos Wookies aparecen en la sexta película?
def get_wookies_in_sixth_movie():
    film_url = 'https://swapi.dev/api/films/3/'  # Cambia esto según la película correcta
    film_data = get_data(film_url)
    
    if film_data:
        wookie_count = 0
        for character_url in film_data['characters']:
            character_data = get_data(character_url)
            if character_data and 'Wookie' in character_data['name']:
                wookie_count += 1
        return wookie_count
    else:
        return None

# Pregunta c) Cuál es el nombre de la aeronave más grande en toda la saga?
def get_largest_starship():
    starships_url = 'https://swapi.dev/api/starships/'
    starships_data = get_data(starships_url)
    
    if starships_data:
        largest_starship = max(starships_data['results'], key=lambda x: int(x['length']))
        return largest_starship['name']
    else:
        return None

if __name__ == '__main__':
    arid_planets_count = get_arid_planets_films_count()
    wookies_in_sixth_movie = get_wookies_in_sixth_movie()
    largest_starship_name = get_largest_starship()

    print(f'Pregunta a) En cuántas películas aparecen planetas cuyo clima sea árido?: {arid_planets_count}')
    print(f'Pregunta b) Cuántos Wookies aparecen en la sexta película?: {wookies_in_sixth_movie}')
    print(f'Pregunta c) Cuál es el nombre de la aeronave más grande en toda la saga?: {largest_starship_name}')
