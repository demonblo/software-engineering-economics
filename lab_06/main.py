import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QMainWindow, QTableWidgetItem

from PyQt5.QtWidgets import QApplication

import math

from matplotlib import pyplot



standart_eaf = {
    'RELY': 1,  # требуемая надежность 0.75-1.4
    'DATA': 1,  # Размер быза даннных 0.94-1.16
    'CPLX': 1,  # Сложность продукта 0.70-1.65
    'TIME': 1,  # Ограничение времени выполнения 1-1.65
    'STOR': 1,  # Ограничение объема основной памяти 1-1.56
    'VIRT': 1,  # Изменчивость виртуальной машины 0.87-1.3
    'TURN': 1,  # Время реакции компьютера 0.8-1.3
    'ACAP': 1,  # Способности аналитика 1.46-0.71
    'AEXP': 1,  # Знание приложений 1.29-0.82
    'PCAP': 1,  # Способности программиста 1.42-0.7
    'VEXP': 1,  # Знание виртуальной машины 1.21 - 0.9
    'LEXP': 1,  # Знание языка программирования  1.14-0.95
    'MODP': 1,  # Использование современных методов 1.24-0.8
    'TOOL': 1,  # Использование программных инструментов 1.24-0.83
    'SCED': 1,  # Требуемые сроки разработки 1.23-1.1
}

base_code_value = 25  # 000

def get_standart_eaf():
    return standart_eaf.copy()


def normal_variant(eaf, size):
    work = 3.2 * eaf * (size ** 1.05)
    time = 2.5 * (work ** 0.38)
    return {
        'work': work,
        'time': time
    }


def inter_variant(eaf, size):
    work = 3.0 * eaf * (size ** 1.12)
    time = 2.5 * (work ** 0.35)
    return {
        'work': work,
        'time': time
    }


def inbuild_variant(eaf, size):
    work = 2.8 * eaf * (size ** 1.2)
    time = 2.5 * (work ** 0.32)
    return {
        'work': work,
        'time': time
    }


def calc_eaf(eaf_list):
    eaf = 1
    for i in eaf_list.keys():
        eaf *= eaf_list[i]
    return eaf


def GraphExperiment(eaf, mode,  attr_values, attr_name):
    code_size = 300
    model_work = []
    model_time = []

    for attr in attr_values:
        eaf[attr_name] = attr
        if mode == 'normal':
            result = cocomo(code_size=code_size,
                            eaf_list=eaf,
                            variant_func=normal_variant)
        elif mode == 'inter':
            result = cocomo(code_size=code_size,
                            eaf_list=eaf,
                            variant_func=inter_variant)
        else:
            result = cocomo(code_size=code_size,
                            eaf_list=eaf,
                            variant_func=inbuild_variant)

        model_work.append(result['work'])
        model_time.append(result['time'])
        
    return [model_work, model_time]


def graphs(): 
    
    cplx_values = [0.7, 1, 1.3] 
    modes = ['обычный', 'промежуточный', 'встроенный']

    for cplx in cplx_values:
        for mode in modes:
            figure, ax = pyplot.subplots(figsize=(15, 10))
            pyplot.subplots_adjust(hspace=0.5)
            pyplot.grid()
            eaf = get_standart_eaf()
            eaf['CPLX'] = cplx
            
            acap_result = GraphExperiment(eaf, mode, [1.46, 1.19, 1.0, 0.86, 0.71], 'ACAP')
            eaf = get_standart_eaf()
            eaf['CPLX'] = cplx
            aexp_result = GraphExperiment(eaf, mode, [1.29, 1.15, 1.0, 0.91, 0.82], 'AEXP')
            eaf = get_standart_eaf()
            eaf['CPLX'] = cplx
            pcap_result = GraphExperiment(eaf, mode, [1.42, 1.17, 1.0, 0.86, 0.70], 'PCAP')
            eaf = get_standart_eaf()
            eaf['CPLX'] = cplx
            lexp_result = GraphExperiment(eaf, mode, [1.14, 1.07, 1.0, 0.95], 'LEXP')

            pyplot.subplot(121)
            pyplot.title("Трудозатраты Режим: " + mode + " ( CPLX=" + str(cplx) + ")")
            pyplot.plot(['очень низкий', 'низкий', 'номинальный', 'высокий', 'очень высокий'], acap_result[0],'m', label='ACAP')
            pyplot.plot(['очень низкий', 'низкий', 'номинальный', 'высокий', 'очень высокий'], aexp_result[0],'k', label='AEXP')
            pyplot.plot(['очень низкий', 'низкий', 'номинальный', 'высокий', 'очень высокий'], pcap_result[0],'g', label='PCAP')
            pyplot.plot(['очень низкий', 'низкий', 'номинальный', 'высокий'], lexp_result[0], 'b',label='LEXP')
            pyplot.ylabel("PM")
            pyplot.legend()

            pyplot.subplot(122)
            pyplot.title("Время Режим: " + mode + " ( CPLX=" + str(cplx) + ")")
            pyplot.plot(['очень низкий', 'низкий', 'номинальный', 'высокий', 'очень высокий'], acap_result[1], 'm', label='ACAP')
            pyplot.plot(['очень низкий', 'низкий', 'номинальный', 'высокий', 'очень высокий'], aexp_result[1], 'k', label='AEXP')
            pyplot.plot(['очень низкий', 'низкий', 'номинальный', 'высокий', 'очень высокий'], pcap_result[1], 'g', label='PCAP')
            pyplot.plot(['очень низкий', 'низкий', 'номинальный', 'высокий'], lexp_result[1],'b', label='LEXP')
            pyplot.ylabel("TM")
            pyplot.legend()
            pyplot.show()


def cocomo(code_size, eaf_list, variant_func):
    eaf = calc_eaf(eaf_list)
    return variant_func(eaf, code_size)


def simple_expirement(eaf, code_size, mode, basic_salary):
    code_size /=1000
    result = {}
    if mode == 'normal':
        
        result = cocomo(code_size=code_size,
                        eaf_list=eaf,
                        variant_func=normal_variant)
    elif mode == 'inter':
        result = cocomo(code_size=code_size,
                        eaf_list=eaf,
                        variant_func=inter_variant)
    else:
        
        result = cocomo(code_size=code_size,
                        eaf_list=eaf,
                        variant_func=inbuild_variant)

    traditional_result = result
   
    plan_work = result['work'] * 0.08
    plan_time = result['time'] * 0.36
    plan_workers = math.ceil(plan_work / plan_time)

    design_work = result['work'] * 0.18
    design_time = result['time'] * 0.36
    design_workers = math.ceil(design_work / design_time)

    detail_work = result['work'] * 0.25
    detail_time = result['time'] * 0.18
    detail_workers = math.ceil(detail_work / detail_time)

    coding_work = result['work'] * 0.26
    coding_time = result['time'] * 0.18
    coding_workers = math.ceil(coding_work / coding_time)

    integration_work = result['work'] * 0.31
    integration_time = result['time'] * 0.28
    integration_workers = math.ceil(integration_work / integration_time)

    all_works_traditional = [
        plan_work,
        design_work,
        detail_work,
        coding_work,
        integration_work,
    ]

    all_times_traditional = [
        plan_time,
        design_time,
        detail_time,
        coding_time,
        integration_time,
    ]

    workers = [
        plan_workers,
        design_workers,
        detail_workers,
        coding_workers,
        integration_workers,
    ]

    result['work'] += plan_work

    analyz = round(result['work'] * 0.04)
    design = round(result['work'] * 0.12)
    coding = round(result['work'] * 0.44)
    planning = round(result['work'] * 0.06)
    verification = round(result['work'] * 0.14)
    office = round(result['work'] * 0.07)
    quality = round(result['work'] * 0.07)
    manuals = round(result['work'] * 0.06)


    all_works = [
        analyz,
        design,
        coding,
        planning,
        verification,
        office,
        quality,
        manuals
    ]

    sum_work = sum(all_works)

    Xdata = []
    Ydata = []

    summa = 0

    for i in range(len(all_times_traditional)):
        time = summa
        while (time < summa + all_times_traditional[i]):
            Xdata.append(time)
            Ydata.append(workers[i])
            time += 0.01
        summa += all_times_traditional[i]

    pyplot.title('Работники')
    pyplot.grid(True)
    
    pyplot.plot(Xdata, Ydata, 'm')
    '''
    fig, ax = pyplot.subplots()

    ax.bar(x, y)

    ax.set_facecolor('seashell')
    fig.set_facecolor('floralwhite')
    fig.set_figwidth(12)    #  ширина Figure
    fig.set_figheight(6)    #  высота Figure
    '''
    pyplot.xlabel("Месяцы")
    pyplot.ylabel("Количество работников")
    pyplot.show()

    budget_list = []
    kp = 1.2
    ka = 1.3
    if eaf['ACAP'] == 1.46:
        ka = 1
    if eaf['ACAP'] == 0.71:
        ka = 1.5
    if eaf['PCAP'] == 1.42:
        kp = 0.9
    if eaf['PCAP'] == 0.7:
        kp = 1.6
   
    salary = {
        "Programmer": basic_salary * kp,
        "Analytic": basic_salary * ka,
        "Manager": basic_salary ,
        "Tester": basic_salary * 0.6,
        "Architector": basic_salary * 1.4,
    }
    print(ka,kp)

    times = all_times_traditional
    x1 = [(salary['Manager'] + salary['Analytic']) * times[0]]
    budget_list += [(salary['Manager'] + salary['Analytic']) * times[0]]
    x2 = [(salary['Programmer'] + salary['Architector'] + + salary['Analytic'])  * times[1]]
    budget_list += [(salary['Programmer'] + salary['Architector'] + + salary['Analytic'])  * times[1]]
    x3 = [(3*salary['Programmer'] + 3*salary['Architector'] + salary['Analytic']) * times[2]]
    budget_list += [(3*salary['Programmer'] + 3*salary['Architector'] + salary['Analytic']) * times[2]]
    x4 = [(5*salary['Programmer'] + 3* salary['Tester']) * times[3]]
    budget_list += [(5*salary['Programmer'] + 3* salary['Tester']) * times[3]]
    x5 = [(salary['Programmer'] + 4*salary['Tester'] + salary['Analytic']) * times[4]]
    budget_list += [(salary['Programmer'] + 4*salary['Tester'] + salary['Analytic']) * times[4]]
    x6 = [(salary['Programmer'])  * times[1] + (3*salary['Programmer']) * times[2] +(5*salary['Programmer']) * times[3] +(salary['Programmer']) * times[4]]
    x7 = [(salary['Analytic'])  * times[0] + (salary['Analytic'])  * times[1] + (salary['Analytic']) * times[2] +(salary['Analytic']) * times[3] +(salary['Analytic']) * times[4]]
    print("Планирование",x1)
    print("Проектирование продукта",x2)
    print("етальное проектирование",x3)
    print("Kодирование и тестирование",x4)
    print("Интеграция и тестирование",x5)
    print("Всего програмиист", x6)
    print("Всего аналитик", x7)
    sum_budget = 0
    for i in range(len(budget_list)):
        sum_budget += budget_list[i]
    
    print("Всего",sum_budget )
    return {
        'work': traditional_result['work'],
        'time': traditional_result['time'],
        'works_t': all_works_traditional,
        'times_t': all_times_traditional,
        'workers': workers,
        'works': all_works,
        'budget': sum_budget,
       
    }


class MyWindow(QMainWindow):
    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi("window2.ui", self)

        self.StartWorkButton.clicked.connect(lambda: self.startWork())
        self.GraphButton.clicked.connect(lambda: self.drawGraph())

    def startWork(self):
        eaf = standart_eaf
        eaf['RELY'] = float(self.RELYComboBox.currentText())
        eaf['DATA'] = float(self.DATAComboBox.currentText())
        eaf['CPLX'] = float(self.CPLXComboBox.currentText())
        eaf['TIME'] = float(self.TIMEComboBox.currentText())
        eaf['STOR'] = float(self.STORComboBox.currentText())
        eaf['VIRT'] = float(self.VIRTComboBox.currentText())
        eaf['TURN'] = float(self.TURNComboBox.currentText())
        eaf['ACAP'] = float(self.ACAPComboBox.currentText())
        eaf['AEXP'] = float(self.AEXPComboBox.currentText())
        eaf['PCAP'] = float(self.PCAPComboBox.currentText())
        eaf['VEXP'] = float(self.VEXPComboBox.currentText())
        eaf['LEXP'] = float(self.LEXPComboBox.currentText())
        eaf['MODP'] = float(self.MODPComboBox.currentText())
        eaf['TOOL'] = float(self.TOOLComboBox.currentText())
        eaf['SCED'] = float(self.SCEDComboBox.currentText())

        code_size = int(self.SizeSpinBox.value())
        basic_salary =  int(self.SalarySpinBox.value())
        mode = 'normal'
        if self.NormalRadioButton.isChecked():
            mode = 'normal'
        elif self.InterRadioButton.isChecked():
            mode = 'inter'
        elif self.InbuildRadioButton.isChecked():
            mode = 'inbuild'
        #print(mode)

        result = simple_expirement(eaf, code_size, mode, basic_salary)
        #print(result)
    
        self.WorkWithoutLineEdit.setText(str(int(result['work'])))
        self.TimeWithoutLineEdit.setText(str(result['time']))
        
        
        plan_work = int(result['work'] + result['works_t'][0])
        plan_time = result['time'] + result['times_t'][0]
   
        self.WorkWithLineEdit.setText(str(plan_work))
        self.TimeWithLineEdit.setText(str(plan_time))
        self.CostLineEdit.setText(str(result['budget']))
        
    
        
        for i in range(len(result['works_t'])):
            el = result['works_t'][i]
     
            self.TraditionTable.setItem(i, 0, QTableWidgetItem(str('{:.3g}'.format(el))))
    
        for i in range(len(result['times_t'])):
            el = result['times_t'][i]
      
            self.TraditionTable.setItem(i, 1, QTableWidgetItem(str('{:.3g}'.format(el))))
        #for i in range(len(result['workers'])):
        #    el = result['workers'][i]
        #    self.TraditionTable.setItem(i, 2, QTableWidgetItem(str(el)))
        for i in range(len(result['works'])):
            el = result['works'][i]
            self.WbsTable.setItem(i, 0, QTableWidgetItem(str('{:.3g}'.format(el))))
    
    def drawGraph(self):
        graphs()


if __name__ == '__main__':
    app = QApplication([])
    application = MyWindow()
    application.show()

    sys.exit(app.exec())
