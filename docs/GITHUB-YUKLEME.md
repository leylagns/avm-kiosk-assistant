# GitHub'a yükleme (adım adım)

1. Zip'i çıkar; içindeki dosyaları **mevcut repo klasörüne** kopyala (repo `avm-kiosk-assistant` ise onun içine).
2. Terminalde repo klasöründe:
   ```bash
   git add .
   git commit -m "Hafta 1-3: diyagramlar, mockup/DB dokümanları, veri seti, baseline"
   git push
   ```
3. Daha iyi geçmiş için parça parça commit at:
   ```bash
   git add docs/week1 scripts && git commit -m "Hafta 1: diyagramlar ve isterler"
   git add docs/week2 && git commit -m "Hafta 2: ER, şema, veri sözlüğü, teknoloji yığını"
   git add data src tests notebooks results docs/week3 requirements.txt pyproject.toml .gitignore README.md \
     && git commit -m "Hafta 3: veri seti, EDA, E1 baseline"
   git push
   ```
4. Issues: `gh auth login` sonra `bash scripts/create_issues.sh`.
5. Hocaları repoya collaborator olarak ekle (Settings → Collaborators).
