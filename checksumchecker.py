import PySimpleGUI as sg
import hashlib

#define variables
algo_name_list = [
    "SHA1", "SHA224", "SHA256", "SHA384", "SHA512", "MD5"
]

def get_hash_of_file(file, algo):
    with open(file, 'rb') as f:
        data = f.read()
        return str(algo(data).hexdigest())

#design
sg.theme("DarkGrey13")

#layout
layout_compare = [
    [sg.T("Please enter the first checksum:")],
    [sg.I(key="-IN1-")],
    [sg.T("Please enter the second checksum:")],
    [sg.I(key="-IN2-")],
    [sg.B("compare")]
]

layout_calc = [
    [sg.T("Select the Hashing-Algorythm:"), sg.Combo(algo_name_list, key="-ALGO-", readonly=True)],
    [sg.FileBrowse("select a file", key="-FILE-"), sg.T("---", key="-FILENAME-")], 
    [sg.B("calculate file hash"), sg.T("---", key="-STATUS_CALC-")]
]

layout = [
    [sg.B("compare hash"), sg.B("calculate hash")],
    [sg.HorizontalSeparator()],
    [sg.Column(layout_compare, key="-COMPARE-"), sg.Column(layout_calc, key="-CALC-", visible=False)]
]

def main():
    #define variables
    window = sg.Window("checksum checker", layout)
    no_error = True

    while(True):
        event, value = window.read()
        if event == sg.WINDOW_CLOSED:
            break

        #change diplayed panel 
        if "compare hash" == event:
            window["-COMPARE-"].update(visible=True)
            window["-CALC-"].update(visible=False)
        elif "calculate hash" == event:
            window["-CALC-"].update(visible=True)
            window["-COMPARE-"].update(visible=False)

        #calc hash
        if event == "calculate file hash":
            if value["-ALGO-"] == "SHA1":
                algo = hashlib.sha1
            elif value["-ALGO-"] == "SHA224":
                algo = hashlib.sha224
            elif value["-ALGO-"] == "SHA256":
                algo = hashlib.sha256
            elif value["-ALGO-"] == "SHA384":
                algo = hashlib.sha384
            elif value["-ALGO-"] == "SHA512":
                algo = hashlib.sha512
            elif value["-ALGO-"] == "MD5":
                algo = hashlib.md5
            else:
                sg.popup_error("select a algorythm!")
                no_error = False
                continue

            file = value["-FILE-"]
            if file == "":
                sg.popup_error("select a file!")
                no_error = False

            if no_error:
                In2 = get_hash_of_file(file, algo)
                window["-IN2-"].update(In2)
                window["-STATUS_CALC-"].update("sucess")

        #get input
        In1 = value["-IN1-"]
        In2 = value["-IN2-"]

        if event == "compare":
            #conv. in lowercase
            In1 = In1.lower()
            In2 = In2.lower()

            #compare
            if In1 == In2:
                sg.Popup("checksunms are matching", title="output")
            else:
                sg.Popup("checksums are NOT matching", title="output")

if __name__ == "__main__":
    main()