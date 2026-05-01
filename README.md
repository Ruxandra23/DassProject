# Break the Login - AuthX

Proiect pentru cursul **Dezvoltarea Aplicatiilor Software Securizate**.

Aplicatia are doua versiuni:

- **v1** - vulnerabila (intentionat, pentru demo)
- **v2** - securizata

Stack: Python, Flask, SQLite, SQLAlchemy, bcrypt (doar in v2).

---

## Ce face aplicatia

Un mic sistem de autentificare cu:

- register
- login / logout
- forgot password / reset password
- o lista de tickete (ca sa avem ce proteja)

Scopul nu e aplicatia in sine, ci diferenta dintre v1 si v2.

---

## Structura

```
v1_vulnerable/
  app.py
  config.py
  models.py
  seed_test_users.py
  templates/
v2_secure/
  app.py
  config.py
  models.py
  seed_test_users.py
  templates/
```

Fiecare versiune are baza ei de date proprie (`authx_v1.db`, `authx_v2.db`).



## Ce e diferit intre v1 si v2

| Zona | v1 (vulnerabil) | v2 (securizat) |
|---|---|---|
| Hash parole | MD5, fara salt | bcrypt, cu salt |
| Politica parola | accepta orice (chiar si "1") | min. 8 caractere, litera mare, mica si cifra |
| Mesaj la login gresit | "userul nu exista" / "parola gresita" (user enumeration) | mesaj generic "Credentiale invalide" |
| Brute force | nelimitat | lockout 15 min dupa 5 incercari gresite |
| Token reset | predictibil: `reset-{id}-{email}-{ora}`, reutilizabil | `secrets.token_urlsafe(32)`, expira in 1h, one-time |
| Cookie sesiune | fara HttpOnly, fara SameSite strict | HttpOnly, SameSite=Strict |
| Durata sesiune | 1 an | 1 ora |
| Session fixation | id-ul sesiunii nu se roteste la login | `session.clear()` la login |
| SECRET_KEY | hardcodat in cod | random la pornire (sau din env) |
| IDOR pe /tickets | vezi toate ticketele din sistem | vezi doar ticketele tale |
| IDOR pe /tickets/`<id>` | acces la orice ticket dupa id | filtrare pe `owner_id` in query |

---

## Conturi de test

### v1 - http://127.0.0.1:5000

| Email | Parola |
|---|---|
| victim@test.com | 123 |
| admin@test.com | parola |
| user@test.com | 1 |

Parolele slabe sunt acceptate pentru ca v1 nu are validare.

### v2 - http://127.0.0.1:5001

| Email | Parola |
|---|---|
| victim@test.com | Parola123 |
| admin@test.com | Admin123! |
| user@test.com | User2024 |

In v2 toate parolele respecta politica.

---

## Atacuri demonstrate pe v1

- **User enumeration** la login: incerci `inexistent@test.com` -> mesaj diferit fata de `victim@test.com` cu parola gresita.
- **Parole slabe** la register: poti crea cont cu parola "1".
- **Brute force**: nu exista nicio limita la incercari.
- **Hash slab**: parolele sunt MD5, se sparg cu rainbow tables.
- **Reset token predictibil**: daca stii emailul si ora aproximativa, poti reconstrui tokenul si reseta parola altcuiva.
- **IDOR pe tickete**: orice user vede ticketele tuturor; acces direct la `/tickets/3` chiar daca nu e al tau.
- **Cookie nesigur**: poate fi citit din JavaScript (un XSS ar fura sesiunea).

## Cum sunt rezolvate in v2

- bcrypt pentru parole (cu salt automat).
- Validare parola la register si reset.
- Mesaj generic la login + verificare hash dummy cand userul nu exista (sa nu se vada diferenta de timp).
- Lockout temporar dupa 5 incercari (`failed_login_count` + `locked_until`).
- Token reset random cu `secrets`, cu expirare si invalidare dupa folosire.
- Cookie HttpOnly, SameSite=Strict, sesiune scurta.
- `session.clear()` la login (rotatie id sesiune).
- Pe tickete: query filtrat dupa `owner_id`, nu doar verificare ulterioara.



