class Delivery:

    BX = "Boxberry"
    CDEK = "CDEK"
    DPD = "DPD"
    PR = "Почта России"
    AD = "Avito Доставка"

    DOMESTIC = PR, AD
    INTERNATIONAL = BX, CDEK, DPD

    CHOICES = (
        (BX, BX),
        (CDEK, CDEK),
        (DPD, DPD),
        (PR, PR),
        (AD, AD)
    )

    VALUES = (BX, CDEK, DPD, PR, AD)