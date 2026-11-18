# Use Case Diyagramı

```mermaid
flowchart LR
    V([Ziyaretçi])
    A([AVM Yöneticisi])
    subgraph Sistem[AVM Rehber Kiosk]
        UC1(Yazılı soru sor)
        UC2(Mağaza / olanak bul)
        UC3(Kategori önerisi al)
        UC4(Çalışma saati öğren)
        UC5(Kat rehberini gör)
        UC6(Rota ve tarifi gör)
        UC7(Girişi yap)
        UC8(Mağaza / olanak yönet)
        UC9(Model sürümünü seç)
        UC10(Kullanım istatistiklerini gör)
    end
    V --> UC1
    V --> UC3
    V --> UC4
    V --> UC5
    UC1 -. include .-> UC2
    UC2 -. include .-> UC6
    A --> UC7
    A --> UC8
    A --> UC9
    A --> UC10
    UC8 -. include .-> UC7
    UC9 -. include .-> UC7
    UC10 -. include .-> UC7
```

## Aktörler
- **Ziyaretçi:** Kiosk ekranından Türkçe cümle yazar; hesap gerekmez.
- **AVM yöneticisi:** Giriş yapar, mağaza/olanak kataloğunu günceller, kullanılacak modeli seçer.

## Ana senaryo (Ziyaretçi, mağaza bulma)
1. Ziyaretçi "kebap saryı nerede" yazar.
2. Sistem niyeti (`find_store`) ve mağazayı (Kebap Sarayı, 2. kat) çıkarır.
3. Kiosk konumundan mağazaya en kısa rotayı hesaplar.
4. Ekranda harita ve adım adım tarif gösterilir.
