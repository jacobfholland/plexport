def generate_link(media):
    tmdb_id = get_tmdb_id(media)
    imdb_id = get_imdb_id(media)
    tvdb_id = get_tvdb_id(media)
    anidb_id = get_anidb_id(media)
    if tmdb_id:
        return f"https://www.themoviedb.org/movie/{tmdb_id}"
    elif imdb_id:
        return f'https://www.imdb.com/title/{imdb_id}/'
    elif tvdb_id:
        return f'https://www.thetvdb.com/series/{tvdb_id}/'
    elif tvdb_id:
        return f'https://anidb.net/anime/{anidb_id}/'
    return None


def get_tmdb_id(movie):
    prefix = 'com.plexapp.agents.themoviedb://'
    if movie.guid and movie.guid.startswith(prefix):
        return movie.guid[len(prefix):].split('?')[0]
    return None


def get_imdb_id(movie):
    prefix = 'com.plexapp.agents.imdb://'
    if movie.guid and movie.guid.startswith(prefix):
        return movie.guid[len(prefix):]
    return None


def get_tvdb_id(show):
    prefix = 'com.plexapp.agents.tvdb://'
    if show.guid and show.guid.startswith(prefix):
        return show.guid[len(prefix):].split('?')[0]
    return None


def get_anidb_id(anime):
    prefix = 'com.plexapp.agents.anidb://'
    if anime.guid and anime.guid.startswith(prefix):
        return anime.guid[len(prefix):].split('?')[0]
    return None


def get_lastfm_id(album):
    prefix = 'com.plexapp.agents.lastfm://'
    if album.guid and album.guid.startswith(prefix):
        return album.guid[len(prefix):].split('?')[0]
    return None
