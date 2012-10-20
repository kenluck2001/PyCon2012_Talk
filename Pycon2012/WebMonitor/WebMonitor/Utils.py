import webbrowser


def openBrower(url = "http://127.0.0.1:8080/monitor/" ):
    #load the webpage for the log
    handle = webbrowser.get() 
    handle.open_new_tab(url)




if __name__ == '__main__' :
    openBrower()



