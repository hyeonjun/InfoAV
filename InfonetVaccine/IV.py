# -*- coding:utf-8 -*-
import datetime
import os
import sys
import types
import IVconst
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import AllScan

class IV(QMainWindow, AllScan.Ui_AllScanWindow):
    def __init__(self, path, set1, set2, parent = None):
        super(QMainWindow, self).__init__(parent)

        self.path = path
        self.set1 = set1  # arc_file scan?
        self.set2 = set2  # automatic treatment?

        self.initUI(self)
        self.main()



        self.g_scan_time = None


    def define_options(self):
        options = []
        if self.set1 == 2:
            options.append(True)
        else:
            options.append(False)
        if self.set2 == 2:
            options.append(True)
        else:
            options.append(False)

        options.append(False)



        return options


    # -----------------------------------------------------------
    # 악성코드 결과를 한 줄 에 출력하기 위한 함수
    # -----------------------------------------------------------
    def convert_display_filename(self, real_filename):
        # 출력용 이름
        fsencoding = sys.getfilesystemencoding() or sys.getdefaultencoding()
        if isinstance(real_filename, types.UnicodeType):
            display_filename = real_filename.encode(sys.stdout.encoding, 'replace')
        else:
            display_filename = unicode(real_filename, fsencoding).encode(sys.stdout.encoding, 'replace')

        if display_filename[0] == '/' or display_filename[0] == '\\':
            return display_filename[1:]
        else:
            return display_filename


    def display_line(self, filename, message):
        filename += ' '
        filename = self.convert_display_filename(filename)
        len_fname = len(filename)
        len_msg = len(message)

        if len_fname + 1 + len_msg < 64:
            fname = '%s' % filename
        else:
            able_size = 64 - len_msg
            able_size -= 5  # ...
            min_size = able_size / 2
            if able_size % 2 == 0:
                fname1 = filename[:min_size - 1]
            else:
                fname1 = filename[:min_size]
            fname2 = filename[len_fname - min_size:]
            fname = '%s ... %s' % (fname1, fname2)
        # print fname + ' ' + message
        return fname + ' ' + message

    # -----------------------------------------------------------
    # scan의 콜백 함수
    # -----------------------------------------------------------
    def scan_callback(self, ret_value):
        global g_option
        fs = ret_value['file_struct']

        if len(fs.get_additional_filename()) != 0:
            disp_name = '%s (%s)' % (fs.get_master_filename(),
                                     fs.get_additional_filename())
        else:
            disp_name = '%s' % (fs.get_master_filename())

        if ret_value['result']:
            state = 'infected'

            vname = ret_value['virus_name']
            message = '%s : %s' % (state, vname)
        else:
            message = 'ok'
        self.ScanInfo.append(str(self.display_line(disp_name, message)))


    # -----------------------------------------------------------
    # disinfect의 콜백 함수
    # -----------------------------------------------------------
    def disinfect_callback(self, ret_value, action_type):
        fs = ret_value['file_struct']
        message = ''

        if len(fs.get_additional_filename()) != 0:
            disp_name = '%s (%s)' % (fs.get_master_filename(),
                                     fs.get_additional_filename())
        else:
            disp_name = '%s' % (fs.get_master_filename())

        if fs.is_modify():  # 수정 성공?
            if action_type == IVconst.K2_ACTION_DISINFECT:
                message = 'disinfected'
            elif action_type == IVconst.K2_ACTION_DELETE:
                message = 'deleted'

        else:  # 수정 실패
            if action_type == IVconst.K2_ACTION_DISINFECT:
                message = 'disinfected failed'
            elif action_type == IVconst.K2_ACTION_DELETE:
                message = 'deleted failed'

        self.ScanInfo.append(str(self.display_line(disp_name, message)))

    # -----------------------------------------------------------
    # update의 콜백 함수
    # -----------------------------------------------------------
    def update_callback(self, ret_file_info):
        if ret_file_info.is_modify():  # 수정되었다면 결과 출력
            disp_name = ret_file_info.get_filename()

            message = 'updated'
            self.display_line(disp_name, message)
            self.ScanInfo.append(str(self.display_line(disp_name, message)))

    # -----------------------------------------------------------
    # print_result(result)
    # 악성코드 검사 결과를 출력한다.
    # 입력값 : result - 악성코드 검사 결과
    # -----------------------------------------------------------
    def print_result(self, result):
        self.ResultInfo.append('Results:')
        self.ResultInfo.append('Folders               :%d' % result['Folders'])
        self.ResultInfo.append('Files                 :%d' % result['Files'])
        self.ResultInfo.append('Packed                :%d' % result['Packed'])
        self.ResultInfo.append('Infected files        :%d' % result['Infected_files'])
        self.ResultInfo.append('Identified viruses    :%d' % result['Identified_viruses'])
        if result['Disinfected_files']:
            self.ResultInfo.append('Disinfected files :%d' % result['Disinfected_files'])
        elif result['Deleted_files']:
            self.ResultInfo.append('Deleted files     :%d' % result['Deleted_files'])
        self.ResultInfo.append('I/O errors            :%d' % result['IO_errors'])

        # 검사 시간 출력
        t = str(self.g_scan_time).split(':')
        t_h = int(float(t[0]))
        t_m = int(float(t[1]))
        t_s = int(float(t[2]))
        self.ResultInfo.append('Scan time         :%02d:%02d:%02d\n' % (t_h, t_m, t_s))

    def main(self):
        self.show()
        import IVengine
        IV = IVengine.Engine()
        iv_pwd = os.path.abspath(os.path.split(sys.argv[0])[0])  # 프로그램이 실행중인 폴더
        plugins_path = os.path.join(iv_pwd + os.sep + 'InfonetVaccine')

        if not IV.set_plugins(plugins_path):  # 플러그인 엔진 경로 설정
            return 0

        InfoV = IV.create_instance()  # 백신 엔진 인스턴스 생성
        if not InfoV:
            return 0

        options = self.define_options()
        InfoV.set_options(options)

        if not InfoV.init():  # 전체 플러그인 엔진 초기화
            return 0

        if self.path:
            InfoV.set_result()  # 악성코드 검사 결과 초기화

            # 검사 시작 시간 체크
            start_time = datetime.datetime.now()

            # 검사용 path (다중 경로 지원을 위해)
            for scan_path in self.path:
                scan_path = os.path.abspath(scan_path)
                if os.path.exists(scan_path):  # 폴더 혹은 파일이 존재하는가?
                    InfoV.scan(scan_path, self.scan_callback.__func__, self.disinfect_callback.__func__, self.update_callback.__func__)
                else:
                    print 'error'
            # 검사 종료 시간 체크
            end_time = datetime.datetime.now()

            self.g_scan_time = end_time - start_time

            # 검사 결과 출력
            ret = InfoV.get_result()
            self.print_result(ret)

        InfoV.uninit()
if __name__ == '__main__':
    a = QApplication(sys.argv)
    app = IV()
    app.show()
    a.exec_()