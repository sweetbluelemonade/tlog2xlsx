import re
from datetime import datetime

class LogProcessing:
    @staticmethod
    def __xmotion_hw2_pir(data : str):
        sn = re.search(r'SN:([0-9A-Fa-f]+)', data).group(1)
        results = re.findall(r'DUT:GET_PIR:.*?SP', data, 
                             re.DOTALL | re.MULTILINE)
        pir_table = []

        for i in results:
            day, month, year, hour, minute, second = re.search(r'(\d{2})\.(\d{2})\.(\d{4}) (\d{2}):(\d{2}):(\d{2})', 
                                                               i).groups()
            time = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))

            cleaned = re.sub(r"(\d{2}\.\d{2}\.\d{4}\s+\d{2}:\d{2}:\d{2}\.\d{3}|<==|SP|DUT:GET_PIR: |\n|\s{2,}|\t|\u0000|\u0020)", "", i).split(",")
            cleaned = cleaned[0:6] + [cleaned[7], cleaned[9]]
            print(i)
            print(cleaned)

            pir_table.append([time, sn] + [int(a) for a in cleaned])

        paged_table = {
                "PIR" : pir_table
            }

        return paged_table

    __KEYED_HEADERS = {
        'xmotion_hw2_pir' : {"PIR" : [["Time", "SN", "SP", "CP", "SM", "CM", "CCP", "CCM", "NP", "NM"]]}
    }
    __KEYED_LOGPROCESSORS = {
        'xmotion_hw2_pir' : __xmotion_hw2_pir
    }

    @staticmethod
    def get_rows(ltype : str, data : str):
        if ltype in LogProcessing.__KEYED_LOGPROCESSORS:
            return LogProcessing.__KEYED_LOGPROCESSORS[ltype](data)
        else:
            raise ValueError('Bad log type')
    
    @staticmethod
    def get_headers(ltype : str):
        if ltype in LogProcessing.__KEYED_HEADERS:
            return LogProcessing.__KEYED_HEADERS[ltype]
        else:
            raise ValueError('Bad log type')

    