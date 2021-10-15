import re
from Levenshtein import distance
from nltk.corpus import stopwords


class FindDuplicate:

    def __init__(self):
        self.already_recieved_strings_dict = {}
        self.stop_words_used_for_company = ['llc', 'limited', 'ltd',
                                            'ltd.', 'gmbh', 'inc',
                                            'org', 'pvt', 'pvt.', 'corporation']

    def __clean_string__(self, string, to_do_lower=True):
        if to_do_lower:
            clean_string = " ".join([w.replace(",", "") for w in string.lower().split(" ")
                                     if w not in self.stop_words_used_for_company and w not in stopwords.words()
                                     ])
        else:
            clean_string = " ".join([w.replace(",", "") for w in string.split(" ")
                                     if w.lower() not in self.stop_words_used_for_company
                                     ])
        return clean_string

    def __calculate_edit_distance__(self, string1, string2):
        edit_distance = distance(string1, string2)
        return edit_distance

    def __find_if_strings_has_abbreviations__(self, string1, string2):

        # the intuition behind this is that generally,company names are abbreviated either
        # by taking first two letter of the main name or if and is there, & is inserted

        # the string which is smaller most probably has the abbreviated version of the company name
        string1 = self.__clean_string__(string1, to_do_lower=False)
        string2 = self.__clean_string__(string2, to_do_lower=False)

        if len(string1) > len(string2):
            longer_string = string1
            shorter_string = string2
        elif string1 == string2:
            return True
        else:
            longer_string = string2
            shorter_string = string1

        if '&' in shorter_string:
            # check in shorter string
            regex_for_and_abb = r"[A-Za-z]&[A-Za-z]"
            matches_for_abb_and = re.finditer(regex_for_and_abb, shorter_string, re.MULTILINE)
            shorter_version = ''
            for match in matches_for_abb_and:
                shorter_version = match.group()

            # check in bigger string
            regex_for_and = r"[A-Za-z]+\s(AND|and|And|&)\s[A-Za-z]+"

            matches_for_and = re.finditer(regex_for_and, longer_string, re.MULTILINE)

            longer_version = ''
            for match in matches_for_and:
                longer_version = match.group()

            if len(longer_version) > 0 and len(shorter_version) > 0:
                ## now check if shorter version has same initials as longer version

                shorter_version = shorter_version.replace('&', '')

                first_word_in_longer_version = longer_version.split(' ')[0]
                second_word_in_longer_version = longer_version.split(' ')[2]

                abbreviation_of_longer_version = first_word_in_longer_version[0] + second_word_in_longer_version[0]

                if shorter_version.lower() == abbreviation_of_longer_version.lower():
                    return True
                else:
                    return False
            else:
                return False

        else:
            regex_to_find_capital_letter = r"\b[A-Z]{2,}\b"

            matches_for_capital_letter = re.finditer(regex_to_find_capital_letter, shorter_string, re.MULTILINE)

            abb_version_in_shorter_string = ''
            for match in matches_for_capital_letter:
                abb_version_in_shorter_string = match.group()

            splited_longer_version = longer_string.split(" ")[:len(abb_version_in_shorter_string)]

            abb_version_for_longer_string = []
            for i in splited_longer_version:
                abb_version_for_longer_string.append(i[0])

            if len(abb_version_in_shorter_string) > 0 and len(abb_version_for_longer_string) > 0:
                abb_version_for_longer_string = ''.join(abb_version_for_longer_string)

                if abb_version_in_shorter_string.lower() == abb_version_for_longer_string.lower():
                    return True
                else:
                    return False
            else:
                return False

    def __check_if_strings_are_equal_or_has_partial_equality__(self, string1, string2):
        '''

        :param string1:
        :param string2:
        :return:
        '''

        string1 = self.__clean_string__(string1)
        string2 = self.__clean_string__(string2)

        if string1 == string2:
            return True
        else:
            return any([w in string2.split(" ") for w in string1.split(" ")])

    def run_intermediate_steps(self, previous_string, next_string, category):
        '''

        :param previous_string:
        :param next_string:
        :param category:
        :return:
        '''

        # check if the string are partially equal or completely equal
        if category != 'Company_name':
            if self.__check_if_strings_are_equal_or_has_partial_equality__(previous_string, next_string):
                return True
            elif self.__calculate_edit_distance__(self.__clean_string__(previous_string),
                                                  self.__clean_string__(next_string)) < 2:
                return True
            else:
                return False
        else:
            if self.__check_if_strings_are_equal_or_has_partial_equality__(previous_string, next_string):
                return True
            elif self.__calculate_edit_distance__(self.__clean_string__(previous_string),
                                                  self.__clean_string__(next_string)) < 2:
                return True
            else:
                if self.__find_if_strings_has_abbreviations__(previous_string, next_string):
                    return True
                else:
                    return False

    def run_checker(self, new_incoming_string_dict):
        '''
        This function run a checker over a copy of already seen dict and if the string is not present it try to
        add it to the already existing cluster or create a new cluster in a category key.
        :param new_incoming_string_dict:
        :return:
        '''

        category_of_new_string = new_incoming_string_dict['category']
        already_recieved_strings_dict = self.already_recieved_strings_dict.copy()
        if category_of_new_string in already_recieved_strings_dict.keys():
            all_the_previous_strings_from_the_detected_category = already_recieved_strings_dict[category_of_new_string]

            cluster_to_new_string_if_true = ''
            counter = 0
            for cluster, values in all_the_previous_strings_from_the_detected_category.items():
                counter += 1
                last_string_that_was_added = values[-1]
                new_string_that_came = new_incoming_string_dict['string']

                value_obtained = self.run_intermediate_steps(last_string_that_was_added, new_string_that_came,
                                                             category_of_new_string)

                if value_obtained:
                    cluster_to_new_string_if_true = cluster

            if len(cluster_to_new_string_if_true) > 0:
                already_recieved_strings_dict[category_of_new_string][cluster_to_new_string_if_true].append(
                    new_incoming_string_dict['string'])
            else:
                already_recieved_strings_dict[category_of_new_string][f"cluster_{counter}"] = []
                already_recieved_strings_dict[category_of_new_string][f'cluster_{counter}'].append(
                    new_incoming_string_dict['string'])
        else:
            already_recieved_strings_dict[category_of_new_string] = {}
            already_recieved_strings_dict[category_of_new_string]['cluster_0'] = []
            already_recieved_strings_dict[category_of_new_string]['cluster_0'].append(
                new_incoming_string_dict['string'])

        self.already_recieved_strings_dict = already_recieved_strings_dict
        return self.already_recieved_strings_dict
