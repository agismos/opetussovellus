<h1>Tenttisovellus</h1>

Sovelluksen käyttäjä on opettaja tai opiskelija. Käyttäjä voi luoda tunnuksen
joko opettajan tai opiskelijan roolissa. Jos tunnuksen luo opettajan roolissa,
tarvitaan salainen avain.

Sovellusta voi tässä vaiheessa testata paikallisesti. Kloonaamisen jälkeen on luotava
.env-tiedosto, joka määritellään näin:

```bash
DATABASE_URL=<tietokannan-paikallinen-osoite>
SECRET_KEY=<salainen-avain>
TEACHER_KEY=<salainen-avain-opettajan-rekisteröitymistä-varten>
```
Kohtaan TEACHER_KEY tulee keksiä salasana, joka täytyy antaa opettajan tunnusta luotaessa.

Tämän jälkeen ajetaan seuraavat komennot:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r ./requirements.txt
psql < schema.sql
flask run
```

Mitä sovelluksessa voi tehdä tässä vaiheessa:

<ul>
  <li>Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.</li>
  <li>Opiskelija näkee listan tenteistä ja voi ilmoittautua tenttiin.</li>
  <li>Käyttäjä näkee yhteenvedon omista tiedoista.</li>

  <li>Opettaja pystyy luomaan uuden tentin.</li>

  <li>Opettaja pystyy lisäämään tenttiin kysymyksiä ja vastauksia. Vastaukset
      tallentuvat tietokantaan questions, jossa näkyy onko vastaus oikein vai väärin.</li>
  <li>Opettaja näkee yhteenvedon tekemästään tentistä sekä voi lisätä ja poistaa kysymyksiä.</li>
  <li>Opiskelija voi tenttiä tentin, johon on ilmoittautunut.</li>
</ul>

Tehtävää:
<ul>
  <li>Opiskelija näkee yhteenvedon tekemistään tenteistä.</li>
  <li>Opettaja voi tehdä tekemänsä tentin.</li>
