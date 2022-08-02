import unittest

from Lab02 import problem_1, problem_2_1, problem_2_2


class TestProblem1(unittest.TestCase):
    def setUp(self):
        self.tracy = problem_1("Tracy McConnell")
        self.ted = problem_1("Ted")

    def test_easy_tracy_full_name(self):
        full_name = ""
        for d in self.tracy:
            if d["attribute"] == "Full name":
                full_name = d["value"]
        self.assertEqual(full_name, "Tracy McConnell")

    def test_hard_tracy_romances(self):
        romances = []
        for d in self.tracy:
            if d["attribute"] == "Romances":
                romances = d["value"]
        self.assertListEqual(romances, [
                             "Ted Mosby (Husband)", "Max (ex-boyfriend - deceased)", "Louis (ex-boyfriend)"])

    def test_easy_ted_length(self):
        self.assertEqual(len(self.ted), 10)

    def test_medium_ted_birth_date(self):
        birth_date = ""
        for d in self.ted:
            if d["attribute"] == "Born":
                birth_date = d["value"]
        self.assertEqual(birth_date, "April 25, 1978")


class TestProblem2_1(unittest.TestCase):
    def setUp(self):
        self.courses = problem_2_1()

    def test_easy_length(self):
        self.assertEqual(len(self.courses), 81)

    def test_easy_keys(self):
        for course in self.courses:
            self.assertListEqual(sorted(course.keys()), [
                                 "Name of Course", "URL"], msg="Wrong keys")


class TestProblem2_2(unittest.TestCase):
    def setUp(self):
        self.akbc = problem_2_2(
            "https://www.lsf.uni-saarland.de/qisserver/rds?state=verpublish&status=init&vmfile=no&publishid=137193&moduleCall=webInfo&publishConfFile=webInfo&publishSubDir=veranstaltung")

    def test_easy_akbc_length(self):
        # 13 in "Basic Information" + "Responsible Instructors"
        self.assertEqual(len(self.akbc), 14)

    def test_easy_akbc_enroll(self):
        self.assertEqual(self.akbc["Assignment"], "no enrollment")

    def test_easy_akbc_credit(self):
        self.assertEqual(self.akbc["Credits"], "")

    def test_easy_akbc_links(self):
        self.assertListEqual(self.akbc["Additional Links"], [
                             "https://www.mpi-inf.mpg.de/departments/databases-and-information-systems/teaching/ss2022/akbc"])

    def test_easy_akbc_instructors(self):
        self.assertListEqual(self.akbc["Responsible Instructors"], [
                             "Razniewski, Simon , Dr."])


if __name__ == "__main__":
    unittest.main()