import urllib.request
import inspect


class Table:
    def __init__(self, name, description, colum_names, rows):
        self.name = name
        self.description = description
        self.colum_names = colum_names
        self.rows = rows

    def __str__(self):
        return str("Name: " + str(self.name) + " Description: " + self.description + " Column names" + str(self.colum_names) + " rows: " + str(self.rows) + "\n")

    def __repr__(self):
        return str("Name: " + str(self.name) + " Description: " + self.description + " Column names" + str(self.colum_names) + " rows: " + str(self.rows) + "\n")

    def filter(self, criterion):
        return [row for row in self.rows if criterion(row.data)]

    def pprint(self, count=False, meta=False, criterion=lambda x: True):
        rows = self.filter(criterion)
        if not rows:
            print("No data to show!")
            return
        colum_sizes = []
        for i in range(len(self.colum_names)):  # Get the colum sizes
            colum_sizes.append(max([len(row.data[i]) for row in rows]))
        for i in range(len(colum_sizes)):
            colum_sizes[i] = max(len(self.colum_names[i]), colum_sizes[i]) + 2
        print((len(self.name)+1)*"-")
        print(self.name)
        print((len(self.name)+1)*"-"+"\n")
        print(self.description)
        for i, size in enumerate(colum_sizes):
            colum_name = self.colum_names[i]
            diff = size-len(colum_name)
            print(colum_name + diff*" ", end="")
        print()
        for j, row in enumerate(rows):
            if j%5 == 0:
                print(sum(colum_sizes)*"-")
            for i, size in enumerate(colum_sizes):
                data = row.data[i]
                diff = size-len(data)
                print(data + diff*" ", end="")
            print()
        if count:
            print(f"\nNumber of rows: {len(rows)}")
        if meta:
            print("META: " + inspect.getsource(criterion))


class Row:
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return str(self.data)


class TableParser:
    def __init__(self, md=None):
        self.markdown = md
        self.file = None

    def load(self, file):
        self.file = file  # Log the loaded file
        if file.startswith("http"):
            with urllib.request.urlopen(file) as fp:
                self.markdown = fp.read().decode('UTF-8')
        else:
            with open(file, "r") as fp:
                self.markdown = fp.read()

    def markdown(self):
        return self.md

    def tables(self):
        mdlines = [line.strip() for line in self.markdown.split("\n") if line.strip() != ""]  # remove empty lines
        table_indices = [i for i in range(len(mdlines)) if mdlines[i].startswith("##")]  # Get the start indices of the tables
        tables = [mdlines[table_indices[i]:table_indices[i+1]] for i in range(len(table_indices)-1)]  # Get the table lines
        tables.append(mdlines[table_indices[-1]:])  # Append the last table

        names = [table[0][2:].strip() for table in tables]
        tables = [table[1:] for table in tables]

        descriptions = []
        for i, table in enumerate(tables):
            description = ""
            line = table[0]
            while not line.startswith("|"):
                description += table[0] + "\n"
                table = table[1:]  # Remove the processed lin
                line = table[0]
            tables[i] = table  # Write back the processed table
            descriptions.append(description)

        colum_names = []
        for table in tables:
            cnames = [name.strip() for name in table[0].split("|") if name.strip() != ""]
            colum_names.append(cnames)
        tables = [table[2:] for table in tables]

        rows = []
        for table in tables:
            data = []
            for line in table:
                if not line.startswith("|"):
                    continue
                r = [e.strip() for e in line.split("|")][1:-1]
                if any(r):
                    data.append(Row(r))
            rows.append(data)

        out = []
        for i in range(len(names)):
            out.append(Table(names[i], descriptions[i], colum_names[i], rows[i]))
        return out




# Example usage
tp = TableParser()
tp.load("put here local filename or http(s) web address")
tables = tp.tables()
for table in tables:
    table.pprint(count=True, criterion=lambda row: len(row[0]) < 7)
