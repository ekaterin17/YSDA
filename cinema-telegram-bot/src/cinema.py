import aiohttp
import src.message as msg
import typing as tp

from urllib.parse import quote
from src.keys import keys


class Cinema:
    def __init__(self) -> None:
        pass

    def get_url(self, title_encoded: str) -> str:
        return f"http://kinopoiskapiunofficial.tech/api/v2.1/films/search-by-keyword?keyword={title_encoded}&page="

    def parse_json(self, json: tp.Dict[str, tp.Any]) -> str:
        n_films = min(3, len(json['films']))
        if n_films == 0:
            out = msg.ERROR_MSG
        else:
            out = ''

        for film in json['films'][:n_films]:
            out += '🔹 ' + film['nameRu'] + ', '
            if 'year' in film.keys():
                out += film['year'] + '\n'
            if 'posterUrl' in film.keys():
                out += film['posterUrl'] + '\n\n'

        if out != msg.ERROR_MSG:
            t = json['keyword'].replace(" ", "+")
            out += f"🍿 http://ikinopoisk.com/search/?do=search&subaction=search&q={t}"
        return out

    async def search(self, title: str) -> str:
        title_encoded = quote(title.replace(" ", "+"))
        headers: tp.Dict[str, str] = {'accept': 'application/json', 'X-API-KEY': keys["X_API_KEY"]}
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(self.get_url(title_encoded)) as response:
                info = await response.json()
                return self.parse_json(info)
