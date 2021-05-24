
csv_file_lga = ['LGA_2011_QLD.csv', 'LGA_2011_OT.csv', 'LGA_2011_NSW.csv', 'LGA_2011_TAS.csv', 'LGA_2011_ACT.csv', 'LGA_2011_WA.csv', 'LGA_2011_NT.csv', 'LGA_2011_SA.csv', 'LGA_2011_VIC.csv']

def generate_lga_city():
    lga_city={}
    for filename in csv_file_lga:
        f = open(filename,'r')
        f.readline()
        for line in f:
            line = line.split(',')
            #print(line)
            lga_code = line[1][1:len(line[1])-1]
            if lga_code not in lga_city:
                city = line[2][1:len(line[2])-1]
                #print(city)
                city_list = city.split('(')
                #print(city_list)
                if city_list[0][-1] == ' ':
                    city_name = city_list[0][:len(city_list[0])-1]
                else:
                    city_name = city_list[0]
                # print(city_name+'#')
                lga_city[lga_code] = city_name
    return lga_city


def city_socio_enconomic(lga_city):
    city_enconomic_index = {}
    with open('by Local Government Area.csv', 'r') as f:
        f.readline()
        count = 0
        for line in f:
            line = line.split(',')
            city_enconomic_index[lga_city[line[1]]] = line[2]

    #print(city_enconomic_index)
    return city_enconomic_index

lga_city = generate_lga_city()

city_enconomic_index = city_socio_enconomic(generate_lga_city())