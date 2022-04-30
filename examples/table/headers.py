from quo.table import Table

data = [
        [1, 'John Smith', 'This is a rather long description that might look better if it is wrapped a bit']
        ]


Table(data, headers=("Issue Id", "Author", "Description"), column_width=[None, None, 30])
