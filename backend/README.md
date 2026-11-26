# Ludoteka - backend

REST API dla aplikacji do zarządzania własną biblioteką gier z integracją ze sklepem Steam oraz autoryzacją użytkowników przez tokeny JWT.

## Szybki start

1. Dodaj plik `.env` w głównym katalogu projektu (obok `docker-compose.yml`) i wklej do niego:
   ```env
   DATABASE_URL=postgresql+psycopg://postgres:twoje_haslo@db:5432/biblioteka_gier
   SECRET_KEY=twoj_tajny_klucz_do_jwt
