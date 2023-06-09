def vehicleClass():
    data = {1: {'results': [{'id': 1, 'name': 'Sedan'}]},
            12: {'results': [{'id': 1, 'name': 'Sedan'}, {'id': 12, 'name': 'Comfort Sedan '}]},
            41: {'results': [{'id': 1, 'name': 'Sedan'}, {'id': 41, 'name': 'EV Sedan'}]},
            42: {'results': [{'id': 1, 'name': 'Sedan'}, {'id': 41, 'name': 'EV Sedan'},
                             {'id': 42, 'name': 'EV Business Sedan'}, {'id': 2, 'name': 'Business Sedan'}]},
            2: {'results': [{'id': 1, 'name': 'Sedan'}, {'id': 12, 'name': 'Comfort Sedan '},
                            {'id': 2, 'name': 'Business Sedan'}]},
            43: {'results': [{'id': 1, 'name': 'Sedan'}, {'id': 41, 'name': 'EV Sedan'},
                             {'id': 42, 'name': 'EV Business Sedan'}, {'id': 2, 'name': 'Business Sedan'},
                             {'id': 43, 'name': 'EV First Class Sedan'}, {'id': 40, 'name': 'First Class'}]},
            40: {'results': [{'id': 1, 'name': 'Sedan'}, {'id': 12, 'name': 'Comfort Sedan '},
                             {'id': 2, 'name': 'Business Sedan'}, {'id': 40, 'name': 'First Class'}]},
            44: {'results': [{'id': 44, 'name': 'Rolls Royce Ghost'}]},
            45: {'results': [{'id': 45, 'name': 'Rolls Royce Phantom'}]},
            46: {'results': [{'id': 46, 'name': 'Bentley'}]},
            47: {'results': [{'id': 47, 'name': 'Classic Car'}]},
            6: {'results': [{'id': 1, 'name': 'Sedan'}, {'id': 6, 'name': 'MPV-4'}]},
            13: {'results': [{'id': 1, 'name': 'Sedan'}, {'id': 2, 'name': 'Business Sedan'},
                             {'id': 6, 'name': 'MPV-4'}, {'id': 13, 'name': 'Business MPV-4'}]},
            3: {'results': [{'id': 1, 'name': 'Sedan'}, {'id': 6, 'name': 'MPV-4'}, {'id': 3, 'name': 'MPV5'}]},
            48: {'results': [{'id': 1, 'name': 'Sedan'}, {'id': 41, 'name': 'EV Sedan'}, {'id': 48, 'name': 'EV SUV'}]},
            49: {'results': [{'id': 1, 'name': 'Sedan'}, {'id': 41, 'name': 'EV Sedan'},
                             {'id': 42, 'name': 'EV Business Sedan'}, {'id': 2, 'name': 'Business Sedan'},
                             {'id': 6, 'name': 'MPV-4'}, {'id': 48, 'name': 'EV SUV'},
                             {'id': 49, 'name': 'EV Business SUV'}]},
            4: {'results': [{'id': 1, 'name': 'Sedan'}, {'id': 2, 'name': 'Business Sedan'},
                            {'id': 6, 'name': 'MPV-4'}, {'id': 13, 'name': 'Business MPV-4'},
                            {'id': 3, 'name': 'MPV5'}, {'id': 4, 'name': 'Business MPV5'}]},
            36: {'results': [{'id': 1, 'name': 'Sedan'}, {'id': 2, 'name': 'Business Sedan'},
                             {'id': 6, 'name': 'MPV-4'}, {'id': 3, 'name': 'MPV5'}, {'id': 4, 'name': 'Business MPV5'},
                             {'id': 36, 'name': 'Business Van'}]},
            50: {'results': [{'id': 50, 'name': 'Wheelchair Van'}]},
            51: {'results': [{'id': 50, 'name': 'Wheelchair Van'},
                             {'id': 51, 'name': 'wheelchair minibus'}]},
            52: {'results': [{'id': 1, 'name': 'Sedan'}, {'id': 52, 'name': 'School Minivan'}]},
            21: {'results': [{'id': 21, 'name': '6 Passenger Stretch Sedan'}]},
            22: {'results': [{'id': 21, 'name': '6 Passenger Stretch Sedan'},
                             {'id': 22, 'name': '8 Passenger Stretch Sedan'}]},
            23: {'results': [{'id': 21, 'name': '6 Passenger Stretch Sedan'},
                             {'id': 22, 'name': '8 Passenger Stretch Sedan'},
                             {'id': 23, 'name': '10 Passenger Stretch Sedan'}]},
            24: {'results': [{'id': 21, 'name': '6 Passenger Stretch Sedan'},
                             {'id': 22, 'name': '8 Passenger Stretch Sedan'},
                             {'id': 23, 'name': '10 Passenger Stretch Sedan'},
                             {'id': 24, 'name': '12 Passenger Stretch SUV'}]},
            27: {'results': [{'id': 21, 'name': '6 Passenger Stretch Sedan'},
                             {'id': 22, 'name': '8 Passenger Stretch Sedan'},
                             {'id': 23, 'name': '10 Passenger Stretch Sedan'},
                             {'id': 24, 'name': '12 Passenger Stretch SUV'},
                             {'id': 27, 'name': '16 Passenger Stretch Limo'}]},
            25: {'results': [{'id': 25, 'name': '12 Passenger Party Bus'}]},
            26: {'results': [{'id': 25, 'name': '12 Passenger Party Bus'},
                             {'id': 26, 'name': '14 Passenger Party Bus'}]},
            28: {'results': [{'id': 25, 'name': '12 Passenger Party Bus'}, {'id': 26, 'name': '14 Passenger Party Bus'},
                             {'id': 28, 'name': '23 passenger party bus'}]},
            5: {'results': [{'id': 6, 'name': 'MPV-4'}, {'id': 3, 'name': 'MPV5'}, {'id': 5, 'name': 'Minibus-8'}]},
            9: {'results': [{'id': 6, 'name': 'MPV-4'}, {'id': 3, 'name': 'MPV5'}, {'id': 5, 'name': 'Minibus-8'},
                            {'id': 9, 'name': 'Minibus-10'}]},
            10: {'results': [{'id': 6, 'name': 'MPV-4'}, {'id': 3, 'name': 'MPV5'}, {'id': 5, 'name': 'Minibus-8'},
                             {'id': 9, 'name': 'Minibus-10'}, {'id': 10, 'name': 'Minibus-12'}]},
            11: {'results': [{'id': 6, 'name': 'MPV-4'}, {'id': 3, 'name': 'MPV5'}, {'id': 5, 'name': 'Minibus-8'},
                             {'id': 9, 'name': 'Minibus-10'}, {'id': 10, 'name': 'Minibus-12'},
                             {'id': 11, 'name': 'Minibus-14'}]},
            56: {'results': [{'id': 56, 'name': '9-School Minibus'}]},
            57: {'results': [{'id': 56, 'name': '9-School Minibus'}, {'id': 57, 'name': '14-School Minibus'}]},
            29: {'results': [{'id': 5, 'name': 'Minibus-8'}, {'id': 9, 'name': 'Minibus-10'},
                             {'id': 10, 'name': 'Minibus-12'}, {'id': 11, 'name': 'Minibus-14'},
                             {'id': 29, 'name': '16-seat Bus'}]},
            30: {'results': [{'id': 5, 'name': 'Minibus-8'}, {'id': 9, 'name': 'Minibus-10'},
                             {'id': 10, 'name': 'Minibus-12'}, {'id': 11, 'name': 'Minibus-14'},
                             {'id': 29, 'name': '16-seat Bus'}, {'id': 30, 'name': '20-seat Bus'}]},
            31: {'results': [{'id': 5, 'name': 'Minibus-8'}, {'id': 9, 'name': 'Minibus-10'},
                             {'id': 10, 'name': 'Minibus-12'}, {'id': 11, 'name': 'Minibus-14'},
                             {'id': 29, 'name': '16-seat Bus'}, {'id': 30, 'name': '20-seat Bus'},
                             {'id': 31, 'name': '23-seat Bus'}]},
            32: {'results': [{'id': 5, 'name': 'Minibus-8'}, {'id': 9, 'name': 'Minibus-10'},
                             {'id': 10, 'name': 'Minibus-12'}, {'id': 11, 'name': 'Minibus-14'},
                             {'id': 29, 'name': '16-seat Bus'}, {'id': 30, 'name': '20-seat Bus'},
                             {'id': 31, 'name': '23-seat Bus'}, {'id': 32, 'name': '27-seat Bus'}]},
            33: {'results': [{'id': 5, 'name': 'Minibus-8'}, {'id': 9, 'name': 'Minibus-10'},
                             {'id': 10, 'name': 'Minibus-12'}, {'id': 11, 'name': 'Minibus-14'},
                             {'id': 29, 'name': '16-seat Bus'}, {'id': 30, 'name': '20-seat Bus'},
                             {'id': 31, 'name': '23-seat Bus'}, {'id': 32, 'name': '27-seat Bus'},
                             {'id': 33, 'name': '36-seat Bus'}]},
            34: {'results': [{'id': 29, 'name': '16-seat Bus'}, {'id': 30, 'name': '20-seat Bus'},
                             {'id': 31, 'name': '23-seat Bus'}, {'id': 32, 'name': '27-seat Bus'},
                             {'id': 33, 'name': '36-seat Bus'}, {'id': 34, 'name': '44-seat Coach Bus'}]},
            35: {'results': [{'id': 29, 'name': '16-seat Bus'}, {'id': 30, 'name': '20-seat Bus'},
                             {'id': 31, 'name': '23-seat Bus'}, {'id': 32, 'name': '27-seat Bus'},
                             {'id': 33, 'name': '36-seat Bus'}, {'id': 34, 'name': '44-seat Coach Bus'},
                             {'id': 35, 'name': '55-seat Coach Bus'}]},
            58: {'results': [{'id': 58, 'name': '16-School bus'}]},
            59: {'results': [{'id': 58, 'name': '16-School bus'}, {'id': 59, 'name': '20-School bus'}]},
            60: {'results': [{'id': 58, 'name': '16-School bus'}, {'id': 59, 'name': '20-School bus'},
                             {'id': 60, 'name': '23-School bus'}]},
            61: {'results': [{'id': 58, 'name': '16-School bus'}, {'id': 59, 'name': '20-School bus'},
                             {'id': 60, 'name': '23-School bus'}, {'id': 61, 'name': '30-School bus'}]},
            62: {'results': [{'id': 58, 'name': '16-School bus'}, {'id': 59, 'name': '20-School bus'},
                             {'id': 60, 'name': '23-School bus'}, {'id': 61, 'name': '30-School bus'},
                             {'id': 62, 'name': '36-School Bus'}]},
            63: {'results': [{'id': 58, 'name': '16-School bus'}, {'id': 59, 'name': '20-School bus'},
                             {'id': 60, 'name': '23-School bus'}, {'id': 61, 'name': '30-School bus'},
                             {'id': 62, 'name': '36-School Bus'}, {'id': 63, 'name': '44-School Bus'}]},
            64: {'results': [{'id': 58, 'name': '16-School bus'}, {'id': 59, 'name': '20-School bus'},
                             {'id': 60, 'name': '23-School bus'}, {'id': 61, 'name': '30-School bus'},
                             {'id': 62, 'name': '36-School Bus'}, {'id': 63, 'name': '44-School Bus'},
                             {'id': 64, 'name': '72-School bus'}]},
            0:{}}
    return data

if __name__ == "__main__":
    print(len(vehicleClass()))