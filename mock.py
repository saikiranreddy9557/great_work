

import unittest
from unittest import mock

from sam import sample



class test_util(unittest.TestCase):


    def setUp(self):

        self.patcher = mock.patch("sam.json.dumps",return_value = 11)
        self.patcher.start()


    def test_convo(self):

        self.obj = sample()

        # with mock.patch("sam.json.dumps") as f:
        #     f.return_value = 11
            
           
        data = self.obj.convo({"some value"})

        self.assertEqual(data,11)

    def tearDown(self) :
        self.patcher.stop()



if __name__ == "__main__":
    unittest.main()
