import json
import nltk
import spacy
import enchant
from nltk.tokenize import word_tokenize

# download some nltk modules
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

# python3 -m spacy download en_core_web_sm
nlp = spacy.load("en_core_web_sm")


class ClassfiyStrings:

    def __init__(self, string='Empty'):
        '''
        This engine takes a string and classify that string into one of these class:
            Location
            Address
            Serial_number
            Company_name
            Physical_good
            Others

        At the end it return the category of the string.
        :param string:
        '''
        self.string = string

    def check_if_serial_number(self):

        def present_in_nltk_corpus(string):
            dictionary = enchant.Dict("en_GB")
            string_splitted = string.lower().split(' ')
            for i in string_splitted:
                if dictionary.check(i):
                    return True
            return False

        # check if there is no space in the string and check if it is all caps or check if serial number is only number or aphanumeric

        if not present_in_nltk_corpus(self.string):
            if '/' in self.string or '.' in self.string or "\\" in self.string:
                string_mod = self.string.replace('/', '').replace('.', '').replace("\\", '')
                if string_mod.isnumeric():
                    return True
                if string_mod.isupper() and string_mod.isalnum():
                    return True
                else:
                    return False
            else:
                if self.string.isnumeric():
                    return True
                if self.string.isupper() and self.string.isalnum():
                    return True
                else:
                    return False
        else:
            return False

    def check_if_address(self, string):

        def check_if_location_or_address(string):
            docs = nlp(string)
            for ent in docs.ents:
                if ent.label_ == "GPE" or ent.label_ == "LOC":
                    return True
            return False

        ## now we have to check if there some road number
        #           or keywords like street, road etc and written
        if check_if_location_or_address(string) or any(map(check_if_location_or_address, string.split(' '))):
            if any(char.isdigit() for char in string) or any(
                    map(self.string.lower().__contains__, ['road', 'rue', 'boulevard', 'avenue', 'rd'])):
                return "Address"
            else:
                return "Location"
        else:
            return "not location/address"

    def check_if_company_name(self):
        def initial_check(string):
            string = string.lower().capitalize()
            company_name_if_present = nlp(string)
            for entity in company_name_if_present.ents:
                if entity.label_ == "ORG":
                    return True
            return False

        ## check for the first time by giving the whole string

        if initial_check(self.string):
            return True
        else:
            ## divide the list into individual elements
            if any(map(initial_check, self.string.split(' '))):
                return True
            else:
                ## make bigrams of the string and then check
                string_list = self.string.split(' ')
                strings_to_test_now = [" ".join(string_list[i:i + 2]) for i in range(0, len(string_list), 2)]
                if any(map(initial_check, strings_to_test_now)):
                    return True
                else:
                    return False

    def check_if_physical_goods(self):

        # for this category we will check if it is a noun or not and if there are nouns we will
        # check if it not location, or country name or company name

        # also, there is a slim chance to have two nouns coming together consecutively it can also help

        # another final resort could be that if the string doesn't belong to any other category it is most probably
        # a physical goods, given the string received are only from these categories overall.

        tags_given_to_string = nltk.pos_tag(word_tokenize(self.string.lower()))

        words_that_are_noun = []
        words_that_are_noun_idx = []
        for idx, tuple_value in enumerate(tags_given_to_string):
            word = tuple_value[0]
            tag = tuple_value[1]
            if tag == 'NN' or tag == 'NNP' or tag == 'NNS':
                if self.check_if_address(word) == 'not location/address' \
                        and not self.check_if_company_name():
                    words_that_are_noun.append(word)
                    words_that_are_noun_idx.append(idx)

        def check_consecutive(l):
            return sorted(l) == list(range(min(l), max(l) + 1))

        if len(words_that_are_noun) > 1:
            if check_consecutive(words_that_are_noun_idx):
                return True
            else:
                return self.brut_force_checking_for_physical_goods(words_that_are_noun)
        else:
            return self.brut_force_checking_for_physical_goods(words_that_are_noun)

    def brut_force_checking_for_physical_goods(self, words_that_are_noun):

        '''
        It is the hard way, we will check if the noun is not a person's first or last name with direct matching
        :param words_that_are_noun:
        :return:
        '''

        all_names_dict = json.load(open("data/all_people_names/all_names.json", "r"))

        found_proper_name = 0
        for i in words_that_are_noun:
            if i.strip().lower() in all_names_dict.keys():
                found_proper_name += 1
        if found_proper_name > 0:
            return False
        else:
            return True

    def run(self):

        # check if the string is a location
        if self.check_if_address(self.string) == 'Location':
            return 'Location'
        elif self.check_if_address(self.string) == 'Address':
            return 'Address'
        if self.check_if_serial_number():
            return 'Serial_number'
        elif self.check_if_company_name():
            return 'Company_name'
        elif self.check_if_physical_goods():
            return 'Physical_good'
        else:
            return 'Others'