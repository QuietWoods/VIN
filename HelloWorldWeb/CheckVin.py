# -*- coding:UTF-8 -*-
import json
import chardet
class CheckVin:

    '校验VIN是否正确'
    #  VIN码 17每一位对应的权值
    __vinWeight = [8, 7, 6, 5, 4, 3, 2, 10, 0, 9, 8, 7, 6, 5, 4, 3, 2]
    # VIN码 每一位对应的数值
    __vinValue = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'A': 1, 'B': 2,
                'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'P': 7,
                'R': 9, 'S': 2, 'T': 3, 'U': 4, 'V': 5, 'W': 6, 'X': 7, 'Y': 8, 'Z': 9}

    def __init__(self):
        pass

    def __del__(self):
        class_name = self.__class__.__name__
        print class_name, "del"

    def isformat(self, vin):
        vin = str(vin)
        if vin.isalnum() is True and len(vin) == 17:
            return True
        else:
            return False

    # 校验VIN
    def checkVin(self, vin):
        result = False
        if self.isformat(vin) is False:
            return result
        uppervin = vin.upper()
        if vin == None or uppervin.count('O') > 0 or uppervin.count('I') > 0 or uppervin.count('Q') > 0:
            return result
        if len(uppervin) == 17:
            vinArr = bytes(uppervin)
            amount = 0
            # VIN码从从第一位开始，码数字的对应值×该位的加权值，计算全部17位的乘积值相加
            for i in range(len(vinArr)):
                amount += self.__vinValue[vinArr[i]] * self.__vinWeight[i]
            # for item in vinArr:
            #     amount += self.__vinValue[item] * self.__vinWeight[item]
            # 乘积值相加除以11、若余数为10，即为字母Ｘ
            temp = amount % 11
            if temp == 10 and vinArr[8] == 'X':
                    result = True
            else:
                # VIN码从从第一位开始，码数字的对应值×该位的加权值，计算全部17位的乘积值相加除以11，所得的余数，即为第九位校验值
                if str(temp) == vinArr[8]:
                    result = True
        return result

    def getVINInNinth(self, vin):
        result = -1
        if self.isformat(vin) is False:
            return result
        vinArr = bytes(vin.upper())
        if len(vinArr) != 17:
            return result
        amount = 0
        # VIN码从从第一位开始，码数字的对应值×该位的加权值，计算全部17位的乘积值相加
        for i in range(len(vinArr)):
            amount += self.__vinValue[vinArr[i]] * self.__vinWeight[i]
        temp = amount % 11
        if temp == 10:
            result = 'X'
        else:
            result = temp
        return result



