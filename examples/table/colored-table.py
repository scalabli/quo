from quo.table import Table

datas = [
        ["Name", "Gender", "Age"],
        ["Alice", "F", 24],
        ["Bob", "M", 19],
        ["Dave", "M", 24]
        ]

table = Table(datas)
table.print()
