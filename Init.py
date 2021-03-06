import os
import csv
from sys import argv
from DataGenerator import DataGenerator as dg, TypeData
import io
from Convert import to_sign, Sign
import json


class Init():

    def __init__(self, arg):

        self.__data = Data(arg)
        self._dg = dg()
        self.__start()

    # def _convert_array(self, val=None):

    #     # TODO Delete function
    #     """Convert whatever data to array"""

    #     return val if type(val).__name__ == 'list' else [val]

    def _prepare_to_sql(self, val):
        """Prepare data for sql example """

        return Sign.Comma if Data.Options.get(val) else Sign.Nothing

    def __build_data(self):
        """To Generate data according to parameter"""

        if self.__data.typefile == 'sql':

            cnt = ""

            for index, val in enumerate(self.__data.options):

                # TODO to organize code better

                if len(self.__data.options) - 1 > index:

                    cnt += str(to_sign(self._dg.choose_data(val),
                                       self._prepare_to_sql(val))) + ","
                else:

                    cnt += str(to_sign(self._dg.choose_data(val),
                                       self._prepare_to_sql(val)))

            return to_sign(cnt, Sign.Parentheses)

        elif self.__data.typefile == 'json':

            cnt = []

            for _ in range(0, self.__data.count):

                tmp = {}

                for index, val in enumerate(self.__data.options):
                    # get key for json
                    key = str(Data.Options['-' if val.find("-") == 1 else val])
                    result = str(self._dg.choose_data(val))
                    tmp[key] = result

                cnt.append(tmp)

            return cnt

        elif self.__data.typefile == 'csv':

            cnt = []

            for index, val in enumerate(self.__data.options):
                cnt.append(self._dg.choose_data(val))

            return cnt

    def __build_file(self):

        if self.__data.typefile == 'sql':

            file = open('result.sql', 'w')

            for x in range(0, self.__data.count):

                if self.__data.count - 1 > x:

                    file.write(self.__build_data()+",\n")

                else:

                    file.write(self.__build_data())

            file.close()

        elif self.__data.typefile == "json":

            with open("result.json", "w") as file:

                result = self.__build_data()
                json.dump(result, file)

        elif self.__data.typefile == "csv":

            with open('result.csv', 'w', newline='') as file:
                writer = csv.writer(file, delimiter='|', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                for _ in range(0, self.__data.count):
                    result = self.__build_data()
                    writer.writerow(result)

    def __start(self):

        if self.__data.ready:

            try:

                self.__build_file()

            except Exception as e:

                print(e.args)
                # self.__help()

        else:

            self.__help()

    def __help(self):

        print("*****************************************")
        print("*                                       *")
        print("*            Data Generator X1000       *")
        print("*                                       *")
        print("*****************************************")
        print("Note: File name can UPPER and lower!")
        print("Always the item last'll be acount records!")
        print("SQL")
        print("CVS")
        print("JSON")
        print("Options\n")
        print("1:Man Name")
        print("2:Woman Name")
        print("3:Surname")
        print("4:Country")
        print("?-?:Values Integer")
        print("6:Email")
        print("7:Product")
        print("8:Telephone\n")
        print("Example \nsql 1 2 4 1-100 10")


class Data():

    # options_sql = ['1', '2', '3', '4', '6', '7', '8']
    Files = ['json', 'sql', 'csv']
    Options = {'1': 'namem',
                    '2': 'namef',
                    '3': 'surmane',
                    '4': 'country',
                    '-': 'number',
                    '6': 'email',
                    '7': 'product',
                    '8': 'telephone'}

    def __init__(self, arg=[]):

        # arguments
        self.__arg = arg[1:]

        # to process arguments
        self.typefile = self.__get_typefile()
        self.count = self.__get_count()
        self.options = self.__get_options()
        self.ready = self.__validate()

    def __get_options(self):
        """Get arguments and send to prepara for to use in generator"""

        data = self.__arg[1:-1]
        # self.__process_taginteger(dt=processdata)
        return data if len(data) > 0 else False

    def __get_count(self):
        """Get count to generate"""

        return int(list(filter(lambda x: self.__arg[-1:][0] is x, self.__arg))[0])

    def __get_typefile(self):
        """Get type file for to generate"""

        return self.__arg[:1][0] if self.__arg[:1][0] in self.Files else False

    def __process_taginteger(self, dt=[]):

        for index, i in enumerate(dt):

            fnt = []

            if i.find('-') and len(i.split('-')) == 2:

                fnt = ['-'] + i.split("-")
                dt[index] = fnt

    def __validate(self):
        """Validate options"""

        if bool(self.typefile) and bool(self.count) and bool(self.options):
            return True
        else:
            return False


if __name__ == "__main__":

    p = Init(argv)
