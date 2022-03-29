import pandas as pd

class OptionsDataProcessor:

    def __init__(self):
        self.activeProcessing = True

    def processPrices(self, csvPrices):
        dataFrame = pd.read_csv(str(csvPrices))
        return dataFrame

if __name__ == "__main__":
    nameFile = "bats_us_options_mkt_share_2022-02-11_-_2022-03-25.csv"
    _optionsPriceProcessor = OptionsDataProcessor()
    df = _optionsPriceProcessor.processPrices(nameFile)
    print(df)


