from quo.dialog import CheckBox

result = CheckBox("gi", values=[
        ("eggs", "Eggs"),
        ("bacon", "<blue>Bacon</blue>"),
        ("croissants", "20 Croissants"),
        ("daily", "The breakfast of the day"),
    ]
)

if result:
    print("dd")
else:
    print("ok")