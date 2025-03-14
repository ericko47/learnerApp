import re
from datetime import date

from numpy.core.defchararray import strip


class Check:

    def isName(name, minlen):
        if len(name) < minlen:
            return "Enter full Name"
        elif not re.match('^[a-zA-Z. ]*$', name):
            return 'Name can only contain string and dots'
        elif not (' ' in name):
            return "Full name contains two or more names"
        else:
            return True

    @staticmethod
    def isEmail(email):
        if re.search(r"^[\w.+\-]+@[\w]+\.[a-z]{2,3}$", email):
            return True
        else:
            return 'email invalid'

    @staticmethod
    def isYob(yob):
        year = date.today().year - 13
        if len(str(yob)) != 4:
            return 'Incorrect year specified'
        if int(yob) >= year:
            return "Too young to be in university"
        return True

    @staticmethod
    def isId(sid):
        if sid.isdigit and len(sid) == 8:
            return True
        else:
            return 'Incorrect ID number specified'

    @staticmethod
    def isPhone(phn):
        if 10 <= len(phn) <= 14:
            return True
        else:
            return 'Incorrect Phone number specified'

    @staticmethod
    def isReg(reg):
        if re.search(r"^[a-zA-Z][0-9]{2,3}/[0-9]/[0-9]{4}/[0-9]{2,3}$", reg):
            return reg
        else:
            return 'Incorrect Reg.No. format'

    @staticmethod
    def isCourse(cos):
        departments = [
            ['Department of commerce', 'Department of Economics'],
            ['Biological and Biomedical Science Technology', 'Chemistry and Biochemistry',
             'Mathematics', 'Computing and Informatics', 'Earth Science']
        ]

        course_list = [
            ['Bachelor of Commerce', 'Bachelor of Agribusiness Management'],
            ['BSc in Economics and Statistics', 'BA in Economics and Sociology',
             'BA in Economics and History', 'BA in Agricultural Economics'],
            ['BSc in Biomedical Science and Technology', 'BSC in Physics', 'Bsc in Chemistry', 'BSC in Biology',
             'Bsc in Mathematics'],
            ['BSc Botany/Zoology', 'BSc Biochemistry', 'Certificate in Science Laboratory Technology'],
            ['BSc Statistics'],
            ['BSc Computer Science', 'BSc in Information and Communication Technology', 'Diploma in ICT'],
            ['BSc in Environmental Science', 'BSc in Natural Resource Management', 'BSc in Geography']
        ]

        if type(cos) == str:
            if cos == 'GEO':
                fac = 'School of Science and applied Technology'
                dep = 'Earth Science'
                cos = 'BSc in Geography'
                return fac, dep, cos
            if cos == 'BOTA':
                fac = 'School of Science and applied Technology'
                dep = 'Chemistry and Biochemistry'
                cos = 'BSc Botany/Zoology'
                return fac, dep, cos
            if cos == 'BIO CHEM':
                fac = 'School of Science and applied Technology'
                dep = 'MATHEMATICS'
                cos = "BSc Biochemistry"
                return fac, dep, cos
            if cos == 'STAT':
                fac = 'School of Science and applied Technology'
                dep = 'Chemistry and Biochemistry'
                cos = 'BSc Statistics'
                return fac, dep, cos
            if cos == 'ENV SCI':
                fac = 'School of Science and applied Technology'
                dep = 'Earth Science'
                cos = 'BSc Environmental Science'
                return fac, dep, cos
            if cos == 'NRM':
                fac = 'School of Science and applied Technology'
                dep = 'Earth Science'
                cos = 'BSc in Natural resource Management'
                return fac, dep, cos
            if cos == 'AGEC':
                fac = 'School of Business and Economics'
                dep = 'Department of Economics'
                cos = 'BA in Agricultural Economics'
                return fac, dep, cos
            if cos == 'BIO MED':
                fac = 'School of Science and applied Technology'
                dep = 'Biological and Biomedical Science Technology'
                cos = 'Biomedical Science'
                return fac, dep, cos
            if cos == 'PHYSICS':
                fac = 'School of Science and applied Technology'
                dep = 'Biological and Biomedical Science Technology'
                cos = 'BSc Physics'
                return fac, dep, cos
            if cos == 'CHEMISTRY':
                fac = 'School of Science and applied Technology'
                dep = 'Biological and Biomedical Science Technology'
                cos = 'BSc Chemistry'
                return fac, dep, cos
            if cos == 'BIOLOGY':
                fac = 'School of Science and applied Technology'
                dep = 'Biological and Biomedical Science Technology'
                cos = 'BSc in Biology'
                return fac, dep, cos
            if cos == 'MATHEMATICS':
                fac = 'School of Science and applied Technology'
                dep = 'Biological and Biomedical Science Technology'
                cos = 'BSc Mathematics'
                return fac, dep, cos
            if cos == 'BCOM':
                fac = 'School of Business and Economics'
                dep = 'Department of commerce'
                cos = 'Bachelor of Commerce'
                return fac, dep, cos
            if cos == 'AGBM':
                fac = 'School of Business and Economics'
                dep = 'Department of commerce'
                cos = 'Bachelor of Agribusiness Management'
                return fac, dep, cos
            if cos == 'ECON STAT':
                fac = 'School of Business and Economics'
                dep = 'Department of Economics'
                cos = 'BSc in Economics and Statistics'
                return fac, dep, cos
            if cos == 'ECON SOCI':
                fac = 'School of Business and Economics'
                dep = 'Department of Economics'
                cos = 'BA in Economics and Sociology'
                return fac, dep, cos
            if cos == 'ECON HIST':
                fac = 'School of Business and Economics'
                dep = 'Department of Economics'
                cos = 'BA in Economics and History'
                return fac, dep, cos
            if cos == 'BICT':
                fac = 'School of Science and applied Technology'
                dep = 'Computing and Informatics'
                cos = 'BSc Information and communication Technology'
                return fac, dep, cos
            if cos == 'COMPS':
                fac = 'School of Science and applied Technology'
                dep = 'Computing and Informatics'
                cos = 'BSc Computer Science'
                return fac, dep, cos
            if cos == 'DICT':
                fac = 'School of Science and applied Technology'
                dep = 'Computing and Informatics'
                cos = 'Diploma in Information and communication Technology'
                return fac, dep, cos
            return False
        else:
            return False

    @staticmethod
    def isGender(gender):
        gender_list = ['Male', 'Female', 'Other']
        for gen in gender_list:
            if gen == gender:
                return True
        return "Gender is not valid"
