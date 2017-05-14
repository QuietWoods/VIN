# -*- coding:UTF-8 -*-

import json
class Vin:

    '解析所有汽车公司的VIN码，参数：VIN规则json文件和vin码；返回解析结果。'
    __content = None             # json文件内容dict类型变量

    def __init__(self, filename, vin):
        self.filename = filename
        self.vin = vin
        try:
            fo = open(filename, 'r')
            self.__content = json.load(fo)
        except Exception, e:
            print "JSON file loading failed！"+e.message

    def __del__(self):
        class_name = self.__class__.__name__
        print class_name, "del"

    # 得到json数据
    def getContent(self, str1, str2):
        try:
            result = self.__content[str1][str2]
        except Exception, e:
            result = 'null'
            print 'Illegal parameters：' + e.message
        return result
        # for items in self.__content:
        #     for item in items:
        #         print(self.__content[items][item])
        # 此方法行不通，不能正常遍历。

    # VIN除前三位，之后的每一位对应一个标识。
    def singleMarkVin(self, vin_dict, vinArray):
        result = {vin_dict["1to3"]: self.getContent(vin_dict["1to3"], vinArray[:3])}
        dict_length = 3 + vin_dict.__len__() - 1
        for i in range(3, dict_length):
            if i != 8:
                result[vin_dict[str(i + 1)]] = self.getContent(vin_dict[str(i + 1)], vinArray[i])
            else:
                pass
        result[vin_dict[str(dict_length + 1)]] = self.getContent(vin_dict[str(dict_length + 1)], vinArray[dict_length])
        return result

    # VIN的七八位合并使用。
    def mergeMarkVin(self, vin_dict, vinArray):
        result = {vin_dict["1to3"]: self.getContent(vin_dict["1to3"], vinArray[:3])}
        dict_length = 3 + vin_dict.__len__() + 1
        for i in range(3, dict_length):
            if i > 8 or i < 6:
                temp = self.getContent(vin_dict[str(i + 1)], vinArray[i])
                if type(temp) is dict:
                    try:
                        result[vin_dict[str(i + 1)]] = temp[vinArray[6:8]]
                    except Exception, e:
                        result[vin_dict[str(i + 1)]] = 'null'
                        print 'Illegal parameters：' + e.message
                else:
                    result[vin_dict[str(i + 1)]] = temp
            elif i == 6:
                result[vin_dict["7to8"]] = self.getContent(vin_dict["7to8"], vinArray[6:8])
            else:
                pass
        return result

    # 获得东风乘用车VIN解析结果
    def getDFCYC(self):
        vinArray = bytes(self.vin)
        vin_dict = {"1to3":"WMI", "4": "BRAND", "5": "VTYPE", "6": "ENGINE", "7": "RESTRAINT", "8": "TRANSMISSION", "10": "YEAR",
                    "11": "ASSEMBLY"}
        return self.singleMarkVin(vin_dict, vinArray)

    # 获得广汽本田VIN解析结果
    def getGQBT(self):
        vinArray = bytes(self.vin)
        vin_dict = {"1to3":"WMI", "4": "VDS", "10": "YEAR", "11": "ASSEMBLY"}
        result = {vin_dict["1to3"]: self.getContent(vin_dict["1to3"], vinArray[:3])}
        dictVDS = self.getContent(vin_dict["4"], vinArray[3:8])
        for items in dictVDS:
            if type(dictVDS[items]) is dict:
                for item in sorted(dictVDS[items]):
                    result[item] = dictVDS[items][item]
            else:
                result[items] = dictVDS[items]
        result[vin_dict["10"]] = self.getContent(vin_dict["10"], vinArray[9])
        result[vin_dict["11"]] = self.getContent(vin_dict["11"], vinArray[10])
        return result

    # 获得上汽大众VIN解析结果
    def getSQDZ(self):
        vinArray = bytes(self.vin)
        vin_dict = {"1to3": "WMI", "4": "KAROSSERIE", "5": "MOTOR", "6": "RUECKHALTSYSTEM", "7to8": "FZG-KLASSE", "10": "YEAR", "11": "ASSEMBLY"}
        result = {vin_dict["1to3"]: self.getContent(vin_dict["1to3"], vinArray[:3])}
        result[vin_dict["4"]] = self.getContent(vin_dict["4"], vinArray[3])
        temp = self.getContent(vin_dict["7to8"], vinArray[6:8])
        print temp
        if temp == 'null':
            result[vin_dict["7to8"]] = 'null'
            result[vin_dict["5"]] = 'null'
        else:
            result[vin_dict["7to8"]] = temp.keys()[0]
            try:
                result[vin_dict["5"]] = temp[temp.keys()[0]][vinArray[4]]
            except Exception, e:
                result[vin_dict["5"]] = 'null'
        result[vin_dict["6"]] = self.getContent(vin_dict["6"], vinArray[5])
        result[vin_dict["10"]] = self.getContent(vin_dict["10"], vinArray[9])
        result[vin_dict["11"]] = self.getContent(vin_dict["11"], vinArray[10])
        return result

    # 获得北汽福田戴姆勒VIN解析结果
    def getBQFTDML(self):
        vinArray = bytes(self.vin)
        vin_dict = {"1to3": "WMI", "4": "VSERIES", "5": "TMASS", "6": "BTYPE", "7": "ENGINE", "8": "WHEELBASE", "10": "YEAR", "11": "ASSEMBLY"}
        return self.singleMarkVin(vin_dict, vinArray)

    # 获得北京奔驰VIN解析结果
    def getBJBC(self):
        vinArray = bytes(self.vin)
        vin_dict = {"1to3": "WMI", "4": "VSERIES", "5": "BTYPE", "6to7": "ENGINE", "8": "RESTRAINT", "10": "YEAR"}
        result = {vin_dict["1to3"] : self.getContent(vin_dict["1to3"], vinArray[:3])}
        for i in range(3, 5):
            result[vin_dict[str(i + 1)]] = self.getContent(vin_dict[str(i + 1)], vinArray[i])
        result[vin_dict["6to7"]] = self.getContent(vin_dict["6to7"], vinArray[5:7])
        result[vin_dict["8"]] = self.getContent(vin_dict["8"], vinArray[7])
        result[vin_dict["10"]] = self.getContent(vin_dict["10"], vinArray[9])
        return result

    # 获得北京汽车集团有限公司VIN解析结果
    def getBJQC(self):
        vinArray = bytes(self.vin)
        vin_dict_LNB_LPB = {"1to3": "WMI", "4": "VTYPE", "5": "LENGTH&SEATING", "6": "BTYPE", "7": "ENGINE", \
                        "8": "RESTRAINT","10": "YEAR", "11": "ASSEMBLY"}
        vin_dict_LHB = {"1to3": "WMI", "4": "VTYPE", "5": "TCARGO&CCARGO", "6": "BTYPE", "7": "ENGINE",\
                        "8": "WHEELBASE","10": "YEAR", "11": "ASSEMBLY"}
        vin_dict_LMB = {"1to3": "WMI", "4": "PPOSITION", "5": "TCARGO&CCARGO", "6": "BTYPE", "7": "ENGINE",\
                        "8": "WHEELBASE","10": "YEAR", "11": "ASSEMBLY"}
        vin_dict_LJB = {"1to3": "WMI", "4": "VTYPE", "5": "TCARGO&CCARGO", "6": "BTYPE", "7": "BRAKE", \
                        "8": "WHEELBASE","10": "YEAR", "11": "ASSEMBLY"}

        wmi = vinArray[:3]
        if wmi == 'LHB':
            vin_dict = vin_dict_LHB
        elif wmi == 'LMB':
            vin_dict = vin_dict_LMB
        elif wmi == 'LJB':
            vin_dict = vin_dict_LJB
        elif wmi == 'LNB' or wmi == 'LPB':
            vin_dict = vin_dict_LNB_LPB
        else:
            return 'Illegal VIN'
        temp = self.__content[wmi]
        result= {vin_dict["1to3"] : self.getContent(vin_dict["1to3"], wmi)}
        # 此循环不调用getContent方法，因为数据有差异
        for i in range(3, 8):
            if i != 8:
                try:
                    result[vin_dict[str(i + 1)]] = temp[vin_dict[str(i + 1)]][vinArray[i]]
                except Exception, e:
                    result[vin_dict[str(i + 1)]] = 'null'
                    print 'Illegal parameters：' + e.message
            else:
                pass
        result[vin_dict["10"]] = self.getContent(vin_dict["10"], vinArray[9])
        result[vin_dict["11"]] = self.getContent(vin_dict["11"], vinArray[10])
        return result

    # 获得东风商用车VIN解析结果
    def getDFSYC(self):
        vinArray = bytes(self.vin)
        vin_dict_car = {"1to3": "WMI", "4": "VTYPE", "5": "CAR_BODY_STYLE", "6": "CAR_ENGINE", "7": "CAR_BUS_TYPE",
                            "8": "NON_TRAILER_AXLEBASE", "10": "YEAR", "11": "ASSEMBLY"}
        vin_dict_bus = {"1to3": "WMI", "4": "VTYPE", "5": "BUS_CHASSIS_LENGTH", "6": "TRUCK_BUS_ENGINE", "7": "CAR_BUS_TYPE",
                        "8": "NON_TRAILER_AXLEBASE", "10": "YEAR", "11": "ASSEMBLY"}
        vin_dict_buschassis = {"1to3": "WMI", "4": "VTYPE", "5": "BUS_CHASSIS_LENGTH", "6": "TRUCK_BUS_ENGINE", "7": "BUS_CHASSIS",
                        "8": "NON_TRAILER_AXLEBASE", "10": "YEAR", "11": "ASSEMBLY"}
        vin_dict_trailer = {"1to3": "WMI", "4": "VTYPE", "5": "NON_CAR_BUS_TMASS", "6": "TRAILER_AXLE_V", "7": "TRAILER_STYLE",
                               "8": "TRAILER_LENGTH", "10": "YEAR", "11": "ASSEMBLY"}
        vin_dict_truck = {"1to3": "WMI", "4": "VTYPE", "5": "NON_CAR_BUS_TMASS", "6": "TRUCK_BUS_ENGINE", "7": "TRUCK_DRIVE",
                               "8": "NON_TRAILER_AXLEBASE", "10": "YEAR", "11": "ASSEMBLY"}
        vin_dict_truckchassis = {"1to3": "WMI", "4": "VTYPE", "5": "NON_CAR_BUS_TMASS", "6": "TRUCK_BUS_ENGINE", "7": "TRUCK_DRIVE",
                          "8": "NON_TRAILER_AXLEBASE", "10": "YEAR", "11": "ASSEMBLY"}
        vType = self.getContent("VTYPE", vinArray[3])
        temp_vType = vType.split(' ')
        temp0 = temp_vType[0].encode('utf-8')

        if temp0 == '乘用车':
            vin_dict = vin_dict_car
        elif temp0 == '客车':
            vin_dict = vin_dict_bus
        elif temp0 == '客车底盘':
            vin_dict = vin_dict_buschassis
        elif temp0 == '挂车':
            vin_dict = vin_dict_trailer
        elif temp_vType[1].encode('utf-8') == '完整车辆':
            vin_dict = vin_dict_truck
        else:
            vin_dict = vin_dict_truckchassis
        return self.singleMarkVin(vin_dict, vinArray)

    # 获得一汽大众VIN解析结果
    def getYQDZ(self):
        vinArray = bytes(self.vin)
        vin_dict = {"1to3": "WMI", "4": "ENGINE_MOTOR_CAPACITY", "5": "CAR_BODY_STYLE", "6": "ENGINE", "7to8": "VTYPE", "10": "YEAR",
                    "11": "ASSEMBLY"}
        return self.mergeMarkVin(vin_dict, vinArray)

    # 获得大众进口车VIN解析结果
    def getDZJK(self):
        vinArray = bytes(self.vin)
        vin_dict = {"1to3": "WMI", "4": "VMODEL", "5": "MOTOR", "6": "RESTRAINT",
                    "7to8": "VTYPE", "10": "YEAR", "11": "ASSEMBLY"}
        return self.mergeMarkVin(vin_dict, vinArray)




