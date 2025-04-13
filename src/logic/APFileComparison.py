import pandas as pd
import os
from datetime import datetime

from pygments.lexers.oberon import ComponentPascalLexer


class Comparison:
    def __init__(self,account,profile,passport):
        """
        accound: pdf
        description: txt
        passport: png
        profile: docx
        """
        date_fields = {
            'issue_date': '%d%m%Y',
            'expiration_date': '%d%m%Y',
            'date_of_birth': '%Y-%m-%d',
            'ID Issue Date': '%Y-%m-%d',
            'ID Expiry Date': '%Y-%m-%d'
        }


        # png
        date_of_birth_value = passport.loc[passport['Field'] == 'date_of_birth', 'Value'].iloc[0]

        self.passport = passport
        self.passport['Field'] = self.passport['Field'].str.lower().str.replace(" ", "", regex=False)
        #self.passport = passport.set_index("Field").T
        try:
            self.passport.loc[self.passport['Field'] == 'date_of_birth', 'Value'] = pd.to_datetime(
                self.passport.loc[self.passport['Field'] == 'date_of_birth', 'Value'], format='%d%m%Y'
            )
        except Exception:
            self.passport.loc[self.passport['Field'] == 'date_of_birth', 'Value'] = pd.Timestamp('2000-01-01')

        try:
            self.passport.loc[self.passport['Field'] == 'issue_date', 'Value'] = pd.to_datetime(
                self.passport.loc[self.passport['Field'] == 'issue_date', 'Value'], format='%d%m%Y'
            )
        except Exception:
            self.passport.loc[self.passport['Field'] == 'issue_date', 'Value'] = pd.Timestamp('2000-01-01')

        try:
            self.passport.loc[self.passport['Field'] == 'expiration_date', 'Value'] = pd.to_datetime(
                self.passport.loc[self.passport['Field'] == 'expiration_date', 'Value'], format='%d%m%Y'
            )
        except Exception:
            self.passport.loc[self.passport['Field'] == 'expiration_date', 'Value'] = pd.Timestamp('2000-01-01')


        # docx
        self.profile = profile
        self.profile['Field'] = self.profile['Field'].str.lower().str.replace(" ", "", regex=False)
        try:
            self.profile.loc[self.profile['Field'] == 'dateofbirth', 'Value'] = pd.to_datetime(
                self.profile.loc[self.profile['Field'] == 'dateofbirth', 'Value'], format='%Y-%m-%d'
            )
        except Exception:
            self.profile.loc[self.profile['Field'] == 'dateofbirth', 'Value'] = pd.Timestamp('2000-01-02')

        try:
            self.profile.loc[self.profile['Field'] == 'idissuedate', 'Value'] = pd.to_datetime(
                self.profile.loc[self.profile['Field'] == 'idissuedate', 'Value'], format='%Y-%m-%d'
            )
        except Exception:
            self.profile.loc[self.profile['Field'] == 'idissuedate', 'Value'] = pd.Timestamp('2000-01-02')

        try:
            self.profile.loc[self.profile['Field'] == 'idexpirydate', 'Value'] = pd.to_datetime(
                self.profile.loc[self.profile['Field'] == 'idexpirydate', 'Value'], format='%Y-%m-%d'
            )
        except Exception:
            self.profile.loc[self.profile['Field'] == 'idexpirydate', 'Value'] = pd.Timestamp('2000-01-02')
        #self.profile = profile.set_index("Field").T
        self.account = account
        self.account['Field'] = self.account['Field'].str.lower().str.replace(" ", "", regex=False)

        print(self.profile)

    def CrossMatchingProperties(self):
        name = ["name", "First/ Middle Name (s)", "account_holder_name"]
        passport = ["passport_number", "Passport No/ Unique ID"]
        date_of_birth = ["date_of_birth", "Date of birth"]
        IDIssueDate = ["ID Issue Date", "issue_date"]
        IDExpiryDate = ["ID Expiry Date", "expiration_date"]

        name = Comparison.compare(self, name)
        passport = Comparison.compare(self, passport)
        date_of_birth = Comparison.compare(self, date_of_birth)
        IDIssueDate = Comparison.compare(self, IDIssueDate)
        IDExpiryDate = Comparison.compare(self, IDExpiryDate)
        return name & passport & date_of_birth & IDIssueDate & IDExpiryDate

    def findField(self, nameVersions):
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

    def compare(self, nameVersions):
        # hardcode
        nameVersions = [name.lower().replace(" ", "") for name in nameVersions]
        matches = Comparison.findField(self, nameVersions)

        names = {
            "profile": False,
            "passport": False,
            "account": False
        }
        print(f"matches: \n{matches}\n")
        for name1, val1 in matches.items():
            for name2, val2 in matches.items():
                if name1 == name2:
                    continue
                for val in val1:
                    try:
                        if val.lower().replace(" ", "") in [v.lower().replace(" ", "") for v in val2]:
                            names[name1] = True
                            print(f"Val1 {name1}:\n{val1}\nVal2 {name2}:\n{val2}")
                    except:
                        if val in [v for v in val2]:
                            names[name1] = True
                            print(f"Val1 {name1}:\n{val1}\nVal2 {name2}:\n{val2}")

        # find name entry
        filtered_values = [value for value in names.values() if value]
        all_true = all(filtered_values)
        if all_true == False:
            print(f"====== FALSE ======\n{matches}\n")
        return all_true

def comparePrecise(account="", profile="", passport=""):
    Client = Comparison(account, profile, passport)
    return Client.CrossMatchingProperties()

if __name__ == "__main__":
    comparePrecise()
