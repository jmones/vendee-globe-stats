class Decryptor:
    def __init__(self):
        self._CONST_OBS_1 = 8111253
        self._CONST_OBS_2 = 4544506
        self._CONST_OBS_3 = 13986479
        self._CONST_OBS_4 = 16744512

    def _reset(self):
        self.ks1 = self._CONST_OBS_1 
        self.ks2 = self._CONST_OBS_2
        self.ks3 = self._CONST_OBS_3
        self.ks4 = self._CONST_OBS_4

    def _iterate_keystream(self):
        x = self.ks1
        x = x ^ ((x << 11) & 0xffffff)
        x = x ^ ((x >> 8) & 0xffffff)
        self.ks1 = self.ks2
        self.ks2 = self.ks3
        self.ks3 = self.ks4
        self.ks4 = self.ks4 ^ ((self.ks4 >> 19) & 0xfffff) 
        self.ks4 = self.ks4 ^ x

    def _decrypt_byte(self, input):
        output = input ^ (self.ks1 & 0xff)
        self._iterate_keystream()
        return output
    
    def decrypt(self, data):
        self._reset()
        for ii in range(0, data[0]):
            self._iterate_keystream()
        length = (self._decrypt_byte(data[1])<<16) + (self._decrypt_byte(data[2])<<8) + self._decrypt_byte(data[3])
        ii = 4
        jj = 0
        result = bytearray(length)
        while ii<len(data) and jj<length:
            x = data[ii]
            x = (x ^ (ii & 0xff)) ^ 0xa3
            ii += 1
            for kk in range(7, -1, -1):
                if (x & (1<<kk)) == 0:
                    result[jj] = self._decrypt_byte(data[ii])
                    ii += 1
                    jj += 1
                else:
                    byte = self._decrypt_byte(data[ii])
                    count = (byte >> 4) + 3
                    offset = (((byte & 0xf) << 8) | self._decrypt_byte(data[ii+1])) + 1
                    ii += 2
                    for l in range(count):
                        result[jj] = result[jj-offset]
                        jj += 1
                if ii>=len(data) or jj>=length:
                    break
        return result.decode("utf-8")