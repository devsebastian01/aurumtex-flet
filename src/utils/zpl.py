import win32print
import win32api

def generate_zpl_code(roll: dict) -> str:
    print(roll)
    zpl = f"""
            ^FO100,29^A0N,21,20^CI28^FDCOLOR: {roll['color']}^FS^CI27
            ^FO100,60^A0N,21,20^CI28^FDROLLO: {roll['roll']}^FS^CI27
            ^FO100,89^A0N,20,20^CI28^FDMTS: {roll['mts']} | KG: {roll['kg']}^FS^CI27
            ^FO100,121^A0N,21,20^CI28^FD{roll['container']} | {roll['item']}^FS^CI27
            ^BY2,2,50
            ^FO100,160^BCN,80,Y,N,N
            ^FD{roll['uuid']}^FS
            """
    return zpl

def generate_zpl_single(roll: dict) -> str:
    zpl = f"""
            ^XA
            ^MMT
            ^PW800
            ^LL300
            ^LS0
            ^FO100,29^A0N,21,20^CI28^FDCOLOR: {roll['color']}^FS^CI27
            ^FO100,60^A0N,21,20^CI28^FDROLLO: {roll['roll']}^FS^CI27
            ^FO100,89^A0N,20,20^CI28^FDMTS: {roll['mts']} | KG: {roll['kg']}^FS^CI27
            ^FO100,121^A0N,21,20^CI28^FD{roll['container']} | {roll['item']}^FS^CI27
            ^BY2,2,50
            ^FO100,160^BCN,80,Y,N,N
            ^FD{roll['uuid']}^FS
            ^PQ1,0,1,Y
            ^XZ
            """
    return zpl


def generate_zpl_pair(roll1: dict, roll2: dict) -> str:
    zpl = f"""
        ^XA
        ^MMT
        ^PW800
        ^LL300
        ^LS0

        ^FO100,29^A0N,21,20^CI28^FDCOLOR: {roll1['color']}^FS^CI27
        ^FO100,60^A0N,21,20^CI28^FDROLLO: {roll1['roll']}^FS^CI27
        ^FO100,89^A0N,20,20^CI28^FDMTS: {roll1['mts']} | KG: {roll1['kg']}^FS^CI27
        ^FO100,121^A0N,21,20^CI28^FD{roll1['container']} | {roll1['item']}^FS^CI27
        ^BY2,2,50
        ^FO100,160^BCN,80,Y,N,N
        ^FD{roll1['uuid']}^FS

        ^FO500,29^A0N,21,20^CI28^FDCOLOR: {roll2['color']}^FS^CI27
        ^FO500,60^A0N,21,20^CI28^FDROLLO: {roll2['roll']}^FS^CI27
        ^FO500,89^A0N,20,20^CI28^FDMTS: {roll2['mts']} | KG: {roll2['kg']}^FS^CI27
        ^FO500,121^A0N,21,20^CI28^FD{roll2['container']} | {roll2['item']} ^FS^CI27
        ^BY2,2,50
        ^FO500,160^BCN,80,Y,N,N
        ^FD{roll2['uuid']}^FS

        ^PQ1,0,1,Y
        ^XZ
        """
    return zpl


def send_zpl_to_usb(printer_name: str, zpl_code: str):
    try:
        printer = win32print.OpenPrinter(printer_name)
        hPrinter = win32print.StartDocPrinter(printer, 1, ("Etiqueta", None, "RAW"))
        win32print.StartPagePrinter(printer)
        win32print.WritePrinter(printer, zpl_code.encode('utf-8'))
        win32print.EndPagePrinter(printer)
        win32print.EndDocPrinter(printer)
        win32print.ClosePrinter(printer)
        print("> INFO: ZPL send to usb print")
    except Exception as e:
        print(f"> ERROR to connect print: {e}")
    pass

