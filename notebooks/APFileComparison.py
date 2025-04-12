import pandas as pd
import os

from pygments.lexers.oberon import ComponentPascalLexer


class Comparison:
    def __init__(self):
        current_folder = os.getcwd()
        file_path = os.path.join(current_folder, f"FileComparisonData/")

        
        self.passport = pd.read_csv(f"{file_path}passport_info_same_name.csv")
        self.passport['Field'] = self.passport['Field'].str.lower().str.replace(" ", "", regex=False)
        self.profile = pd.read_csv(f"{file_path}profile_preproc_same_name.csv")
        self.profile['Field'] = self.profile['Field'].str.lower().str.replace(" ", "", regex=False)
        self.account = pd.read_csv(f"{file_path}pdf_prepro.csv")
        self.account['Field'] = self.account['Field'].str.lower().str.replace(" ", "", regex=False)

    def CrossMatchingProperties(self):
        name = ["name", "First/ Middle Name (s)", "account_holder_name"]

        name = Comparison.compare(self,name)
        print(name)



    def findField(self,nameVersions):
        matchesProfile = []
        matchesPassport = []
        matchesAccount = []
        for name in nameVersions:
            matchesProfile.extend(self.profile[self.profile['Field'] == name].values[:, 1])
            matchesPassport.extend(self.passport[self.passport['Field'] == name].values[:, 1])
            matchesAccount.extend(self.account[self.account['Field'] == name].values[:, 1])

        matches = {
            "profile": matchesProfile,
            "passport": matchesPassport,
            "account": matchesAccount
        }

        return matches

    def compare(self,nameVersions):
        # hardcode
        nameVersions = [name.lower().replace(" ", "") for name in nameVersions]
        matches = Comparison.findField(self,nameVersions)

        names = {
            "profile": False,
            "passport": False,
            "account": False
        }
        for name1, val1 in matches.items():
            for name2, val2 in matches.items():
                if name1 == name2:
                    continue
                for val in val1:
                    if val in val2:
                        names[name1] = True

        # find name entry
        all_true = all(names.values())
        return all_true



Client = Comparison()

Client.CrossMatchingProperties()