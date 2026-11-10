# Skill: miniaturki ofert Allegro z AI

Skill dla Claude Code. Prowadzi przez zrobienie miniaturki oferty Allegro (pierwsze zdjęcie)
i scen do galerii w generatorze obrazów AI, tak żeby pokazywały realny towar i spełniały
wymagania Allegro: białe tło #FFFFFF, zero cieni, zero dodanych napisów i znaków wodnych,
produkt w całości w kadrze.

## Instalacja

Skopiuj katalog `allegro-miniaturki` do `~/.claude/skills/` (Windows: `C:\Users\<ty>\.claude\skills\`)
i uruchom Claude Code ponownie. Skrypty kontrolne wymagają Pythona:

```
pip install numpy opencv-python pillow
```

## Co jest w środku

- `allegro-miniaturki/SKILL.md`: reguły, prompty, przebieg, kontrola odbioru.
- `allegro-miniaturki/scripts/biale-tlo.py`: dobiela tło do #FFFFFF i mierzy margines produktu.
- `allegro-miniaturki/scripts/bramka-tla.py`: bramka tła (siatka 24x24, zero cieni i smug).

## Czego tu nie ma

Skill nie zawiera generatora obrazów. Podłącz własne narzędzie, które przyjmuje prompt
i zdjęcie referencyjne.
