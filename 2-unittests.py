import unittest
import subprocess
import requests
import sys

port = '49160'
hostname = 'localhost'

class TestHW2(unittest.TestCase):

    def setUp(self):
        global hostname, port
        self.s = 'http://'+hostname+':'+port
        #within limit (249 chars)
        self.key1 = '_yJnRhMUqNHXlUvxTie9jfQ0n6DX2of2ET13aW1LGLnvF9ZBxowE5NluZ3bH0Ctlw65S6XjYftCIzIIWDRd8bS5ykWKZvZGVvQDvakcODw___yiN8purA8Xfl_9WOzCLGYyJF4K2q3yOaOnd6Iu9SEo_hOBInXYkTHBTiGPPPAgt360RGaExts2_gyR8Xg0u8HVZgXrpWjWrRMTBN78Zj7INR2YnsJYzXWooTyU_tOV49O7xDYsgiS6MD'
        #at border (250 chars)
        self.key2 = '6TLxbmwMTN4hX7L0QX5_NflWH0QKfrTlzcuM5PUQHS52___lCzKbEMxLZHhtfww3KcMoboDLjB6mw_wFfEz5v_TtHqvGOZnk4_8aqHga79BaHXzpU9_IRbdjYdQutAU0HEuji6Ny1Ol_MSaBF4JdT0aiG_N7xAkoPH3AlmVqDN45KDGBz7_YHrLnbLEK11SQxZcKXbFomh9JpH_sbqXIaifqOy4g06Ab0q3WkNfVzx7H0hGhNlkINf5PF1'
        #outside limit (251 chars)
        self.key3 = '6TLxbmwMTN4hX7L0QX5_NflWH0QKfrTlzcuM5PUQHS52___lCizKbEMxLZHhtfww3KcMoboDLjB6mw_wFfEz5v_TtHqvGOZnk4_8aqHga79BaHXzpU9_IRbdjYdQutAU0HEuji6Ny1Ol_MSaBF4JdT0aiG_N7xAkoPH3AlmVqDN45KDGBz7_YHrLnbLEK11SQxZcKXbFomh9JpH_sbqXIaifqOy4g06Ab0q3WkNfVzx7H0hGhNlkINf5PF12'
        with open('hw2testvaluefile.txt') as f:
            self.val1 = f.read()
        self.val2 = 'asjdhvksadjfbakdjs'
        self.val3 = 'bknsdfnbKSKJDBVKpnkjgbsnk'

    def test_a_put_nonexistent_key(self):
        res = requests.put(self.s+'/kvs/foo',data = {'val':'bart'})
        d = res.json()
        self.assertEqual(res.status_code,201)
        self.assertEqual(d['replaced'],0)
        self.assertEqual(d['msg'],'success')

    def test_b_put_existing_key(self):
        res = requests.put(self.s+'/kvs/foo',data= {'val':'bart'})
        d = res.json()
        self.assertEqual(d['replaced'],1)
        self.assertEqual(d['msg'],'success')

    def test_c_get_nonexistent_key(self):
        res = requests.get(self.s+'/kvs/faa')
        d = res.json()
        self.assertEqual(res.status_code,404)
        self.assertEqual(d['msg'],'error')
        self.assertEqual(d['error'],'key does not exist')

    def test_d_get_existing_key(self):
        res = requests.get(self.s+'/kvs/foo')
        d = res.json()
        self.assertEqual(d['msg'],'success')
        self.assertEqual(d['value'],'bart')

    def test_e_del_nonexistent_key(self):
        res = requests.delete(self.s+'/kvs/faa')
        d = res.json()  
        self.assertEqual(res.status_code,404)
        self.assertEqual(d['msg'],'error')
        self.assertEqual(d['error'],'key does not exist')

    def test_f_del_existing_key(self):
        res = requests.delete(self.s+'/kvs/foo')
        d = res.json()
        self.assertEqual(d['msg'],'success')

    def test_g_get_deleted_key(self):
        res = requests.get(self.s+'/kvs/foo')
        d = res.json()
        self.assertEqual(res.status_code,404)
        self.assertEqual(d['msg'],'error')
        self.assertEqual(d['error'],'key does not exist')

    def test_h_put_deleted_key(self):
        res = requests.put(self.s+'/kvs/foo',data= {'val':'bart'})
        d = res.json()
        self.assertEqual(res.status_code,201)
        self.assertEqual(d['replaced'],0)
        self.assertEqual(d['msg'],'success')

    def test_i_put_nonexistent_key(self):
        res = requests.put(self.s+'/kvs/'+self.key1,data = {'val':self.val1})
        d = res.json()
        self.assertEqual(res.status_code,201)
        self.assertEqual(d['replaced'],0)
        self.assertEqual(d['msg'],'success')

    def test_j_put_existing_key(self):
        res = requests.put(self.s+'/kvs/'+self.key1,data= {'val':self.val2})
        d = res.json()
        self.assertEqual(d['replaced'],1)
        self.assertEqual(d['msg'],'success')

    def test_k_get_nonexistent_key(self):
        res = requests.get(self.s+'/kvs/'+self.key2)
        d = res.json()
        self.assertEqual(res.status_code,404)
        self.assertEqual(d['msg'],'error')
        self.assertEqual(d['error'],'key does not exist')

    def test_l_get_existing_key(self):
        res = requests.get(self.s+'/kvs/'+self.key1)
        d = res.json()
        self.assertEqual(d['msg'],'success')
        self.assertEqual(d['value'],self.val2)

    def test_m_put_key_too_long(self):
        res = requests.put(self.s+'/kvs/'+self.key3,data= {'val':self.val2})
        d = res.json()
        print(res)
        print(d)
        self.assertNotEqual(res.status_code,200)
        self.assertNotEqual(res.status_code,201)
        self.assertEqual(d['msg'],'error')
        #self.assertEqual(d['error'],'key too long')

    def test_n_del_existing_key(self):
        res = requests.delete(self.s+'/kvs/'+self.key1)
        d = res.json()
        self.assertEqual(d['msg'],'success')

    def test_o_get_deleted_key(self):
        res = requests.get(self.s+'/kvs/'+self.key1)
        d = res.json()
        self.assertEqual(res.status_code,404)
        self.assertEqual(d['msg'],'error')
        self.assertEqual(d['error'],'key does not exist')

    def test_p_put_deleted_key(self):
        res = requests.put(self.s+'/kvs/'+self.key1,data= {'val':self.val3})
        d = res.json()
        self.assertEqual(res.status_code,201)
        self.assertEqual(d['replaced'],0)
        self.assertEqual(d['msg'],'success')

    def test_q_put_key_without_value(self):
        res = requests.put(self.s+'/kvs/'+self.key2)
        d = res.json()
        print(res)
        print(d)
        self.assertNotEqual(res.status_code,200)
        self.assertNotEqual(res.status_code,201)
        self.assertEqual(d['msg'],'error')
    

if __name__ == '__main__':
    unittest.main()
