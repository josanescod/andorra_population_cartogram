# Cartograma de la població d'Andorra (2023)

Visualització cartogràfica de la distribució de la població a Andorra durant l'any 2023.

[Visualitza el cartograma aquí](https://josanescod.github.io/andorra_population_cartogram/)

---

## Descripció
Aquest projecte mostra un **cartograma** (mapa distorsionat per població) d'Andorra, on les àrees geogràfiques es redimensionen segons la seva població. Això permet identificar ràpidament les zones més i menys poblades del país.

## Fonts

- Mapes i dades espacials: [GADM](https://gadm.org/download_country.html)

- Dades de població per parròquia (2023): [Viquipèdia](https://ca.wikipedia.org/wiki/Parr%C3%B2quies_d%27Andorra)


## Instal·lació i execució en local

**Requisits previs**

- Python 3.x
- pip per  a la instal·lació de dependències


1. Clonar el repositori:

```bash
git clone git@gitlab.com:jsanchezesc/andorra_population_cartogram.git
cd andorra_population_cartogram 
```

2. Instal·lar les dependències:

```bash
pip3 install -r requirements.txt
```

3. Generar el cartograma:

```bash
python3 ex1_cartogrm.py
```

4. Visualitzar el resultat: 

- Iniciar un servidor web local per visualitzar el cartograma al navegador

```bash
python3 -m http.server

```

- Obrir el navegador i acedir a: http://localhost:8000

---





